#!/usr/bin/env python3
"""Replace flat About nav links with About dropdown across site HTML."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ABOUT_DESKTOP = """      <div class="nav-about" id="navAbout">
        <button class="nav-svc-btn" type="button">About
          <svg class="nav-chevron" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
        <div class="nav-dd nav-dd-about">
          <div class="nav-dd-arrow"></div>
          <a href="{prefix}about.html" class="dd-simple">About Us</a>
          <a href="{prefix}washington-state-sales-tax.html" class="dd-simple">WA Sales Tax Notice</a>
        </div>
      </div>"""

ABOUT_MOBILE = """    <a href="#" onclick="document.getElementById('mobileAboutList').classList.toggle('open');return false" style="display:flex;justify-content:space-between;align-items:center">About <span>▾</span></a>
    <div class="mobile-svc-list" id="mobileAboutList">
      <a href="{prefix}about.html">About Us</a>
      <a href="{prefix}washington-state-sales-tax.html">WA Sales Tax Notice</a>
    </div>"""


def prefix_for(path: Path) -> str:
    rel = path.relative_to(ROOT)
    depth = len(rel.parts) - 1
    return "../" * depth if depth else ""


def patch_file(path: Path) -> bool:
    if "preview" in path.parts or path.name == "washington-state-sales-tax.html":
        return False

    text = path.read_text(encoding="utf-8")
    original = text
    prefix = prefix_for(path)

    # Desktop nav: first About link inside <nav class="nav">
    nav_about_pat = re.compile(
        r'(<nav class="nav">.*?)(<a href="(?:\.\./)*about\.html"[^>]*>About</a>)',
        re.DOTALL,
    )
    if nav_about_pat.search(text):
        text = nav_about_pat.sub(
            r"\1" + ABOUT_DESKTOP.format(prefix=prefix),
            text,
            count=1,
        )

    # Mobile menu: About link after Home (various home href patterns)
    mobile_pat = re.compile(
        r'(<div class="mobile-menu"[^>]*>.*?'
        r'<a href="(?:#|(?:\.\./)*index\.html)"[^>]*>Home</a>\s*)'
        r'(<a href="(?:\.\./)*about\.html"[^>]*>About</a>)',
        re.DOTALL,
    )
    if mobile_pat.search(text) and "mobileAboutList" not in text:
        text = mobile_pat.sub(
            r"\1" + ABOUT_MOBILE.format(prefix=prefix),
            text,
            count=1,
        )

    # Blog-style mobile without Home first
    if "mobileAboutList" not in text:
        mobile_pat2 = re.compile(
            r'(<div class="mobile-menu"[^>]*>\s*)'
            r'(<a href="(?:\.\./)*index\.html"[^>]*>Home</a>\s*)'
            r'(<a href="(?:\.\./)*about\.html"[^>]*>About</a>)',
            re.DOTALL,
        )
        if mobile_pat2.search(text):
            text = mobile_pat2.sub(
                r"\1\2" + ABOUT_MOBILE.format(prefix=prefix),
                text,
                count=1,
            )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    updated = []
    for path in sorted(ROOT.rglob("*.html")):
        if patch_file(path):
            updated.append(path.relative_to(ROOT))
    print(f"Updated {len(updated)} files")
    for p in updated:
        print(f"  {p}")


if __name__ == "__main__":
    main()
