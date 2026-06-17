#!/usr/bin/env python3
"""Build Anywhere MITM rule sets from readable source files."""

from __future__ import annotations

import base64
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def js_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def write_google_cn_redirect() -> None:
    source_path = ROOT / "anywhere" / "mitm" / "source" / "google-cn-redirect.js"
    output_path = ROOT / "anywhere" / "mitm" / "google-cn-redirect.amrs"
    script = js_base64(source_path)
    pattern = r"^https?:\/\/(?:(?:www\.)?(?:g|google)\.cn|(?:ditu|maps)\.google\.cn)(?=[:\/?#]|$)"
    lines = [
        "# Google CN Redirect - Anywhere MITM RuleSet",
        "# GENERATED-FROM: anywhere/mitm/source/google-cn-redirect.js",
        "",
        "name = Google CN 307 Redirect",
        "hostname = google.cn, g.cn",
        "",
        f"0, 100, {pattern}, {script}",
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    write_google_cn_redirect()
    print("google-cn-redirect.amrs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
