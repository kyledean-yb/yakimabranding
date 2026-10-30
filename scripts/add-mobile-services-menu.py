#!/usr/bin/env python3
"""Add a collapsible Services list to the mobile (hamburger) menu on every page.

Links are copied from each page's desktop Services dropdown so prefixes and
EN/ES URLs always match. Safe to re-run: pages that already have the list are
refreshed in place.
"""

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NAV_SERVICES_RE = re.compile(
    r'<div class="nav-services" id="navServices">\s*<button class="nav-svc-btn"[^>]*>\s*([^<]+?)\s*<svg.*?'
    r'<div class="nav-dd-grid">(.*?)</div>\s*</div>\s*</div>',
    re.S,
)
CARD_RE = re.compile(
    r'<a href="([^"]+)" class="dd-card[^"]*">.*?<span class="dd-name">(.*?)</span>'
    r'(?:<span class="dd-desc">(.*?)</span>)?',
    re.S,
)
EXISTING_RE = re.compile(
    r'\s*<a href="#" onclick="document\.getElementById\(\'mobileServicesList\'\).*?</a>\s*'
    r'<div class="mobile-svc-list" id="mobileServicesList">.*?</div>',
    re.S,
)
ABOUT_LIST_RE = re.compile(r'(<div class="mobile-svc-list" id="mobileAboutList">.*?</div>)', re.S)


def mobile_services_block(label: str, cards) -> str:
    rows = "\n".join(
        f'      <a href="{href}" class="mobile-about-row"><strong>{name}</strong>'
        + (f"<span>{desc}</span>" if desc else "")
        + "</a>"
        for href, name, desc in cards
    )
    return (
        "\n    <a href=\"#\" onclick=\"document.getElementById('mobileServicesList').classList.toggle('open');return false\" "
        f'style="display:flex;justify-content:space-between;align-items:center">{label} <span>▾</span></a>\n'
        '    <div class="mobile-svc-list" id="mobileServicesList">\n'
        f"{rows}\n"
        "    </div>"
    )


def patch(text: str) -> str:
    m = NAV_SERVICES_RE.search(text)
    if not m:
        return text
    label = html.unescape(m.group(1)).strip()
    cards = CARD_RE.findall(m.group(2))
    if not cards:
        return text
    block = mobile_services_block(label, cards)
    text = EXISTING_RE.sub("", text, count=1)
    return ABOUT_LIST_RE.sub(lambda a: a.group(1) + block, text, count=1)


def main() -> int:
    changed = 0
    for path in ROOT.rglob("*.html"):
        if any(part in {"node_modules", "next", ".next", "_next"} for part in path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding="utf-8")
        if 'id="mobileMenu"' not in text:
            continue
        new = patch(text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
    print(f"updated {changed} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
