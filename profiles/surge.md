# Surge Profile

Rule sets are matched in profile order, so the sections below are listed in the
order they must appear in `[Rule]`. Narrow overlays come first, broad
broad direct fallbacks come last.

There is no proxy-side fallback set: anything no set claims goes to `FINAL`,
which is the proxy policy. Every IP rule file carries `no-resolve`, so an
unmatched domain is never resolved locally.

Direct Extra:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/direct-extra.conf,DIRECT,extended-matching
```

`direct-extra` carries the Kuro and CITIC direct domains; no separate files exist.

Speedtest:

```ini
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/speedtest.conf,Speedtest,extended-matching
```

AI / PayPal:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/ai.conf,AI,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/paypal.conf,PayPal,extended-matching
```

Stream:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/stream.conf,Media,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/stream-hk.conf,MediaHK,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/stream-tw.conf,MediaTW,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/stream-jp.conf,MediaJP,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/stream-us.conf,MediaUS,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/stream-kr.conf,MediaKR,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/stream-eu.conf,MediaEU,extended-matching
```

Telegram:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/telegram.conf,Telegram,extended-matching
```

Apple:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple-proxy.conf,Proxy,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple.conf,DIRECT,extended-matching
```

`apple-proxy` must come before `apple`. The unified `apple` set (one file; the
SKK Apple CDN domainset is folded in) carries the broad `DOMAIN-SUFFIX,apple.com`,
`icloud.com`, and `me.com` suffixes from SKK Apple Services, so anything not
carved out ahead of it takes the direct route.
Keep Stream before `apple-proxy` as well, so Apple TV+ playback stays on the
Stream policy.

Microsoft CDN / Download:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/microsoft-cdn.conf,DIRECT,extended-matching
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/download.conf,Download,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/download.conf,Download,extended-matching
```

Google:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/google.conf,Google,extended-matching
```

Keep Stream before Google. The Google upstream includes YouTube, and Stream
should own YouTube routing.

Base direct:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/direct.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/cn-domain.conf,DIRECT,extended-matching
```

`direct` is SKK Direct (LAN names, PT trackers, academic sites, downloader
processes); it already contains every SKK LAN domain rule. `cn-domain` is the
China domain fallback and already contains SKK Domestic.

IP rules:

```ini
IP-CIDR,17.0.0.0/8,DIRECT,no-resolve
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/ip/telegram-ip.conf,Telegram,no-resolve
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/ip/lan-ip.conf,DIRECT
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/ip/china-ip.conf,DIRECT
```

Keep non-IP rule sets before IP rule sets in profile order.

`IP-CIDR,17.0.0.0/8,DIRECT,no-resolve` must lead the IP section. iOS opens QUIC
connections to iCloud and migrates them across the server pool; only the first
packet carries an SNI, so the migrated paths reach the rule engine as bare IPs and
match no domain rule. Without this line they fall through `china-ip` and `GEOIP,CN`
to `FINAL` and land on a proxy policy. Surge's `block-quic` option defaults to
`per-policy`, under which proxy policies block QUIC and DIRECT does not, so those
paths are dropped and logged as `17.248.x.x:443 (Port Map)` / `QUIC-BLOCK`. This is
`block-quic`, not `udp-policy-not-supported-behaviour`; the latter governs UDP that
hits a policy without relay support and is unrelated here.

The visible symptom is a half-completed iCloud account session: the Apple ID avatar
does not render in iOS Settings and iCloud reports `家人共享信息不可用`. Global
direct mode hides the bug because every path then matches DIRECT. `no-resolve` keeps
the rule from claiming domain requests, which the Apple domain sets above already
handle.

Place this rule first in the IP section of every Surge-family and Mihomo profile
(Surge, Shadowrocket, Loon, Mihomo, Stash), not just Surge. The sing-box template
deliberately omits it; see the profile repository's `singbox/README.md`. `17.0.0.0/8` does not
overlap `telegram-ip`, `lan-ip`, or `china-ip`, so its position among them is
behaviourally free — but keep the order uniform across profiles so the sections stay
diffable.

Do not add private domains, private media services, proxy nodes, subscription
URLs, or tokens to this repository.
