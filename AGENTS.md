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

`outputs` controls Anywhere `.arrs` files. `artifacts` controls Surge, Loon,
Mihomo, and sing-box files; artifact patches are explicit and do not inherit
same-named Anywhere output patches. `artifacts[*].clients` can narrow client
artifact generation while still writing the matching `plain/` file.

Current generated groups:

- `proxy`: SKK CDN domainset + non_ip + SKK Global, excluding Apple time sync and DigiCert certificate infrastructure.
- `apple`: SKK Apple CDN + CN + Services, with `is1-ssl.mzstatic.com` and `time.apple.com` added.
- `download`: SKK Download domainset + non_ip. Do not merge Microsoft CDN into it.
- `domestic`: SKK Domestic non_ip rules.
- `direct`: SKK Direct non_ip rules. Do not merge `direct-extra` into it.
- `lan`: SKK LAN non_ip rules. The Anywhere `lan.arrs` output also includes SKK LAN IP CIDR rules.
- `lan-ip`: SKK LAN IP CIDR rules, kept as a separate generated rule set for non-Anywhere clients and legacy Anywhere subscriptions.
- `china-ip`: SKK China IP CIDR rules. Do not restore SKK `ip/domestic.conf`.
- `cdn`: SKK CDN domainset + non_ip, excluding Apple time sync and DigiCert certificate infrastructure.
- `apple-cdn`: SKK Apple CDN domainset + non_ip, with `is1-ssl.mzstatic.com` added.
- `apple-cn`: SKK Apple CN.
- `apple-services`: SKK Apple Services, with `time.apple.com` added.
- `speedtest`: SKK Speedtest domainset.
- `ai`: v2fly `category-ai-!cn`, with explicit Claude/Anthropic additions.
- `stream`, `stream-hk`, `stream-tw`, `stream-jp`, `stream-us`, `stream-kr`, `stream-eu`: SKK Stream Services non_ip rule sets.
- `google`: v2fly `google`, generated only for Surge/Loon/plain. It includes YouTube via upstream; keep Stream before Google in profiles.
- `cn-domain`: v2fly `geolocation-cn`, generated for Surge/Loon/plain and as an optional Anywhere direct fallback.
- `not-cn-domain`: v2fly `geolocation-!cn`, generated only for Surge/Loon/plain.
- `telegram`: SKK Telegram domains. The Anywhere `telegram.arrs` output also includes SKK Telegram IP CIDR rules.
- `telegram-ip`: SKK Telegram IP CIDR, kept as a separate generated rule set for non-Anywhere clients and legacy Anywhere subscriptions.
- `paypal`: v2fly `paypal`.
- `microsoft`: v2fly `microsoft`.
- `microsoft-cdn`: SKK Microsoft CDN.
- `direct-extra`: explicit direct overlay for WeChat service domains, Kuro, CITIC, `videocc.net`, `cache.video.iqiyi.com`, and DigiCert certificate infrastructure.
- `crypto`: v2fly `category-cryptocurrency`, generated for Anywhere and Surge/Loon/plain text only. Do not merge Dler's Crypto list.

Manual overlays currently outside `config/rules.json`:

- `anywhere/kuro.arrs`
- `anywhere/citic.arrs`
- `surge/domainset/kuro.conf`
- `anywhere/mitm/google-cn-redirect.amrs`
- `anywhere/mitm/source/youtube-enhance-anywhere.js`
- `anywhere/mitm/source/vendor/maasea-youtube.response.js`

Do not treat `anywhere/*.arrs` as upstream input. They are client artifacts or manual overlays.

## Output Formats

Anywhere:

- Generated from `outputs[*].targets.anywhere` in `config/rules.json`.
- `domestic`, `direct`, `google`, `not-cn-domain`, `speedtest`, and Microsoft are intentionally not generated for Anywhere.
- `domestic` and `direct` SKK sources include client-specific matchers that ARRS cannot represent.
- `stream*` is generated for Anywhere because its SKK sources are domain/non-IP rules that map cleanly to ARRS.
- `proxy` replaces the old separate CDN/global runtime rules in new Anywhere profiles. `apple` replaces the split Apple rule sets. `lan` and `telegram` combine domain and IP CIDR rules for Anywhere. `cn-domain` is a broad v2fly `geolocation-cn` direct fallback. `cdn`, split Apple, `lan-ip`, `telegram-ip`, `kuro`, and `citic` Anywhere files remain published only for compatibility.
- `download` Anywhere output contains the domainset portion only; SKK Download non_ip includes wildcard and URL regex rules that do not map cleanly to ARRS.
- Format mapping in `scripts/build_rules.py`:
  - `0`: IPv4 CIDR
  - `1`: IPv6 CIDR
  - `2`: domain or domain suffix
  - `3`: domain keyword
