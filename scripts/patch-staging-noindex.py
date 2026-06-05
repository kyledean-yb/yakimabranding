#!/usr/bin/env python3
"""Add noindex,nofollow to all public HTML pages (staging)."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SKIP_DIRS = {"preview", "partials", "ui_kits", "posts"}

from site_staging_seo_snippet import STAGING_ROBOTS_META

ROBOTS_META_RE = re.compile(
    r'\s*<meta\s+name="robots"\s+content="[^"]*"\s*/?\s*>\s*',
    re.IGNORECASE,
)
VIEWPORT_RE = re.compile(
    r'(<meta\s+name="viewport"[^>]*>)',
    re.IGNORECASE,
)
CHARSET_RE = re.compile(
    r'(<meta\s+charset[^>]*>)',
    re.IGNORECASE,
)


def inject_noindex(text: str) -> str:
    if STAGING_ROBOTS_META in text:
        return text

    text = ROBOTS_META_RE.sub("\n", text)

    if VIEWPORT_RE.search(text):
        return VIEWPORT_RE.sub(rf"\1\n{STAGING_ROBOTS_META}", text, count=1)
    if CHARSET_RE.search(text):
        return CHARSET_RE.sub(rf"\1\n{STAGING_ROBOTS_META}", text, count=1)
    return text.replace("<head>", f"<head>\n{STAGING_ROBOTS_META}", 1)


def main() -> None:
    patched = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP_DIRS:
            continue
        original = path.read_text(encoding="utf-8")
        updated = inject_noindex(original)
        if updated == original:
            continue
        path.write_text(updated, encoding="utf-8")
        patched += 1
        print(f"patched {rel}")
    print(f"patched {patched} files")


if __name__ == "__main__":
    main()
