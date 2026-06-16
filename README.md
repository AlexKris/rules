# Rules

Personal routing rule overlays and profiles for proxy clients.

This repository keeps small, opinionated rule sets that complement upstream
rulesets such as Sukka Ruleset, MetaCubeX meta-rules-dat, and blackmatrix7
ios_rule_script. It is not intended to be a full mirror of those projects.

## Rule Sets

### Anywhere

- `anywhere/kuro.arrs`
- `anywhere/citic.arrs`

Import the raw URLs in Anywhere and assign both rule sets to `DIRECT`:

```text
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/kuro.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/citic.arrs
```

### Surge

- `surge/domainset/kuro.conf`

Use it as a `DOMAIN-SET`:

```ini
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/kuro.conf,DIRECT,extended-matching
```

## Scope

Private domains, private media services, proxy nodes, subscription URLs, and
tokens are intentionally excluded.

## License

Original code, scripts, custom rules, and profiles in this repository are
licensed under AGPL-3.0 unless otherwise stated. Generated or derived files may
reference third-party upstream rules; those parts remain under their original
licenses.
