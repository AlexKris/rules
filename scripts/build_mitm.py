#!/usr/bin/env python3
"""Build Anywhere MITM rule sets from local source files."""

from __future__ import annotations

import base64
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MITM_DIR = ROOT / "anywhere" / "mitm"
SOURCE_DIR = MITM_DIR / "source"
YOUTUBE_ADAPTER = SOURCE_DIR / "youtube-enhance-anywhere.js"
YOUTUBE_VENDOR = SOURCE_DIR / "vendor" / "maasea-youtube.response.js"
YOUTUBE_OUTPUT = MITM_DIR / "youtube-enhance-anywhere.amrs"
YOUTUBE_PLACEHOLDER = "__YOUTUBE_RESPONSE_JS_BASE64__"


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def render_youtube_script() -> str:
    adapter = YOUTUBE_ADAPTER.read_text(encoding="utf-8")
    vendor_b64 = b64(YOUTUBE_VENDOR.read_bytes())
    if YOUTUBE_PLACEHOLDER not in adapter:
        raise ValueError(f"{YOUTUBE_ADAPTER} is missing {YOUTUBE_PLACEHOLDER}")
    return adapter.replace(YOUTUBE_PLACEHOLDER, vendor_b64)


def write_youtube_enhance() -> None:
    script_b64 = b64(render_youtube_script().encode("utf-8"))
    pattern = r"^https:\/\/youtubei\.googleapis\.com\/(youtubei\/v1\/(browse|next|player|search|reel\/reel_watch_sequence|guide|account\/get_setting|get_watch))(\?(.*))?$"
    lines = [
        "# Anywhere MITM - YouTube Enhance",
        "# GENERATED-FROM:",
        "# - anywhere/mitm/source/youtube-enhance-anywhere.js",
        "# - anywhere/mitm/source/vendor/maasea-youtube.response.js",
        "",
        "name     = YouTube (Music) Enhance - Anywhere",
        "hostname = googlevideo.com, youtubei.googleapis.com, doubleclick.net, googlesyndication.com, googleadservices.com, googleads.g.doubleclick.net",
        "",
        "# URL-level ad blocking",
        r"0, 0, ^https?:\/\/[\w-]+\.googlevideo\.com\/initplayback.+&oad, 2",
        r"0, 0, ^https?:\/\/googleads\.g\.doubleclick\.net\/pagead\/, 2",
        r"0, 0, ^https?:\/\/pagead2\.googlesyndication\.com\/pagead\/, 2",
        r"0, 0, ^https?:\/\/[\w-]+\.doubleclick\.net\/.*\/ad, 2",
        r"0, 0, ^https?:\/\/static\.doubleclick\.net\/instream\/, 2",
        "",
        "# Protobuf response processor with Surge compatibility stubs",
        f"1, 100, {pattern}, {script_b64}",
    ]
    YOUTUBE_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    write_youtube_enhance()
    print(YOUTUBE_OUTPUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
