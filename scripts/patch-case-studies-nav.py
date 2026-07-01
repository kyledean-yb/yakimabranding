#!/usr/bin/env python3
"""Add Case Studies to About dropdown and mobile nav across all HTML pages."""

import re
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from about_nav_snippet import about_nav_dropdown
from site_urls import page_href

CASE_STUDIES_CARD = re.compile(
    r'<a href="[^"]*case-studies[^"]*" class="dd-card[^"]*">.*?</a>\s*',
    re.DOTALL,
)

TAX_CARD = re.compile(
    r'(<a href="[^"]*washington-state-sales-tax[^"]*" class="dd-card[^"]*">)',
    re.DOTALL,
)

MOBILE_CASE_ROW = re.compile(
    r'<a href="[^"]*case-studies[^"]*" class="mobile-about-row"><strong>Case Studies</strong>.*?</a>\s*',
    re.DOTALL,
)

MOBILE_TAX_ROW = re.compile(
    r'(<a href="[^"]*washington-state-sales-tax[^"]*" class="mobile-about-row"><strong>WA Sales Tax Notice</strong>)',
    re.DOTALL,
)


def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth if depth else ""


def active_for(path: Path) -> Optional[str]:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "about.html":
        return "about"
    if rel == "washington-state-sales-tax.html":
        return "tax"
    if rel.startswith("about/case-studies/"):
        return "case-studies"
    return None


def case_studies_card_html(prefix: str, active: Optional[str]) -> str:
    cases_cls = " is-active" if active == "case-studies" else ""
    href = page_href("about/case-studies/index.html")
    return f"""              <a href="{href}" class="dd-card{cases_cls}">
                <div class="dd-ic" style="background:var(--wash-violet);color:var(--yb-violet)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="8" y1="7" x2="16" y2="7"/><line x1="8" y1="11" x2="14" y2="11"/></svg></div>
                <div><span class="dd-name">Case Studies</span><span class="dd-desc">Client results &amp; project highlights</span></div>
              </a>
              """


def mobile_case_row(prefix: str) -> str:
    href = page_href("about/case-studies/index.html")
    return f"""      <a href="{href}" class="mobile-about-row"><strong>Case Studies</strong><span>Client results &amp; project highlights</span></a>
      """


def patch_about_dropdown(text: str, prefix: str, active: Optional[str]) -> str:
    grid_match = re.search(
        r'(<div class="nav-dd-about-grid">)(.*?)(</div>\s*</div>\s*</div>\s*</div>)',
        text,
        re.DOTALL,
    )
    if not grid_match:
        return text
    grid_inner = grid_match.group(2)
    if CASE_STUDIES_CARD.search(grid_inner):
        grid_inner = CASE_STUDIES_CARD.sub("", grid_inner)
    if "Case Studies" in grid_inner:
        return text
    insert = case_studies_card_html(prefix, active)
    new_inner = TAX_CARD.sub(insert + r"\1", grid_inner, count=1)
    return text[: grid_match.start(2)] + new_inner + text[grid_match.end(2) :]


def patch_mobile_about(text: str, prefix: str) -> str:
    if "mobileAboutList" not in text:
        return text
    if MOBILE_CASE_ROW.search(text):
        text = MOBILE_CASE_ROW.sub("", text)
    if "Case Studies</strong>" in text and "mobileAboutList" in text:
        return text
    return MOBILE_TAX_ROW.sub(mobile_case_row(prefix) + r"\1", text, count=1)


def replace_full_dropdown(text: str, prefix: str, active: Optional[str]) -> str:
    pattern = re.compile(
        r'<div class="nav-dd nav-dd-about">.*?</div>\s*</div>\s*</div>',
        re.DOTALL,
    )
    if not pattern.search(text):
        return text
    return pattern.sub(about_nav_dropdown(prefix, active).rstrip(), text, count=1)


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    prefix = prefix_for(path)
    active = active_for(path)

    text = replace_full_dropdown(text, prefix, active)
    text = patch_about_dropdown(text, prefix, active)
    text = patch_mobile_about(text, prefix)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    count = 0
    for path in sorted(ROOT.rglob("*.html")):
        if "preview" in path.parts or "scraps" in path.parts:
            continue
        if patch(path):
            count += 1
            print(path.relative_to(ROOT))
    print(f"\nPatched {count} files")


if __name__ == "__main__":
    main()
