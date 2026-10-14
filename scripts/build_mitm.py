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
YOUTUBE_PLACEHOLDER = "__YOUTUBE_RESPONSE_JS_BASE64__"
YOUTUBE_UMP_ADAPTER = SOURCE_DIR / "youtube-ump-anywhere.js"
YOUTUBE_UMP_VENDOR = SOURCE_DIR / "vendor" / "maasea-youtube.ump.js"
YOUTUBE_UMP_PLACEHOLDER = "__YOUTUBE_UMP_JS_BASE64__"
YOUTUBE_ONESIE = SOURCE_DIR / "youtube-onesie-anywhere.js"
YOUTUBE_OUTPUT = MITM_DIR / "youtube-enhance-anywhere.amrs"


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def render_script(adapter_path: Path, vendor_path: Path, placeholder: str) -> str:
    adapter = adapter_path.read_text(encoding="utf-8")
    vendor_b64 = b64(vendor_path.read_bytes())
    if placeholder not in adapter:
        raise ValueError(f"{adapter_path} is missing {placeholder}")
    return adapter.replace(placeholder, vendor_b64)


def write_youtube_enhance() -> None:
    script_b64 = b64(
        render_script(YOUTUBE_ADAPTER, YOUTUBE_VENDOR, YOUTUBE_PLACEHOLDER).encode("utf-8")
    )
    ump_b64 = b64(
        render_script(YOUTUBE_UMP_ADAPTER, YOUTUBE_UMP_VENDOR, YOUTUBE_UMP_PLACEHOLDER).encode("utf-8")
    )
    onesie_b64 = b64(YOUTUBE_ONESIE.read_bytes())
    pattern = r"^https:\/\/youtubei\.googleapis\.com\/(youtubei\/v1\/(browse|next|player|search|reel\/reel_watch_sequence|guide|account\/get_setting|get_watch))(\?(.*))?$"
    ump_pattern = r"^https?:\/\/[\w-]+\.googlevideo\.com\/initplayback.+&ack.*"
    key_pattern = r"^https:\/\/youtubei\.googleapis\.com\/youtubei\/v1\/(config|log_event)(\?.*)?$"
    lines = [
        "# Anywhere MITM - YouTube Enhance",
        "# GENERATED-FROM:",
        "# - anywhere/mitm/source/youtube-enhance-anywhere.js",
        "# - anywhere/mitm/source/vendor/maasea-youtube.response.js",
        "# - anywhere/mitm/source/youtube-onesie-anywhere.js",
        "# - anywhere/mitm/source/youtube-ump-anywhere.js",
        "# - anywhere/mitm/source/vendor/maasea-youtube.ump.js",
        "",
        "name     = YouTube (Music) Enhance - Anywhere",
        "hostname = youtubei.googleapis.com, googlevideo.com, doubleclick.net, googlesyndication.com",
        "",
        "# URL-level ad blocking",
        r"0, 0, ^https:\/\/youtubei\.googleapis\.com\/youtubei\/v1\/player\/ad_break, 2",
        r"0, 0, ^https?:\/\/googleads\.g\.doubleclick\.net\/pagead\/, 2",
        r"0, 0, ^https?:\/\/pagead2\.googlesyndication\.com\/pagead\/, 2",
        r"0, 0, ^https?:\/\/[\w-]+\.doubleclick\.net\/.*\/ad, 2",
        r"0, 0, ^https?:\/\/static\.doubleclick\.net\/instream\/, 2",
        r"0, 0, ^https?:\/\/[\w-]+\.googlevideo\.com\/initplayback(\?.*oad=.+)$, 2",
        "",
        "# Maasea protobuf engine inside a Surge environment shim",
        f"1, 100, {pattern}, {script_b64}",
        "",
        "# Without the hot-hash header the server keeps sending the hot config that",
        "# carries the onesie key. A script cannot drop it conditionally, and replaying",
        "# log_event through Anywhere.http fails against Google front ends.",
        r"0, 2, ^https:\/\/youtubei\.googleapis\.com\/youtubei\/v1\/log_event, x-youtube-hot-hash-data",
        "",
        "# Onesie key gate: capture keys, pass only known-key initplayback requests",
        f"1, 100, {key_pattern}, {onesie_b64}",
        f"0, 100, {ump_pattern}, {onesie_b64}",
        "",
        "# Maasea local UMP engine: strips the ads inside the onesie initplayback stream",
        f"1, 100, {ump_pattern}, {ump_b64}",
        "",
        "[Parameter]",
        '1, 0, blockUpload, Block Upload Button, , true, "[true, false]"',
        '1, 0, blockImmersive, Block Immersive Button, , true, "[true, false]"',
        '1, 0, blockShorts, Block Shorts Button, , false, "[true, false]"',
    ]
    YOUTUBE_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    write_youtube_enhance()
    print(YOUTUBE_OUTPUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
