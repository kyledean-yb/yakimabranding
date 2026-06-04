#!/usr/bin/env python3
"""Patch insights + post pages with consistent section waves (no API)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

WAVE_HERO_TO_SOFT = (
    '<div class="wave-div wave-from-navy wave-to-soft">'
    '<svg viewBox="0 0 1440 70" preserveAspectRatio="none">'
    '<path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z"/></svg></div>'
)
WAVE_HERO_TO_WHITE = (
    '<div class="wave-div wave-from-navy wave-to-white">'
    '<svg viewBox="0 0 1440 70" preserveAspectRatio="none">'
    '<path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z"/></svg></div>'
)
WAVE_FOOTER_FROM_SOFT = (
    '<div class="wave-div wave-to-footer wave-from-soft">'
    '<svg viewBox="0 0 1440 70" preserveAspectRatio="none">'
    '<path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z"/></svg></div>\n'
)
WAVE_FOOTER_FROM_WHITE = (
    '<div class="wave-div wave-to-footer wave-from-white">'
    '<svg viewBox="0 0 1440 70" preserveAspectRatio="none">'
    '<path d="M0,70 C360,0 1080,0 1440,70 L1440,70 L0,70 Z"/></svg></div>\n'
)

HERO_WAVE_RE = re.compile(
    r'<div class="wave-div"[^>]*>.*?</div>\s*',
    re.DOTALL,
)
FOOTER_INSERT_RE = re.compile(r"\n<footer class=\"footer\">")


def patch_insights():
    path = ROOT / "insights.html"
    text = path.read_text(encoding="utf-8")
    text = HERO_WAVE_RE.sub(WAVE_HERO_TO_SOFT + "\n", text, count=1)
    if "wave-to-footer" not in text:
        text = FOOTER_INSERT_RE.sub("\n" + WAVE_FOOTER_FROM_SOFT + "<footer class=\"footer\">", text, count=1)
    path.write_text(text, encoding="utf-8")
    print("patched insights.html")


def patch_posts():
    for path in (ROOT / "blog" / "posts").glob("*.html"):
        text = path.read_text(encoding="utf-8")
        text = HERO_WAVE_RE.sub(WAVE_HERO_TO_WHITE + "\n", text, count=1)
        text = text.replace(
            '<section style="background:#fff;padding:48px 0 88px">',
            '<section class="blog-article">',
        )
        if "wave-to-footer" not in text:
            text = FOOTER_INSERT_RE.sub(
                "\n" + WAVE_FOOTER_FROM_WHITE + '<footer class="footer">',
                text,
                count=1,
            )
        path.write_text(text, encoding="utf-8")
        print(f"patched {path.name}")


if __name__ == "__main__":
    patch_insights()
    patch_posts()
