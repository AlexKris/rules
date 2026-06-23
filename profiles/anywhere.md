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
Lan             -> DIRECT
LAN IP          -> DIRECT
China IP        -> DIRECT
Direct Extra    -> DIRECT
Kuro            -> DIRECT
CITIC           -> DIRECT
Apple           -> DIRECT
Download        -> Download

AI              -> proxy chain
Bahamut         -> proxy chain
Telegram        -> proxy chain
Telegram IP     -> proxy chain
Binance         -> proxy chain
Crypto          -> proxy chain
PayPal          -> proxy chain

Proxy           -> proxy chain

ChinaDomain     -> DIRECT
GeoIP_CN        -> DIRECT
```

Notes:

- Anywhere does not evaluate custom rule sets as a linear top-to-bottom rule
  list. A set assigned to `Default` is inactive; a set assigned to `DIRECT`,
  `REJECT`, or a proxy chain participates in the User tier.
- All custom rule sets share the User tier. Within that tier, the more specific
  match wins: domain suffix before keyword, deeper suffix before broader suffix,
  longer keyword before shorter keyword, and longer CIDR prefix before shorter
  CIDR prefix.
- Domain and IP rules are independent. `LAN IP`, `China IP`, and `Telegram IP`
  match only literal or real destination IPs and do not resolve domains. This is
  effectively `no-resolve` behavior by implementation.
- If both a host and an IP are known, the domain decision wins over an IP-CIDR
  decision. Avoid putting identical rules in multiple custom sets with different
  targets, because exact duplicates can become last-write-wins.
- Use `Proxy` instead of separate CDN/global runtime rules. Legacy `CDN` and
  split Apple rule sets remain published for compatibility.
- `Proxy` is a broad CDN/global proxy fallback and overlaps with `Download`,
  `Telegram`, `PayPal`, and `Crypto`; keep those as separate sets so their
  assignments remain explicit.
- `Domestic` and upstream `Direct` are not published for Anywhere because ARRS cannot represent all upstream matchers.
- `Google`, `cn-domain`, and `not-cn-domain` are not published for Anywhere.
- `Lan` is a non-IP rule set; `LAN IP` is the separate CIDR set.
- `Direct Extra` is the personal direct overlay.
- `Kuro`, `CITIC`, `Direct Extra`, `PayPal`, and `Crypto` are intentionally separate rule sets.
- If `Binance` is a separate local rule set, assign it explicitly; if it uses
  the same proxy chain as `Crypto`, `Crypto` alone is usually enough.
- `Speedtest` and `Stream` are not published for Anywhere.
- `getui` is intentionally not included.
- Keep private domains and proxy subscriptions out of this repository.
