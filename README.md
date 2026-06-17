# Rules

Personal routing rule overlays and profiles for proxy clients.

This repository keeps opinionated generated rule sets and small custom overlays
that complement upstream rulesets such as Sukka Ruleset, MetaCubeX
meta-rules-dat, and blackmatrix7 ios_rule_script. It is not intended to be a
full mirror of those projects.

Generated CDN and Apple rules are based on Sukka Ruleset with local exclusions
for Apple time sync and DigiCert certificate infrastructure domains.

## Rule Sets

### Anywhere

- `anywhere/cdn.arrs`
- `anywhere/apple-cdn.arrs`
- `anywhere/apple-cn.arrs`
- `anywhere/apple-services.arrs`
- `anywhere/kuro.arrs`
- `anywhere/citic.arrs`
- `anywhere/direct-extra.arrs`
- `anywhere/mitm/google-cn-redirect.amrs`

Import the raw URLs in Anywhere and assign them as follows:

```text
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/cdn.arrs              -> proxy chain
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple-cdn.arrs        -> DIRECT or AppleCDN
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple-cn.arrs         -> DIRECT
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple-services.arrs   -> DIRECT or AppleSvc
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/kuro.arrs             -> DIRECT
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/citic.arrs            -> DIRECT
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/direct-extra.arrs     -> DIRECT
```

Import MITM rule sets separately in Anywhere MITM:

```text
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/mitm/google-cn-redirect.amrs
```

### Surge

- `surge/domainset/cdn.conf`
- `surge/non-ip/cdn.conf`
- `surge/domainset/apple-cdn.conf`
- `surge/non-ip/apple-cdn.conf`
- `surge/non-ip/apple-cn.conf`
- `surge/non-ip/apple-services.conf`
- `surge/non-ip/direct-extra.conf`
- `surge/domainset/kuro.conf`

Use them as remote rule sets:

```ini
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/cdn.conf,CDN,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/cdn.conf,CDN,extended-matching
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/apple-cdn.conf,AppleCDN,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple-cdn.conf,AppleCDN,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple-cn.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple-services.conf,AppleSvc,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/direct-extra.conf,DIRECT,extended-matching
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/kuro.conf,DIRECT,extended-matching
```

The same Surge text files can be used by Shadowrocket.

### Mihomo

Use the generated `.mrs` files with `behavior: domain` and `format: mrs`.

```yaml
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/domainset/cdn.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/cdn.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/domainset/apple-cdn.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/apple-cdn.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/apple-cn.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/apple-services.mrs
url: https://raw.githubusercontent.com/AlexKris/rules/main/mihomo/non-ip/direct-extra.mrs
```

### sing-box

Use the generated `.srs` files as remote rule sets.

```text
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/domainset/cdn.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/cdn.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/domainset/apple-cdn.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/apple-cdn.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/apple-cn.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/apple-services.srs
https://raw.githubusercontent.com/AlexKris/rules/main/sing-box/non-ip/direct-extra.srs
```

## Build

Regenerate rule files manually:

```sh
python3 scripts/build_rules.py
```

## Scope

Private domains, private media services, proxy nodes, subscription URLs, and
tokens are intentionally excluded.

## License

Original code, scripts, custom rules, and profiles in this repository are
licensed under AGPL-3.0 unless otherwise stated. Generated or derived files may
reference third-party upstream rules; those parts remain under their original
licenses.
