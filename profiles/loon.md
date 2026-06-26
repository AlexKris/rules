# Loon Profile

Use the generated `.list` files in `[Remote Rule]`. Replace policy names with
your local policy groups where needed.

Stream:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/stream.list,policy=Media,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/stream-hk.list,policy=MediaHK,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/stream-tw.list,policy=MediaTW,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/stream-jp.list,policy=MediaJP,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/stream-us.list,policy=MediaUS,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/stream-kr.list,policy=MediaKR,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/stream-eu.list,policy=MediaEU,enabled=true
```

Speedtest:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/domainset/speedtest.list,policy=Speedtest,enabled=true
```

AI:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/ai.list,policy=AI,enabled=true
```

Telegram:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/telegram.list,policy=Telegram,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/ip/telegram-ip.list,policy=Telegram,enabled=true
```

Crypto:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/crypto.list,policy=Crypto,enabled=true
```

PayPal:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/paypal.list,policy=PayPal,enabled=true
```

Microsoft:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/microsoft-cdn.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/microsoft.list,policy=Proxy,enabled=true
```

Google:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/google.list,policy=Google,enabled=true
```

Keep Stream before Google. The Google upstream includes YouTube, and Stream
should own YouTube routing.

Apple:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/domainset/apple.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/apple.list,policy=DIRECT,enabled=true
```

Download:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/domainset/download.list,policy=Download,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/download.list,policy=Download,enabled=true
```

Base direct:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/domestic.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/direct.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/lan.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/direct-extra.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/cn-domain.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/ip/lan-ip.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/ip/china-ip.list,policy=DIRECT,enabled=true
```

Loon matches domain rules before IP rules for domain targets. IP rules still use
`no-resolve` to avoid unnecessary DNS lookups.

Proxy fallback:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/domainset/proxy.list,policy=Proxy,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/proxy.list,policy=Proxy,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/not-cn-domain.list,policy=Proxy,enabled=true
```

Keep proxy fallback after dedicated proxy policy groups. `proxy` and
`not-cn-domain` are broad rules and can otherwise capture Stream, Google, AI,
Crypto, PayPal, Telegram, and Microsoft traffic first.

Loon rule sets omit `DOMAIN-WILDCARD` and `PROCESS-NAME`, which are not listed
in Loon's official rule syntax. Use `direct-extra` for Kuro and CITIC; no
separate Loon compatibility files are generated for them.
