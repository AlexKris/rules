# Loon Profile

Use the generated `.list` files in `[Remote Rule]`, in this order. Replace
policy names with your local policy groups where needed. Keep `[Rule]` to the
local `IP-CIDR,17.0.0.0/8,DIRECT,no-resolve` line (and `PROCESS-NAME` rules on
macOS) plus `FINAL`; local rules match before remote ones.

Direct Extra:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/direct-extra.list,policy=DIRECT,enabled=true
```

Use `direct-extra` for Kuro and CITIC; no separate files are generated for them.

Speedtest:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/domainset/speedtest.list,policy=Speedtest,enabled=true
```

AI / PayPal:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/ai.list,policy=AI,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/paypal.list,policy=PayPal,enabled=true
```

Stream:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/stream-jp.list,policy=MediaJP,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/stream-tw.list,policy=MediaTW,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/stream.list,policy=Media,enabled=true
```

`stream-hk`, `stream-us`, `stream-kr`, and `stream-eu` are also published.

Telegram:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/telegram.list,policy=Telegram,enabled=true
```

Apple:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/apple-proxy.list,policy=Proxy,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/apple.list,policy=DIRECT,enabled=true
```

`apple-proxy` must come before `apple`; `apple` carries the broad `apple.com`,
`icloud.com`, and `me.com` suffixes. Keep Stream before `apple-proxy` so Apple
TV+ stays on the Stream policy.

Microsoft CDN / Download:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/microsoft-cdn.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/domainset/download.list,policy=Download,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/download.list,policy=Download,enabled=true
```

Google:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/google.list,policy=Google,enabled=true
```

Keep Stream before Google. The Google upstream includes YouTube, and Stream
should own YouTube routing.

Base direct:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/direct.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/non-ip/cn-domain.list,policy=DIRECT,enabled=true
```

`direct` already contains every SKK LAN domain rule; `cn-domain` already
contains SKK Domestic.

IP rules:

```ini
https://raw.githubusercontent.com/AlexKris/rules/main/loon/ip/telegram-ip.list,policy=Telegram,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/ip/lan-ip.list,policy=DIRECT,enabled=true
https://raw.githubusercontent.com/AlexKris/rules/main/loon/ip/china-ip.list,policy=DIRECT,enabled=true
```

Loon matches domain rules before IP rules for domain targets. Every line in the
IP lists carries `no-resolve`, so an unmatched domain is never resolved locally
and falls through to `FINAL`. There is no proxy-side fallback set.

Loon rule sets omit `DOMAIN-WILDCARD` and `PROCESS-NAME`, which are not listed
in Loon's official rule syntax.
