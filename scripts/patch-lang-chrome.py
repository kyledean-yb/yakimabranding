#!/usr/bin/env python3
"""Restamp shared header/footer with language switcher on English pages."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from site_footer_snippet import site_footer_html
from site_i18n import clean_path_from_file, hreflang_links
from site_nav_snippet import site_header_html

HEADER_RE = re.compile(r'<div class="header top" id="header">.*?</div>\s*(?=<section|<main|<div class="wave|<div class="hub-hero|<div style="background)', re.DOTALL)
# Fallback: match header through closing of mobile-menu parent (header top div)
HEADER_RE_FALLBACK = re.compile(
    r'<div class="header top" id="header">[\s\S]*?<div class="mobile-menu" id="mobileMenu">[\s\S]*?</div>\s*</div>',
    re.DOTALL,
)
FOOTER_RE = re.compile(r'<footer class="footer">.*?</footer>', re.DOTALL)
HREFLANG_RE = re.compile(
    r'<link\b[^>]*\bhreflang=["\'][^"\']+["\'][^>]*/?>\s*',
    re.I,
)

EXCLUDE_DIRS = {
    "preview",
    "partials",
    "ui_kits",
    "posts",
    "scripts",
    "assets",
    "js",
    "node_modules",
    "next",
    "es",
    "_next",
}


def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth


def is_public_page(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part.startswith(".") for part in rel.parts):
        return False
    if rel.parts[0] in EXCLUDE_DIRS:
        return False
    return True


def about_active_for(path: Path) -> str | None:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "about.html" or rel.startswith("about/") and "case-studies" not in rel:
        if "thank-you" in rel:
            return None
        if rel.startswith("about/") and rel.count("/") == 1 and not rel.endswith("index.html"):
            # team pages
            return "about"
        if rel == "about.html":
            return "about"
    if "case-studies" in rel:
        return "case-studies"
    if "washington-state-sales-tax" in rel:
        return "tax"
    return None


def inject_hreflang(text: str, current_clean: str) -> str:
    text = HREFLANG_RE.sub("", text)
    links = hreflang_links(current_clean)
    if "</head>" in text:
        return text.replace("</head>", links + "\n</head>", 1)
    return text


def main() -> None:
    patched = 0
    for path in sorted(ROOT.rglob("*.html")):
        if not is_public_page(path):
            continue
        text = path.read_text(encoding="utf-8")
        if 'id="header"' not in text and not FOOTER_RE.search(text):
            continue

        prefix = prefix_for(path)
        current = clean_path_from_file(path)
        about = about_active_for(path)
        header = site_header_html(prefix, about, lang="en", current_path=current).strip()
        footer = site_footer_html(prefix, lang="en", current_path=current).strip()

        updated = text
        if HEADER_RE_FALLBACK.search(updated):
            updated, n = HEADER_RE_FALLBACK.subn(header, updated, count=1)
            if n != 1:
                print(f"warn header {path.relative_to(ROOT)}")
        if FOOTER_RE.search(updated):
            updated, n = FOOTER_RE.subn(footer, updated, count=1)
            if n != 1:
                print(f"warn footer {path.relative_to(ROOT)}")

        updated = inject_hreflang(updated, current)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            patched += 1
            print(f"patched {path.relative_to(ROOT)}")

    print(f"patched {patched} pages")


if __name__ == "__main__":
    main()
