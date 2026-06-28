#!/usr/bin/env python3
"""Build generated routing rule sets for multiple proxy clients."""

from __future__ import annotations

import argparse
import io
import ipaddress
import json
import re
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "rules.json"
MAX_RULES_PER_SET = 100000
V2FLY_DEFAULT_BASE_URL = "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data"
V2FLY_ARCHIVE_URL = "https://github.com/v2fly/domain-list-community/archive/refs/heads/master.tar.gz"
V2FLY_ARCHIVE_CACHE: dict[str, list[str]] | None = None

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
    attrs: frozenset[str] = frozenset()

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


def normalize_wildcard(value: str) -> str | None:
    wildcard = value.strip().lower()
    if not wildcard or " " in wildcard or "/" in wildcard:
        return None
    return wildcard


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


def normalize_text_matcher(value: str) -> str | None:
    matcher = value.strip()
    return matcher or None


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

    if rule_type in {"DOMAIN", "DOMAIN-SUFFIX"}:
        normalized = normalize_domain(value)
        return (Rule(rule_type, normalized), None) if normalized else (None, rule_type)
    if rule_type == "DOMAIN-KEYWORD":
        normalized = normalize_keyword(value)
        return (Rule(rule_type, normalized), None) if normalized else (None, rule_type)
    if rule_type == "DOMAIN-WILDCARD":
        normalized = normalize_wildcard(value)
        return (Rule(rule_type, normalized), None) if normalized else (None, rule_type)
    if rule_type in {"IP-CIDR", "IP-CIDR6"}:
        normalized = normalize_cidr(value, rule_type)
        return (Rule(rule_type, normalized), None) if normalized else (None, rule_type)
    if rule_type in {"USER-AGENT", "PROCESS-NAME", "URL-REGEX"}:
        normalized = normalize_text_matcher(value)
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


def v2fly_data_url(base_url: str, list_name: str) -> str:
    return f"{base_url.rstrip('/')}/{quote(list_name, safe='!-._~/')}"


