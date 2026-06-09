#!/usr/bin/env python3
"""Patch internal href/action/data-redirect values to clean URLs across the site."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from site_urls import patch_html_href

EXCLUDE_DIRS = {"preview", "partials", "ui_kits", "scripts", "assets", "js", "node_modules", "data"}
HREF_RE = re.compile(
    r'''(?P<attr>href|data-redirect|action)\s*=\s*(?P<quote>["'])(?P<value>(?:\\.|(?!\2).)*?)\2''',
    re.IGNORECASE,
)


def is_public_html(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part.startswith(".") for part in rel.parts):
        return False
    if rel.parts and rel.parts[0] in EXCLUDE_DIRS:
        return False
    return True


def patch_html_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    changed = False

    def repl(match: re.Match) -> str:
        nonlocal changed
        value = match.group("value")
        if ".html" not in value:
            return match.group(0)
        new_value = patch_html_href(value, path)
        if new_value != value:
            changed = True
        quote = match.group("quote")
        attr = match.group("attr")
        return f'{attr}={quote}{new_value}{quote}'

    updated = HREF_RE.sub(repl, text)
    if changed:
        path.write_text(updated, encoding="utf-8")
    return changed


def patch_partials() -> int:
    count = 0
    for path in sorted((ROOT / "partials").rglob("*.html")):
        if patch_html_file(path):
            count += 1
            print(f"patched {path.relative_to(ROOT)}")
    return count


def patch_data_files() -> int:
    count = 0
    loc_file = ROOT / "data" / "locationHubs.js"
    if not loc_file.exists():
        return 0
    text = loc_file.read_text(encoding="utf-8")
    original = text
    mapping = {
        "services/branding.html": "/branding",
        "services/seo.html": "/seo",
        "services/google-ads.html": "/google-ads",
        "services/social-media.html": "/social-media",
        "services/web-design.html": "/web-design",
    }
    for old, new in mapping.items():
        text = text.replace(f'"href": "{old}"', f'"href": "{new}"')
    if text != original:
        loc_file.write_text(text, encoding="utf-8")
        count += 1
        print(f"patched {loc_file.relative_to(ROOT)}")
    return count


def main() -> None:
    html_patched = 0
    for path in sorted(ROOT.rglob("*.html")):
        if not is_public_html(path):
            continue
        if patch_html_file(path):
            html_patched += 1
            print(f"patched {path.relative_to(ROOT)}")

    partial_patched = patch_partials()
    data_patched = patch_data_files()
    print(f"patched {html_patched} html, {partial_patched} partials, {data_patched} data files")


if __name__ == "__main__":
    main()
