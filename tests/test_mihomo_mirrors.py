from __future__ import annotations

import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_rules  # noqa: E402


def convert(root: Path, name: str, lines: list[str], behavior: str = "domain") -> Path:
    text = root / f"{name}.txt"
    text.write_text("\n".join(lines) + "\n", encoding="utf-8")
    target = root / f"{name}.mrs"
    subprocess.run(["mihomo", "convert-ruleset", behavior, "text", str(text), str(target)],
                   check=True, capture_output=True)
    return target


@unittest.skipUnless(shutil.which("mihomo") and shutil.which("zstd"), "mihomo and zstd are required")
class MihomoMirrorTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = convert(self.root, "source", ["+.example.org", "exact.example.net"])
        self.target = self.root / "mihomo/geosite/test.mrs"
        self.config = {"mihomo_mirrors": {"geosite/test.mrs": {
            "path": "source.mrs", "url": "https://example.org/test.mrs",
        }}}
        root_patch = patch.object(build_rules, "ROOT", self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)

    def test_local_copy_preserves_upstream_bytes(self) -> None:
        with patch.object(build_rules, "REQUIRE_LOCAL_SOURCES", True):
            build_rules.sync_mihomo_mirrors(self.config)
        self.assertEqual(self.source.read_bytes(), self.target.read_bytes())

    def test_missing_strict_source_never_falls_back_to_network(self) -> None:
        self.source.unlink()
        with patch.object(build_rules, "REQUIRE_LOCAL_SOURCES", True), \
                patch.object(build_rules.urllib.request, "urlopen") as fetch:
            with self.assertRaises(FileNotFoundError):
                build_rules.sync_mihomo_mirrors(self.config)
            fetch.assert_not_called()
        self.assertFalse(self.target.exists())

    def test_remote_fallback_preserves_bytes(self) -> None:
        data = self.source.read_bytes()
        self.source.unlink()
        with patch.object(build_rules, "REQUIRE_LOCAL_SOURCES", False), \
                patch.object(build_rules.urllib.request, "urlopen", return_value=io.BytesIO(data)):
            build_rules.sync_mihomo_mirrors(self.config)
        self.assertEqual(data, self.target.read_bytes())

    def test_invalid_second_source_does_not_replace_any_mirror(self) -> None:
        self.target.parent.mkdir(parents=True)
        self.target.write_bytes(b"previous published file")
        (self.root / "invalid.mrs").write_bytes(b"not a rule set")
        self.config["mihomo_mirrors"]["geosite/invalid.mrs"] = {
            "path": "invalid.mrs", "url": "https://example.org/invalid.mrs",
        }
        with self.assertRaisesRegex(ValueError, "invalid mirrored MRS"):
            build_rules.sync_mihomo_mirrors(self.config)
        self.assertEqual(b"previous published file", self.target.read_bytes())
        self.assertFalse((self.root / "mihomo/geosite/invalid.mrs").exists())

    def test_non_domain_behavior_is_rejected(self) -> None:
        convert(self.root, "source", ["10.0.0.0/8"], behavior="ipcidr")
        with self.assertRaisesRegex(ValueError, "not domain behavior"):
            build_rules.sync_mihomo_mirrors(self.config)
        self.assertFalse(self.target.exists())

    def test_empty_rule_set_is_rejected(self) -> None:
        empty = subprocess.run(["zstd", "-c"], input=b"MRS\x01\x00" + (0).to_bytes(8, "big"),
                               capture_output=True, check=True).stdout
        self.source.write_bytes(empty)
        with self.assertRaisesRegex(ValueError, "empty mirrored rule set"):
            build_rules.sync_mihomo_mirrors(self.config)
        self.assertFalse(self.target.exists())


if __name__ == "__main__":
    unittest.main()