- Anywhere output files include headers with rule count and source URLs.

Surge / Shadowrocket:

- `surge/domainset/*.conf` contains bare exact domains and leading-dot suffixes.
- `surge/non-ip/*.conf` contains `DOMAIN`, `DOMAIN-SUFFIX`, and `DOMAIN-KEYWORD` rules.
- `surge/non-ip/*.conf` can also contain `DOMAIN-WILDCARD` and `URL-REGEX` when upstream uses them.
- `surge/non-ip/direct.conf`, `surge/non-ip/domestic.conf`, and
  `surge/non-ip/stream*.conf` also preserve SKK `USER-AGENT` and
  `PROCESS-NAME` rules.
- `surge/ip/*.conf` contains `IP-CIDR` and `IP-CIDR6` rules with `no-resolve`.
- Generated from `plain/domainset/*.txt` and `plain/non-ip/*.txt`.
- Shadowrocket can use the same Surge text files where profile syntax allows it.

Loon:

- `loon/domainset/*.list` converts domainset rules to full `DOMAIN` and
  `DOMAIN-SUFFIX` rules; it does not use Surge `DOMAIN-SET` bare-domain syntax.
- `loon/non-ip/*.list` contains `DOMAIN`, `DOMAIN-SUFFIX`,
  `DOMAIN-KEYWORD`, `URL-REGEX`, and `USER-AGENT` when upstream uses supported
  client matchers.
- `loon/non-ip/*.list` intentionally omits `DOMAIN-WILDCARD` and
  `PROCESS-NAME` because they are not listed in Loon's official rule syntax.
- `loon/ip/*.list` contains `IP-CIDR` and `IP-CIDR6` rules with `no-resolve`.
- Use files in Loon `[Remote Rule]` as `URL,policy=<Policy>,enabled=true`.

Mihomo:

- Generated `.mrs` files require `mihomo` CLI.
- Domain `.mrs` (`mihomo/domainset/*.mrs`, `mihomo/non-ip/*.mrs`) use `behavior: domain` and are built by `write_mihomo_domain_mrs`, which emits bare domain-set lines: exact domain, `+.` for suffix, `*`/`?` wildcards.
- DO NOT feed the classical `DOMAIN,`/`DOMAIN-SUFFIX,`-prefixed `plain/*.txt` to `mihomo convert-ruleset domain`. Mihomo then stores each whole line (e.g. `domain-suffix,steamcontent.com`) as a single literal domain that never matches real queries, silently breaking the whole rule set (traffic falls through to geosite/GEOIP fallbacks). The domain-set format is mandatory.
- `DOMAIN-KEYWORD` cannot be represented in a domain `.mrs`. For non-ip sets that contain keywords it is published separately as a `behavior: classical` text rule-set at `mihomo/classical/<name>.list` (keyword lines only), so profiles can keep keyword matching via a classical rule-provider. It is still kept inline in Surge/Loon/plain and as `domain_keyword` in sing-box.
- IP `.mrs` (`mihomo/ip/*.mrs`) use `behavior: ipcidr`, generated from `plain/ip/*.txt`.
- Google and broad CN geosite fallback rules should use MetaCubeX official geosite files, not local generated `.mrs` files.

sing-box:

- Generated `.srs` rule sets require `sing-box` CLI.
- JSON files are temporary build inputs and are not published.
- Published remote rule sets should use `.srs` with `format: binary` in client profiles.
- Google and broad CN geosite fallback rules should use SagerNet official geosite files, not local generated `.srs` files.

Plain:

- `plain/domainset/*.txt`, `plain/non-ip/*.txt`, and `plain/ip/*.txt` are generated observable artifacts.
- Plain files use normalized rule syntax such as `DOMAIN` and `DOMAIN-SUFFIX`.
- Plain domain files may include `DOMAIN-WILDCARD`; these are valid Mihomo domain rules and are converted to sing-box `domain_regex`.
- `URL-REGEX` is preserved only in Surge and Loon outputs and is intentionally omitted from plain/Mihomo/sing-box artifacts.
- Plain stream files intentionally omit `USER-AGENT` and `PROCESS-NAME`; `USER-AGENT` is preserved in Surge and Loon outputs, while `PROCESS-NAME` is preserved only in Surge outputs.
- They are not sources; edit `config/rules.json` and regenerate instead.

