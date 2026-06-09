"""Shared SEO vs. PPC comparison + video section."""

from pathlib import Path

PARTIAL = Path(__file__).resolve().parents[1] / "partials" / "seo-vs-ppc-section.html"


def seo_vs_ppc_section_html(prefix: str = "../") -> str:
    return PARTIAL.read_text(encoding="utf-8").replace("__PREFIX__", prefix)
