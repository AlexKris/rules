# Rules

Personal routing rule overlays and profiles for proxy clients.

This repository keeps opinionated generated rule sets and small custom overlays
that complement upstream rulesets such as Sukka Ruleset, MetaCubeX
meta-rules-dat, v2fly domain-list-community, and blackmatrix7
ios_rule_script. It is not intended to be a
full mirror of those projects.

Generated artifacts are based on the normalized rule model in
`config/rules.json`, with explicit local add/exclude patches. `plain/` contains
observable normalized text artifacts; client-specific files are generated from
the same rule model.

## Distribution

Recommended rule distribution endpoint:

```text
https://alexkris-rules.pages.dev/
```

Example URLs:

```text
https://alexkris-rules.pages.dev/anywhere/proxy.arrs
https://alexkris-rules.pages.dev/surge/non-ip/proxy.conf
https://alexkris-rules.pages.dev/mihomo/non-ip/proxy.mrs
https://alexkris-rules.pages.dev/sing-box/non-ip/proxy.srs
https://alexkris-rules.pages.dev/profile/tool/setup.sh
https://alexkris-rules.pages.dev/profile/tool/proxy/heki.sh
```

GitHub Raw URLs remain usable as a fallback mirror, but client profiles should
prefer the Cloudflare Pages endpoint once deployment is verified.

Profile tool scripts are published from a strict whitelist in the separate
`AlexKris/profile` repository. The Pages build does not publish the whole
profile repository or untracked local files.

## Rule Sets

### Anywhere

- `anywhere/proxy.arrs`
- `anywhere/apple.arrs`
- `anywhere/download.arrs`
- `anywhere/lan.arrs`
- `anywhere/lan-ip.arrs`
- `anywhere/china-ip.arrs`
- `anywhere/cn-domain.arrs`
- `anywhere/cdn.arrs`
- `anywhere/apple-cdn.arrs`
- `anywhere/apple-cn.arrs`
- `anywhere/apple-services.arrs`
- `anywhere/ai.arrs`
- `anywhere/telegram.arrs`
- `anywhere/telegram-ip.arrs`
- `anywhere/paypal.arrs`
- `anywhere/kuro.arrs`
- `anywhere/citic.arrs`
- `anywhere/direct-extra.arrs`
- `anywhere/crypto.arrs`
- `anywhere/stream.arrs`
- `anywhere/stream-hk.arrs`
- `anywhere/stream-tw.arrs`
- `anywhere/stream-jp.arrs`
- `anywhere/stream-us.arrs`
- `anywhere/stream-kr.arrs`
- `anywhere/stream-eu.arrs`
- `anywhere/mitm/google-cn-redirect.amrs`
- `anywhere/mitm/youtube-enhance-anywhere.amrs`

Import the raw URLs in Anywhere and assign them as follows:

```text
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/proxy.arrs            -> proxy chain
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple.arrs            -> DIRECT
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/download.arrs         -> Download
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/lan.arrs              -> DIRECT
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/china-ip.arrs         -> DIRECT
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/cn-domain.arrs        -> DIRECT
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/ai.arrs               -> proxy chain
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/telegram.arrs         -> proxy chain
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/paypal.arrs           -> proxy chain
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/direct-extra.arrs     -> DIRECT
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/crypto.arrs           -> proxy chain
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream.arrs           -> Stream or proxy chain
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-hk.arrs        -> MediaHK
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-tw.arrs        -> MediaTW
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-jp.arrs        -> MediaJP
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-us.arrs        -> MediaUS
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-kr.arrs        -> MediaKR
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-eu.arrs        -> MediaEU
```

`proxy` replaces the old separate CDN/global runtime rules for new Anywhere
profiles. `apple` replaces the split Apple rule sets. `lan` and `telegram`
contain both domain and IP CIDR rules. `cn-domain` is a broad direct fallback
based on v2fly `geolocation-cn`. Legacy `cdn`, split Apple, `lan-ip`,
`telegram-ip`, `kuro`, and `citic` files remain published for compatibility
but are not recommended for new profiles.

`domestic` and `direct` are not published for Anywhere because their SKK
sources include client-specific matchers that ARRS cannot represent.
`not-cn-domain` is intentionally not published for Anywhere. `direct-extra`
keeps precise personal direct fixes, including Kuro, CITIC, `videocc.net`,
`cache.video.iqiyi.com`, and DigiCert certificate infrastructure.

Import MITM rule sets separately in Anywhere MITM:

```text
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/mitm/google-cn-redirect.amrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/mitm/youtube-enhance-anywhere.amrs
```

`google-cn-redirect.amrs` uses native Anywhere transparent rewrite rules. It
does not require a JavaScript MITM script.
`youtube-enhance-anywhere.amrs` is generated from local JavaScript sources under
`anywhere/mitm/source/`.

### Surge

