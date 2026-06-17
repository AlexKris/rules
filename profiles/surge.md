# Surge Profile

Use the generated CDN and Apple rules before broad domestic/global fallback
rules.

CDN:

```ini
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/cdn.conf,CDN,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/cdn.conf,CDN,extended-matching
```

Apple:

```ini
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/apple-cdn.conf,AppleCDN,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple-cdn.conf,AppleCDN,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple-cn.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple-services.conf,AppleSvc,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/direct-extra.conf,DIRECT,extended-matching
```

Kuro:

```ini
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/kuro.conf,DIRECT,extended-matching
```

Do not add private domains, private media services, proxy nodes, subscription
URLs, or tokens to this repository.
