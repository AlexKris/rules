# AGENTS.md

## Repository Purpose

This repository publishes personal, opinionated proxy rule overlays for multiple clients. It is not a full upstream mirror. Keep the repository public-safe: do not commit private media domains, proxy subscriptions, node names, tokens, or other personal infrastructure secrets.

Respond in Simplified Chinese by default when discussing this repository.

## Current Rule Model

`config/rules.json` is the source of truth for generated rule sets. The generated outputs are not sources.

Pipeline:

```text
upstream URLs / explicit local rules in config/rules.json
  -> scripts/build_rules.py parses, normalizes, deduplicates, applies explicit add/exclude patches
  -> generated client artifacts
```

`outputs` controls Anywhere `.arrs` files. `artifacts` controls Surge,
Mihomo, and sing-box files; artifact patches are explicit and do not inherit
same-named Anywhere output patches.

Current generated groups:

- `cdn`: SKK CDN domainset + non_ip, excluding Apple time sync and DigiCert certificate infrastructure.
- `apple-cdn`: SKK Apple CDN domainset + non_ip, with `is1-ssl.mzstatic.com` added.
- `apple-cn`: SKK Apple CN.
- `apple-services`: SKK Apple Services, with `time.apple.com` added.
- `direct-extra`: explicit direct overlay for WeChat service domains, `videocc.net`, `cache.video.iqiyi.com`, and DigiCert certificate infrastructure.
- `crypto`: `category-cryptocurrency` from `yuumimi/rules`, based on v2fly domain-list-community.

Manual overlays currently outside `config/rules.json`:

- `anywhere/kuro.arrs`
- `anywhere/citic.arrs`
- `surge/domainset/kuro.conf`
- `anywhere/mitm/source/google-cn-redirect.js`

Do not treat `anywhere/*.arrs` as upstream input. They are client artifacts or manual overlays.

## Output Formats

Anywhere:

- Generated from `outputs[*].targets.anywhere` in `config/rules.json`.
- Format mapping in `scripts/build_rules.py`:
  - `0`: IPv4 CIDR
  - `1`: IPv6 CIDR
  - `2`: domain or domain suffix
  - `3`: domain keyword
- Anywhere output files include headers with rule count and source URLs.

Surge / Shadowrocket:

- `surge/domainset/*.conf` contains bare exact domains and leading-dot suffixes.
- `surge/non-ip/*.conf` contains `DOMAIN`, `DOMAIN-SUFFIX`, and `DOMAIN-KEYWORD` rules.
- Generated from `artifacts` in `config/rules.json`, using SKK effective rules plus explicit local patches.
- Shadowrocket can use the same Surge text files where profile syntax allows it.

Mihomo:

- Generated `.mrs` files require `mihomo` CLI.
- Generated from the same `artifacts` entries as Surge.
- Use `behavior: domain` and `format: mrs` for these outputs.

sing-box:

- Generated `.json` and `.srs` rule sets require `sing-box` CLI.
- Generated from the same `artifacts` entries as Surge.
- Published remote rule sets should use `.srs` with `format: binary` in client profiles.

MITM:

- `scripts/build_mitm.py` builds `anywhere/mitm/google-cn-redirect.amrs` from `anywhere/mitm/source/google-cn-redirect.js`.
- Edit the JS source, not the generated `.amrs`, then run the MITM build script.

## Build Commands

Run from the repository root:

```sh
python3 scripts/build_rules.py
python3 scripts/build_mitm.py
```

`build_rules.py` requires network access and these local CLIs:

```sh
mihomo
sing-box
```

If either CLI is missing, do not hand-edit generated `.mrs` or `.srs` files. Install the CLI or defer generation.

## Verification

Before committing rule changes, run the checks relevant to the changed files:

```sh
python3 -m json.tool config/rules.json >/tmp/rules_config.json
git diff --check
```

For generated rules:

```sh
python3 scripts/build_rules.py
```

For MITM rules:

```sh
python3 scripts/build_mitm.py
```

Spot-check important routing expectations after generation:

```sh
rg -n "time\.apple\.com|ocsp\.digicert\.com|binance\.com|okx\.com" anywhere surge
```

Expected behavior:

- `time.apple.com` belongs in Apple Services, not CDN.
- DigiCert certificate infrastructure belongs in Direct Extra, not CDN.
- Kuro and CITIC remain separate rule sets.
- `getui` remains intentionally excluded unless the user explicitly changes policy.
- Crypto currently uses only `category-cryptocurrency`; do not merge Dler's Crypto list unless the user explicitly accepts its unclear license risk.

## Change Rules

- Prefer editing `config/rules.json` and regenerating outputs over hand-editing generated files.
- Keep manual overlays small and explicit. If a manual overlay grows or needs multiple client formats, move it into `config/rules.json` and generation.
- Preserve lowercase file names and hyphenated rule ids, e.g. `apple-cdn`, `direct-extra`.
- Do not add unrelated client formats just because a source exists. Add outputs only when the target client profile actually needs them.
- If adding an upstream source, check its license first and update `NOTICE.md` when appropriate.
- Avoid Dler or other no-license lists as direct generated sources unless the user explicitly approves the licensing tradeoff.
- Do not commit private domains, private media services, proxy nodes, subscription URLs, API keys, account ids, or tokens.

## Git

Use Conventional Commits, for example:

```text
feat: add anywhere crypto rules
fix: preserve surge domainset suffix semantics
docs: document rule maintenance workflow
```

Do not include AI/Codex attribution in commit messages.
