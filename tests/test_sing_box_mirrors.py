from __future__ import annotations

import io
import json
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


@unittest.skipUnless(shutil.which("sing-box"), "sing-box is required")
class SingBoxMirrorTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / "source.srs"
        source_json = self.root / "source.json"
        source_json.write_text(json.dumps({
            "version": 3,
            "rules": [{"domain_suffix": ["example.org"], "domain_regex": [r"^test\d+\.example$"]}],
        }))
        subprocess.run(["sing-box", "rule-set", "compile", str(source_json),
                        "-o", str(self.source)], check=True, capture_output=True)
        self.target = self.root / "sing-box/geosite/test.srs"
        self.config = {"sing_box_mirrors": {"geosite/test.srs": {
            "path": "source.srs", "url": "https://example.org/test.srs",
        }}}
        root_patch = patch.object(build_rules, "ROOT", self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)

    def test_local_copy_preserves_upstream_bytes_including_regex(self) -> None:
        with patch.object(build_rules, "REQUIRE_LOCAL_SOURCES", True):
            build_rules.sync_sing_box_mirrors(self.config)
        self.assertEqual(self.source.read_bytes(), self.target.read_bytes())

    def test_missing_strict_source_never_falls_back_to_network(self) -> None:
        self.source.unlink()
        with patch.object(build_rules, "REQUIRE_LOCAL_SOURCES", True), \
                patch.object(build_rules.urllib.request, "urlopen") as fetch:
            with self.assertRaises(FileNotFoundError):
                build_rules.sync_sing_box_mirrors(self.config)
            fetch.assert_not_called()
        self.assertFalse(self.target.exists())

    def test_remote_fallback_preserves_bytes(self) -> None:
        data = self.source.read_bytes()
        self.source.unlink()
        with patch.object(build_rules, "REQUIRE_LOCAL_SOURCES", False), \
                patch.object(build_rules.urllib.request, "urlopen", return_value=io.BytesIO(data)):
            build_rules.sync_sing_box_mirrors(self.config)
        self.assertEqual(data, self.target.read_bytes())

    def test_invalid_second_source_does_not_replace_any_mirror(self) -> None:
        self.target.parent.mkdir(parents=True)
        self.target.write_bytes(b"previous published file")
        (self.root / "invalid.srs").write_bytes(b"not a rule set")
        self.config["sing_box_mirrors"]["geosite/invalid.srs"] = {
            "path": "invalid.srs", "url": "https://example.org/invalid.srs",
        }
        with self.assertRaises(subprocess.CalledProcessError):
            build_rules.sync_sing_box_mirrors(self.config)
        self.assertEqual(b"previous published file", self.target.read_bytes())
        self.assertFalse((self.root / "sing-box/geosite/invalid.srs").exists())

    def test_empty_rule_set_is_rejected(self) -> None:
        empty_json = self.root / "empty.json"
        empty_json.write_text('{"version": 3, "rules": []}')
        subprocess.run(["sing-box", "rule-set", "compile", str(empty_json),
                        "-o", str(self.source)], check=True, capture_output=True)
        with self.assertRaisesRegex(ValueError, "empty mirrored rule set"):
            build_rules.sync_sing_box_mirrors(self.config)
        self.assertFalse(self.target.exists())


if __name__ == "__main__":
    unittest.main()
