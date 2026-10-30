#!/usr/bin/env python3
"""Insert a featured case studies section above Insights on the home page (EN + ES).

Idempotent: replaces any existing block between the home-cases markers.
Re-run after editing case_studies_content.py or rebuilding index.html.
"""
from __future__ import annotations

import json
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from case_studies_content import CASE_STUDIES  # noqa: E402

FEATURED = [
    ("local-refrigeration-services-seo-growth", 0),
    ("roofing-contractor-inbound-marketing", 3),
    ("local-electrical-contractor-seo-growth", 0),
]

COPY = {
    "en": {
        "eyebrow": "Case Studies",
        "heading": "Results We've Delivered for Clients",
        "lead": "A few recent wins from SEO, Google Ads and website projects, with the numbers to back them up.",
        "all": "View All Case Studies",
        "read": "Read case study",
        "base": "/about/case-studies",
    },
    "es": {
        "eyebrow": "Casos de éxito",
        "heading": "Resultados que hemos logrado para nuestros clientes",
        "lead": "Algunos logros recientes en SEO, Google Ads y proyectos web, con los números que los respaldan.",
        "all": "Ver todos los casos de éxito",
        "read": "Leer caso de éxito",
        "base": "/es/about/case-studies",
    },
}

START, END = "<!-- home-cases:start -->", "<!-- home-cases:end -->"
ANCHOR = "<!-- BLOG / INSIGHTS -->"
ARROW = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" '
         'stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/>'
         '<polyline points="12 5 19 12 12 19"/></svg>')

CSS = """<style>
.home-cases{padding:88px 0 24px}
.home-cases .blog-top{margin-bottom:36px}
.hc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.hc-card{position:relative;display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:28px 26px 24px;box-shadow:var(--sh-sm);text-decoration:none;color:inherit;overflow:hidden;transition:transform .2s var(--ease,ease),box-shadow .2s var(--ease,ease)}
.hc-card::before{content:"";position:absolute;inset:0 0 auto;height:4px;background:var(--hc-accent)}
.hc-card:hover{transform:translateY(-4px);box-shadow:var(--sh-md,0 12px 32px rgba(15,30,60,.12))}
.hc-tag{align-self:flex-start;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--hc-accent);background:color-mix(in srgb,var(--hc-accent) 10%,#fff);border-radius:var(--r-pill);padding:5px 12px}
.hc-stat{margin:22px 0 2px;font-family:var(--font-display);font-weight:800;font-size:clamp(2.4rem,4vw,3rem);line-height:1;color:var(--hc-accent)}
.hc-stat-label{font-size:13px;font-weight:600;color:var(--fg3)}
.hc-card h3{margin:18px 0 20px;font-size:17px;line-height:1.4;color:var(--ink);flex:1}
.hc-link{display:inline-flex;align-items:center;gap:6px;font-weight:700;font-size:14px;color:var(--yb-blue)}
@media(max-width:900px){.hc-grid{grid-template-columns:1fr;max-width:560px;margin:0 auto}}
</style>"""


def load_es() -> dict[str, str]:
    return json.loads((ROOT / "data" / "i18n" / "es-cache.json").read_text(encoding="utf-8"))


def tr(text: str, lang: str, es: dict[str, str]) -> str:
    if lang != "es":
        return text
    if text not in es:
        print(f"  missing es translation: {text}")
    return es.get(text, text)


def block(lang: str, es: dict[str, str]) -> str:
    c = COPY[lang]
    studies = {s["slug"]: s for s in CASE_STUDIES}
    cards = []
    for slug, stat_i in FEATURED:
        s = studies[slug]
        stat = s["heroStats"][stat_i]
        cards.append(
            f'      <a class="hc-card" href="{c["base"]}/{slug}" style="--hc-accent:{s["accent"]}">\n'
            f'        <span class="hc-tag">{escape(tr(s["hubTag"], lang, es))}</span>\n'
            f'        <span class="hc-stat">{escape(stat["value"])}</span>\n'
            f'        <span class="hc-stat-label">{escape(tr(stat["label"], lang, es))}</span>\n'
            f'        <h3>{escape(tr(s["title"], lang, es))}</h3>\n'
            f'        <span class="hc-link">{escape(c["read"])} {ARROW}</span>\n'
            f'      </a>'
        )
    return f"""{START}
{CSS}
<section class="home-cases" id="case-studies">
  <div class="container">
    <div class="blog-top">
      <div style="max-width:560px">
        <span class="eyebrow" style="color:var(--yb-coral)">{escape(c["eyebrow"])}</span>
        <h2 style="margin:14px 0 12px">{escape(c["heading"])}</h2>
        <p class="yb-lead">{escape(c["lead"])}</p>
      </div>
      <a href="{c["base"]}" class="btn btn-ghost">{escape(c["all"])}
        {ARROW}
      </a>
    </div>
    <div class="hc-grid">
{chr(10).join(cards)}
    </div>
  </div>
</section>
{END}
"""


def process(path: Path, lang: str, es: dict[str, str]) -> None:
    html = path.read_text(encoding="utf-8")
    html = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", html, flags=re.S)
    pos = html.find(ANCHOR)
    if pos == -1:
        pos = html.find('<section id="insights">')
    if pos == -1:
        print(f"  no insights anchor: {path.relative_to(ROOT)}")
        return
    path.write_text(html[:pos] + block(lang, es) + html[pos:], encoding="utf-8")
    print(f"  · {path.relative_to(ROOT)}")


def main() -> None:
    es = load_es()
    process(ROOT / "index.html", "en", es)
    process(ROOT / "es" / "index.html", "es", es)


if __name__ == "__main__":
    main()
