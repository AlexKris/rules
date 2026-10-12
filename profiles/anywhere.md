# Anywhere Profile

Import the following rule sets and keep them in this Routing list order (top to
bottom). Identical patterns in two sets go to the higher set, so the order
matters where sets overlap:

```text
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/direct-extra.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/lan.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/china-ip.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/ai.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/paypal.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-hk.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-tw.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-jp.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-us.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-kr.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/stream-eu.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/telegram.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple-proxy.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/apple.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/download.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/google.arrs
https://raw.githubusercontent.com/AlexKris/rules/main/anywhere/cn-domain.arrs
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
Direct Extra    -> DIRECT
LAN             -> DIRECT
China IP        -> DIRECT
AI              -> AI chain
PayPal          -> PayPal chain
Stream          -> Stream chain
Stream HK       -> MediaHK
Stream TW       -> MediaTW
Stream JP       -> MediaJP
Stream US       -> MediaUS
Stream KR       -> MediaKR
Stream EU       -> MediaEU
Telegram        -> Telegram chain
Apple Proxy     -> PROXY
Apple           -> DIRECT
Download        -> Download
Google          -> Google chain
CN Domain       -> DIRECT
```

Required ordering:

- `Apple Proxy` above `Apple`: both contain `apple.news`.
- `Stream` and `AI` above `Google`: `Google` also contains `youtube.com`,
  `googlevideo.com`, `ai.studio`, and `deepmind.com`.
- `CN Domain` below `Stream`, `AI`, and `Google`: it shares a few identical
  entries with each of them.

App settings:

- Leave every built-in service (Google, YouTube, Netflix, ChatGPT, Claude,
  Telegram, X, TikTok, Spotify, ...) on `Default`. A built-in service with any
  other action sits in the Built-in tier and beats every custom set regardless
  of specificity; for example, built-in YouTube on `PROXY` overrides `Stream`.
  On `Default` it only catches destinations no custom set matches and sends
  them to the default route.
- Turn on `Prevent DNS Leak`. Otherwise a domain that matches no domain rule is
  resolved (system DNS by default) and its IPv4 address is checked against the
  IP CIDR rules. With it on, `LAN`, `China IP`, and `Telegram` IP rules apply
  only to literal IP destinations, like `no-resolve` on other clients.
- Turn off `Country Bypass`. Its bundled per-country rules cannot be audited,
  and `CN Domain` plus `China IP` already cover the same intent.
- Unmatched traffic takes the default route, so no proxy-side fallback set is
  published.

How Anywhere matches:

- Tiers, first match wins: ADBlock > Built-in > User > Neutral > Country
  Bypass. A higher tier beats a more specific rule in a lower tier.
- A set on `DIRECT`, `REJECT`, `PROXY`, or a chain stays in its origin tier
  (User for custom sets). `PROXY` routes to the same default target as an
  unmatched connection but still as an explicit action. A set on `Default`
  drops to the Neutral tier and routes to the default target.
- Within a tier: deepest suffix, then longest keyword, then longest CIDR
  prefix; suffix before keyword; identical patterns go to the set higher in
  the Routing list.
- Each custom set is limited to 100,000 rules; an import or refresh above that
  is rejected.

Notes:

- `CN Domain` uses the same rules as the Surge, Loon, Mihomo, and sing-box
  outputs: v2fly `cn`, the Tranco-ranked Loyalsoldier direct list, and SKK
  Domestic.
- `Google` is v2fly `google`, which includes YouTube.
- `Stream` adds `ytimg.com` and `youtu.be` so YouTube thumbnails and short
  links follow the video policy.
- `Telegram` contains both Telegram domain and IP CIDR rules. Legacy
  `Telegram IP` remains published for compatibility.
- `LAN` contains both LAN domain and IP CIDR rules. Legacy `LAN IP` remains
  published for compatibility.
- `Apple` is the single Apple set; the split Apple files are no longer
  published.
- Upstream `Direct`, `Speedtest`, and `Microsoft CDN` are not published for
  Anywhere.
- `Direct Extra` is the personal direct overlay and includes Kuro, CITIC,
  `videocc.net`, `cache.video.iqiyi.com`, and DigiCert certificate
  infrastructure.
- `getui` is intentionally not included.
- Keep private domains and proxy subscriptions out of this repository.