def load_v2fly_archive() -> dict[str, list[str]]:
    global V2FLY_ARCHIVE_CACHE
    if V2FLY_ARCHIVE_CACHE is not None:
        return V2FLY_ARCHIVE_CACHE

    request = urllib.request.Request(
        V2FLY_ARCHIVE_URL,
        headers={"User-Agent": "AlexKris-rules-builder/1.0"}
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            archive_data = response.read()
    except Exception as error:
        raise RuntimeError(f"failed to fetch {V2FLY_ARCHIVE_URL}: {error}") from error

    data_files: dict[str, list[str]] = {}
    with tarfile.open(fileobj=io.BytesIO(archive_data), mode="r:gz") as archive:
        for member in archive.getmembers():
            if not member.isfile():
                continue
            parts = member.name.split("/", 2)
            if len(parts) != 3 or parts[1] != "data":
                continue
            extracted = archive.extractfile(member)
            if extracted is None:
                continue
            data_files[parts[2]] = extracted.read().decode("utf-8-sig", errors="replace").splitlines()

    V2FLY_ARCHIVE_CACHE = data_files
    return data_files


def read_v2fly_lines(base_url: str, list_name: str) -> list[str]:
    if base_url.rstrip("/") == V2FLY_DEFAULT_BASE_URL:
        data_files = load_v2fly_archive()
        if list_name not in data_files:
            raise KeyError(f"v2fly list not found in archive: {list_name}")
        return data_files[list_name]
    return fetch_lines(v2fly_data_url(base_url, list_name))


def split_v2fly_attrs(line: str) -> tuple[str, frozenset[str]]:
    fields = line.split()
    if not fields:
        return "", frozenset()
    attrs = frozenset(
        field[1:]
        for field in fields[1:]
        if field.startswith("@") and len(field) > 1 and not field.startswith("@-")
    )
    return fields[0], attrs


def parse_v2fly_rule_line(line: str) -> tuple[Rule | None, str | None]:
    cleaned = clean_line(line)
    if cleaned is None:
        return None, None

    expression, attrs = split_v2fly_attrs(cleaned)
    if not expression:
        return None, None

    if expression.startswith("regexp:"):
        return None, "REGEXP"
    if expression.startswith("domain:"):
        value = expression.removeprefix("domain:")
        normalized = normalize_domain(value)
        return (Rule("DOMAIN-SUFFIX", normalized, attrs), None) if normalized else (None, "DOMAIN")
    if expression.startswith("full:"):
        value = expression.removeprefix("full:")
        normalized = normalize_domain(value)
        return (Rule("DOMAIN", normalized, attrs), None) if normalized else (None, "FULL")
    if expression.startswith("keyword:"):
        value = expression.removeprefix("keyword:")
        normalized = normalize_keyword(value)
        return (Rule("DOMAIN-KEYWORD", normalized, attrs), None) if normalized else (None, "KEYWORD")
    if expression.startswith("include:"):
        return None, None
    if ":" in expression:
        return None, expression.split(":", 1)[0].upper()

    normalized = normalize_domain(expression)
    return (Rule("DOMAIN-SUFFIX", normalized, attrs), None) if normalized else (None, "DOMAIN")


def v2fly_include_filter(expression: str) -> tuple[str, Callable[[Rule], bool]]:
    fields = expression.split()
    target = fields[0].removeprefix("include:")
    include_attrs = {
        field[1:]
        for field in fields[1:]
        if field.startswith("@") and len(field) > 1 and not field.startswith("@-")
    }
    exclude_attrs = {
        field[2:]
        for field in fields[1:]
        if field.startswith("@-") and len(field) > 2
    }

    def matches(rule: Rule) -> bool:
        return include_attrs.issubset(rule.attrs) and rule.attrs.isdisjoint(exclude_attrs)

    return target, matches


def parse_v2fly_list(
    list_name: str,
    base_url: str,
    cache: dict[str, tuple[list[Rule], dict[str, int]]],
    stack: tuple[str, ...] = ()
) -> tuple[list[Rule], dict[str, int]]:
    if list_name in cache:
        return cache[list_name]
    if list_name in stack:
        chain = " -> ".join((*stack, list_name))
        raise ValueError(f"recursive v2fly include detected: {chain}")

    rules: list[Rule] = []
    skipped: dict[str, int] = {}
    seen: set[tuple[str, str, frozenset[str]]] = set()

    for line in read_v2fly_lines(base_url, list_name):
        cleaned = clean_line(line)
        if cleaned is None:
            continue

        if cleaned.startswith("include:"):
            target, matches = v2fly_include_filter(cleaned)
            included_rules, included_skipped = parse_v2fly_list(target, base_url, cache, (*stack, list_name))
            for skipped_type, count in included_skipped.items():
                skipped[skipped_type] = skipped.get(skipped_type, 0) + count
            for rule in included_rules:
                if not matches(rule):
                    continue
                full_key = (rule.rule_type, rule.value, rule.attrs)
                if full_key not in seen:
                    rules.append(rule)
                    seen.add(full_key)
            continue

        rule, skipped_type = parse_v2fly_rule_line(cleaned)
        if rule is not None:
            full_key = (rule.rule_type, rule.value, rule.attrs)
            if full_key not in seen:
                rules.append(rule)
                seen.add(full_key)
        elif skipped_type:
            skipped[skipped_type] = skipped.get(skipped_type, 0) + 1

    cache[list_name] = (rules, skipped)
    return rules, skipped


def parse_v2fly_source(source_config: dict) -> tuple[list[Rule], dict[str, int]]:
    base_url = source_config.get("base_url", "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data")
    cache: dict[str, tuple[list[Rule], dict[str, int]]] = {}
    rules: list[Rule] = []
    skipped: dict[str, int] = {}
    seen: set[tuple[str, str]] = set()

    for list_name in source_config["lists"]:
        parsed_rules, parsed_skipped = parse_v2fly_list(list_name, base_url, cache)
        for skipped_type, count in parsed_skipped.items():
            skipped[skipped_type] = skipped.get(skipped_type, 0) + count
        for rule in parsed_rules:
            if rule.key not in seen:
                rules.append(rule)
                seen.add(rule.key)

    return rules, skipped


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
        if source_config.get("kind") == "v2fly":
            rules, skipped = parse_v2fly_source(source_config)
            loaded[source_id] = rules
            skipped_by_source[source_id] = skipped
            continue

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
        source_config = config["sources"][source_id]
        if "urls" in source_config:
            urls.extend(source_config["urls"])
        elif source_config.get("kind") == "v2fly":
            base_url = source_config.get("base_url", "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data")
            urls.extend(v2fly_data_url(base_url, list_name) for list_name in source_config["lists"])
    return urls


def write_anywhere(path: Path, output_config: dict, rules: list[Rule], skipped: dict[str, int], sources: list[str]) -> None:
    arrs_lines = [
        f"{RULE_TYPE_TO_ARRS[rule.rule_type]}, {rule.value}"
        for rule in rules
        if rule.rule_type in RULE_TYPE_TO_ARRS
    ]
    skipped_for_anywhere = dict(skipped)
    for rule in rules:
        if rule.rule_type not in RULE_TYPE_TO_ARRS:
            skipped_for_anywhere[rule.rule_type] = skipped_for_anywhere.get(rule.rule_type, 0) + 1
    lines = [
        f"# NAME: {output_config['name']}",
        "# GENERATED-FOR: Anywhere Routing Rule Set",
        f"# DESCRIPTION: {output_config['description']}",
        f"# RULES: {len(arrs_lines)}",
        f"# SKIPPED: {sum(skipped_for_anywhere.values())}"
    ]
    if skipped_for_anywhere:
        lines.append("# SKIPPED-TYPES: " + ", ".join(f"{key}={skipped_for_anywhere[key]}" for key in sorted(skipped_for_anywhere)))
    if sources:
        lines.append("# SOURCES:")
        lines.extend(f"# - {source}" for source in sources)
    lines.extend(["", f"name = {output_config['name']}"])
    lines.extend(arrs_lines)
    write_text(path, lines)


def write_surge_domainset(path: Path, rules: list[Rule]) -> None:
    write_text(path, domainset_rule_lines(rules))


def write_surge_non_ip(path: Path, rules: list[Rule], include_client_rules: bool = False) -> None:
    write_text(path, surge_non_ip_rule_lines(rules, include_client_rules))


def write_surge_ip(path: Path, rules: list[Rule]) -> None:
    write_text(path, surge_ip_rule_lines(rules))


def write_loon_domainset(path: Path, rules: list[Rule]) -> None:
    write_text(path, loon_domainset_rule_lines(rules))


def write_loon_non_ip(path: Path, rules: list[Rule], include_client_rules: bool = False) -> None:
    write_text(path, loon_non_ip_rule_lines(rules, include_client_rules))


def write_loon_ip(path: Path, rules: list[Rule]) -> None:
    write_text(path, surge_ip_rule_lines(rules))


def domainset_rule_lines(rules: list[Rule]) -> list[str]:
    lines = []
    for rule in rules:
        if rule.rule_type == "DOMAIN":
            lines.append(rule.value)
        elif rule.rule_type == "DOMAIN-SUFFIX":
            lines.append(f".{rule.value}")
    return lines


def mihomo_domain_lines(rules: list[Rule]) -> list[str]:
    """Lines for `mihomo convert-ruleset domain text`.

    Mihomo's domain behavior expects a bare domain-set (no DOMAIN/DOMAIN-SUFFIX
    prefixes): `example.com` for exact, `+.example.com` for suffix, and `*`/`?`
    wildcards. Feeding classical-prefixed lines makes Mihomo store the whole
    string (e.g. `domain-suffix,example.com`) as a literal domain that never
    matches. DOMAIN-KEYWORD cannot be represented in a domain MRS and is dropped.
    """
    lines = []
    for rule in rules:
        if rule.rule_type == "DOMAIN":
            lines.append(rule.value)
        elif rule.rule_type == "DOMAIN-SUFFIX":
            lines.append(f"+.{rule.value}")
        elif rule.rule_type == "DOMAIN-WILDCARD":
            lines.append(rule.value)
    return lines


def domain_rule_lines(rules: list[Rule]) -> list[str]:
    return [
        f"{rule.rule_type},{rule.value}"
        for rule in rules
        if rule.rule_type in {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "DOMAIN-WILDCARD"}
    ]


def loon_domainset_rule_lines(rules: list[Rule]) -> list[str]:
    return [
        f"{rule.rule_type},{rule.value}"
        for rule in rules
        if rule.rule_type in {"DOMAIN", "DOMAIN-SUFFIX"}
    ]


def loon_non_ip_rule_lines(rules: list[Rule], include_client_rules: bool) -> list[str]:
    rule_types = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "URL-REGEX"}
    if include_client_rules:
        rule_types.add("USER-AGENT")
    return [
        f"{rule.rule_type},{rule.value}"
        for rule in rules
        if rule.rule_type in rule_types
    ]


