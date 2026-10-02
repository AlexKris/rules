# Mirrored Foundation Rule Sets

Files in `geosite/` and `geoip/` are unmodified binary copies of selected files
from the `rule-set` branches of these projects:

- https://github.com/SagerNet/sing-geosite/tree/rule-set
- https://github.com/SagerNet/sing-geoip/tree/rule-set

The generator source is available at the respective projects' `main` branches.
Both generator projects are GPL-3.0-or-later, copyright (C) 2022 nekohasekai:

- https://github.com/SagerNet/sing-geosite/blob/main/LICENSE
- https://github.com/SagerNet/sing-geoip/blob/main/LICENSE
- https://www.gnu.org/licenses/gpl-3.0.html

The geosite data originates from v2fly/domain-list-community:
https://github.com/v2fly/domain-list-community

## Domain Data License

MIT License

Copyright (c) 2018-2019 V2Ray

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## IP Data Attribution

`geoip/geoip-cn.srs` includes GeoLite2 data created by MaxMind, available from
https://www.maxmind.com. SagerNet converts the database distributed by
https://github.com/Dreamacro/maxmind-geoip into SRS; this mirror makes no further
changes. The data remains subject to Creative Commons Attribution-ShareAlike
4.0 and the GeoLite End User License Agreement, including its update and
redistribution conditions:

- https://creativecommons.org/licenses/by-sa/4.0/
- https://www.maxmind.com/en/geolite/eula
