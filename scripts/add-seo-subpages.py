#!/usr/bin/env python3
"""Build the SEO subpages (/seo/local-seo, /seo/ai-search, /seo/technical-seo, /seo/website-migration)."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from schema_markup import SITE, breadcrumb, faq_schema, global_schemas, render_schema_head, service_schema, webpage_schema
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_footer_snippet import site_footer_html
from site_lead_form_snippet import lead_form_html
from site_nav_snippet import site_header_html
from site_staging_seo_snippet import STAGING_ROBOTS_META
from site_tracking_snippet import ATTRIBUTER_FOOTER_BLOCK, GTM_BODY_NOSCRIPT_BLOCK, TRACKING_HEAD_BLOCK

_spec = importlib.util.spec_from_file_location("ai_pages", ROOT / "scripts" / "add-ai-services-pages.py")
_ai = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ai)
BASE_CSS = _ai.PAGE_CSS
SCHEDULE = _ai.SCHEDULE

EXTRA_CSS = """
.hero-proof{display:inline-flex;align-items:center;gap:10px;margin:0 0 28px;padding:10px 16px;border-radius:var(--r-pill);background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);color:#fff;font-size:14px;font-weight:600}
.text-link{font-weight:700;color:var(--yb-blue)}
.prose{max-width:760px;margin:0 auto}
.prose p{color:var(--fg2);font-size:16px;line-height:1.75;margin:0 0 16px}
.prose p:first-child{font-size:18px;color:var(--ink);line-height:1.7}
.prose p:last-child{margin-bottom:0}
.sub-split{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:56px;align-items:center}
.sub-split h2{margin:14px 0 20px}
.sub-split .prose{max-width:none;margin:0}
.sub-aside{position:relative;overflow:hidden;border-radius:var(--r-xl);padding:34px 32px;background:var(--grad-navy);color:#fff;box-shadow:0 24px 60px rgba(22,32,58,.22)}
.sub-aside::before{content:'';position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.7;pointer-events:none}
.sub-aside::after{content:'';position:absolute;width:220px;height:220px;right:-70px;top:-70px;border-radius:50%;background:radial-gradient(circle,rgba(43,196,240,.35),transparent 70%);pointer-events:none}
.sub-aside > *{position:relative;z-index:1}
.sub-aside-title{display:block;font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--yb-cyan);margin-bottom:18px}
.sub-aside ul{list-style:none;margin:0;padding:0;display:grid;gap:12px}
.sub-aside li{display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:var(--r-md);background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);font-weight:600;font-size:15px}
.sub-aside li svg{width:18px;height:18px;flex:none;color:var(--yb-cyan)}
.sub-cards{display:flex;flex-wrap:wrap;justify-content:center;gap:20px}
.sub-card{flex:0 1 calc((100% - 40px)/3);position:relative;overflow:hidden;background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:26px 24px;box-shadow:var(--sh-sm);transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease}
.sub-card::before{content:'';position:absolute;left:0;right:0;top:0;height:3px;background:var(--grad-brand);transform:scaleX(0);transform-origin:left;transition:transform .3s ease}
.sub-card:hover{transform:translateY(-4px);box-shadow:var(--sh-md);border-color:transparent}
.sub-card:hover::before{transform:scaleX(1)}
.sub-card-ic{width:46px;height:46px;border-radius:var(--r-md);display:flex;align-items:center;justify-content:center;margin-bottom:16px}
.sub-card-ic svg{width:22px;height:22px}
.sub-card h3{font-family:var(--font-display);font-weight:700;font-size:17px;color:var(--ink);margin:0 0 8px}
.sub-card p{font-size:14.5px;color:var(--fg2);line-height:1.65;margin:0}
.sec-navy{position:relative;overflow:hidden;background:var(--grad-navy)}
.sec-navy::before{content:'';position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.6;pointer-events:none}
.sec-navy > .container{position:relative;z-index:1}
.sec-navy h2{color:#fff}
.sec-navy .prose p,.sec-navy p{color:var(--fg2-on-dark)}
.results-split{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:56px;align-items:center}
.results-split h2{margin:14px 0 20px}
.results-split p{font-size:16px;line-height:1.75;margin:0 0 16px}
.results-stats{display:grid;gap:16px}
.results-stat{display:flex;align-items:center;gap:20px;padding:22px 24px;border-radius:var(--r-lg);background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);backdrop-filter:blur(6px)}
.results-stat-big{font-family:var(--font-display);font-weight:800;font-size:clamp(2.1rem,3.4vw,2.8rem);line-height:1;min-width:180px;background:linear-gradient(135deg,#7fb2ff 0%,#2bc4f0 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.results-stat-label{font-size:15px;font-weight:600;color:#fff;line-height:1.4}
.results-link{display:inline-flex;align-items:center;gap:8px;margin-top:8px}
.timeline{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(var(--steps,5),minmax(0,1fr));gap:18px;counter-reset:step}
.timeline li{position:relative;background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:26px 22px 24px;box-shadow:var(--sh-sm)}
.timeline-n{display:flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:50%;background:var(--grad-brand);color:#fff;font-family:var(--font-display);font-weight:800;font-size:18px;margin-bottom:16px;box-shadow:0 8px 20px rgba(63,111,214,.3)}
.timeline li:not(:last-child)::after{content:'';position:absolute;top:47px;left:calc(22px + 44px + 10px);right:-18px;height:2px;background:linear-gradient(90deg,rgba(43,196,240,.6),rgba(43,196,240,0))}
.timeline[style*="--steps:3"] li:nth-child(3n)::after{display:none}
.timeline h3{font-family:var(--font-display);font-weight:700;font-size:16.5px;color:var(--ink);margin:0 0 8px}
.timeline p{font-size:14px;color:var(--fg2);line-height:1.6;margin:0}
.sec-navy .timeline li{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.12);box-shadow:none}
.sec-navy .timeline h3{color:#fff}
.sec-navy .timeline p{color:var(--fg2-on-dark)}
.sec-navy .eyebrow{color:var(--yb-cyan) !important}
.seo-sub-related{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:28px}
.seo-sub-related a{padding:9px 16px;border-radius:var(--r-pill);border:1px solid var(--line);background:#fff;font-size:14px;font-weight:600;color:var(--ink)}
.seo-sub-related a:hover{border-color:var(--yb-cyan);color:var(--yb-blue)}
@media(max-width:1100px){.timeline{grid-template-columns:repeat(min(var(--steps,5),3),minmax(0,1fr))}.timeline li::after{display:none}}
@media(max-width:900px){.sub-split,.results-split{grid-template-columns:1fr;gap:36px}.sub-card{flex-basis:calc((100% - 20px)/2)}.timeline{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.sub-card{flex-basis:100%}.timeline{grid-template-columns:1fr}.results-stat{flex-direction:column;align-items:flex-start;gap:8px}.results-stat-big{min-width:0}}
"""

ARROW = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'


SUBPAGES = [
    ("local-seo", "Local SEO"),
    ("ai-search", "AI Search"),
    ("technical-seo", "Technical SEO"),
    ("website-migration", "Website Migrations"),
]


def hero_visual() -> str:
    text = (ROOT / "seo" / "index.html").read_text(encoding="utf-8")
    m = re.search(r'(    <div class="svc-hero-visual">.*?)\s*</div>\s*</section>', text, re.S)
    if not m:
        raise SystemExit("could not find hero visual on seo/index.html")
    return m.group(1)


ICON_PATHS = {
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="13" y2="17"/>',
    "map": '<polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/>',
    "list": '<line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><circle cx="4" cy="6" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="18" r="1"/>',
    "star": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    "chart": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    "search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "copy": '<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
    "eye": '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
    "info": '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>',
    "message": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "activity": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
    "layout": '<rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/>',
    "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "merge": '<circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M6 21V9a9 9 0 0 0 9 9"/>',
    "shuffle": '<polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/><line x1="4" y1="4" x2="9" y2="9"/>',
    "spark": '<path d="M12 3l1.9 5.8L20 10l-6.1 1.2L12 17l-1.9-5.8L4 10l6.1-1.2z"/>',
}
ICON_RULES = [
    ("business profile", "pin"), ("service page", "file"), ("location", "map"), ("listing", "list"),
    ("review", "star"), ("report", "chart"), ("index", "search"), ("slow", "zap"), ("duplicate", "copy"),
    ("broken", "link"), ("structured", "code"), ("difficult to access", "eye"), ("business information", "info"),
    ("answers real questions", "message"), ("technical seo", "code"), ("monitoring", "activity"),
    ("redesign", "layout"), ("platform", "layers"), ("domain", "globe"), ("consolidation", "merge"), ("url", "shuffle"),
]
CARD_TONES = [
    ("var(--wash-cyan)", "var(--yb-cyan)"), ("var(--wash-blue)", "var(--yb-blue)"), ("var(--wash-violet)", "var(--yb-violet)"),
    ("var(--wash-mint)", "#159468"), ("var(--wash-amber)", "#c77f12"), ("var(--wash-coral)", "var(--yb-coral)"),
]
BG_HEX = {"#fff": "#ffffff", "#ffffff": "#ffffff", "var(--bg-soft)": "#F6F8FC", "navy": "#1B2A4A"}


def icon_svg(name: str) -> str:
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON_PATHS[name]}</svg>'


def card_icon(title: str) -> str:
    t = title.lower()
    for key, name in ICON_RULES:
        if key in t:
            return name
    return "spark"


def section_open(bg: str, extra_attrs: str = "", cls: str = "") -> str:
    hexbg = BG_HEX[bg]
    if bg == "navy":
        return f'<section class="sec-navy{(" " + cls) if cls else ""}" data-bg="{hexbg}"{extra_attrs}>'
    cls_attr = f' class="{cls}"' if cls else ""
    return f'<section{cls_attr} style="background:{bg}" data-bg="{hexbg}"{extra_attrs}>'


def wave(top: str, bottom: str) -> str:
    return (f'<div class="wave-div" style="background:{top}"><svg viewBox="0 0 1440 70" preserveAspectRatio="none">'
            f'<path d="M0,70 C480,0 960,0 1440,70 L1440,70 L0,70 Z" fill="{bottom}"/></svg></div>')


def auto_waves(body: str, start: str = "#ffffff", end: str = "#ffffff") -> str:
    out, prev, pos = [], start, 0
    for m in re.finditer(r'<section[^>]*data-bg="(#[0-9A-Fa-f]{6})"', body):
        out.append(body[pos:m.start()])
        if m.group(1).lower() != prev.lower():
            out.append(wave(prev, m.group(1)) + "\n")
        prev, pos = m.group(1), m.start()
    out.append(body[pos:])
    if prev.lower() != end.lower():
        out.append("\n" + wave(prev, end))
    return "".join(out)


def section_head(eyebrow: str, heading: str, intro: str = "", align: str = "center") -> str:
    intro_html = f'\n      <p style="color:var(--fg2);font-size:16px;line-height:1.75">{intro}</p>' if intro else ""
    if align == "left":
        return f"""      <span class="eyebrow" style="color:#2BC4F0">{eyebrow}</span>
      <h2>{heading}</h2>"""
    return f"""    <div style="text-align:center;max-width:720px;margin:0 auto 44px">
      <span class="eyebrow" style="color:#2BC4F0">{eyebrow}</span>
      <h2 style="margin:14px 0 {16 if intro else 0}px">{heading}</h2>{intro_html}
    </div>"""


def prose_section(bg: str, eyebrow: str, heading: str, paragraphs: list[str], extra: str = "", aside: tuple[str, list[str]] | None = None) -> str:
    paras = "\n".join(f"      <p>{p}</p>" for p in paragraphs)
    if aside:
        title, items = aside
        lis = "".join(f"<li>{CHECK}<span>{i}</span></li>" for i in items)
        return f"""{section_open(bg)}
  <div class="container sub-split">
    <div>
{section_head(eyebrow, heading, align="left")}
    <div class="prose">
{paras}
{extra}
    </div>
    </div>
    <aside class="sub-aside"><span class="sub-aside-title">{title}</span><ul>{lis}</ul></aside>
  </div>
</section>"""
    return f"""{section_open(bg)}
  <div class="container">
{section_head(eyebrow, heading)}
    <div class="prose">
{paras}
{extra}
    </div>
  </div>
</section>"""


def cards_section(bg: str, eyebrow: str, heading: str, cards: list[tuple[str, str]], intro: str = "") -> str:
    items = []
    for i, (t, d) in enumerate(cards):
        wash, color = CARD_TONES[i % len(CARD_TONES)]
        items.append(
            f'      <div class="sub-card"><div class="sub-card-ic" style="background:{wash};color:{color}">{icon_svg(card_icon(t))}</div>'
            f'<h3>{t}</h3><p>{d}</p></div>'
        )
    return f"""{section_open(bg)}
  <div class="container">
{section_head(eyebrow, heading, intro)}
    <div class="sub-cards">
""" + "\n".join(items) + """
    </div>
  </div>
</section>"""


def results_section(bg: str, heading: str, paragraphs: list[str], stats: list[tuple[str, str]], link: tuple[str, str] | None, after: list[str] | None = None) -> str:
    paras = "\n".join(f"      <p>{p}</p>" for p in paragraphs + (after or []))
    stat_html = "".join(
        f'<div class="results-stat"><span class="results-stat-big">{big}</span><span class="results-stat-label">{label}</span></div>'
        for big, label in stats
    )
    link_html = f'      <a class="btn btn-grad results-link" href="{link[1]}">{link[0]} {ARROW}</a>' if link else ""
    return f"""{section_open(bg)}
  <div class="container results-split">
    <div>
{section_head("Results", heading, align="left")}
{paras}
{link_html}
    </div>
    <div class="results-stats">{stat_html}</div>
  </div>
</section>"""


def steps_section(bg: str, steps: list[tuple[str, str]], heading: str = "How we work") -> str:
    items = "\n".join(
        f'      <li><span class="timeline-n">{i}</span><h3>{t}</h3><p>{d}</p></li>'
        for i, (t, d) in enumerate(steps, 1)
    )
    cols = len(steps) if len(steps) <= 5 else 3
    return f"""{section_open(bg, ' id="how-it-works"')}
  <div class="container">
{section_head("How It Works", heading)}
    <ol class="timeline" style="--steps:{cols}">
{items}
    </ol>
  </div>
</section>"""


def faq_section(bg: str, faqs: list[tuple[str, str]], slug: str) -> str:
    items = "".join(
        f'<div class="faq-item"><button class="faq-q" type="button" style="--faq-ac:#2BC4F0">{q}'
        f'<span class="faq-icon">+</span></button><div class="faq-a"><div class="faq-a-inner">{a}</div></div></div>'
        for q, a in faqs
    )
    related = "".join(
        f'<a href="/seo/{s}">{name}</a>' for s, name in SUBPAGES if s != slug
    )
    return f"""{section_open(bg, ' id="faq"', 'faq-visibility-section')}
  <div class="container">
{section_head("FAQ", "Frequently Asked Questions")}
    <div class="faq-visibility-grid" id="visibility-score">
    <div class="faq-visibility-faqs">
    <div class="faq-list" style="border-top:1px solid var(--line)">
{items}
    </div>
    <div class="seo-sub-related"><a href="/seo">All SEO Services</a>{related}</div>
    </div>
    <aside class="faq-visibility-widget">
      <div class="visibility-widget-card">
        <div class="visibility-widget-card__head">
          <span class="eyebrow" style="color:#2BC4F0">Free SEO Tool</span>
          <h3>Run Your Visibility Score</h3>
          <p>See how your business shows up in local search. We&rsquo;ll email your results, no obligation.</p>
        </div>
        <div class="visibility-widget-card__body">
          <div class="visibility-widget-wrap">
            <p class="visibility-widget-loading" aria-hidden="true">Loading visibility tool&hellip;</p>
            <widget-app style_key="wk_ea5bc5a588df89d69feae137"></widget-app>
          </div>
        </div>
      </div>
    </aside>
    </div>
  </div>
</section>"""


def build_page(page: dict) -> str:
    slug = page["slug"]
    rel = f"seo/{slug}"
    url = f"{SITE}/{rel}"
    prefix = "../"
    header = site_header_html(prefix, current_path=f"/{rel}").strip()
    footer = site_footer_html(prefix, current_path=f"/{rel}").strip()
    form = lead_form_html(page["form_source"], redirect="/services/thank-you-seo", default_interest="seo")

    faq_plain = [{"q": q, "a": re.sub(r"<[^>]+>", "", a)} for q, a in page["faqs"]]
    schemas = global_schemas() + [
        service_schema(page["service_name"], page["service_type"], url, page["meta"]),
        breadcrumb([(1, "Home", SITE), (2, "SEO", f"{SITE}/seo"), (3, page["service_name"], url)]),
        webpage_schema(page["title"], url, page["meta"]),
        faq_schema(faq_plain),
    ]

    proof = f'      <p class="hero-proof">{page["proof"]}</p>\n' if page.get("proof") else ""
    sec_btn_href, sec_btn_label = page["hero_secondary"]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="../favicon.png" type="image/png">
<link rel="apple-touch-icon" href="../favicon.png">
{STAGING_ROBOTS_META}
<title>{escape(page["title"], quote=False)}</title>
<meta name="description" content="{escape(page["meta"])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Yakima Branding">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{escape(page["title"])}">
<meta property="og:description" content="{escape(page["meta"])}">
<link rel="stylesheet" href="../colors_and_type.css">
<link rel="stylesheet" href="../insights.css">
<link rel="stylesheet" href="../lead-form.css">
<style>{BASE_CSS}{EXTRA_CSS}</style>
<link rel="stylesheet" href="../site.css">
<link rel="stylesheet" href="https://widget.advicelocal.com/bundle.css">
<link rel="stylesheet" href="../visibility-widget.css">
{render_schema_head(schemas)}
{TRACKING_HEAD_BLOCK}
</head>
<body>
{GTM_BODY_NOSCRIPT_BLOCK}
{ACCESSIBE_BODY_SCRIPT}
{header}

<section class="svc-hero">
  <div class="svc-hero-mesh"></div>
  <div class="hero-logo-overlay hero-logo-overlay--left" aria-hidden="true">
    <img src="../assets/yb-logo-white.png" alt="">
  </div>
  <div class="container svc-hero-inner">
    <div class="svc-hero-text">
      <span class="eyebrow" style="color:var(--yb-cyan)">{page["eyebrow"]}</span>
      <h1>{page["h1"]}</h1>
      <p class="hero-lead">{page["lead"]}</p>
{proof}      <div class="svc-hero-actions">
        <a href="#contact" class="btn btn-grad btn-lg">{page["hero_primary"]} {ARROW}</a>
        <a href="{sec_btn_href}" class="btn btn-ghost-white">{sec_btn_label}</a>
      </div>
    </div>
{hero_visual()}
  </div>
</section>

<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 80" preserveAspectRatio="none" style="height:80px"><path d="M0,0 C360,80 1080,80 1440,0 L1440,80 L0,80 Z" fill="#ffffff"/></svg></div>

{auto_waves(page["body"])}

<section style="background:#fff" id="contact">
  <div class="container">
    <div style="text-align:center;max-width:720px;margin:0 auto 40px">
      <span class="eyebrow" style="color:#2BC4F0">Get Started</span>
      <h2 style="margin:14px 0 12px">Book a Meeting or Send Us a Message</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">Grab a 30 minute intro call, or send a note and we'll get back to you.</p>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start" class="why-main-grid">
      <div>
        <p style="color:var(--fg2);font-size:16px;line-height:1.75;margin-bottom:24px">An introduction meeting to learn more about your business, your goals, and how we can help you grow. No commitment required.</p>
{SCHEDULE}
      </div>
      <div style="background:#fff;border-radius:var(--r-xl);padding:28px;box-shadow:var(--sh-sm);border:1px solid var(--line)">
        <h3 style="font-size:20px;margin:0 0 20px">Send Us a Message</h3>
{form}
      </div>
    </div>
  </div>
</section>

<div class="wave-div" style="background:#ffffff"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div>
<div style="background:var(--grad-navy)">
<div class="svc-cta">
  <div class="svc-cta-mesh"></div>
  <div class="container svc-cta-inner">
    <span class="eyebrow" style="color:var(--yb-cyan)">{page["eyebrow"]}</span>
    <h2 style="margin:14px 0 14px;color:#fff;font-size:clamp(1.8rem,2.6vw,2.4rem)">{page["cta_heading"]}</h2>
    <p style="color:var(--fg2-on-dark);font-size:16px;margin-bottom:32px">{page["cta_body"]}</p>
    <div class="svc-cta-btns">
      <a href="#contact" class="btn btn-grad btn-lg">{page["cta_primary"]}</a>
      <a href="tel:5099019735" class="btn btn-ghost-white btn-lg">509-901-9735</a>
    </div>
  </div>
</div>
</div>

{footer}

<script src="../js/newsletter-popup.js" defer></script>
<script src="../js/chat-widget.js" defer></script>
<script src="../js/hero-orbit.js" defer></script>
<script src="../js/site.js?v=2" defer></script>
<script src="../js/lead-form-config.js" defer></script>
<script src="../js/lead-form.js" defer></script>
<script src="https://widget.advicelocal.com/bundle.js" defer></script>
<script src="../js/visibility-widget.js" defer></script>
<script>
document.getElementById('hamburger')?.addEventListener('click', function () {{
  document.getElementById('mobileMenu')?.classList.toggle('open');
}});
document.querySelectorAll('.faq-q').forEach(function (btn) {{
  btn.addEventListener('click', function () {{
    var item = btn.closest('.faq-item');
    var panel = item.querySelector('.faq-a');
    var open = btn.classList.contains('active');
    document.querySelectorAll('.faq-q.active').forEach(function (b) {{
      b.classList.remove('active');
      b.closest('.faq-item').querySelector('.faq-a').style.maxHeight = '0';
    }});
    if (!open) {{
      btn.classList.add('active');
      panel.style.maxHeight = panel.scrollHeight + 'px';
    }}
  }});
}});
</script>
{ATTRIBUTER_FOOTER_BLOCK}
</body>
</html>
"""


# ---------------------------------------------------------------- page copy

def local_seo() -> dict:
    faqs = [
        ("How is local SEO different from traditional SEO?",
         "Traditional SEO helps a website appear for relevant searches more broadly. Local SEO focuses on people searching in a specific geographic area, including Google Maps and searches with local intent."),
        ("Do I need a physical address to appear on Google Maps?",
         "A Google Business Profile generally requires a legitimate business location that meets Google's eligibility rules. If you visit customers rather than serving them at your address, you may be able to hide the address and list your service area instead."),
        ("Why don't I appear in every city I serve?",
         "Distance is an important factor in Google's local map results. You may have a harder time appearing on the map in areas farther from your business location. Well developed location pages can still help your website appear in the regular search results for those areas."),
        ("How long does local SEO take?",
         "It depends on your current website, competition, and service area. Some profile and listing improvements may have an effect within weeks, while new service and location pages often take several months to gain traction."),
        ("Can you help us get more reviews?",
         "Yes. We can help you build a process for asking customers to leave honest reviews and responding to the feedback you receive. We don't purchase or fabricate reviews."),
    ]
    body = "\n\n".join([
        prose_section("#fff", "Local SEO", "What is local SEO?", [
            "Local SEO helps your business appear when people search for services in a particular city or area. That includes Google Maps, your Google Business Profile, and the regular search results for the services you offer.",
            "A big part of the work is making sure Google has accurate information about your business. But that isn't enough on its own. Your website also needs useful pages about your services, clear information about where you work, and a consistent presence across other websites and directories.",
            "Your location will always influence where you appear on Google Maps. We focus on the other factors you can improve, from your business profile to the content on your website.",
        ], aside=("Where customers find you", ["Google Maps", "Your Google Business Profile", "Regular search results", "Directories like Yelp, Bing, and Apple Maps"])),
        results_section("navy", "Helping an electrical contractor reach more customers through search", [
            "A residential and commercial electrical contractor serving the Greater Bay Area had an established business and a solid reputation. Most of its new work, however, came through paid advertising and subcontractor referrals. The website wasn't bringing in much traffic from people searching for electrical services.",
            "We expanded the site's service and location content, improved the company's Google Business Profile and directory listings, and monitored rankings and leads as the campaign progressed.",
        ], [
            ("+112%", "organic search traffic year over year"),
            ("+204%", "keywords ranking on page one"),
            ("+366%", "search impressions at peak"),
        ], ("Read the Full Case Study", "/about/case-studies/local-electrical-contractor-seo-growth")),
        cards_section("var(--bg-soft)", "What's Included", "Our local SEO services", [
            ("Google Business Profile optimization", "We review your categories, services, business details, photos, and other profile information to make sure customers can find accurate, useful information about your company."),
            ("Service page development", "Customers search for specific services, not just broad business categories. We create and improve pages around the work you want to attract, whether that's electrical panel upgrades, EV charger installation, or another service."),
            ("Location pages", "If you serve several cities or communities, your website should make that clear. We develop location pages that reflect the services you provide in each area, rather than repeating the same copy with a different city name."),
            ("Business listings", "We review your information across relevant directories, including Yelp, Bing, Apple Maps, and industry specific websites. Inconsistent contact details can confuse customers and search engines alike."),
            ("Review strategy", "Customer reviews help people decide whom to contact. We can help you establish a straightforward process for requesting genuine reviews and responding to customer feedback."),
            ("Rankings and lead reporting", "We monitor local search visibility and report on the calls, form submissions, and other leads your website generates, using the tracking available for your business."),
        ]),
        steps_section("#fff", [
            ("Review your current visibility", "We look at where your business appears in local results, how your Google Business Profile is set up, and how your website compares with local competitors."),
            ("Address the basics", "We correct business information, improve your profile, and resolve listing issues that may be affecting visibility."),
            ("Improve your website", "We prioritize the service and location pages most relevant to your business goals."),
            ("Strengthen your local presence", "We continue working on reviews, relevant listings, and opportunities for local mentions and links."),
            ("Measure results", "Each month, we review rankings and available lead data to decide where to focus next."),
        ]),
        faq_section("var(--bg-soft)", faqs, "local-seo"),
    ])
    return dict(
        slug="local-seo",
        title="Local SEO Services for Contractors & Service Businesses | YB Marketing",
        meta="Help customers in your service area find your business on Google Maps and in local search. Local SEO services with clear reporting on rankings and leads.",
        service_name="Local SEO",
        service_type="Local Search Engine Optimization",
        form_source="Local SEO Service Page",
        eyebrow="Local SEO",
        h1="Get found by customers in your service area",
        lead="When someone searches for an electrician, plumber, or roofing company nearby, you want your business to be one of the options they see. We help service businesses improve their visibility on Google Maps and in local search results.",
        hero_primary="Get in Touch",
        hero_secondary=("tel:5099019735", "509-901-9735"),
        body=body,
        faqs=faqs,
        cta_heading="Ready to show up in more local searches?",
        cta_body="Tell us about your business and the areas you serve. We'll talk through where you stand and what we'd focus on first.",
        cta_primary="Schedule a Meeting",
    )


def ai_search() -> dict:
    faqs = [
        ("Is AI search optimization the same as SEO?",
         "They overlap considerably. A well structured website, useful content, and accurate business information can support both. AI search optimization adds a focus on how your business appears in generated answers and how those appearances are monitored."),
        ("Can you guarantee that ChatGPT will recommend my business?",
         "No. AI responses change, and no agency controls which businesses an AI tool mentions. We can improve the information available about your business and track its appearance in relevant responses."),
        ("Which AI platforms do you monitor?",
         "Our coverage includes ChatGPT, Google AI Overviews and AI Mode, Gemini, and Perplexity."),
        ("Do I need AI search optimization if I'm already investing in SEO?",
         "You may already have a good starting point. We would first review your existing SEO work and identify whether additional content, technical improvements, or AI visibility monitoring would be worthwhile."),
        ("How can I tell whether my business appears in AI search?",
         "We can review a set of questions your potential customers are likely to ask and show you which businesses appear in the responses."),
    ]
    body = "\n\n".join([
        prose_section("#fff", "AI Search Optimization", "What is AI search optimization?", [
            "AI search optimization, sometimes called generative engine optimization (GEO), focuses on improving how your business is represented in AI generated search answers.",
            "Someone might ask an AI tool which HVAC companies serve their area, what a particular home repair should cost, or how to choose a contractor. Depending on the tool and the question, the answer may include business names, website links, or information gathered from multiple sources.",
            "There isn't a separate trick that guarantees a mention. Much of the work starts with the same things that matter in SEO: accurate business details, useful service pages, a technically accessible website, and a credible presence beyond your own site. We build on that foundation and pay attention to the questions people are asking through AI search.",
        ], aside=("Where we track your visibility", ["ChatGPT", "Google AI Overviews and AI Mode", "Gemini", "Perplexity"])),
        prose_section("var(--bg-soft)", "Why It Matters", "Customers are researching businesses in new ways", [
            "A customer who once compared several Google results may now start by asking an AI tool for an explanation or recommendation. Your business needs to be easy to understand wherever that research takes place.",
            "AI answers vary by platform, wording, and available sources. That's why we look at both traditional search performance and how your business appears in relevant AI responses. The goal is to understand where you're visible, where competitors are being mentioned, and what information could be improved.",
        ]),
        cards_section("#fff", "What's Included", "What we focus on", [
            ("Accurate business information", "We review how your services, locations, and company details appear across your website and relevant third party profiles. Consistency helps people and search systems understand what your business does."),
            ("Content that answers real questions", "We improve key pages so they address the questions customers ask before making a purchase or contacting a business. The writing should be useful to people first, while making important information easy for search tools to identify."),
            ("Technical SEO and structured data", "We check whether important pages can be accessed and read by relevant crawlers. We also review structured data where appropriate to help describe your business and services."),
            ("Reviews and third party visibility", "We look at relevant directories, customer reviews, and other websites that mention your business. These sources can help establish a clearer picture of your company beyond what appears on your own site."),
            ("AI search monitoring", "We test relevant questions across supported AI search tools and record whether your business is mentioned, how it is described, and which competitors appear. Because AI answers can change, we treat these results as a snapshot and look for patterns over time."),
        ]),
        steps_section("var(--bg-soft)", [
            ("Establish a starting point", "We choose questions relevant to your services and locations, then review the responses from the AI platforms included in your tracking."),
            ("Review your online presence", "We check your website, business profiles, technical setup, and other information sources for gaps or inconsistencies."),
            ("Improve priority pages", "We update important service content so it answers common customer questions clearly and accurately."),
            ("Work on supporting signals", "We address relevant listings, review opportunities, and other credible mentions of your business."),
            ("Check progress", "We repeat the agreed upon tests and review changes alongside your broader SEO performance."),
        ]),
        faq_section("#fff", faqs, "ai-search"),
    ])
    return dict(
        slug="ai-search",
        title="AI Search Optimization Services (GEO) | YB Marketing",
        meta="Improve how your business appears in ChatGPT, Google AI Overviews, Gemini, and other AI search experiences with a strategy built on strong SEO fundamentals.",
        service_name="AI Search Optimization",
        service_type="Generative Engine Optimization",
        form_source="AI Search SEO Service Page",
        eyebrow="AI Search Optimization",
        h1="Help customers find your business through AI search",
        lead="Customers are starting to use tools like ChatGPT and Google's AI search features to research services and compare businesses. We help make sure your website and business information are clear, accurate, and easier for these tools to find and reference.",
        hero_primary="Get in Touch",
        hero_secondary=("tel:5099019735", "509-901-9735"),
        body=body,
        faqs=faqs,
        cta_heading="Want your business to show up in AI search?",
        cta_body="Tell us about your business and we'll talk through how your customers are searching and where we'd start.",
        cta_primary="Schedule a Meeting",
    )


def technical_seo() -> dict:
    faqs = [
        ("How is technical SEO different from other SEO services?",
         "Content SEO focuses on what your pages say and which searches they're relevant to. Technical SEO focuses on whether those pages can be found, indexed, and understood properly. Both are important."),
        ("My SEO audit tool gives my website a high score. Do I still need an audit?",
         'Possibly. Automated scores don\'t always reflect the importance of an issue. A problem preventing a major service page from being indexed may matter far more than dozens of minor warnings. We explain more in <a class="text-link" href="/blog/posts/seo-audit-what-actually-matters">Why an SEO Score Is Not the Same Thing as an SEO Strategy</a>.'),
        ("Do you need access to my website?",
         "We can perform an initial public facing review without website access. Google Search Console access helps us investigate indexing and search performance in more detail. Making changes generally requires website access or coordination with your developer."),
        ("Does website speed affect SEO?",
         "Page performance is one of several factors that can affect search. It also matters to visitors. A faster, easier to use site can improve the experience for people who arrive through any marketing channel."),
        ("Does technical SEO help with AI search?",
         "It can. If important content is inaccessible to a crawler, that limits the information it can retrieve. Technical improvements help make your site easier for search systems to access, though they don't guarantee inclusion in AI generated answers."),
    ]
    body = "\n\n".join([
        prose_section("#fff", "Technical SEO", "What is technical SEO?", [
            "Technical SEO deals with how your website is built and how search engines access its content. It includes indexing, page performance, redirects, mobile usability, internal linking, duplicate content, and structured data.",
            "These issues aren't always obvious when you're browsing the site yourself. A page might look perfectly normal but be blocked from indexing. An outdated redirect might send visitors to the wrong place. Two similar pages might be competing for the same search terms.",
            "We review how the site actually functions, not just the score an automated audit tool assigns it.",
        ], aside=("What we look at", ["Indexing", "Page performance", "Redirects and broken links", "Mobile usability", "Internal linking", "Duplicate content", "Structured data"])),
        cards_section("var(--bg-soft)", "Common Problems We Find", "Technical issues that can affect search performance", [
            ("Pages missing from Google's index", "Important pages may be blocked, marked as duplicates, or difficult for Google to discover. We investigate why they aren't appearing and what needs to change."),
            ("Slow page performance", "Large images, unnecessary scripts, and certain plugins can make a website slow, especially on mobile devices. We look for improvements that make sense for the site."),
            ("Duplicate content and conflicting URLs", "Old pages, inconsistent canonical tags, or multiple URLs targeting the same subject can create confusion about which page should appear in search."),
            ("Broken links and redirects", "Links to deleted pages and long redirect chains make navigation harder for visitors and can create unnecessary crawling issues."),
            ("Structured data problems", "We review relevant structured data to make sure it accurately reflects the business and page content. Incorrect or unsupported markup can cause problems rather than help."),
            ("Content that is difficult to access", "Some website features rely heavily on scripts or interactions. We check whether important content is available to search engines and other relevant crawlers."),
        ]),
        steps_section("navy", [
            ("Audit the website", "We crawl the site and review available Google Search Console data for indexing, performance, and other technical issues."),
            ("Investigate the findings", "We look at the site's setup, templates, plugins, links, and redirects to understand what's causing the problems."),
            ("Prioritize the work", "We separate issues that need attention from lower impact recommendations, so you know what should be fixed first."),
            ("Make or coordinate fixes", "Depending on how your website is managed, we can implement approved changes or work with your developer on the required updates."),
            ("Keep an eye on performance", "We continue checking for new issues and review the impact of completed work."),
        ]),
        faq_section("#fff", faqs, "technical-seo"),
    ])
    return dict(
        slug="technical-seo",
        title="Technical SEO Services & Website Audits | YB Marketing",
        meta="Find and fix technical website issues affecting search visibility, including indexing errors, slow pages, redirects, duplicate content, and site structure.",
        service_name="Technical SEO",
        service_type="Technical Search Engine Optimization",
        form_source="Technical SEO Service Page",
        eyebrow="Technical SEO",
        h1="Make sure your website can be found and indexed",
        lead="Even strong website content can struggle in search results when pages aren't being indexed, the site is difficult to navigate, or technical issues interfere with how search engines access it. We identify those problems and help get them resolved.",
        hero_primary="Get in Touch",
        hero_secondary=("tel:5099019735", "509-901-9735"),
        body=body,
        faqs=faqs,
        cta_heading="Think something on your site is holding back your rankings?",
        cta_body="Tell us what you're seeing and we'll talk through what could be causing it and what we'd look at first.",
        cta_primary="Schedule a Meeting",
    )


def website_migration() -> dict:
    faqs = [
        ("Will my website lose rankings after a redesign?",
         "Not necessarily. Some movement is possible after a major change, but a well planned migration can reduce avoidable problems. The amount of disruption depends on what changes and how the transition is handled."),
        ("How long should redirects stay in place?",
         "Google generally recommends keeping redirects for at least a year after a site move. Where practical, keeping redirects longer can continue to help people using old links, especially if you still own the previous domain."),
        ("When should we involve an SEO team?",
         "Ideally, before the new website's page structure and URLs are finalized. It's easier to plan around existing search performance than to investigate lost traffic after launch."),
        ("Can you work with our website developer?",
         "Yes. We can prepare the URL mapping, redirect requirements, and SEO launch checklist for your developer, or coordinate more of the implementation when we're involved in the website project."),
        ("What if we've already launched and traffic has dropped?",
         "We can review what changed, compare old and new URLs, check indexing and redirects, and look for the likely causes. Some problems can be corrected, although recovery time and results will vary."),
    ]
    body = "\n\n".join([
        prose_section("#fff", "Website Migration SEO", "What is a website migration?", [
            "A website migration is a significant change to your site that can affect how search engines find and index its pages. It might involve changing domains, moving to a different platform, reorganizing URLs, or combining multiple websites.",
            "These projects involve more than transferring content. Existing pages may already rank for valuable searches or have links from other websites. When those pages are removed or renamed without a proper plan, search engines and visitors can end up at missing or unrelated URLs.",
            "We help map out those changes before launch and monitor the site afterward, so problems can be identified and addressed quickly.",
        ], aside=("Changes that count as a migration", ["Changing domains", "Moving to a new platform", "Reorganizing URLs", "Combining multiple websites"])),
        cards_section("var(--bg-soft)", "When You Need This", "Common reasons for a migration", [
            ("Website redesigns", "Especially when the redesign changes URLs, navigation, or page structure."),
            ("Platform changes", "Moving between WordPress, Wix, Squarespace, or another website platform."),
            ("Domain changes", "Updating your website address as part of a rebrand or business change."),
            ("Website consolidations", "Combining separate brands, locations, or websites into one."),
            ("Major URL or protocol changes", "Reorganizing large sections of a website or correcting HTTP/HTTPS and www configurations."),
        ]),
        steps_section("navy", [
            ("Review the existing website", "We gather the current URLs and use available analytics, Search Console data, and backlink information to identify important pages."),
            ("Plan the new URL structure", "We match old pages to relevant destinations on the new site and document the redirects needed for launch."),
            ("Check the new site before launch", "We review staging pages for missing content, broken links, metadata issues, indexing restrictions, and other potential problems."),
            ("Support the launch", "We check redirects, submit the appropriate sitemap, and handle applicable Search Console steps for a domain move."),
            ("Monitor the transition", "We watch indexing, traffic, rankings, and errors after launch, investigate unexpected changes, and make adjustments where needed."),
            ("Update important external links", "We identify business profiles, directory listings, and other important references that should point to the new site."),
        ]),
        faq_section("#fff", faqs, "website-migration"),
    ])
    return dict(
        slug="website-migration",
        title="Website Migration SEO Services | YB Marketing",
        meta="Redesigning your website, changing domains, or moving platforms? Protect existing search visibility with URL mapping, redirects, launch checks, and post launch monitoring.",
        service_name="Website Migration SEO",
        service_type="Website Migration",
        form_source="Website Migration SEO Service Page",
        eyebrow="Website Migration SEO",
        h1="Protect your search traffic when you launch a new website",
        lead="A new website should be an improvement, not a reason to lose the search visibility you've already built. We help businesses plan redesigns, domain changes, and platform moves with SEO in mind from the beginning.",
        hero_primary="Get in Touch",
        hero_secondary=("tel:5099019735", "509-901-9735"),
        body=body,
        faqs=faqs,
        cta_heading="Redesigning or moving your website?",
        cta_body="Bring us into the planning process early. We'll help identify the pages and search visibility that need to be protected during the move.",
        cta_primary="Schedule a Meeting",
    )


def main() -> None:
    for builder in (local_seo, ai_search, technical_seo, website_migration):
        page = builder()
        out = ROOT / "seo" / f"{page['slug']}.html"
        out.write_text(build_page(page), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
