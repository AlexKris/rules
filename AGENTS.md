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
  -> plain text rule artifacts
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
- `speedtest`: SKK Speedtest domainset.
- `ai`: v2fly `category-ai-!cn`, with explicit Claude/Anthropic additions.
- `stream`, `stream-hk`, `stream-tw`, `stream-jp`, `stream-us`, `stream-kr`, `stream-eu`: SKK Stream Services non_ip rule sets.
- `telegram`: SKK Telegram domains.
- `telegram-ip`: SKK Telegram IP CIDR.
- `paypal`: v2fly `paypal`.
- `microsoft`: v2fly `microsoft`.
- `microsoft-cdn`: SKK Microsoft CDN.
- `direct-extra`: explicit direct overlay for WeChat service domains, `videocc.net`, `cache.video.iqiyi.com`, and DigiCert certificate infrastructure.
- `crypto`: v2fly `category-cryptocurrency`.

Manual overlays currently outside `config/rules.json`:

- `anywhere/kuro.arrs`
- `anywhere/citic.arrs`
- `surge/domainset/kuro.conf`
- `anywhere/mitm/source/google-cn-redirect.js`

Do not treat `anywhere/*.arrs` as upstream input. They are client artifacts or manual overlays.

## Output Formats

Anywhere:

- Generated from `outputs[*].targets.anywhere` in `config/rules.json`.
- `speedtest`, `stream*`, and Microsoft are intentionally not generated for Anywhere.
- Format mapping in `scripts/build_rules.py`:
  - `0`: IPv4 CIDR
  - `1`: IPv6 CIDR
  - `2`: domain or domain suffix
  - `3`: domain keyword
- Anywhere output files include headers with rule count and source URLs.

Surge / Shadowrocket:

- `surge/domainset/*.conf` contains bare exact domains and leading-dot suffixes.
- `surge/non-ip/*.conf` contains `DOMAIN`, `DOMAIN-SUFFIX`, and `DOMAIN-KEYWORD` rules.
- `surge/non-ip/stream*.conf` also preserves SKK `USER-AGENT` and `PROCESS-NAME` rules.
- `surge/ip/*.conf` contains `IP-CIDR` and `IP-CIDR6` rules with `no-resolve`.
- Generated from `plain/domainset/*.txt` and `plain/non-ip/*.txt`.
- Shadowrocket can use the same Surge text files where profile syntax allows it.

Mihomo:

- Generated `.mrs` files require `mihomo` CLI.
- Generated from `plain/domainset/*.txt`, `plain/non-ip/*.txt`, and `plain/ip/*.txt`.
- Use `behavior: domain` for domain/non-ip `.mrs` files.
- Use `behavior: ipcidr` for `mihomo/ip/*.mrs`.

sing-box:

- Generated `.srs` rule sets require `sing-box` CLI.
- JSON files are temporary build inputs and are not published.
- Published remote rule sets should use `.srs` with `format: binary` in client profiles.

Plain:

- `plain/domainset/*.txt`, `plain/non-ip/*.txt`, and `plain/ip/*.txt` are generated observable artifacts.
- Plain files use normalized rule syntax such as `DOMAIN` and `DOMAIN-SUFFIX`.
- Plain stream files intentionally omit `USER-AGENT` and `PROCESS-NAME`; those are preserved only in Surge outputs.
- They are not sources; edit `config/rules.json` and regenerate instead.

v2fly:

- `kind: "v2fly"` sources read v2fly `data/*` files directly.
- `include:` is resolved recursively.
- bare domains and `domain:` become `DOMAIN-SUFFIX`; `full:` becomes `DOMAIN`; `keyword:` becomes `DOMAIN-KEYWORD`.
- `regexp:` is intentionally skipped and counted in generated headers.
- v2fly attributes such as `@ads` and `@cn` are parsed for include filtering only and are not written to generated client files.

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
rg -n "time\.apple\.com|ocsp\.digicert\.com|binance\.com|okx\.com|openrouter\.ai|paypal\.com|ctldl\.windowsupdate\.com|91\.108\.4\.0/22" anywhere surge plain
```

Expected behavior:

- `time.apple.com` belongs in Apple Services, not CDN.
- DigiCert certificate infrastructure belongs in Direct Extra, not CDN.
- AI uses v2fly `category-ai-!cn`; exact upstream `@ads` entries may be preserved, while `regexp:` entries are skipped.
- Stream Surge outputs preserve SKK `USER-AGENT` and `PROCESS-NAME`; plain/Mihomo/sing-box outputs are domain-only.
- Telegram IP belongs in `telegram-ip`, not mixed into `telegram`.
- Microsoft CDN remains separate from broad Microsoft.
- PayPal remains separate from broad CDN and proxy rule sets.
- Kuro and CITIC remain separate rule sets.
- `getui` remains intentionally excluded unless the user explicitly changes policy.
- Crypto uses v2fly `category-cryptocurrency`; do not merge Dler's Crypto list unless the user explicitly accepts its unclear license risk.

## Change Rules

- Prefer editing `config/rules.json` and regenerating outputs over hand-editing generated files.
- Keep manual overlays small and explicit. If a manual overlay grows or needs multiple client formats, move it into `config/rules.json` and generation.
- Preserve lowercase file names and hyphenated rule ids, e.g. `apple-cdn`, `direct-extra`.
- Do not add unrelated client formats just because a source exists. Add outputs only when the target client profile actually needs them.
- If adding an upstream source, check its license first and update `NOTICE.md` when appropriate.
- Avoid Dler or other no-license lists as direct generated sources unless the user explicitly approves the licensing tradeoff.
- Prefer SKK published files from `https://raw.githubusercontent.com/SukkaLab/ruleset.skk.moe/master/List/...` over `https://ruleset.skk.moe/List/...`.
- Do not commit private domains, private media services, proxy nodes, subscription URLs, API keys, account ids, or tokens.

## Git

Use Conventional Commits, for example:

```text
feat: add anywhere crypto rules
fix: preserve surge domainset suffix semantics
docs: document rule maintenance workflow
```

Do not include AI/Codex attribution in commit messages.
