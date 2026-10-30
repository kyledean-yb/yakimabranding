#!/usr/bin/env python3
"""Replace the desktop nav and mobile menu on every page with the mega menu. Safe to re-run."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mega_nav import ROOT, patch_html  # noqa: E402

SKIP = {"next", "node_modules", ".git", ".vercel", "scripts"}


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if SKIP & set(rel.parts):
            continue
        text = path.read_text(encoding="utf-8")
        if '<nav class="nav' not in text and 'id="mobileMenu"' not in text:
            continue
        lang = "es" if rel.parts[0] == "es" else "en"
        new = patch_html(text, lang)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
    print(f"updated {changed} pages")


if __name__ == "__main__":
    main()