def surge_non_ip_rule_lines(rules: list[Rule], include_client_rules: bool) -> list[str]:
    rule_types = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "DOMAIN-WILDCARD", "URL-REGEX"}
    if include_client_rules:
        rule_types.update({"USER-AGENT", "PROCESS-NAME"})
    return [
        f"{rule.rule_type},{rule.value}"
        for rule in rules
        if rule.rule_type in rule_types
    ]


def ip_rule_lines(rules: list[Rule]) -> list[str]:
    return [
        rule.value
        for rule in rules
        if rule.rule_type in {"IP-CIDR", "IP-CIDR6"}
    ]


def surge_ip_rule_lines(rules: list[Rule]) -> list[str]:
    return [
        f"{rule.rule_type},{rule.value},no-resolve"
        for rule in rules
        if rule.rule_type in {"IP-CIDR", "IP-CIDR6"}
    ]


def write_mihomo_mrs(path: Path, plain_path: Path, behavior: str) -> None:
    if not plain_path.read_text(encoding="utf-8").strip():
        relative_path = plain_path.relative_to(ROOT)
        raise ValueError(f"{relative_path} has no domain rules for Mihomo MRS")

    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["mihomo", "convert-ruleset", behavior, "text", str(plain_path), str(path)],
        cwd=ROOT,
        check=True
    )


