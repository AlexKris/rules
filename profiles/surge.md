# Surge Profile

Rule sets are matched in profile order, so the sections below are listed in the
order they must appear in `[Rule]`. Narrow overlays come first, broad
domestic/global fallbacks come last.

The unified `proxy` set is a *fallback*, not a lead rule: it sits after the
per-service sets and after `cn-domain`, so a service-specific set can claim its
own domains first.

Kuro / Direct Extra:

```ini
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/kuro.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/direct-extra.conf,DIRECT,extended-matching
```

Speedtest:

```ini
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/speedtest.conf,Speedtest,extended-matching
```

AI / PayPal / Crypto:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/ai.conf,AI,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/paypal.conf,PayPal,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/crypto.conf,Crypto,extended-matching
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
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/apple.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple.conf,DIRECT,extended-matching
```

`apple-proxy` must come before `apple`. The unified `apple` set carries the
broad `DOMAIN-SUFFIX,apple.com`, `icloud.com`, and `me.com` suffixes from SKK
Apple Services, so anything not carved out ahead of it takes the direct route.
Keep Stream before `apple-proxy` as well, so Apple TV+ playback stays on the
Stream policy.

Microsoft CDN / Download:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/microsoft-cdn.conf,DIRECT,extended-matching
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/download.conf,Download,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/download.conf,Download,extended-matching
```

Microsoft / Google:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/microsoft.conf,Proxy,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/google.conf,Google,extended-matching
```

Keep Stream before Google. The Google upstream includes YouTube, and Stream
should own YouTube routing.

Base direct:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/domestic.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/direct.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/cn-domain.conf,DIRECT,extended-matching
```

Proxy fallback:

```ini
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/proxy.conf,Proxy,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/proxy.conf,Proxy,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/lan.conf,DIRECT
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/not-cn-domain.conf,Proxy,extended-matching
```

`not-cn-domain` is a broad proxy fallback for text-rule clients. `lan` must be ordered before it, otherwise a broad `DOMAIN-SUFFIX` in `not-cn-domain` can steal a LAN management domain and send it to the proxy.

IP rules:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/ip/telegram-ip.conf,Telegram,no-resolve
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/ip/lan-ip.conf,DIRECT
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/ip/china-ip.conf,DIRECT
```

Keep non-IP rule sets before IP rule sets in profile order.

Do not add private domains, private media services, proxy nodes, subscription
URLs, or tokens to this repository.