- `surge/domainset/proxy.conf`
- `surge/non-ip/proxy.conf`
- `surge/domainset/apple.conf`
- `surge/non-ip/apple.conf`
- `surge/domainset/download.conf`
- `surge/non-ip/download.conf`
- `surge/non-ip/domestic.conf`
- `surge/non-ip/direct.conf`
- `surge/non-ip/lan.conf`
- `surge/ip/lan-ip.conf`
- `surge/ip/china-ip.conf`
- `surge/domainset/cdn.conf`
- `surge/domainset/speedtest.conf`
- `surge/non-ip/cdn.conf`
- `surge/non-ip/stream.conf`
- `surge/non-ip/stream-hk.conf`
- `surge/non-ip/stream-tw.conf`
- `surge/non-ip/stream-jp.conf`
- `surge/non-ip/stream-us.conf`
- `surge/non-ip/stream-kr.conf`
- `surge/non-ip/stream-eu.conf`
- `surge/non-ip/google.conf`
- `surge/non-ip/cn-domain.conf`
- `surge/non-ip/not-cn-domain.conf`
- `surge/domainset/apple-cdn.conf`
- `surge/non-ip/apple-cdn.conf`
- `surge/non-ip/apple-cn.conf`
- `surge/non-ip/apple-services.conf`
- `surge/non-ip/ai.conf`
- `surge/non-ip/telegram.conf`
- `surge/ip/telegram-ip.conf`
- `surge/non-ip/crypto.conf`
- `surge/non-ip/paypal.conf`
- `surge/non-ip/microsoft.conf`
- `surge/non-ip/microsoft-cdn.conf`
- `surge/non-ip/direct-extra.conf`
- `surge/domainset/kuro.conf`

Use them as remote rule sets:

```ini
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/proxy.conf,Proxy,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/proxy.conf,Proxy,extended-matching
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/apple.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple.conf,DIRECT,extended-matching
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/download.conf,Download,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/download.conf,Download,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/domestic.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/direct.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/lan.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/ip/lan-ip.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/ip/china-ip.conf,DIRECT,extended-matching
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/cdn.conf,CDN,extended-matching
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/speedtest.conf,Speedtest,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/cdn.conf,CDN,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/stream.conf,Media,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/stream-hk.conf,MediaHK,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/stream-tw.conf,MediaTW,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/stream-jp.conf,MediaJP,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/stream-us.conf,MediaUS,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/stream-kr.conf,MediaKR,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/stream-eu.conf,MediaEU,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/google.conf,Google,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/cn-domain.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/not-cn-domain.conf,Proxy,extended-matching
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/apple-cdn.conf,AppleCDN,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple-cdn.conf,AppleCDN,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple-cn.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple-services.conf,AppleSvc,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/ai.conf,AI,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/telegram.conf,Telegram,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/ip/telegram-ip.conf,Telegram,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/crypto.conf,Crypto,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/paypal.conf,PayPal,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/microsoft.conf,Proxy,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/microsoft-cdn.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/direct-extra.conf,DIRECT,extended-matching
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/kuro.conf,DIRECT,extended-matching
```

`domestic`, `direct`, and `lan` are non-IP direct rule sets and should stay
before IP rule sets such as `lan-ip` and `china-ip` in profile order. `direct`
is the upstream base direct rule set; `direct-extra` is the personal overlay.
Put `stream*` before `google`; v2fly `google` includes YouTube, and stream
rules should own YouTube routing.

The same Surge text files can be used by Shadowrocket.

### Loon

Use generated `.list` files as Loon remote rules:

```ini
[Remote Rule]
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/stream.list,policy=Media,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/ai.list,policy=AI,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/telegram.list,policy=Telegram,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/ip/telegram-ip.list,policy=Telegram,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/crypto.list,policy=Crypto,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/paypal.list,policy=PayPal,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/microsoft-cdn.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/microsoft.list,policy=Proxy,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/google.list,policy=Google,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/domainset/apple.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/apple.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/domainset/download.list,policy=Download,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/download.list,policy=Download,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/direct-extra.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/cn-domain.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/ip/lan-ip.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/ip/china-ip.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/domainset/proxy.list,policy=Proxy,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/proxy.list,policy=Proxy,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/not-cn-domain.list,policy=Proxy,enabled=true
```

Loon domainset outputs are converted to full `DOMAIN` and `DOMAIN-SUFFIX`
rules. Loon non-IP outputs keep `DOMAIN`, `DOMAIN-SUFFIX`, `DOMAIN-KEYWORD`,
`URL-REGEX`, and `USER-AGENT` where supported. `DOMAIN-WILDCARD` and
`PROCESS-NAME` are intentionally omitted from Loon outputs because they are not
listed in Loon's official rule syntax. Keep broad `proxy` and `not-cn-domain`
fallback rules after dedicated policy rules.

### Mihomo

