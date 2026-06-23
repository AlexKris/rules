# Surge Profile

Use the generated unified proxy and direct rules before broad domestic/global
fallback rules.

Proxy:

```ini
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/proxy.conf,Proxy,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/proxy.conf,Proxy,extended-matching
```

Speedtest:

```ini
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/speedtest.conf,Speedtest,extended-matching
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

Google:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/google.conf,Google,extended-matching
```

Keep Stream before Google. The Google upstream includes YouTube, and Stream
should own YouTube routing.

Apple:

```ini
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/apple.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/apple.conf,DIRECT,extended-matching
```

Download:

```ini
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/download.conf,Download,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/download.conf,Download,extended-matching
```

Base direct:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/domestic.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/direct.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/lan.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/direct-extra.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/cn-domain.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/not-cn-domain.conf,Proxy,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/ip/lan-ip.conf,DIRECT,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/ip/china-ip.conf,DIRECT,extended-matching
```

Keep non-IP direct rule sets before IP rule sets in profile order.
`not-cn-domain` is a broad proxy fallback for text-rule clients.

AI:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/ai.conf,AI,extended-matching
```

Telegram:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/telegram.conf,Telegram,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/ip/telegram-ip.conf,Telegram,extended-matching
```

Crypto:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/crypto.conf,Crypto,extended-matching
```

PayPal:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/paypal.conf,PayPal,extended-matching
```

Microsoft:

```ini
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/microsoft.conf,Proxy,extended-matching
RULE-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/non-ip/microsoft-cdn.conf,DIRECT,extended-matching
```

Kuro:

```ini
DOMAIN-SET,https://raw.githubusercontent.com/AlexKris/rules/main/surge/domainset/kuro.conf,DIRECT,extended-matching
```

Do not add private domains, private media services, proxy nodes, subscription
URLs, or tokens to this repository.