def write_mihomo_domain_mrs(path: Path, rules: list[Rule]) -> None:
    lines = mihomo_domain_lines(rules)
    if not lines:
        relative_path = path.relative_to(ROOT)
        raise ValueError(f"{relative_path} has no domain rules for Mihomo MRS")

    path.parent.mkdir(parents=True, exist_ok=True)
    src_path = path.with_name(path.name + ".src.txt")
    write_text(src_path, lines)
    try:
        subprocess.run(
            ["mihomo", "convert-ruleset", "domain", "text", str(src_path), str(path)],
            cwd=ROOT,
            check=True
        )
    finally:
        src_path.unlink(missing_ok=True)


def wildcard_to_domain_regex(value: str) -> str:
    return "^" + re.escape(value).replace("\\*", ".*").replace("\\?", ".") + "$"


def sing_box_rule_set(rules: list[Rule]) -> dict:
    domain: list[str] = []
    domain_suffix: list[str] = []
    domain_keyword: list[str] = []
    domain_regex: list[str] = []
    ip_cidr: list[str] = []
    for rule in rules:
        if rule.rule_type == "DOMAIN":
            domain.append(rule.value)
        elif rule.rule_type == "DOMAIN-SUFFIX":
            domain_suffix.append(rule.value)
        elif rule.rule_type == "DOMAIN-KEYWORD":
            domain_keyword.append(rule.value)
        elif rule.rule_type == "DOMAIN-WILDCARD":
            domain_regex.append(wildcard_to_domain_regex(rule.value))
        elif rule.rule_type in {"IP-CIDR", "IP-CIDR6"}:
            ip_cidr.append(rule.value)

    rule_object: dict[str, list[str]] = {}
    if domain:
        rule_object["domain"] = domain
    if domain_suffix:
        rule_object["domain_suffix"] = domain_suffix
    if domain_keyword:
        rule_object["domain_keyword"] = domain_keyword
    if domain_regex:
        rule_object["domain_regex"] = domain_regex
    if ip_cidr:
        rule_object["ip_cidr"] = ip_cidr

    return {"version": 3, "rules": [rule_object]}


