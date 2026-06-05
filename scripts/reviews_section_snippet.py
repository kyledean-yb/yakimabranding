"""Scrolling Google reviews section (matches index.html)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTIAL = ROOT / "partials" / "reviews-scroll.html"


def reviews_section_html() -> str:
    return PARTIAL.read_text(encoding="utf-8")
