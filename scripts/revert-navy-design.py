#!/usr/bin/env python3
"""Revert navy zone / wave markup to pre-gradient-refactor inline design."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Wave transitions — restore inline backgrounds + path fills
WAVE_REVERTS = [
    (
        '<div class="wave-div wave-to-navy from-soft"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z"/></svg></div><div class="yb-navy-zone">',
        '<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div><div style="background:var(--grad-navy)">',
    ),
    (
        '<div class="wave-div wave-to-navy from-soft"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z"/></svg></div>',
        '<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div>',
    ),
    (
        '<div class="wave-div wave-to-navy from-white"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z"/></svg></div><div class="yb-navy-zone">',
        '<div class="wave-div" style="background:#ffffff"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div><div style="background:var(--grad-navy)">',
    ),
    (
        '<div class="wave-div wave-to-navy from-white"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z"/></svg></div>',
        '<div class="wave-div" style="background:#ffffff"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div>',
    ),
    (
        '<div class="wave-div wave-to-navy from-white"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,30 C480,10 960,70 1440,50 L1440,70 L0,70 Z"/></svg></div>',
        '<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,30 C480,10 960,70 1440,50 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div>',
    ),
    (
        '<div class="wave-div wave-from-navy to-soft"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z"/></svg></div>',
        '<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>',
    ),
    (
        '<div class="wave-div wave-to-white from-soft"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z"/></svg></div>',
        '<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#ffffff"/></svg></div>',
    ),
    (
        '<div class="wave-div wave-to-soft from-white"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,70 C360,0 1080,0 1440,70 L1440,70 L0,70 Z"/></svg></div>',
        '<div class="wave-div" style="background:#ffffff"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,70 C360,0 1080,0 1440,70 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>',
    ),
    (
        '<div class="wave-div wave-to-navy from-soft"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,30 C480,10 960,70 1440,50 L1440,70 L0,70 Z"/></svg></div>',
        '<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,30 C480,10 960,70 1440,50 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div>',
    ),
    (
        '<div class="wave-div wave-from-navy to-white"><svg viewBox="0 0 1440 80" preserveAspectRatio="none" style="height:80px"><path d="M0,0 C360,80 1080,80 1440,0 L1440,80 L0,80 Z"/></svg></div>',
        '<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 80" preserveAspectRatio="none" style="height:80px"><path d="M0,0 C360,80 1080,80 1440,0 L1440,80 L0,80 Z" fill="#ffffff"/></svg></div>',
    ),
    (
        '<div class="wave-div wave-from-navy to-white"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z"/></svg></div>',
        '<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>',
    ),
    (
        '<div class="wave-div wave-to-navy from-soft"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,35 C360,70 1080,0 1440,35 L1440,70 L0,70 Z"/></svg></div>',
        '<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,35 C360,70 1080,0 1440,35 L1440,70 L0,70 Z" fill="#ffffff"/></svg></div>',
    ),
    (
        '<div class="wave-div wave-to-soft from-white"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,70 C480,0 960,0 1440,70 L1440,70 L0,70 Z"/></svg></div>',
        '<div class="wave-div" style="background:#ffffff"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,70 C480,0 960,0 1440,70 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>',
    ),
    (
        '<div class="wave-div wave-to-soft from-white"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,35 C360,0 1080,70 1440,35 L1440,70 L0,70 Z"/></svg></div>',
        '<div class="wave-div" style="background:#ffffff"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,35 C360,0 1080,70 1440,35 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>',
    ),
    (
        '<div class="wave-div wave-to-navy from-soft"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z"/></svg></div><div style="background:var(--grad-navy)">',
        '<div class="wave-div" style="background:var(--bg-soft)"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div><div style="background:var(--grad-navy)">',
    ),
]


def patch(text: str) -> str:
    text = text.replace('<div class="yb-navy-zone">', '<div style="background:var(--grad-navy)">')
    text = text.replace("</div><!-- /navy-zone -->", "</div><!-- /navy-zone -->")

    # Stats band inside navy wrapper: transparent so parent gradient shows through
    text = re.sub(
        r'(<div style="background:var\(--grad-navy\)">\s*<!-- STATS BAND -->\s*)<div class="stats-band">',
        r'\1<div class="stats-band" style="background:transparent">',
        text,
        count=1,
    )
    text = re.sub(
        r'(<div style="background:var\(--grad-navy\)">\s*<div class="stats-band">)',
        r'<div style="background:var(--grad-navy)">\n  <div class="stats-band" style="background:transparent">',
        text,
    )

    for old, new in WAVE_REVERTS:
        text = text.replace(old, new)

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
    print(f"\nReverted {n} HTML files")


if __name__ == "__main__":
    main()
