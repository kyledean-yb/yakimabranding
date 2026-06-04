#!/usr/bin/env python3
"""Upgrade About dropdown to card-style panel across all HTML pages."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from about_nav_snippet import about_nav_dropdown, about_nav_shell

OLD_DD = re.compile(
    r'<div class="nav-dd nav-dd-about">\s*'
    r'<div class="nav-dd-arrow"></div>\s*'
    r'<a href="[^"]*about\.html" class="dd-simple[^"]*">About Us</a>\s*'
    r'<a href="[^"]*washington-state-sales-tax\.html" class="dd-simple[^"]*">WA Sales Tax Notice</a>\s*'
    r'</div>',
    re.DOTALL,
)

OLD_SHELL = re.compile(
    r'<div class="nav-about" id="navAbout">\s*'
    r'<button class="nav-svc-btn"[^>]*>About\s*'
    r'<svg class="nav-chevron"[^>]*>.*?</svg>\s*'
    r'</button>\s*'
    r'<div class="nav-dd nav-dd-about">.*?</div>\s*'
    r'</div>\s*</div>',
    re.DOTALL,
)

MOBILE_OLD = re.compile(
    r'<div class="mobile-svc-list" id="mobileAboutList">\s*'
    r'<a href="[^"]*about\.html">About Us</a>\s*'
    r'<a href="[^"]*washington-state-sales-tax\.html"[^>]*>WA Sales Tax Notice</a>\s*'
    r'</div>',
    re.DOTALL,
)


def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth if depth else ""


def mobile_about_list(prefix: str) -> str:
    return f"""    <div class="mobile-svc-list" id="mobileAboutList">
      <a href="{prefix}about.html" class="mobile-about-row"><strong>About Us</strong><span>Meet our team &amp; our story</span></a>
      <a href="{prefix}washington-state-sales-tax.html" class="mobile-about-row"><strong>WA Sales Tax Notice</strong><span>Oct 2025 tax updates for WA businesses</span></a>
    </div>"""


def active_for(path: Path):
    if path.name == "about.html":
        return "about"
    if path.name == "washington-state-sales-tax.html":
        return "tax"
    return None


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    prefix = prefix_for(path)
    active = active_for(path)
    btn_style = "color:var(--yb-blue)" if active else ""

    if OLD_DD.search(text):
        text = OLD_DD.sub(about_nav_dropdown(prefix, active), text)

    if "nav-dd-about-inner" not in text and "nav-about" in text:
        m = OLD_SHELL.search(text)
        if m:
            text = text[: m.start()] + about_nav_shell(prefix, active, btn_style) + text[m.end() :]

    if MOBILE_OLD.search(text):
        text = MOBILE_OLD.sub(mobile_about_list(prefix), text)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    count = 0
    for path in sorted(ROOT.rglob("*.html")):
        if "preview" in path.parts:
            continue
        if patch(path):
            count += 1
            print(path.relative_to(ROOT))
    print(f"\nUpgraded {count} files")


if __name__ == "__main__":
    main()
