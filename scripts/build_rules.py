#!/usr/bin/env python3
"""Build generated routing rule sets for multiple proxy clients."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import subprocess
import sys
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "rules.json"
MAX_RULES_PER_SET = 100000

RULE_TYPE_TO_ARRS = {
    "IP-CIDR": 0,
    "IP-CIDR6": 1,
    "DOMAIN": 2,
    "DOMAIN-SUFFIX": 2,
    "DOMAIN-KEYWORD": 3
}

ALIASES = {
    "HOST": "DOMAIN",
    "HOST-SUFFIX": "DOMAIN-SUFFIX",
    "HOST-KEYWORD": "DOMAIN-KEYWORD",
    "IP6-CIDR": "IP-CIDR6"
}


@dataclass(frozen=True)
class Rule:
    rule_type: str
    value: str

    @property
    def key(self) -> tuple[str, str]:
        return self.rule_type, self.value


def clean_line(raw: str) -> str | None:
    line = raw.strip()
    if not line or line.startswith("#") or line.startswith(";"):
        return None
    if line in {"payload:", "rules:", "rule-providers:"}:
        return None
    if line.startswith("- "):
        line = line[2:].strip()
    if line.startswith("'") and line.endswith("'"):
        line = line[1:-1].strip()
    if line.startswith('"') and line.endswith('"'):
        line = line[1:-1].strip()
    line = re.sub(r"\s+#.*$", "", line)
    line = re.sub(r"\s+//.*$", "", line)
    return line.strip() or None


def split_rule_line(line: str) -> list[str]:
    return [field.strip() for field in line.split(",") if field.strip()]


def normalize_domain(value: str) -> str | None:
    domain = value.strip().strip(".").lower()
    if not domain or " " in domain or "/" in domain:
        return None
    return domain


def normalize_keyword(value: str) -> str | None:
    keyword = value.strip().lower()
    return keyword or None


def normalize_cidr(value: str, rule_type: str) -> str | None:
    try:
        network = ipaddress.ip_network(value.strip(), strict=False)
    except ValueError:
        return None
    if rule_type == "IP-CIDR" and network.version != 4:
        return None
    if rule_type == "IP-CIDR6" and network.version != 6:
        return None
    return str(network)


def infer_bare_rule(line: str, default_domain_type: str) -> str:
    bare = line.strip().strip("'\"")
    if bare.startswith("+."):
        return f"DOMAIN-SUFFIX,{bare[2:]}"
    if bare.startswith("."):
        return f"DOMAIN-SUFFIX,{bare[1:]}"
    try:
        network = ipaddress.ip_network(bare, strict=False)
    except ValueError:
        network = None
    if network is not None:
        return f"IP-CIDR6,{bare}" if network.version == 6 else f"IP-CIDR,{bare}"
    if "," not in bare and "." in bare and " " not in bare:
        return f"{default_domain_type},{bare}"
    return bare


def parse_rule(line: str, default_domain_type: str) -> tuple[Rule | None, str | None]:
    cleaned = clean_line(line)
    if cleaned is None:
        return None, None

    fields = split_rule_line(infer_bare_rule(cleaned, default_domain_type))
    if len(fields) < 2:
        return None, "UNKNOWN"

    rule_type = ALIASES.get(fields[0].upper(), fields[0].upper())
    value = fields[1]

    if rule_type == "DOMAIN-WILDCARD":
        return None, rule_type
    if rule_type in {"DOMAIN", "DOMAIN-SUFFIX"}:
        normalized = normalize_domain(value)
        return (Rule(rule_type, normalized), None) if normalized else (None, rule_type)
    if rule_type == "DOMAIN-KEYWORD":
        normalized = normalize_keyword(value)
        return (Rule(rule_type, normalized), None) if normalized else (None, rule_type)
    if rule_type in {"IP-CIDR", "IP-CIDR6"}:
        normalized = normalize_cidr(value, rule_type)
        return (Rule(rule_type, normalized), None) if normalized else (None, rule_type)
    return None, rule_type


def fetch_lines(url: str) -> list[str]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "AlexKris-rules-builder/1.0"}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8-sig", errors="replace").splitlines()
    except Exception as error:
        raise RuntimeError(f"failed to fetch {url}: {error}") from error


def parse_lines(
    lines: Iterable[str],
    default_domain_type: str,
    source_marker_domains: set[str]
) -> tuple[list[Rule], dict[str, int]]:
    rules: list[Rule] = []
    seen: set[tuple[str, str]] = set()
    skipped: dict[str, int] = {}
    for line in lines:
        rule, skipped_type = parse_rule(line, default_domain_type)
        if rule is not None and rule.value in source_marker_domains:
            continue
        if rule is not None and rule.key not in seen:
            rules.append(rule)
            seen.add(rule.key)
        elif skipped_type:
            skipped[skipped_type] = skipped.get(skipped_type, 0) + 1
    return rules, skipped


def read_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_source_rules(config: dict) -> tuple[dict[str, list[Rule]], dict[str, dict[str, int]]]:
    source_marker_domains = set(config.get("source_marker_domains", []))
    loaded: dict[str, list[Rule]] = {}
    skipped_by_source: dict[str, dict[str, int]] = {}
    for source_id, source_config in config["sources"].items():
        default_type = "DOMAIN" if source_config.get("kind") == "domainset" else "DOMAIN-SUFFIX"
        lines: list[str] = []
        for url in source_config["urls"]:
            lines.extend(fetch_lines(url))
            lines.append("")
        rules, skipped = parse_lines(lines, default_type, source_marker_domains)
        loaded[source_id] = rules
        skipped_by_source[source_id] = skipped
    return loaded, skipped_by_source


def collect_output_rules(
    output_id: str,
    output_config: dict,
    source_rules: dict[str, list[Rule]],
    source_skipped: dict[str, dict[str, int]],
    source_marker_domains: set[str]
) -> tuple[list[Rule], dict[str, int]]:
    rules: list[Rule] = []
    skipped: dict[str, int] = {}
    seen: set[tuple[str, str]] = set()

    for source_id in output_config.get("sources", []):
        for skipped_type, count in source_skipped.get(source_id, {}).items():
            skipped[skipped_type] = skipped.get(skipped_type, 0) + count
        for rule in source_rules[source_id]:
            if rule.key not in seen:
                rules.append(rule)
                seen.add(rule.key)

    if output_config.get("rules"):
        parsed, parsed_skipped = parse_lines(output_config["rules"], "DOMAIN-SUFFIX", source_marker_domains)
        skipped.update(parsed_skipped)
        for rule in parsed:
            if rule.key not in seen:
                rules.append(rule)
                seen.add(rule.key)

    if output_config.get("add"):
        parsed, parsed_skipped = parse_lines(output_config["add"], "DOMAIN-SUFFIX", source_marker_domains)
        skipped.update(parsed_skipped)
        for rule in parsed:
            if rule.key not in seen:
                rules.append(rule)
                seen.add(rule.key)

    excludes = {normalize_domain(value) for value in output_config.get("exclude", [])}
    excludes.discard(None)
    if excludes:
        rules = [rule for rule in rules if rule.value not in excludes]

    if len(rules) > MAX_RULES_PER_SET:
        raise ValueError(f"{output_id} has {len(rules)} rules, above Anywhere limit {MAX_RULES_PER_SET}")
    return rules, skipped


def apply_rule_overrides(
    rules: list[Rule],
    overrides: dict | None,
    source_marker_domains: set[str]
) -> list[Rule]:
    if overrides is None:
        return list(rules)

    result = list(rules)
    seen = {rule.key for rule in result}

    for line in overrides.get("add", []):
        rule, _ = parse_rule(line, "DOMAIN-SUFFIX")
        if rule is not None and rule.value not in source_marker_domains and rule.key not in seen:
            result.append(rule)
            seen.add(rule.key)

    excludes = {normalize_domain(value) for value in overrides.get("exclude", [])}
    excludes.discard(None)
    if excludes:
        result = [rule for rule in result if rule.value not in excludes]
    return result


def write_text(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def source_urls_for(output_config: dict, config: dict) -> list[str]:
    urls: list[str] = []
    for source_id in output_config.get("sources", []):
        urls.extend(config["sources"][source_id]["urls"])
    return urls


def write_anywhere(path: Path, output_config: dict, rules: list[Rule], skipped: dict[str, int], sources: list[str]) -> None:
    lines = [
        f"# NAME: {output_config['name']}",
        "# GENERATED-FOR: Anywhere Routing Rule Set",
        f"# DESCRIPTION: {output_config['description']}",
        f"# RULES: {len(rules)}",
        f"# SKIPPED: {sum(skipped.values())}"
    ]
    if skipped:
        lines.append("# SKIPPED-TYPES: " + ", ".join(f"{key}={skipped[key]}" for key in sorted(skipped)))
    if sources:
        lines.append("# SOURCES:")
        lines.extend(f"# - {source}" for source in sources)
    lines.extend(["", f"name = {output_config['name']}"])
    lines.extend(f"{RULE_TYPE_TO_ARRS[rule.rule_type]}, {rule.value}" for rule in rules if rule.rule_type in RULE_TYPE_TO_ARRS)
    write_text(path, lines)


def write_surge_domainset(path: Path, rules: list[Rule]) -> None:
    lines = []
    for rule in rules:
        if rule.rule_type == "DOMAIN":
            lines.append(rule.value)
        elif rule.rule_type == "DOMAIN-SUFFIX":
            lines.append(f".{rule.value}")
    write_text(path, lines)


def write_surge_non_ip(path: Path, rules: list[Rule]) -> None:
    write_text(path, domain_rule_lines(rules))


def domain_rule_lines(rules: list[Rule]) -> list[str]:
    return [
        f"{rule.rule_type},{rule.value}"
        for rule in rules
        if rule.rule_type in {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD"}
    ]


def write_mihomo_mrs(path: Path, rules: list[Rule]) -> None:
    lines = domain_rule_lines(rules)
    if not lines:
        relative_path = path.relative_to(ROOT)
        raise ValueError(f"{relative_path} has no domain rules for Mihomo MRS")

    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as temp:
        temp.write("\n".join(lines) + "\n")
        temp_path = Path(temp.name)
    try:
        subprocess.run(
            ["mihomo", "convert-ruleset", "domain", "text", str(temp_path), str(path)],
            cwd=ROOT,
            check=True
        )
    finally:
        temp_path.unlink(missing_ok=True)


def write_sing_box_json(path: Path, rules: list[Rule]) -> None:
    domain: list[str] = []
    domain_suffix: list[str] = []
    domain_keyword: list[str] = []
    ip_cidr: list[str] = []
    for rule in rules:
        if rule.rule_type == "DOMAIN":
            domain.append(rule.value)
        elif rule.rule_type == "DOMAIN-SUFFIX":
            domain_suffix.append(rule.value)
        elif rule.rule_type == "DOMAIN-KEYWORD":
            domain_keyword.append(rule.value)
        elif rule.rule_type in {"IP-CIDR", "IP-CIDR6"}:
            ip_cidr.append(rule.value)

    rule_object: dict[str, list[str]] = {}
    if domain:
        rule_object["domain"] = domain
    if domain_suffix:
        rule_object["domain_suffix"] = domain_suffix
    if domain_keyword:
        rule_object["domain_keyword"] = domain_keyword
    if ip_cidr:
        rule_object["ip_cidr"] = ip_cidr

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"version": 3, "rules": [rule_object]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )


def write_sing_box_srs(json_path: Path, srs_path: Path) -> None:
    subprocess.run(
        ["sing-box", "rule-set", "compile", str(json_path), "-o", str(srs_path)],
        cwd=ROOT,
        check=True
    )


def artifact_rules(
    artifact_id: str,
    artifact_config: dict,
    config: dict,
    source_rules: dict[str, list[Rule]],
    built_outputs: dict[str, list[Rule]]
) -> list[Rule]:
    source_marker_domains = set(config.get("source_marker_domains", []))
    source_id = artifact_config["source"]
    if source_id in source_rules:
        rules = source_rules[source_id]
    elif source_id in built_outputs:
        rules = built_outputs[source_id]
    else:
        raise KeyError(f"{artifact_id} uses unknown artifact source: {source_id}")
    return apply_rule_overrides(rules, artifact_config, source_marker_domains)


def write_generated_outputs(
    config: dict,
    source_rules: dict[str, list[Rule]],
    source_skipped: dict[str, dict[str, int]]
) -> dict[str, list[Rule]]:
    source_marker_domains = set(config.get("source_marker_domains", []))
    built_outputs: dict[str, list[Rule]] = {}
    skipped_outputs: dict[str, dict[str, int]] = {}

    for output_id, output_config in config["outputs"].items():
        rules, skipped = collect_output_rules(output_id, output_config, source_rules, source_skipped, source_marker_domains)
        built_outputs[output_id] = rules
        skipped_outputs[output_id] = skipped
        if "anywhere" in output_config.get("targets", {}):
            write_anywhere(
                ROOT / output_config["targets"]["anywhere"],
                output_config,
                rules,
                skipped,
                source_urls_for(output_config, config)
            )

    for name, artifact_config in config["artifacts"]["domainset"].items():
        rules = artifact_rules(name, artifact_config, config, source_rules, built_outputs)
        write_surge_domainset(ROOT / "surge" / "domainset" / f"{name}.conf", rules)
        write_mihomo_mrs(ROOT / "mihomo" / "domainset" / f"{name}.mrs", rules)
        json_path = ROOT / "sing-box" / "domainset" / f"{name}.json"
        write_sing_box_json(json_path, rules)
        write_sing_box_srs(json_path, json_path.with_suffix(".srs"))

    for name, artifact_config in config["artifacts"]["non-ip"].items():
        rules = artifact_rules(name, artifact_config, config, source_rules, built_outputs)
        write_surge_non_ip(ROOT / "surge" / "non-ip" / f"{name}.conf", rules)
        write_mihomo_mrs(ROOT / "mihomo" / "non-ip" / f"{name}.mrs", rules)
        json_path = ROOT / "sing-box" / "non-ip" / f"{name}.json"
        write_sing_box_json(json_path, rules)
        write_sing_box_srs(json_path, json_path.with_suffix(".srs"))

    return built_outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=CONFIG_PATH)
    args = parser.parse_args()

    config = read_config(args.config)
    source_rules, source_skipped = load_source_rules(config)
    built_outputs = write_generated_outputs(config, source_rules, source_skipped)
    for output_id, rules in built_outputs.items():
        print(f"{output_id}: {len(rules)} rules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
