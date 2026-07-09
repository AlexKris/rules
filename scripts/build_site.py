#!/usr/bin/env python3
"""Build the static rule distribution site."""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "_site"
PUBLISHED_DIRS = [
    "anywhere",
    "surge",
    "loon",
    "mihomo",
    "sing-box",
    "plain",
    "profiles",
]
EXCLUDED_OUTPUTS = [
    Path("anywhere/mitm/source"),
]


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_published_dirs() -> None:
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True)

    for directory in PUBLISHED_DIRS:
        source = ROOT / directory
        if not source.is_dir():
            raise FileNotFoundError(f"missing published directory: {directory}")
        shutil.copytree(
            source,
            SITE_DIR / directory,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
        )

    for relative_path in EXCLUDED_OUTPUTS:
        path = SITE_DIR / relative_path
        if path.exists():
            shutil.rmtree(path)


def site_files() -> list[Path]:
    files = []
    for directory in PUBLISHED_DIRS:
        files.extend(path for path in (SITE_DIR / directory).rglob("*") if path.is_file())
    return sorted(files, key=lambda path: path.relative_to(SITE_DIR).as_posix())


def write_headers() -> None:
    (SITE_DIR / "_headers").write_text(
        """/*
  Access-Control-Allow-Origin: *
  Cache-Control: public, max-age=300, s-maxage=3600
""",
        encoding="utf-8",
    )


def write_manifest(files: list[Path], generated_at: str) -> None:
    entries = [
        {
            "path": path.relative_to(SITE_DIR).as_posix(),
            "size": path.stat().st_size,
            "sha256": file_digest(path),
        }
        for path in files
    ]
    manifest = {
        "generated_at": generated_at,
        "file_count": len(entries),
        "files": entries,
    }
    (SITE_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_index(files: list[Path], generated_at: str) -> None:
    grouped: dict[str, list[str]] = {}
    for path in files:
        relative_path = path.relative_to(SITE_DIR).as_posix()
        group = relative_path.split("/", 1)[0]
        grouped.setdefault(group, []).append(relative_path)

    sections = []
    for group in PUBLISHED_DIRS:
        links = grouped.get(group, [])
        if not links:
            continue
        items = "\n".join(
            f'<li><a href="/{escape(link)}">{escape(link)}</a></li>'
            for link in links
        )
        sections.append(f"<section><h2>{escape(group)}</h2><ul>{items}</ul></section>")

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Rules</title>
  <style>
    body {{ font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 2rem; line-height: 1.5; }}
    main {{ max-width: 960px; }}
    h1 {{ margin-bottom: 0.25rem; }}
    h2 {{ margin-top: 2rem; }}
    ul {{ padding-left: 1.25rem; }}
    li {{ margin: 0.125rem 0; }}
    a {{ color: #1a56db; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .meta {{ color: #59636e; }}
    code {{ background: #f3f4f6; padding: 0.1rem 0.25rem; border-radius: 4px; }}
  </style>
</head>
<body>
  <main>
    <h1>Rules</h1>
    <p class="meta">Generated at {escape(generated_at)}. Manifest: <a href="/manifest.json"><code>manifest.json</code></a>.</p>
    {''.join(sections)}
  </main>
</body>
</html>
"""
    (SITE_DIR / "index.html").write_text(html, encoding="utf-8")


def main() -> int:
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    copy_published_dirs()
    files = site_files()
    write_headers()
    write_manifest(files, generated_at)
    write_index(files, generated_at)
    print(f"Built {SITE_DIR.relative_to(ROOT)} with {len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