Use the generated `.mrs` files with `behavior: domain` and `format: mrs`.
Domain `.mrs` files cannot contain `DOMAIN-KEYWORD` rules. Rule sets that need
keyword matching also publish keyword-only text providers under
`mihomo/classical/*.list`; use those with `behavior: classical` and
`format: text` alongside the matching `.mrs` provider.

```yaml
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/domainset/proxy.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/proxy.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/domainset/apple.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/apple.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/domainset/download.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/download.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/domestic.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/direct.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/lan.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/domainset/cdn.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/domainset/speedtest.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/cdn.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/stream.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/stream-hk.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/stream-tw.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/stream-jp.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/stream-us.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/stream-kr.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/stream-eu.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/domainset/apple-cdn.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/apple-cdn.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/apple-cn.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/apple-services.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/ai.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/telegram.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/paypal.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/microsoft.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/microsoft-cdn.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/direct-extra.mrs
```

Keyword supplements currently exist for rule sets such as `proxy`, `cdn`,
`direct`, and some `stream*` files:

```yaml
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/classical/proxy.list
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/classical/cdn.list
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/classical/direct.list
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/classical/stream.list
```

Use `behavior: ipcidr` and `format: mrs` for IP rules:

```yaml
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/ip/telegram-ip.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/ip/lan-ip.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/ip/china-ip.mrs
```

Google and broad CN geosite fallback rules are not generated by this repository
for Mihomo/Stash. Use MetaCubeX `geo/geosite/google.mrs`,
`geo/geosite/cn.mrs`, and `geo/geosite/geolocation-!cn.mrs` directly.
Crypto is generated only as Anywhere and Surge/Loon/plain text rules; use geosite
or client-native alternatives if a Mihomo/Stash binary rule is needed.

### sing-box

Use the generated `.srs` files as remote rule sets.

```text
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/domainset/proxy.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/proxy.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/domainset/apple.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/apple.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/domainset/download.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/download.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/domestic.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/direct.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/lan.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/domainset/cdn.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/domainset/speedtest.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/cdn.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/stream.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/stream-hk.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/stream-tw.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/stream-jp.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/stream-us.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/stream-kr.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/stream-eu.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/domainset/apple-cdn.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/apple-cdn.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/apple-cn.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/apple-services.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/ai.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/telegram.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/ip/telegram-ip.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/ip/lan-ip.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/ip/china-ip.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/paypal.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/microsoft.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/microsoft-cdn.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/direct-extra.srs
```

Google and broad CN geosite fallback rules are not generated by this repository
for sing-box. Use SagerNet `geosite-google.srs`, `geosite-cn.srs`, and
`geosite-geolocation-!cn.srs` directly.
Crypto is generated only as Anywhere and Surge/Loon/plain text rules; use geosite
or client-native alternatives if a sing-box binary rule is needed.

### Plain

Generated plain text files under `plain/` are observable normalized rule sets.
Domain files use normalized rule syntax such as `DOMAIN`, `DOMAIN-SUFFIX`, and
`DOMAIN-WILDCARD`; IP files use normalized CIDR values. Some client outputs,
including Surge and Loon, preserve extra supported matcher types directly from
the shared rule model.

## Build

GitHub Actions checks out upstream sources into `.upstream/` before building:

```text
.upstream/skk/List
.upstream/v2fly/data
.upstream/profile
```

Local builds prefer the same `.upstream/` paths when present and fall back to
remote upstream URLs when they are absent. To reproduce the CI path locally:

```sh
mkdir -p .upstream
git clone --depth 1 --filter=blob:none --sparse https://github.com/SukkaLab/ruleset.skk.moe.git .upstream/skk
git -C .upstream/skk sparse-checkout set List
git clone --depth 1 --filter=blob:none --sparse https://github.com/v2fly/domain-list-community.git .upstream/v2fly
git -C .upstream/v2fly sparse-checkout set data
```

Profile tool scripts are optional for local site builds. If `.upstream/profile`
is absent, `scripts/build_site.py` skips `/profile/...` output. To test the
Profile tool output locally, point `.upstream/profile` at a checkout of
`AlexKris/profile` before running the site build.

Regenerate rule files manually:

```sh
python3 scripts/build_rules.py
python3 scripts/build_mitm.py
python3 scripts/build_site.py
```

Use `RULES_REQUIRE_LOCAL_SOURCES=1 python3 scripts/build_rules.py` to force the
same no-fallback upstream behavior as CI.

Generated rules are also built by GitHub Actions once per day after upstream
SKK scheduled builds. The workflow requires local upstream checkouts in CI and
commits only when generated files change. It also checks out a strict whitelist
of profile tool scripts for Pages distribution under `/profile/`.

## Scope

Private domains, private media services, proxy nodes, subscription URLs, and
tokens are intentionally excluded.

## License

Original code, scripts, custom rules, and profiles in this repository are
licensed under AGPL-3.0 unless otherwise stated. Generated or derived files may
reference third-party upstream rules; those parts remain under their original
licenses.