def write_sing_box_srs(path: Path, rules: list[Rule]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as temp:
        json.dump(sing_box_rule_set(rules), temp, ensure_ascii=False, indent=2)
        temp.write("\n")
        temp_path = Path(temp.name)
    try:
        subprocess.run(
            ["sing-box", "rule-set", "compile", str(temp_path), "-o", str(path)],
            cwd=ROOT,
            check=True
        )
    finally:
        temp_path.unlink(missing_ok=True)


def write_plain_domainset(path: Path, rules: list[Rule]) -> None:
    write_text(path, domain_rule_lines(rules))


def write_plain_non_ip(path: Path, rules: list[Rule]) -> None:
    write_text(path, domain_rule_lines(rules))


def write_plain_ip(path: Path, rules: list[Rule]) -> None:
    write_text(path, ip_rule_lines(rules))


def artifact_rules(
    artifact_id: str,
    artifact_config: dict,
    config: dict,
    source_rules: dict[str, list[Rule]],
    built_outputs: dict[str, list[Rule]]
) -> list[Rule]:
    source_marker_domains = set(config.get("source_marker_domains", []))
    source_ids = artifact_config["sources"] if "sources" in artifact_config else [artifact_config["source"]]
    rules: list[Rule] = []
    seen: set[tuple[str, str]] = set()

    for source_id in source_ids:
        if source_id in source_rules:
            source = source_rules[source_id]
        elif source_id in built_outputs:
            source = built_outputs[source_id]
        else:
            raise KeyError(f"{artifact_id} uses unknown artifact source: {source_id}")
        for rule in source:
            if rule.key not in seen:
                rules.append(rule)
                seen.add(rule.key)

    return apply_rule_overrides(rules, artifact_config, source_marker_domains)


def write_generated_outputs(
    config: dict,
    source_rules: dict[str, list[Rule]],
    source_skipped: dict[str, dict[str, int]]
) -> dict[str, list[Rule]]:
    source_marker_domains = set(config.get("source_marker_domains", []))
    built_outputs: dict[str, list[Rule]] = {}
    skipped_outputs: dict[str, dict[str, int]] = {}

    def artifact_clients(artifact_config: dict) -> set[str]:
        return set(artifact_config.get("clients", ["surge", "mihomo", "sing-box", "loon"]))

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
        clients = artifact_clients(artifact_config)
        plain_path = ROOT / "plain" / "domainset" / f"{name}.txt"
        write_plain_domainset(plain_path, rules)
        if "surge" in clients:
            write_surge_domainset(ROOT / "surge" / "domainset" / f"{name}.conf", rules)
        if "loon" in clients:
            write_loon_domainset(ROOT / "loon" / "domainset" / f"{name}.list", rules)
        if "mihomo" in clients:
            write_mihomo_domain_mrs(ROOT / "mihomo" / "domainset" / f"{name}.mrs", rules)
        if "sing-box" in clients:
            write_sing_box_srs(ROOT / "sing-box" / "domainset" / f"{name}.srs", rules)

    for name, artifact_config in config["artifacts"]["non-ip"].items():
        rules = artifact_rules(name, artifact_config, config, source_rules, built_outputs)
        clients = artifact_clients(artifact_config)
        plain_path = ROOT / "plain" / "non-ip" / f"{name}.txt"
        write_plain_non_ip(plain_path, rules)
        if "surge" in clients:
            write_surge_non_ip(
                ROOT / "surge" / "non-ip" / f"{name}.conf",
                rules,
                artifact_config.get("surge-client-rules", False)
            )
        if "loon" in clients:
            write_loon_non_ip(
                ROOT / "loon" / "non-ip" / f"{name}.list",
                rules,
                artifact_config.get("surge-client-rules", False)
            )
        if "mihomo" in clients:
            write_mihomo_domain_mrs(ROOT / "mihomo" / "non-ip" / f"{name}.mrs", rules)
        if "sing-box" in clients:
            write_sing_box_srs(ROOT / "sing-box" / "non-ip" / f"{name}.srs", rules)

    for name, artifact_config in config["artifacts"].get("ip", {}).items():
        rules = artifact_rules(name, artifact_config, config, source_rules, built_outputs)
        clients = artifact_clients(artifact_config)
        plain_path = ROOT / "plain" / "ip" / f"{name}.txt"
        write_plain_ip(plain_path, rules)
        if "surge" in clients:
            write_surge_ip(ROOT / "surge" / "ip" / f"{name}.conf", rules)
        if "loon" in clients:
            write_loon_ip(ROOT / "loon" / "ip" / f"{name}.list", rules)
        if "mihomo" in clients:
            write_mihomo_mrs(ROOT / "mihomo" / "ip" / f"{name}.mrs", plain_path, "ipcidr")
        if "sing-box" in clients:
            write_sing_box_srs(ROOT / "sing-box" / "ip" / f"{name}.srs", rules)

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
