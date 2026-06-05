#!/usr/bin/env python3
"""Inject newsletter-popup.js before site.js on all public pages."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SKIP_DIRS = {"preview", "partials", "ui_kits", "posts"}
SKIP_FILES = {"blog.html"}

from site_newsletter_popup_snippet import NEWSLETTER_POPUP_SCRIPT

EXISTING_RE = re.compile(
    r'\s*<script src="[^"]*js/newsletter-popup\.js"[^>]*></script>\s*',
    re.IGNORECASE,
)


def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth


def inject_script(text: str, prefix: str) -> str:
    if "newsletter-popup.js" in text:
        return text

    tag = NEWSLETTER_POPUP_SCRIPT.format(prefix=prefix)
    site_tag = f'<script src="{prefix}js/site.js"'
    if site_tag in text:
        return text.replace(site_tag, f"{tag}\n{site_tag}", 1)
    return text.replace("</body>", f"\n{tag}\n</body>", 1)


def main() -> None:
    patched = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if rel.name in SKIP_FILES:
            continue
        if rel.parts and rel.parts[0] in SKIP_DIRS:
            continue
        prefix = prefix_for(path)
        original = path.read_text(encoding="utf-8")
        if "site.js" not in original and "newsletter-popup.js" not in original:
            continue
        cleaned = EXISTING_RE.sub("\n", original)
        updated = inject_script(cleaned, prefix)
        if updated == original:
            continue
        path.write_text(updated, encoding="utf-8")
        patched += 1
        print(f"patched {rel}")
    print(f"patched {patched} files")


if __name__ == "__main__":
    main()
