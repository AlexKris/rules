# Notice

This repository contains personal overlay rules and client profiles.

Upstream rules are referenced for personal configuration and may be used as
inputs for future generated files. Third-party rule content remains licensed by
its original authors and projects.

Known upstream sources used by the related profiles include:

- Sukka Ruleset: https://github.com/SukkaW/Surge
- Sukka Ruleset published files: https://github.com/SukkaLab/ruleset.skk.moe
- v2fly domain-list-community: https://github.com/v2fly/domain-list-community
- SagerNet sing-geosite: https://github.com/SagerNet/sing-geosite
  - `geosite-private.srs` is mirrored unchanged; upstream domain data comes
    from v2fly domain-list-community (MIT), with SagerNet's processing.
  - SagerNet's generator project is GPL-3.0-or-later. See the published
    `sing-box/NOTICE.md` for attribution and upstream source/license links.
- MetaCubeX meta-rules-dat: https://github.com/MetaCubeX/meta-rules-dat
- Loyalsoldier surge-rules: https://github.com/Loyalsoldier/surge-rules
  - `direct.txt` (GPL-3.0) is merged into `cn-domain` after a Tranco ranking
    filter; its data comes mainly from felixonmars dnsmasq-china-list:
    https://github.com/felixonmars/dnsmasq-china-list
- Tranco: https://tranco-list.eu
  - A pinned top-1M list is used only to filter `direct.txt` entries; no
    ranking data is published.
- blackmatrix7 ios_rule_script: https://github.com/blackmatrix7/ios_rule_script
- Maasea sgmodule: https://github.com/Maasea/sgmodule
  - `anywhere/mitm/source/vendor/maasea-youtube.response.js` is derived from
    Maasea's YouTube Enhance script, licensed under Apache-2.0.

Private domains, private media services, proxy nodes, subscription URLs, and
tokens must not be committed to this repository.
