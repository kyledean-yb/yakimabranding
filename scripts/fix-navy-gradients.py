#!/usr/bin/env python3
"""Unify navy strip gradients and wave transition colors site-wide.

DEPRECATED: Reverted 2026-06 — use scripts/revert-navy-design.py instead.
Running this script will re-break Why Choose / stats navy backgrounds.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def patch(text: str) -> str:
    # Wave dividers → shared classes (background from section above; path fill via CSS)
    text = text.replace(
        '<div class="wave-div" style="background:#F6F8FC">',
        '<div class="wave-div wave-to-navy from-soft">',
    )
    text = text.replace(
        '<div class="wave-div" style="background:var(--bg-soft)">',
        '<div class="wave-div wave-to-navy from-soft">',
    )
    text = text.replace(
        '<div class="wave-div" style="background:#ffffff">',
        '<div class="wave-div wave-to-navy from-white">',
    )
    text = text.replace(
        '<div class="wave-div" style="background:#fff">',
        '<div class="wave-div wave-to-navy from-white">',
    )

    # Navy → light
    text = re.sub(
        r'<div class="wave-div" style="background:#1B2A4A">'
        r'(<svg viewBox="0 0 1440 70" preserveAspectRatio="none">'
        r'<path d="[^"]+" fill="#F6F8FC"/>)',
        r'<div class="wave-div wave-from-navy to-soft">\1'.replace(
            ' fill="#F6F8FC"', ""
        ),
        text,
    )
    text = re.sub(
        r'<div class="wave-div" style="background:#1B2A4A">'
        r'(<svg viewBox="0 0 1440 70" preserveAspectRatio="none">'
        r'<path d="([^"]+)" fill="#F6F8FC"/>)',
        r'<div class="wave-div wave-from-navy to-soft"><svg viewBox="0 0 1440 70" preserveAspectRatio="none">'
        r'<path d="\1"/>',
        text,
    )
    text = re.sub(
        r'<div class="wave-div" style="background:#1B2A4A">'
        r'(<svg viewBox="0 0 1440 80" preserveAspectRatio="none" style="height:80px">'
        r'<path d="([^"]+)" fill="#ffffff"/>)',
        r'<div class="wave-div wave-from-navy to-white"><svg viewBox="0 0 1440 80" preserveAspectRatio="none" style="height:80px">'
        r'<path d="\1"/>',
        text,
    )
    text = re.sub(
        r'<div class="wave-div" style="background:#1B2A4A">'
        r'(<svg viewBox="0 0 1440 70" preserveAspectRatio="none">'
        r'<path d="([^"]+)" fill="#ffffff"/>)',
        r'<div class="wave-div wave-from-navy to-white"><svg viewBox="0 0 1440 70" preserveAspectRatio="none">'
        r'<path d="\1"/>',
        text,
    )

    # Glued wave + zone (service pages)
    text = text.replace(
        '"/></svg></div><div style="background:#1B2A4A">',
        '"/></svg></div><div class="yb-navy-zone">',
    )
    text = text.replace(
        'fill="#1B2A4A"/></svg></div><div style="background:#1B2A4A">',
        '"/></svg></div><div class="yb-navy-zone">',
    )
    text = text.replace(
        'fill="#1B2A4A"/></svg></div><div style="background:var(--grad-navy)">',
        '"/></svg></div><div class="yb-navy-zone">',
    )

    text = text.replace('<div style="background:#1B2A4A">', '<div class="yb-navy-zone">')
    text = text.replace(
        '<div style="background:var(--grad-navy)">', '<div class="yb-navy-zone">'
    )

    # Path fill now controlled by .wave-to-navy in site.css
    text = text.replace(' fill="#1B2A4A"', "")

    return text


def main():
    n = 0
    for path in sorted(ROOT.rglob("*.html")):
        if "preview" in path.parts or "ui_kits" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        updated = patch(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            n += 1
            print(path.relative_to(ROOT))
    print(f"\nPatched {n} files")


if __name__ == "__main__":
    main()
