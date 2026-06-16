# Anywhere Profile

Import the following custom rule sets and assign them to `DIRECT`:

```text
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/kuro.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/citic.arrs
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
AppleCN         -> DIRECT
AppleServices   -> DIRECT
Direct          -> DIRECT
Kuro            -> DIRECT
CITIC           -> DIRECT
ChinaDomain     -> DIRECT
GeoIP_CN        -> DIRECT
```

Notes:

- `Kuro` and `CITIC` are intentionally separate rule sets.
- `getui` is intentionally not included.
- Keep private domains and proxy subscriptions out of this repository.
