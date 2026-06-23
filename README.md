# Rules

Personal routing rule overlays and profiles for proxy clients.

This repository keeps opinionated generated rule sets and small custom overlays
that complement upstream rulesets such as Sukka Ruleset, MetaCubeX
meta-rules-dat, v2fly domain-list-community, and blackmatrix7
ios_rule_script. It is not intended to be a
full mirror of those projects.

Generated artifacts are based on normalized plain text rule sets under
`plain/`, with explicit local add/exclude patches. Client-specific files are
derived from those plain text artifacts.

## Rule Sets

### Anywhere

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
- `anywhere/mitm/google-cn-redirect.amrs`

Import the raw URLs in Anywhere and assign them as follows:

```text
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/cdn.arrs              -> proxy chain
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple-cdn.arrs        -> DIRECT or AppleCDN
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple-cn.arrs         -> DIRECT
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple-services.arrs   -> DIRECT or AppleSvc
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/ai.arrs               -> proxy chain
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/telegram.arrs         -> proxy chain
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/telegram-ip.arrs      -> proxy chain
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/paypal.arrs           -> proxy chain
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/kuro.arrs             -> DIRECT
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/citic.arrs            -> DIRECT
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/direct-extra.arrs     -> DIRECT
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/crypto.arrs           -> proxy chain
```

Import MITM rule sets separately in Anywhere MITM:

```text
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/mitm/google-cn-redirect.amrs
```

### Surge

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
- `surge/domainset/apple-cdn.conf`
- `surge/non-ip/apple-cdn.conf`
- `surge/non-ip/apple-cn.conf`
- `surge/non-ip/apple-services.conf`
- `surge/non-ip/ai.conf`
- `surge/non-ip/telegram.conf`
- `surge/ip/telegram-ip.conf`
- `surge/non-ip/paypal.conf`
- `surge/non-ip/microsoft.conf`
- `surge/non-ip/microsoft-cdn.conf`
- `surge/non-ip/direct-extra.conf`
- `surge/domainset/kuro.conf`

Use them as remote rule sets:

```ini
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
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/apple-cdn.conf,AppleCDN,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple-cdn.conf,AppleCDN,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple-cn.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple-services.conf,AppleSvc,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/ai.conf,AI,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/telegram.conf,Telegram,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/ip/telegram-ip.conf,Telegram,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/paypal.conf,PayPal,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/microsoft.conf,Microsoft,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/microsoft-cdn.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/direct-extra.conf,DIRECT,extended-matching
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/kuro.conf,DIRECT,extended-matching
```

The same Surge text files can be used by Shadowrocket.

### Mihomo

Use the generated `.mrs` files with `behavior: domain` and `format: mrs`.

```yaml
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

Use `behavior: ipcidr` and `format: mrs` for Telegram IP:

```yaml
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/ip/telegram-ip.mrs
```

### sing-box

Use the generated `.srs` files as remote rule sets.

```text
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
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/paypal.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/microsoft.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/microsoft-cdn.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/direct-extra.srs
```

### Plain

Generated plain text files under `plain/` are the observable normalized rule
sets used to build Surge, Mihomo, and sing-box artifacts. They use normalized
rule syntax such as `DOMAIN` and `DOMAIN-SUFFIX`.

## Build

Regenerate rule files manually:

```sh
python3 scripts/build_rules.py
python3 scripts/build_mitm.py
```

Generated rules are also built by GitHub Actions once per day after upstream
SKK scheduled builds. The workflow commits only when generated files change.

## Scope

Private domains, private media services, proxy nodes, subscription URLs, and
tokens are intentionally excluded.

## License

Original code, scripts, custom rules, and profiles in this repository are
licensed under AGPL-3.0 unless otherwise stated. Generated or derived files may
reference third-party upstream rules; those parts remain under their original
licenses.
