from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_rules  # noqa: E402


class GoogleAIScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rules, _ = build_rules.parse_lines(
            (ROOT / "plain/non-ip/ai.txt").read_text().splitlines(), "DOMAIN", set()
        )

    def matches_ai(self, host: str) -> bool:
        return any(
            (rule.rule_type == "DOMAIN" and host == rule.value)
            or (rule.rule_type == "DOMAIN-SUFFIX"
                and (host == rule.value or host.endswith("." + rule.value)))
            or (rule.rule_type == "DOMAIN-KEYWORD" and rule.value in host)
            for rule in self.rules
        )

    def test_google_ai_service_endpoints_are_covered(self) -> None:
        # Official Antigravity enterprise allowlist and Remote Control host.
        hosts = [
            "gemini.google.com", "gemini.gstatic.com", "generativelanguage.googleapis.com",
            "antigravity.google", "antigravity.google.com", "antigravity-pa.googleapis.com",
            "cloudcode-pa.googleapis.com", "daily-cloudcode-pa.googleapis.com",
            "businessaicode.googleapis.com", "businessaicode.us.rep.googleapis.com",
            "businessaicode.eu.rep.googleapis.com", "businessaicode.mtls.googleapis.com",
            "aiplatform.googleapis.com", "aiplatform.us.rep.googleapis.com",
            "aiplatform.eu.rep.googleapis.com", "aiplatform.mtls.googleapis.com",
            "discoveryengine.googleapis.com", "us-discoveryengine.googleapis.com",
            "eu-discoveryengine.googleapis.com", "discoveryengine.mtls.googleapis.com",
            "us-discoveryengine.mtls.googleapis.com", "eu-discoveryengine.mtls.googleapis.com",
        ]
        for host in hosts:
            with self.subTest(host=host):
                self.assertTrue(self.matches_ai(host))

    def test_shared_google_services_are_not_claimed_by_ai(self) -> None:
        for host in (
            "www.google.com", "mail.google.com", "drive.google.com", "accounts.google.com",
            "oauth2.googleapis.com", "www.googleapis.com", "storage.googleapis.com",
            "www.gstatic.com", "lh3.googleusercontent.com", "update.googleapis.com",
            "www.youtube.com", "maps.googleapis.com", "notbusinessaicode.googleapis.com",
            "businessaicode.googleapis.com.example.org",
        ):
            with self.subTest(host=host):
                self.assertFalse(self.matches_ai(host))


if __name__ == "__main__":
    unittest.main()