v2fly:

- `kind: "v2fly"` sources read v2fly `data/*` files directly.
- The default v2fly source is loaded from the GitHub source archive once per build, not fetched as many individual raw files.
- `include:` is resolved recursively.
- v2fly `google` includes YouTube upstream; profile ordering must keep Stream before Google when Google is a separate policy.
- bare domains and `domain:` become `DOMAIN-SUFFIX`; `full:` becomes `DOMAIN`; `keyword:` becomes `DOMAIN-KEYWORD`.
- `regexp:` is intentionally skipped and counted in generated headers.
- v2fly attributes such as `@ads` and `@cn` are parsed for include filtering only and are not written to generated client files.

MITM:

- `anywhere/mitm/google-cn-redirect.amrs` is maintained directly.
- It uses native Anywhere transparent rewrite rules, not JavaScript.
- `scripts/build_mitm.py` builds `anywhere/mitm/youtube-enhance-anywhere.amrs`
  from local JavaScript sources under `anywhere/mitm/source/`.
- Edit the JS sources, not the generated YouTube `.amrs`, then run the MITM
  build script.

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
rg -n "time\.apple\.com|ocsp\.digicert\.com|youtube\.com|google\.com|googleapis\.com|apple\.com|icloud\.com|mzstatic\.com|officecdn\.microsoft\.com|binance\.com|okx\.com|openrouter\.ai|paypal\.com|ctldl\.windowsupdate\.com|91\.108\.4\.0/22|10\.0\.0\.0/8|192\.168\.0\.0/16|1\.1\.8\.0/24" anywhere surge loon plain
```

Expected behavior:

- `time.apple.com` belongs in Apple Services, not CDN.
- Unified `proxy` contains CDN and SKK Global rules, but excludes Apple time sync and DigiCert certificate infrastructure.
- Unified `apple` contains Apple CDN, CN, Services, `is1-ssl.mzstatic.com`, and `time.apple.com`; it is intended for DIRECT.
- `download` remains separate from `microsoft-cdn`.
- `domestic`, `direct`, and `lan` are non-IP direct rule sets and belong before IP rule sets in profiles.
- `lan-ip` and `china-ip` are IP/CIDR direct rule sets; Surge outputs include `no-resolve`.
- `direct` is upstream base direct; `direct-extra` is the personal direct overlay.
- DigiCert certificate infrastructure belongs in Direct Extra, not CDN.
- AI uses v2fly `category-ai-!cn`; exact upstream `@ads` entries may be preserved, while `regexp:` entries are skipped.
- Stream Surge outputs preserve SKK `USER-AGENT` and `PROCESS-NAME`; Loon outputs preserve `USER-AGENT` and skip `PROCESS-NAME`; plain/Mihomo/sing-box outputs are domain-only.
- Google uses v2fly `google` and includes YouTube upstream; Stream must be ordered before Google in profiles.
- `cn-domain` is generated for Surge/Loon/plain and as an optional Anywhere direct fallback; `not-cn-domain` is Surge/Loon/plain-only. Do not generate local Mihomo or sing-box artifacts for either.
- For Anywhere, `telegram.arrs` combines Telegram domain and IP CIDR rules.
  Keep `telegram-ip` published separately for non-Anywhere clients and legacy
  Anywhere subscriptions.
- For Anywhere, `lan.arrs` combines LAN domain and IP CIDR rules. Keep
  `lan-ip` published separately for non-Anywhere clients and legacy Anywhere
  subscriptions.
- Microsoft CDN remains separate from broad Microsoft.
- PayPal remains separate from broad CDN and proxy rule sets.
- Kuro and CITIC remain separate compatibility rule sets; their direct domains also belong in Direct Extra for new Anywhere profiles.
- `getui` remains intentionally excluded unless the user explicitly changes policy.
- Crypto uses v2fly `category-cryptocurrency`; it is generated for Anywhere and Surge/Loon/plain text only. Do not merge Dler's Crypto list unless the user explicitly accepts its unclear license risk.

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
