from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_rules  # noqa: E402
from build_rules import Rule  # noqa: E402


def values(rules: list[Rule]) -> list[tuple[str, str]]:
    return [rule.key for rule in rules]


class RedundantDomainRuleTests(unittest.TestCase):
    def test_exact_domain_covered_by_same_suffix_is_removed(self) -> None:
        rules = [Rule("DOMAIN", "example.com"), Rule("DOMAIN-SUFFIX", "example.com")]
        self.assertEqual([("DOMAIN-SUFFIX", "example.com")],
                         values(build_rules.remove_redundant_domain_rules(rules)))

    def test_exact_domain_covered_by_parent_suffix_is_removed(self) -> None:
        rules = [Rule("DOMAIN", "mail.google.com"), Rule("DOMAIN-SUFFIX", "google.com")]
        self.assertEqual([("DOMAIN-SUFFIX", "google.com")],
                         values(build_rules.remove_redundant_domain_rules(rules)))

    def test_child_suffix_covered_by_parent_suffix_is_removed(self) -> None:
        rules = [Rule("DOMAIN-SUFFIX", "a.b.example.com"), Rule("DOMAIN-SUFFIX", "example.com")]
        self.assertEqual([("DOMAIN-SUFFIX", "example.com")],
                         values(build_rules.remove_redundant_domain_rules(rules)))

    def test_lookalike_and_sibling_domains_are_kept(self) -> None:
        rules = [
            Rule("DOMAIN-SUFFIX", "ample.com"),
            Rule("DOMAIN-SUFFIX", "example.com"),
            Rule("DOMAIN", "notexample.com"),
            Rule("DOMAIN", "a.example.org"),
            Rule("DOMAIN-SUFFIX", "b.example.org"),
        ]
        self.assertEqual(values(rules), values(build_rules.remove_redundant_domain_rules(rules)))

    def test_exact_parent_does_not_cover_children(self) -> None:
        rules = [Rule("DOMAIN", "example.com"), Rule("DOMAIN", "www.example.com"),
                 Rule("DOMAIN-SUFFIX", "cdn.example.com")]
        self.assertEqual(values(rules), values(build_rules.remove_redundant_domain_rules(rules)))

    def test_non_domain_rules_are_kept_even_when_matching(self) -> None:
        rules = [
            Rule("DOMAIN-SUFFIX", "example.com"),
            Rule("DOMAIN-KEYWORD", "example"),
            Rule("DOMAIN-WILDCARD", "*.example.com"),
            Rule("URL-REGEX", "^https?://example\\.com/"),
            Rule("USER-AGENT", "Example*"),
            Rule("PROCESS-NAME", "example"),
            Rule("IP-CIDR", "10.0.0.0/8"),
            Rule("IP-CIDR6", "fc00::/7"),
        ]
        self.assertEqual(values(rules), values(build_rules.remove_redundant_domain_rules(rules)))

    def test_keyword_does_not_cover_domains(self) -> None:
        rules = [Rule("DOMAIN-KEYWORD", "google"), Rule("DOMAIN", "google.com")]
        self.assertEqual(values(rules), values(build_rules.remove_redundant_domain_rules(rules)))

    def test_order_of_remaining_rules_is_preserved(self) -> None:
        rules = [
            Rule("DOMAIN", "z.example.net"),
            Rule("DOMAIN", "x.example.com"),
            Rule("DOMAIN-SUFFIX", "b.org"),
            Rule("DOMAIN-SUFFIX", "example.com"),
            Rule("DOMAIN", "a.org"),
        ]
        self.assertEqual(
            [("DOMAIN", "z.example.net"), ("DOMAIN-SUFFIX", "b.org"),
             ("DOMAIN-SUFFIX", "example.com"), ("DOMAIN", "a.org")],
            values(build_rules.remove_redundant_domain_rules(rules)),
        )

    def test_artifact_rules_apply_dedupe_after_overrides(self) -> None:
        config = {"source_marker_domains": []}
        source_rules = {"src": [Rule("DOMAIN", "a.example.com"), Rule("DOMAIN-SUFFIX", "b.example.com")]}
        artifact = {"source": "src", "add": ["DOMAIN-SUFFIX,example.com"]}
        result = build_rules.artifact_rules("t", artifact, config, source_rules, {})
        self.assertEqual([("DOMAIN-SUFFIX", "example.com")], values(result))

    def test_artifact_rules_merge_sources_and_dedupe_across_them(self) -> None:
        config = {"source_marker_domains": []}
        v2fly, _ = build_rules.parse_lines(["DOMAIN-SUFFIX,qq.com", "DOMAIN,end.shallow.ink"], "DOMAIN-SUFFIX", set())
        domainset, _ = build_rules.parse_lines([".cn", ".qq.com", "www.qq.com", ".b.cn"], "DOMAIN", set())
        source_rules = {"v2fly": v2fly, "domainset": domainset}
        artifact = {"sources": ["v2fly", "domainset"]}
        result = build_rules.artifact_rules("t", artifact, config, source_rules, {})
        self.assertEqual(
            [("DOMAIN-SUFFIX", "qq.com"), ("DOMAIN", "end.shallow.ink"), ("DOMAIN-SUFFIX", "cn")],
            values(result),
        )


if __name__ == "__main__":
    unittest.main()
