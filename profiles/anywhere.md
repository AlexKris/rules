# Anywhere Profile

Import the following generated and custom rule sets:

```text
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/proxy.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/download.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/lan.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/china-ip.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/cn-domain.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/ai.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/telegram.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/paypal.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/direct-extra.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/crypto.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-hk.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-tw.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-jp.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-us.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-kr.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-eu.arrs
```

Import the following MITM rule sets separately:

```text
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/mitm/google-cn-redirect.amrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/mitm/youtube-enhance-anywhere.amrs
```

`google-cn-redirect.amrs` uses native transparent rewrite rules and does not
require a JavaScript MITM script.
`youtube-enhance-anywhere.amrs` is generated from local JavaScript sources in
this repository.

Recommended rule-set assignments:

```text
Lan             -> DIRECT
China IP        -> DIRECT
CN Domain       -> DIRECT
Direct Extra    -> DIRECT
Apple           -> DIRECT
Download        -> Download

AI              -> proxy chain
Bahamut         -> proxy chain
Telegram        -> proxy chain
Binance         -> proxy chain
Crypto          -> proxy chain
PayPal          -> proxy chain

Stream          -> Stream / proxy chain
Stream HK       -> MediaHK
Stream TW       -> MediaTW
Stream JP       -> MediaJP
Stream US       -> MediaUS
Stream KR       -> MediaKR
Stream EU       -> MediaEU

Proxy           -> proxy chain
```

Notes:

- Anywhere does not evaluate custom rule sets as a linear top-to-bottom rule
  list. A set assigned to `Default` is inactive; a set assigned to `DIRECT`,
  `REJECT`, or a proxy chain participates in the User tier.
- All custom rule sets share the User tier. Within that tier, the more specific
  match wins: domain suffix before keyword, deeper suffix before broader suffix,
  longer keyword before shorter keyword, and longer CIDR prefix before shorter
  CIDR prefix.
- Domain and IP rules are independent. The IP CIDR rules inside `Lan`,
  `China IP`, and `Telegram` match only literal or real destination IPs and do
  not resolve domains. This is effectively `no-resolve` behavior by
  implementation.
- If both a host and an IP are known, the domain decision wins over an IP-CIDR
  decision. Avoid putting identical rules in multiple custom sets with different
  targets, because exact duplicates can become last-write-wins.
- Use `Proxy` instead of separate CDN/global runtime rules. Legacy `CDN` and
  split Apple rule sets remain published for compatibility.
- Use `Apple` instead of the split `Apple CDN`, `Apple CN`, and
  `Apple Services` rule sets. The split Apple files remain published for
  compatibility.
- `Telegram` contains both Telegram domain and IP CIDR rules. Legacy
  `Telegram IP` remains published for compatibility.
- `Lan` contains both LAN domain and IP CIDR rules. Legacy `LAN IP` remains
  published for compatibility.
- `CN Domain` is a broad direct fallback based on v2fly `geolocation-cn`. It is
  not equivalent to SagerNet `geosite-cn.srs`.
- `Proxy` is a broad CDN/global proxy fallback and overlaps with `Download`,
  `Telegram`, `PayPal`, and `Crypto`; keep those as separate sets so their
  assignments remain explicit.
- `Domestic` and upstream `Direct` are not published for Anywhere because ARRS cannot represent all upstream matchers.
- `Google` and `not-cn-domain` are not published for Anywhere.
- `Direct Extra` is the personal direct overlay and includes Kuro, CITIC,
  `videocc.net`, `cache.video.iqiyi.com`, and DigiCert certificate
  infrastructure.
- Legacy `Kuro` and `CITIC` files remain published for compatibility, but new
  profiles should use `Direct Extra` instead.
- `Direct Extra`, `PayPal`, and `Crypto` are intentionally separate rule sets.
- If `Binance` is a separate local rule set, assign it explicitly; if it uses
  the same proxy chain as `Crypto`, `Crypto` alone is usually enough.
- `Speedtest` is not published for Anywhere.
- `getui` is intentionally not included.
- Keep private domains and proxy subscriptions out of this repository.
