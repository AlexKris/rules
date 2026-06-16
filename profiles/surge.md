# Surge Profile

Kuro is maintained as a Surge `DOMAIN-SET` because it only contains domain
suffixes.

Add this rule before broad domestic/global fallback rules:

```ini
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/kuro.conf,DIRECT,extended-matching
```

This replaces local Kuro rules such as:

```ini
DOMAIN-SUFFIX,kurogame.com,DIRECT,extended-matching
DOMAIN-SUFFIX,kurobbs.com,DIRECT,extended-matching
```

Do not add private domains, private media services, proxy nodes, subscription
URLs, or tokens to this repository.
