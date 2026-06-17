# Anywhere Profile

Import the following generated and custom rule sets:

```text
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/cdn.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple-cdn.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple-cn.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple-services.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/kuro.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/citic.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/direct-extra.arrs
```

Import the following MITM rule sets separately:

```text
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/mitm/google-cn-redirect.amrs
```

Recommended rule-set assignments:

```text
CDN             -> proxy chain
AI              -> proxy chain
Bahamut         -> proxy chain
PayPal          -> proxy chain
Binance         -> proxy chain
Proxy           -> proxy chain

Lan             -> DIRECT
Apple CDN       -> DIRECT or AppleCDN
Apple CN        -> DIRECT
Apple Services  -> DIRECT or AppleSvc
Direct          -> DIRECT
Kuro            -> DIRECT
CITIC           -> DIRECT
Direct Extra    -> DIRECT
ChinaDomain     -> DIRECT
GeoIP_CN        -> DIRECT
```

Notes:

- Use this repository's `CDN` instead of `anywhere-rules` `CDN`; it excludes
  Apple time sync and DigiCert certificate infrastructure domains.
- `Kuro`, `CITIC`, and `Direct Extra` are intentionally separate rule sets.
- `getui` is intentionally not included.
- Keep private domains and proxy subscriptions out of this repository.
