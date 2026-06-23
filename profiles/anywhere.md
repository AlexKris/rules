# Anywhere Profile

Import the following generated and custom rule sets:

```text
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/proxy.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/download.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/lan.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/lan-ip.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/china-ip.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/cdn.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple-cdn.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple-cn.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple-services.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/ai.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/telegram.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/telegram-ip.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/paypal.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/kuro.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/citic.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/direct-extra.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/crypto.arrs
```

Import the following MITM rule sets separately:

```text
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/mitm/google-cn-redirect.amrs
```

Recommended rule-set assignments:

```text
Proxy           -> proxy chain
AI              -> proxy chain
Bahamut         -> proxy chain
PayPal          -> proxy chain
Crypto          -> proxy chain
Binance         -> proxy chain
Telegram        -> proxy chain
Telegram IP     -> proxy chain

Lan             -> DIRECT
Apple           -> DIRECT
Download        -> Download
LAN IP          -> DIRECT
China IP        -> DIRECT
Kuro            -> DIRECT
CITIC           -> DIRECT
Direct Extra    -> DIRECT
ChinaDomain     -> DIRECT
GeoIP_CN        -> DIRECT
```

Notes:

- Use `Proxy` instead of separate CDN/global runtime rules. Legacy `CDN` and
  split Apple rule sets remain published for compatibility.
- `Domestic` and upstream `Direct` are not published for Anywhere because ARRS cannot represent all upstream matchers.
- `Google`, `cn-domain`, and `not-cn-domain` are not published for Anywhere.
- `Lan` is a non-IP rule set. Keep it before IP rule sets in profile order.
- `Direct Extra` is the personal direct overlay.
- `Kuro`, `CITIC`, `Direct Extra`, `PayPal`, and `Crypto` are intentionally separate rule sets.
- `Speedtest` and `Stream` are not published for Anywhere.
- `getui` is intentionally not included.
- Keep private domains and proxy subscriptions out of this repository.
