#!/usr/bin/env python3
"""Generate case study hub and detail pages."""

from __future__ import annotations

import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from case_studies_content import CASE_STUDIES
from schema_markup import seo_head_html
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_footer_snippet import site_footer_html
from site_nav_snippet import site_header_html
from site_staging_seo_snippet import STAGING_ROBOTS_META
from site_urls import page_href

OUT_DIR = ROOT / "about" / "case-studies"
ARROW = (
    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/>'
    '<polyline points="12 5 19 12 12 19"/></svg>'
)


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def render_paragraphs(paragraphs: list[str]) -> str:
    chunks = []
    for para in paragraphs:
        if "<code>" in para or "</" in para:
            chunks.append(f"<p>{para}</p>")
        else:
            chunks.append(f"<p>{esc(para)}</p>")
    return "\n".join(chunks)


def render_sections(sections: list[dict]) -> str:
    parts = []
    for section in sections:
        block = f"<section>\n<h2>{esc(section['heading'])}</h2>\n"
        block += render_paragraphs(section.get("paragraphs", []))
        for sub in section.get("subsections", []):
            block += f"\n<h3>{esc(sub['heading'])}</h3>\n"
            block += render_paragraphs(sub.get("paragraphs", []))
        block += "\n</section>"
        parts.append(block)
    return "\n".join(parts)


def render_meta_panel(meta: list[dict]) -> str:
    items = []
    for item in meta:
        cls = " cs-meta-item--result" if item.get("highlight") else ""
        value_html = ""
        if item.get("tags"):
            tags = "".join(f'<span class="cs-meta-tag">{esc(t)}</span>' for t in item["tags"])
            value_html = f'<span class="cs-meta-item__value"><span class="cs-meta-tags">{tags}</span></span>'
        else:
            value_html = f'<span class="cs-meta-item__value">{esc(item["value"])}</span>'
        items.append(
            f"""        <div class="cs-meta-item{cls}">
          <span class="cs-meta-item__label">{esc(item["label"])}</span>
          {value_html}
        </div>"""
        )
    return f"""    <div class="cs-meta-panel">
      <div class="cs-meta-panel__card">
        <span class="cs-meta-panel__label">Project snapshot</span>
        <div class="cs-meta-grid">
{chr(10).join(items)}
        </div>
      </div>
    </div>"""


def page_shell(
    prefix: str,
    title: str,
    description: str,
    body: str,
    rel_path: str,
    accent: str = "var(--yb-blue)",
    extra_class: str = "",
    extra_stylesheet: str = "",
) -> str:
    p = prefix
    header = site_header_html(p, about_active="case-studies").strip()
    footer = site_footer_html(p).strip()
    schema = seo_head_html(rel_path)
    body_class = f' class="cs-page{extra_class}"' if extra_class else ' class="cs-page"'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{STAGING_ROBOTS_META}
<link rel="icon" href="{p}favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{p}favicon.png">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="https://yakimabranding.com{page_href(rel_path)}">
<link rel="stylesheet" href="{p}colors_and_type.css">
<link rel="stylesheet" href="{p}site.css">
<link rel="stylesheet" href="{p}case-studies.css">
{extra_stylesheet}
<style>
.cs-page {{ --cs-accent: {accent}; }}
</style>
{schema}
</head>
<body{body_class}>
{ACCESSIBE_BODY_SCRIPT}

{header}

{body}

{footer}
<script src="{p}js/newsletter-popup.js" defer></script>
<script src="{p}js/chat-widget.js" defer></script>
<script src="{p}js/site.js" defer></script>
</body>
</html>
"""


def build_hub() -> None:
    prefix = "../../"
    cards = []
    for study in CASE_STUDIES:
        href = page_href(f"about/case-studies/{study['slug']}.html")
        cards.append(
            f"""      <a href="{href}" class="cs-hub-card" style="--cs-accent:{study['accent']}">
        <div class="cs-hub-card__accent"></div>
        <div class="cs-hub-card__body">
          <span class="cs-hub-card__tag">{esc(study['hubTag'])}</span>
          <h2>{esc(study['title'])}</h2>
          <p>{esc(study['hubExcerpt'])}</p>
          <span class="cs-hub-card__link">Read case study {ARROW}</span>
        </div>
      </a>"""
        )

    body = f"""
<main class="cs-hub-page">
  <section class="cs-hub-hero">
    <div class="cs-hub-hero-mesh" aria-hidden="true"></div>
    <div class="hero-logo-overlay hero-logo-overlay--center" aria-hidden="true">
      <img src="{prefix}assets/yb-logo-white.png" alt="">
    </div>
    <div class="container cs-hub-hero-inner">
      <span class="eyebrow">About YB Marketing</span>
      <h1>Case Studies</h1>
      <p>Real engagements across accessibility, WordPress security, paid media, and enterprise-scale web — anonymised where required, specific where it matters.</p>
    </div>
  </section>
  <div class="cs-hub-wave" aria-hidden="true"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z"/></svg></div>
  <section class="cs-hub-listing">
    <div class="container">
      <div class="cs-hub-grid">
{chr(10).join(cards)}
      </div>
    </div>
  </section>
  <div class="wave-div wave-from-soft wave-to-footer" aria-hidden="true"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z"/></svg></div>
</main>
"""
    rel = "about/case-studies/index.html"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "index.html").write_text(
        page_shell(
            prefix,
            "Case Studies — YB Marketing",
            "YB Marketing case studies — enterprise accessibility remediation, WordPress security, and portfolio-scale digital work.",
            body,
            rel,
            extra_class=" cs-hub-page",
            extra_stylesheet=f'<link rel="stylesheet" href="{prefix}blog.css">',
        ),
        encoding="utf-8",
    )
    print(f"  · {rel}")


def build_detail(study: dict) -> None:
    prefix = "../../../"
    slug = study["slug"]
    rel = f"about/case-studies/{slug}.html"
    href = page_href(rel)
    hub_href = page_href("about/case-studies/index.html")

    summary_html = render_paragraphs(study["summary"])
    sections_html = render_sections(study["sections"])
    meta_html = render_meta_panel(study["meta"])

    body = f"""
<main>
  <section class="cs-hero">
    <div class="cs-hero-mesh" aria-hidden="true"></div>
    <div class="container cs-hero-inner">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a><span>/</span>
        <a href="/about">About</a><span>/</span>
        <a href="{hub_href}">Case Studies</a><span>/</span>
        <span>Case Study</span>
      </nav>
      <span class="cs-hero-tag">{esc(study['hubTag'])}</span>
      <h1>{esc(study['title'])}</h1>
    </div>
  </section>

  <div class="container cs-article">
{meta_html}

    <div class="cs-summary">
      <span class="cs-summary__eyebrow">Summary</span>
      {summary_html}
    </div>

    <div class="cs-prose">
      {sections_html}

      <div class="cs-cta-band">
        <p>{study['closingCta']}</p>
      </div>
    </div>
  </div>
  <div class="cs-article-footer-wave" aria-hidden="true"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z"/></svg></div>
</main>
"""
    (OUT_DIR / f"{slug}.html").write_text(
        page_shell(
            prefix,
            study.get("metaTitle", f"{study['title']} — YB Marketing Case Study"),
            study["metaDescription"],
            body,
            rel,
            accent=study["accent"],
        ),
        encoding="utf-8",
    )
    print(f"  · {rel}")


def main() -> None:
    print("Building case studies…")
    build_hub()
    for study in CASE_STUDIES:
        build_detail(study)
    print("Done.")


if __name__ == "__main__":
    main()
