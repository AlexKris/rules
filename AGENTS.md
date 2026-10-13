# AGENTS.md

## Repository Purpose

This repository publishes personal, opinionated proxy rule overlays for multiple clients. It is not a full upstream mirror. Keep the repository public-safe: do not commit private media domains, proxy subscriptions, node names, tokens, or other personal infrastructure secrets.

Respond in Simplified Chinese by default when discussing this repository.

## Current Rule Model

`config/rules.json` is the source of truth for generated rule sets. The generated outputs are not sources.

Pipeline:

```text
local upstream checkouts / upstream URLs / explicit local rules in config/rules.json
  -> scripts/build_rules.py parses, normalizes, deduplicates, applies explicit add/exclude patches,
     drops domain rules already covered by a DOMAIN-SUFFIX in the same set
  -> plain text rule artifacts
  -> generated client artifacts
```

`outputs` controls Anywhere `.arrs` files. `artifacts` controls Surge, Loon,
Mihomo, and sing-box files; artifact patches are explicit and do not inherit
same-named Anywhere output patches. `artifacts[*].clients` can narrow client
artifact generation while still writing the matching `plain/` file.

Rule-set taxonomy:

A rule set exists only for one of these reasons. If none applies, do not add it.

1. Its policy differs from `FINAL` (Proxy): `ai`, `paypal`, `stream*`, `telegram`,
   `google`, `download`, `apple`, `microsoft-cdn`, `direct`, `cn-domain`.
2. It must pre-empt a broader set ordered after it: `apple-proxy` before `apple`,
   `stream` before `google`, `direct-extra` first.
3. It is hand-maintained: `direct-extra` is the only personal overlay.
4. It would settle a domain before a rule that triggers DNS resolution. Every IP
   rule published here carries `no-resolve`, so this never applies; a `proxy` or
   `not-cn-domain` set would only repeat `FINAL`.
5. It keeps known-proxy domains on a proxy when `FINAL` is switched to DIRECT.
   The profiles never do that, so this never applies either.

Domain and IP rules of one service (`telegram` / `telegram-ip`, `lan` / `lan-ip`)
are split only because a Mihomo MRS holds either domains or CIDRs, not both;
Anywhere outputs combine them. Sets with the same policy and the same meaning
are merged: SKK Domestic lives inside `cn-domain`, the Apple domainset inside
`apple`, SKK LAN domains inside `direct`.

Profile order: `direct-extra` > service sets with their own policy > `apple-proxy`
> `apple` > `microsoft-cdn` > `download` > `google` > `direct` > `cn-domain` > IP
rules (`no-resolve`) > `FINAL`.

Current generated groups:

- `apple`: SKK Apple CDN domainset + non_ip + CN + Services, with `is1-ssl.mzstatic.com` and `time.apple.com` added. The domainset rows are folded into the single non-ip set and the ones already covered by the broad suffixes are dropped. It is intended for DIRECT.
- `apple-proxy`: explicit carve-out of Apple domains that must not take the unified `apple` direct route. Generated for Surge, Loon, Mihomo, and sing-box. It must be ordered before `apple` in every profile.
- `download`: SKK Download domainset + non_ip. Do not merge Microsoft CDN into it.
- `game-download`: SKK Game Download domainset.
- `speedtest`: SKK Speedtest domainset.
- `microsoft-cdn`: SKK Microsoft CDN. Broad Microsoft has no rule set; it falls through to `FINAL`.
- `direct`: SKK Direct non_ip rules (LAN names, PT trackers, academic sites, downloader processes). It already contains every SKK LAN domain rule. Do not merge `direct-extra` into it.
- `lan`: Anywhere-only output combining SKK LAN domain and IP CIDR rules.
- `lan-ip`: SKK LAN IP CIDR rules, kept as a separate generated rule set for non-Anywhere clients and legacy Anywhere subscriptions.
- `china-ip`: SKK China IP CIDR rules. Do not restore SKK `ip/domestic.conf`.
- `ai`: v2fly `category-ai-!cn`, with explicit Claude/Anthropic additions. `hf.co` is excluded so that the Hugging Face bulk-download hosts `cdn.hf.co` and `cas-bridge.xethub.hf.co` fall through to `download` instead of the region-restricted AIGC policy; `huggingface.co` stays in `ai`.
- `stream`, `stream-hk`, `stream-tw`, `stream-jp`, `stream-us`, `stream-kr`, `stream-eu`: SKK Stream Services non_ip rule sets. `stream` adds `tv.apple.com` and `hls-svod.itunes.apple.com` so the Apple TV+ chain stays on one policy, and `ytimg.com` / `youtu.be` so YouTube thumbnails and short links follow the video policy instead of `google`.
- `google`: v2fly `google`, generated for Surge/Loon/Mihomo/sing-box/Anywhere/plain. It includes YouTube via upstream; keep Stream before Google in profiles, and above Google in the Anywhere Routing list (identical patterns go to the higher set).
- `cn-domain`: v2fly `cn` (`geolocation-cn` plus the China TLDs in `tld-cn`, including `cn`) plus Loyalsoldier `surge-rules` `direct.txt` filtered by the pinned Tranco top-1M list (`keep_ranked`). A Loyalsoldier rule is kept only when its site (last two labels) is itself listed in `direct.txt` and is ranked; this drops the unranked long tail and the China endpoints of foreign sites (Apple, Google, Microsoft, Kaspersky), which have their own rule sets. `analytics.tiktok.com` is excluded because it is deeper than Stream's `tiktok.com` and would win in Anywhere. SKK Domestic non_ip is merged in as well (domains only; its `USER-AGENT` rows and watermark domain are dropped): it is the hand-curated list of services reachable from mainland China, backfills CDN and API hosts the Tranco filter removes (`ccgslb.com`, `12306.com`), and carries a few foreign services with mainland presence (`battle.net`, Steam connection servers). Generated for Surge/Loon/Mihomo/sing-box/Anywhere/plain from the same rules. To refresh the ranking, replace the list ID in the `keep_ranked` URL with a current one from tranco-list.eu; do not track the daily latest list, which would churn the rules every build. Do not switch to MetaCubeX `geosite:cn` / blackmatrix7 ChinaMax: ChinaMax is self-described as experimental, adds clearly non-China entries (whole `.ms` TLD, garmin.com, java.com, bstatic.com), and MetaCubeX drops v2fly `geolocation-cn` entirely.
- `telegram`: SKK Telegram domains. The Anywhere `telegram.arrs` output also includes SKK Telegram IP CIDR rules.
- `telegram-ip`: SKK Telegram IP CIDR, kept as a separate generated rule set for non-Anywhere clients and legacy Anywhere subscriptions.
- `paypal`: v2fly `paypal`.
- `direct-extra`: explicit direct overlay for WeChat service domains, Kuro, CITIC, `videocc.net`, `cache.video.iqiyi.com`, and DigiCert certificate infrastructure. It also carries two carve-outs that would otherwise be stolen by a policy whose rule set is ordered earlier: the six mainland speedtest endpoints inside `speedtest`, and `cn.download.nvidia.com` (`download` matches it via `DOMAIN-SUFFIX,download.nvidia.com`). The 21Vianet China Microsoft `.cn` domains, `apple-dns.cn`, and `idms-apple.com.akadns.net` stay here as explicit direct entries; they used to be stolen by the removed `microsoft` and `not-cn-domain` sets. Because `direct-extra` is the first rule set in every profile, these take
effect on every client without a per-profile edit.

`apple-proxy` must not contain `statici.icloud.com`. It serves iCloud static assets including the Apple
ID avatar shown in iOS Settings, and a mainland-China Apple ID needs it direct.

Removed groups, do not bring them back: `proxy`, `cdn`, `not-cn-domain`, `crypto`,
`microsoft`, the split Apple sets, `domestic` (now inside `cn-domain`), `lan` non-ip
(inside `direct`), and the Kuro / CITIC compatibility files (inside `direct-extra`).

Manual overlays currently outside `config/rules.json`:

- `anywhere/mitm/google-cn-redirect.amrs`
- `anywhere/mitm/source/youtube-enhance-anywhere.js`
- `anywhere/mitm/source/vendor/maasea-youtube.response.js`

Do not treat `anywhere/*.arrs` as upstream input. They are client artifacts or manual overlays.

## Output Formats

Anywhere:

- Generated from `outputs[*].targets.anywhere` in `config/rules.json`.
- `outputs[*].routing` emits the ARRS `routing` header (`1` Direct, `2` Reject) so Anywhere seeds the action on first import; it is set on the always-direct sets (`direct-extra`, `cn-domain`, `lan`, `lan-ip`, `china-ip`, `apple`). A subscription refresh never changes an action chosen in the app.
- `direct`, `speedtest`, and `microsoft-cdn` are intentionally not generated for Anywhere.
- `direct` SKK source includes client-specific matchers that ARRS cannot represent.
- `stream*` is generated for Anywhere because its SKK sources are domain/non-IP rules that map cleanly to ARRS.
- `lan` and `telegram` combine domain and IP CIDR rules for Anywhere. `cn-domain` uses the same rules as the other clients. `apple-proxy` must sit above `apple` in the Routing list because both contain `apple.news`. `lan-ip` and `telegram-ip` Anywhere files remain published only for compatibility.
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
- `surge/non-ip/direct.conf` and `surge/non-ip/stream*.conf` also preserve SKK
  `USER-AGENT` and `PROCESS-NAME` rules.
- `surge/ip/*.conf` contains `IP-CIDR` and `IP-CIDR6` rules with `no-resolve`.
- Generated from the same in-memory rule model as `plain/`, not from the plain files.
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
- Domain `.mrs` (`mihomo/domainset/*.mrs`, `mihomo/non-ip/*.mrs`) use `behavior: domain` and are built by `write_mihomo_domain_mrs`, which emits bare domain-set lines: exact domain, `+.` for suffix, `*`/`?` wildcards. Mihomo only stores `*` as a whole label (`*.example.com`); a partial-label wildcard such as `download*.mediafire.com` is skipped by `mihomo convert-ruleset` with a warning. The build keeps those out of the MRS, publishes them as `DOMAIN-REGEX` in the classical list below, and fails if mihomo still reports a skipped domain.
- DO NOT feed the classical `DOMAIN,`/`DOMAIN-SUFFIX,`-prefixed `plain/*.txt` to `mihomo convert-ruleset domain`. Mihomo then stores each whole line (e.g. `domain-suffix,steamcontent.com`) as a single literal domain that never matches real queries, silently breaking the whole rule set (traffic falls through to geosite/GEOIP fallbacks). The domain-set format is mandatory.
- `DOMAIN-KEYWORD` and partial-label wildcards cannot be represented in a domain `.mrs`. For non-ip sets that contain them, they are published separately as a `behavior: classical` text rule-set at `mihomo/classical/<name>.list` (`DOMAIN-KEYWORD` and `DOMAIN-REGEX` lines), so profiles can keep matching them via a classical rule-provider next to the `.mrs` provider. Keywords are still kept inline in Surge/Loon/plain and as `domain_keyword` in sing-box.
- IP `.mrs` (`mihomo/ip/*.mrs`) use `behavior: ipcidr`, generated from `plain/ip/*.txt`.
- `mihomo/non-ip/google.mrs` and `mihomo/non-ip/cn-domain.mrs` are generated locally like other domain sets.

sing-box:

- Generated `.srs` rule sets require `sing-box` CLI.
- JSON files are temporary build inputs and are not published.
- Published remote rule sets should use `.srs` with `format: binary` in client profiles.
- Preserve SagerNet semantics for the one foundation rule set listed in
  `config/rules.json` under `sing_box_mirrors` (`geosite-private`). Copy and
  validate the upstream `.srs` bytes into `sing-box/geosite/`, published via our
  Pages. It only selects local DNS for LAN names; Telegram, Google, and China IP
  use the generated `telegram`, `google`, and `china-ip` sets. Do not bring the
  `geosite-telegram`, `geosite-google`, or `geoip-cn` mirrors back.
- Do not feed this mirror through the normalized converter: it skips v2fly
  regex rules.
- CI checks out the whitelisted `rule-set` branch file into
  `.upstream/sing-geosite`; strict local-source mode must fail if the source is
  missing. Invalid or empty SRS must fail the build.

Plain:

- `plain/domainset/*.txt`, `plain/non-ip/*.txt`, and `plain/ip/*.txt` are generated observable artifacts.
- Plain files use normalized rule syntax such as `DOMAIN` and `DOMAIN-SUFFIX`.
- Plain domain files may include `DOMAIN-WILDCARD`; these go into the Mihomo domain MRS when `*` fills a whole label, otherwise into the Mihomo classical list as `DOMAIN-REGEX`, and are always converted to sing-box `domain_regex`.
- `URL-REGEX` is preserved only in Surge and Loon outputs and is intentionally omitted from plain/Mihomo/sing-box artifacts.
- Plain stream files intentionally omit `USER-AGENT` and `PROCESS-NAME`; `USER-AGENT` is preserved in Surge and Loon outputs, while `PROCESS-NAME` is preserved only in Surge outputs.
- They are not sources; edit `config/rules.json` and regenerate instead.

v2fly:

- `kind: "v2fly"` sources read v2fly `data/*` files directly.
- When `local_dir` exists, v2fly sources are loaded from `.upstream/v2fly/data`.
- Without local upstream checkout, the default v2fly source falls back to the GitHub source archive once per build, not many individual raw files.
- `include:` is resolved recursively.
- v2fly `google` includes YouTube upstream; profile ordering must keep Stream before Google when Google is a separate policy.
- bare domains and `domain:` become `DOMAIN-SUFFIX`; `full:` becomes `DOMAIN`; `keyword:` becomes `DOMAIN-KEYWORD`.
- `regexp:` is intentionally skipped and counted in generated headers.
- v2fly attributes such as `@ads` and `@cn` are parsed for include filtering only and are not written to generated client files.

Upstream sources:

- GitHub Actions checks out `SukkaLab/ruleset.skk.moe` to `.upstream/skk` and `v2fly/domain-list-community` to `.upstream/v2fly`.
- GitHub Actions downloads the pinned Tranco list from the `keep_ranked` URL in `config/rules.json` to `.upstream/tranco/top-1m.csv`. It is only a filter; no ranking data is published.
- GitHub Actions also checks out a strict whitelist of `AlexKris/profile` tool scripts to `.upstream/profile` for Pages distribution under `/profile/`.
- `build_rules.py` reads configured `paths` / `local_dir` first and falls back to remote URLs only when local upstreams are absent.
- CI must run `RULES_REQUIRE_LOCAL_SOURCES=1 python3 scripts/build_rules.py` so missing `.upstream` checkouts fail instead of silently using Raw URLs.
- `.upstream/` is local build state and must not be committed.

Profile tool distribution:

- `scripts/build_site.py` publishes only the explicit `PROFILE_TOOL_FILES` whitelist from `.upstream/profile`.
- Do not publish the entire `AlexKris/profile` repository from this project.
- Do not publish untracked profile files or operational/private material such as `tool/openclaw`, `tool/proxy/routes.toml`, `tool/proxy/dns.yml`, `xboard`, or generated runtime configs.
- If adding a profile tool to the whitelist, verify it contains no real token, key, node, subscription, or private infrastructure data.
- If `.upstream/profile` is absent locally, `scripts/build_site.py` should skip `/profile/...` output instead of failing.

MITM:

- `anywhere/mitm/google-cn-redirect.amrs` is maintained directly.
- It uses native Anywhere 302 redirect rules, not JavaScript.
- `scripts/build_mitm.py` builds `anywhere/mitm/youtube-enhance-anywhere.amrs`
  from local JavaScript sources under `anywhere/mitm/source/`.
- Edit the JS sources, not the generated YouTube `.amrs`, then run the MITM
  build script.

## Build Commands

Run from the repository root:

```sh
python3 scripts/build_rules.py
python3 scripts/build_mitm.py
python3 scripts/build_site.py
```

Use `RULES_REQUIRE_LOCAL_SOURCES=1 python3 scripts/build_rules.py` when verifying
the CI path locally.

For a local build that matches CI, prepare upstream checkouts first:

```sh
mkdir -p .upstream
git clone --depth 1 --filter=blob:none --sparse https://github.com/SukkaLab/ruleset.skk.moe.git .upstream/skk
git -C .upstream/skk sparse-checkout set List
git clone --depth 1 --filter=blob:none --sparse https://github.com/v2fly/domain-list-community.git .upstream/v2fly
git -C .upstream/v2fly sparse-checkout set data
git clone --depth 1 --filter=blob:none --sparse --branch release https://github.com/Loyalsoldier/surge-rules.git .upstream/loyalsoldier-surge-rules
git -C .upstream/loyalsoldier-surge-rules sparse-checkout set --no-cone /direct.txt
mkdir -p .upstream/tranco
curl -fL -o .upstream/tranco/top-1m.csv "$(python3 -c 'import json; print(json.load(open("config/rules.json"))["sources"]["loyalsoldier-direct"]["keep_ranked"]["urls"][0])')"
```

Profile tool output is optional locally. Point `.upstream/profile` at a checkout
of `AlexKris/profile` only when verifying `/profile/...` Pages output.

Without `.upstream/`, local `build_rules.py` falls back to remote upstream fetches.
`build_rules.py` requires these local CLIs:

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
python3 scripts/build_site.py
```

For profile tool publication changes, run `bash -n` on every whitelisted
profile script before building the site.

For MITM rules:

```sh
python3 scripts/build_mitm.py
```

Spot-check important routing expectations after generation:

```sh
rg -n "time\.apple\.com|ocsp\.digicert\.com|youtube\.com|google\.com|googleapis\.com|apple\.com|icloud\.com|mzstatic\.com|officecdn\.microsoft\.com|binance\.com|okx\.com|openrouter\.ai|paypal\.com|ctldl\.windowsupdate\.com|91\.108\.4\.0/22|10\.0\.0\.0/8|192\.168\.0\.0/16|1\.1\.8\.0/24" anywhere surge loon plain
```

Expected behavior:

- `time.apple.com` belongs in `apple`.
- Unified `apple` contains the Apple CDN domainset, Apple CDN non_ip, CN, Services, `is1-ssl.mzstatic.com`, and `time.apple.com`; it is intended for DIRECT. There is no separate Apple domainset file.
- `apple` inherits the broad `DOMAIN-SUFFIX,apple.com`, `icloud.com`, and `me.com` suffixes from SKK Apple Services, so it captures every Apple subdomain not claimed earlier. `apple-proxy` must be ordered before it, and Stream must be ordered before `apple-proxy` so Apple TV+ playback stays on the Stream policy.
- `apple-proxy` covers Apple domains SKK routes through CDN/Global (`news-assets.apple.com`, `events-live.apple.com`, `events-delivery.apple.com`, `static.ess.apple.com`, `pba.apple.com`; SKK's `statici.icloud.com` is deliberately left on DIRECT, see above), services unavailable in mainland China (Apple News, iCloud Private Relay `mask*.icloud.com`), and developer endpoints with no mainland CDN presence.
- Apple TV+ belongs to `stream`, not `apple-proxy`. `tv.apple.com` and `hls-svod.itunes.apple.com` are added to `stream` so the whole TV+ chain (`uts-api`, `play-edge`, `linear.tv`, `hls*`) shares one policy. Splitting the chain across two policy groups with different exit regions breaks TV+ region validation.
- Keep `time.apple.com`, `gs-loc.apple.com`, `gsp*-cn.ls.apple.com`, `*-courier.push.apple.com`, `albert.apple.com`, Apple software update CDNs, and `*.apple.com.cn` on DIRECT. Do not add them to `apple-proxy`.
- `download` remains separate from `microsoft-cdn`.
- `direct` and `cn-domain` are non-IP direct rule sets and belong before IP rule sets in profiles.
- `lan-ip` and `china-ip` are IP/CIDR direct rule sets; Surge outputs include `no-resolve`.
- `direct` is upstream base direct; `direct-extra` is the personal direct overlay.
- DigiCert certificate infrastructure belongs in Direct Extra.
- AI uses v2fly `category-ai-!cn`; exact upstream `@ads` entries may be preserved, while `regexp:` entries are skipped.
- Stream Surge outputs preserve SKK `USER-AGENT` and `PROCESS-NAME`; Loon outputs preserve `USER-AGENT` and skip `PROCESS-NAME`; plain/Mihomo/sing-box outputs are domain-only.
- Google uses v2fly `google` and includes YouTube upstream; Stream must be ordered before Google in profiles.
- `cn-domain` is generated for Surge/Loon/Mihomo/sing-box/Anywhere/plain from the same rules and already contains SKK Domestic.
- Domain rules covered by a `DOMAIN-SUFFIX` in the same set (exact domain equal to or under the suffix, or a child suffix) are dropped from every output. `DOMAIN-KEYWORD` is never used to drop domains.
- For Anywhere, `telegram.arrs` combines Telegram domain and IP CIDR rules.
  Keep `telegram-ip` published separately for non-Anywhere clients and legacy
  Anywhere subscriptions.
- For Anywhere, `lan.arrs` combines LAN domain and IP CIDR rules. Keep
  `lan-ip` published separately for non-Anywhere clients and legacy Anywhere
  subscriptions.
- Microsoft CDN is the only Microsoft rule set; broad Microsoft falls through to `FINAL`.
- PayPal remains a separate rule set.
- Kuro and CITIC direct domains live in Direct Extra; no separate files are published.
- `getui` remains intentionally excluded unless the user explicitly changes policy.

## Change Rules

- Prefer editing `config/rules.json` and regenerating outputs over hand-editing generated files.
- Keep manual overlays small and explicit. If a manual overlay grows or needs multiple client formats, move it into `config/rules.json` and generation.
- Preserve lowercase file names and hyphenated rule ids, e.g. `apple-proxy`, `direct-extra`.
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
