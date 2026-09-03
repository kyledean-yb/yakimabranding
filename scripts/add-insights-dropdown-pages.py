#!/usr/bin/env python3
"""Add Client Corner + CRM Tutorials pages and Insights nav dropdown sitewide."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from schema_markup import seo_head_html
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_footer_snippet import site_footer_html
from site_nav_snippet import site_header_html
from site_staging_seo_snippet import STAGING_ROBOTS_META
from site_tracking_snippet import ATTRIBUTER_FOOTER_BLOCK, GTM_BODY_NOSCRIPT_BLOCK, TRACKING_HEAD_BLOCK

CLIENT_VIDEOS = [
    {
        "title": "How AI Search Results Are Ranked",
        "topic": "How AI Search Results Are Ranked",
        "embed": "https://www.youtube.com/embed/fFKG_TkjXq8",
        "paras": [
            "In this Marketing Minute, Kevin breaks down how AI search results are ranked and what that means for businesses trying to get found online.",
            "You'll learn what signals matter most in AI-driven search and how to keep your brand visible as search continues to evolve.",
        ],
    },
    {
        "title": "How AI Impacts Search",
        "topic": "How AI Impacts Search and Leads",
        "embed": "https://www.youtube.com/embed/v2xJVe_odDI",
        "paras": [
            "In this quick demo, Kevin explains how Google search visibility and AI-powered marketing strategies work together to grow your business.",
            "You'll learn how AI and SEO help businesses get found online, attract more local customers, and increase conversions.",
        ],
    },
    {
        "title": "Google AI Search, Reviews, and Listing Power",
        "topic": "Google AI Search, Reviews, and Listing Power",
        "embed": "https://www.youtube.com/embed/Vh6EWJox43E",
        "paras": [
            "In this video, Kevin breaks down how AI-powered search works with Google's evolving ranking systems and why your online presence goes far beyond just your website.",
            "He explains the importance of maintaining strong business listings across multiple platforms and why customer reviews play a critical role in improving visibility, trust, and local search performance.",
        ],
    },
    {
        "title": "Why Bing Business Profiles Matter",
        "topic": "Why Bing Business Profiles Matter",
        "embed": "https://www.youtube.com/embed/M41Eis0Viao",
        "paras": [
            "In this quick video, Kevin explains why having a Bing Business Profile is essential for increasing your online visibility and helping potential customers find your business more easily.",
            "You'll learn how a properly optimized Bing profile can improve search presence, build credibility, and create more opportunities for customer engagement.",
        ],
    },
    {
        "title": "Fixing Your Google Ads",
        "topic": "Fixing Your Google Ads",
        "embed": "https://www.youtube.com/embed/JG6aOZ8_iVA",
        "paras": [
            "In this video, Kevin breaks down how Google Ads are structured and what business owners need to understand to get the best return on their investment.",
            "He explains how proper campaign setup, targeting, and optimization all work together to reduce wasted ad spend and increase high-quality leads.",
            "The focus isn't just on running ads — it's about making sure every dollar is working efficiently to bring in real customers.",
        ],
    },
]

CRM_VIDEOS = [
    {
        "title": "CRM Tool Walkthrough",
        "topic": "Platform Overview",
        "embed": "https://www.youtube.com/embed/HGMEBzswGmQ",
        "paras": [
            "Get a full walkthrough of YB Marketing's Customer Growth & Communication Tool — how the platform is organized and how your team can use it day to day.",
            "Ideal if you're new to the CRM or want a refresher on the core features that keep leads and follow-up on track.",
        ],
    },
    {
        "title": "Opportunities & Pipelines",
        "topic": "Opportunities and Pipelines",
        "embed": "https://www.youtube.com/embed/S3JF6Z0gU-w",
        "paras": [
            "Learn how to work with opportunities and pipelines in the Customer Growth & Communication Tool so you can track deals, move prospects through stages, and keep your sales process clear.",
            "This tutorial helps you turn contacts into organized opportunities your team can actually act on.",
        ],
    },
]

INSIGHTS_DROPDOWN_EN = '''      <div class="nav-insights" id="navInsights">
        <button class="nav-svc-btn" type="button">Insights
          <svg class="nav-chevron" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
        <div class="nav-dd nav-dd-about">
          <div class="nav-dd-arrow"></div>
          <div class="nav-dd-about-inner">
            <div class="nav-dd-about-banner">
              <span class="nav-dd-eyebrow">YB Marketing Insights</span>
              <p class="nav-dd-banner-text">Articles, Marketing Minute &amp; CRM guides</p>
            </div>
            <div class="nav-dd-about-grid">
              <a href="/insights" class="dd-card">
                <div class="dd-ic" style="background:var(--wash-cyan);color:var(--yb-cyan)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="8" y1="7" x2="16" y2="7"/><line x1="8" y1="11" x2="14" y2="11"/></svg></div>
                <div><span class="dd-name">Blog</span><span class="dd-desc">Marketing tips &amp; articles</span></div>
              </a>
              <a href="/client-corner" class="dd-card">
                <div class="dd-ic" style="background:var(--wash-violet);color:var(--yb-violet)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg></div>
                <div><span class="dd-name">Client Corner</span><span class="dd-desc">Resources &amp; Marketing Minute</span></div>
              </a>
              <a href="/crm-tutorials" class="dd-card">
                <div class="dd-ic" style="background:var(--wash-blue);color:var(--yb-blue)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8"/></svg></div>
                <div><span class="dd-name">CRM Tutorials</span><span class="dd-desc">How-to videos for your CRM</span></div>
              </a>
            </div>
          </div>
        </div>
      </div>'''

INSIGHTS_DROPDOWN_ES = '''      <div class="nav-insights" id="navInsights">
        <button class="nav-svc-btn" type="button">Ideas
          <svg class="nav-chevron" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
        <div class="nav-dd nav-dd-about">
          <div class="nav-dd-arrow"></div>
          <div class="nav-dd-about-inner">
            <div class="nav-dd-about-banner">
              <span class="nav-dd-eyebrow">Ideas de YB Marketing</span>
              <p class="nav-dd-banner-text">Artículos, Marketing Minute y guías CRM</p>
            </div>
            <div class="nav-dd-about-grid">
              <a href="/es/insights" class="dd-card">
                <div class="dd-ic" style="background:var(--wash-cyan);color:var(--yb-cyan)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="8" y1="7" x2="16" y2="7"/><line x1="8" y1="11" x2="14" y2="11"/></svg></div>
                <div><span class="dd-name">Blog</span><span class="dd-desc">Consejos y artículos de marketing</span></div>
              </a>
              <a href="/es/client-corner" class="dd-card">
                <div class="dd-ic" style="background:var(--wash-violet);color:var(--yb-violet)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg></div>
                <div><span class="dd-name">Rincón del cliente</span><span class="dd-desc">Recursos y Marketing Minute</span></div>
              </a>
              <a href="/es/crm-tutorials" class="dd-card">
                <div class="dd-ic" style="background:var(--wash-blue);color:var(--yb-blue)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8"/></svg></div>
                <div><span class="dd-name">Tutoriales CRM</span><span class="dd-desc">Videos prácticos de tu CRM</span></div>
              </a>
            </div>
          </div>
        </div>
      </div>'''

MOBILE_INSIGHTS_EN = '''    <a href="#" onclick="document.getElementById('mobileInsightsList').classList.toggle('open');return false" style="display:flex;justify-content:space-between;align-items:center">Insights <span>▾</span></a>
    <div class="mobile-svc-list" id="mobileInsightsList">
      <a href="/insights" class="mobile-about-row"><strong>Blog</strong><span>Marketing tips &amp; articles</span></a>
      <a href="/client-corner" class="mobile-about-row"><strong>Client Corner</strong><span>Resources &amp; Marketing Minute</span></a>
      <a href="/crm-tutorials" class="mobile-about-row"><strong>CRM Tutorials</strong><span>How-to videos for your CRM</span></a>
    </div>'''

MOBILE_INSIGHTS_ES = '''    <a href="#" onclick="document.getElementById('mobileInsightsList').classList.toggle('open');return false" style="display:flex;justify-content:space-between;align-items:center">Ideas <span>▾</span></a>
    <div class="mobile-svc-list" id="mobileInsightsList">
      <a href="/es/insights" class="mobile-about-row"><strong>Blog</strong><span>Consejos y artículos de marketing</span></a>
      <a href="/es/client-corner" class="mobile-about-row"><strong>Rincón del cliente</strong><span>Recursos y Marketing Minute</span></a>
      <a href="/es/crm-tutorials" class="mobile-about-row"><strong>Tutoriales CRM</strong><span>Videos prácticos de tu CRM</span></a>
    </div>'''


def video_cards_html(videos: list[dict]) -> str:
    blocks = []
    for v in videos:
        paras = "".join(f'<p class="video-card-copy">{p}</p>' for p in v["paras"])
        blocks.append(
            f"""      <article class="video-card">
        <div class="video-card-media">
          <iframe src="{v['embed']}" title="{v['title']}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>
        </div>
        <div class="video-card-body">
          <span class="video-card-topic">Topic: {v['topic']}</span>
          <h3>{v['title']}</h3>
          {paras}
        </div>
      </article>"""
        )
    return "\n".join(blocks)


def page_shell(
    *,
    slug: str,
    title: str,
    meta: str,
    eyebrow: str,
    h1: str,
    lead: str,
    section_eyebrow: str,
    section_h2: str,
    section_lead: str,
    videos: list[dict],
    cta_title: str,
    cta_copy: str,
) -> str:
    prefix = "../"
    header = site_header_html(prefix, current_path=f"/{slug}").strip()
    footer = site_footer_html(prefix, current_path=f"/{slug}").strip()
    seo = seo_head_html(f"{slug}/index.html")
    cards = video_cards_html(videos)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="../favicon.png" type="image/png">
<link rel="apple-touch-icon" href="../favicon.png">
{STAGING_ROBOTS_META}
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="stylesheet" href="../colors_and_type.css">
<link rel="stylesheet" href="../site.css">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--font-body);background:var(--bg);color:var(--fg1);-webkit-font-smoothing:antialiased;overflow-x:hidden}}
a{{color:inherit;text-decoration:none}}
.container{{width:100%;max-width:var(--container);margin:0 auto;padding:0 28px}}
.eyebrow{{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--yb-blue)}}
.eyebrow::before{{content:'';width:7px;height:7px;border-radius:50%;background:currentColor}}
.header{{position:sticky;top:0;z-index:50}}
.header.solid{{background:rgba(255,255,255,.88);backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}}
.header.top{{background:rgba(255,255,255,.6);backdrop-filter:blur(12px)}}
.header-inner{{display:flex;align-items:center;justify-content:space-between;height:72px}}
.logo{{display:flex;align-items:center;gap:11px}}
.logo-text{{font-family:var(--font-display);font-weight:800;font-size:22px}}
.logo-text span{{color:var(--yb-blue)}}
.nav{{display:flex;align-items:center;gap:2px}}
.nav-a{{font-weight:600;font-size:15px;padding:8px 14px;border-radius:var(--r-sm)}}
.nav-services,.nav-about,.nav-insights{{position:relative}}
.nav-svc-btn{{display:flex;align-items:center;gap:5px;font-weight:600;font-size:15px;padding:8px 14px;border-radius:var(--r-sm);background:none;border:none;cursor:pointer;font-family:var(--font-body)}}
.btn{{display:inline-flex;align-items:center;gap:8px;border:none;cursor:pointer;font-family:var(--font-body);font-weight:700;font-size:15px;border-radius:var(--r-md);padding:13px 22px}}
.btn-grad{{background:var(--grad-brand);color:#fff;box-shadow:var(--sh-blue)}}
.btn-ghost-white{{background:rgba(255,255,255,.12);color:#fff;border:1.5px solid rgba(255,255,255,.28)}}
.btn-lg{{padding:16px 28px;font-size:16px}}
.hamburger{{display:none;background:none;border:none;cursor:pointer}}
.mobile-menu{{display:none;border-top:1px solid var(--line);background:#fff;padding:12px 28px}}
.mobile-menu a{{display:block;padding:14px 0;font-weight:600;border-bottom:1px solid var(--line)}}
.mobile-svc-list{{display:none;padding:8px 0 8px 16px}}
.mobile-svc-list.open{{display:block}}
.res-hero{{position:relative;overflow:hidden;background:var(--grad-navy);padding:80px 0 96px}}
.res-hero-mesh{{position:absolute;inset:0;background-image:var(--grad-mesh);pointer-events:none}}
.res-hero-inner{{position:relative;max-width:760px}}
.res-hero h1{{margin:16px 0 18px;font-size:clamp(2.2rem,4vw,3.4rem);color:#fff;line-height:1.08}}
.res-hero p{{color:var(--fg2-on-dark);font-size:clamp(1rem,1.3vw,1.15rem);line-height:1.7;margin:0 0 28px;max-width:620px}}
.res-hero-actions{{display:flex;gap:14px;flex-wrap:wrap}}
.wave-div{{line-height:0;font-size:0}}
.wave-div svg{{display:block;width:100%;height:70px}}
.video-section{{padding:88px 0}}
.video-intro{{text-align:center;max-width:720px;margin:0 auto 48px}}
.video-intro h2{{margin:14px 0 16px}}
.video-intro p{{color:var(--fg2);font-size:16px;line-height:1.75}}
.video-list{{display:grid;gap:28px}}
.video-card{{display:grid;grid-template-columns:1.05fr .95fr;gap:28px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:var(--r-xl);padding:20px;box-shadow:0 2px 12px rgba(22,32,58,.05)}}
.video-card:nth-child(even){{grid-template-columns:.95fr 1.05fr}}
.video-card:nth-child(even) .video-card-media{{order:2}}
.video-card-media{{position:relative;aspect-ratio:16/9;border-radius:var(--r-lg);overflow:hidden;background:#0b1220}}
.video-card-media iframe{{position:absolute;inset:0;width:100%;height:100%;border:0}}
.video-card-topic{{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--yb-blue);margin-bottom:10px}}
.video-card-body h3{{font-family:var(--font-display);font-size:clamp(1.15rem,2vw,1.4rem);margin:0 0 12px;color:var(--ink);line-height:1.25}}
.video-card-copy{{color:var(--fg2);font-size:15px;line-height:1.7;margin:0 0 12px}}
.video-card-copy:last-child{{margin-bottom:0}}
.res-cta{{background:var(--grad-navy);padding:80px 0;text-align:center;position:relative;overflow:hidden}}
.res-cta-mesh{{position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.7}}
.res-cta-inner{{position:relative;max-width:680px;margin:0 auto}}
.res-cta h2{{color:#fff;margin:14px 0}}
.res-cta p{{color:var(--fg2-on-dark);margin:0 0 28px;font-size:16px;line-height:1.7}}
.res-cta-btns{{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}}
@media(max-width:1100px){{.nav,.btn-hdr{{display:none}}.hamburger{{display:flex}}.mobile-menu.open{{display:block}}}}
@media(max-width:900px){{.video-card,.video-card:nth-child(even){{grid-template-columns:1fr}}.video-card:nth-child(even) .video-card-media{{order:0}}.video-section{{padding:64px 0}}}}
</style>
{seo}
{TRACKING_HEAD_BLOCK}
</head>
<body>
{GTM_BODY_NOSCRIPT_BLOCK}
{ACCESSIBE_BODY_SCRIPT}
{header}

<section class="res-hero">
  <div class="res-hero-mesh"></div>
  <div class="container res-hero-inner">
    <span class="eyebrow" style="color:var(--yb-cyan)">{eyebrow}</span>
    <h1>{h1}</h1>
    <p>{lead}</p>
    <div class="res-hero-actions">
      <a href="/contact" class="btn btn-grad btn-lg">Get Started Today</a>
      <a href="tel:5099019735" class="btn btn-ghost-white">509-901-9735</a>
    </div>
  </div>
</section>
<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z" fill="#ffffff"/></svg></div>

<section class="video-section">
  <div class="container">
    <div class="video-intro">
      <span class="eyebrow">{section_eyebrow}</span>
      <h2>{section_h2}</h2>
      <p>{section_lead}</p>
    </div>
    <div class="video-list">
{cards}
    </div>
  </div>
</section>

<div class="wave-div" style="background:#ffffff"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div>
<section class="res-cta">
  <div class="res-cta-mesh"></div>
  <div class="container res-cta-inner">
    <span class="eyebrow" style="color:var(--yb-cyan)">Ready to Grow?</span>
    <h2>{cta_title}</h2>
    <p>{cta_copy}</p>
    <div class="res-cta-btns">
      <a href="/contact" class="btn btn-grad btn-lg">Get Started Today</a>
      <a href="tel:5099019735" class="btn btn-ghost-white btn-lg">509-901-9735</a>
    </div>
  </div>
</section>

{footer}
<script src="../js/newsletter-popup.js" defer></script>
<script src="../js/chat-widget.js" defer></script>
<script src="../js/site.js" defer></script>
<script>
document.getElementById('hamburger')?.addEventListener('click', function () {{
  document.getElementById('mobileMenu')?.classList.toggle('open');
}});
</script>
{ATTRIBUTER_FOOTER_BLOCK}
</body>
</html>
"""


def write_pages() -> None:
    # Write insights_nav_snippet first so site_header_html includes dropdown
    insights_snip = ROOT / "scripts" / "insights_nav_snippet.py"
    insights_snip.write_text(
        '''"""Shared Insights dropdown HTML for site nav."""

from typing import Optional

from site_i18n import page_href_lang, t


def insights_nav_dropdown(prefix: str, active: Optional[str] = None, lang: str = "en") -> str:
    """active: 'blog' | 'client-corner' | 'crm-tutorials' | None"""
    _ = prefix
    blog_cls = " is-active" if active == "blog" else ""
    corner_cls = " is-active" if active == "client-corner" else ""
    crm_cls = " is-active" if active == "crm-tutorials" else ""
    return f"""        <div class="nav-dd nav-dd-about">
          <div class="nav-dd-arrow"></div>
          <div class="nav-dd-about-inner">
            <div class="nav-dd-about-banner">
              <span class="nav-dd-eyebrow">{t("YB Marketing Insights", lang)}</span>
              <p class="nav-dd-banner-text">{t("Articles, Marketing Minute & CRM guides", lang)}</p>
            </div>
            <div class="nav-dd-about-grid">
              <a href="{page_href_lang('insights.html', lang)}" class="dd-card{blog_cls}">
                <div class="dd-ic" style="background:var(--wash-cyan);color:var(--yb-cyan)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="8" y1="7" x2="16" y2="7"/><line x1="8" y1="11" x2="14" y2="11"/></svg></div>
                <div><span class="dd-name">{t("Blog", lang)}</span><span class="dd-desc">{t("Marketing tips & articles", lang)}</span></div>
              </a>
              <a href="{page_href_lang('client-corner/index.html', lang)}" class="dd-card{corner_cls}">
                <div class="dd-ic" style="background:var(--wash-violet);color:var(--yb-violet)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg></div>
                <div><span class="dd-name">{t("Client Corner", lang)}</span><span class="dd-desc">{t("Resources & Marketing Minute", lang)}</span></div>
              </a>
              <a href="{page_href_lang('crm-tutorials/index.html', lang)}" class="dd-card{crm_cls}">
                <div class="dd-ic" style="background:var(--wash-blue);color:var(--yb-blue)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8"/></svg></div>
                <div><span class="dd-name">{t("CRM Tutorials", lang)}</span><span class="dd-desc">{t("How-to videos for your CRM", lang)}</span></div>
              </a>
            </div>
          </div>
        </div>"""


def insights_nav_shell(
    prefix: str,
    active: Optional[str] = None,
    btn_style: str = "",
    lang: str = "en",
) -> str:
    style_attr = f' style="{btn_style}"' if btn_style else ""
    return f"""      <div class="nav-insights" id="navInsights">
        <button class="nav-svc-btn" type="button"{style_attr}>{t("Insights", lang)}
          <svg class="nav-chevron" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
{insights_nav_dropdown(prefix, active, lang)}
      </div>"""


def insights_mobile_block(lang: str = "en") -> str:
    return f"""    <a href="#" onclick="document.getElementById('mobileInsightsList').classList.toggle('open');return false" style="display:flex;justify-content:space-between;align-items:center">{t("Insights", lang)} <span>▾</span></a>
    <div class="mobile-svc-list" id="mobileInsightsList">
      <a href="{page_href_lang('insights.html', lang)}" class="mobile-about-row"><strong>{t("Blog", lang)}</strong><span>{t("Marketing tips & articles", lang)}</span></a>
      <a href="{page_href_lang('client-corner/index.html', lang)}" class="mobile-about-row"><strong>{t("Client Corner", lang)}</strong><span>{t("Resources & Marketing Minute", lang)}</span></a>
      <a href="{page_href_lang('crm-tutorials/index.html', lang)}" class="mobile-about-row"><strong>{t("CRM Tutorials", lang)}</strong><span>{t("How-to videos for your CRM", lang)}</span></a>
    </div>"""
''',
        encoding="utf-8",
    )
    print("wrote scripts/insights_nav_snippet.py")

    # Patch site_nav_snippet to use insights dropdown
    nav_path = ROOT / "scripts" / "site_nav_snippet.py"
    text = nav_path.read_text(encoding="utf-8")
    if "insights_nav_snippet" not in text:
        text = text.replace(
            "from about_nav_snippet import about_nav_shell\n",
            "from about_nav_snippet import about_nav_shell\n"
            "from insights_nav_snippet import insights_mobile_block, insights_nav_shell\n",
        )
        text = text.replace(
            '      <a href="{page_href_lang(\'insights.html\', lang)}" class="nav-a">{t("Insights", lang)}</a>\n',
            "      {insights_nav_shell(prefix, None, '', lang)}\n",
        )
        text = text.replace(
            '    <a href="{page_href_lang(\'insights.html\', lang)}">{t("Insights", lang)}</a>\n',
            "    {insights_mobile_block(lang)}\n",
        )
        nav_path.write_text(text, encoding="utf-8")
        print("patched site_nav_snippet.py")

    # i18n strings
    i18n = ROOT / "scripts" / "site_i18n.py"
    text = i18n.read_text(encoding="utf-8")
    additions = {
        "YB Marketing Insights": "Ideas de YB Marketing",
        "Articles, Marketing Minute & CRM guides": "Artículos, Marketing Minute y guías CRM",
        "Blog": "Blog",
        "Marketing tips & articles": "Consejos y artículos de marketing",
        "Client Corner": "Rincón del cliente",
        "Resources & Marketing Minute": "Recursos y Marketing Minute",
        "CRM Tutorials": "Tutoriales CRM",
        "How-to videos for your CRM": "Videos prácticos de tu CRM",
    }
    for en, es in additions.items():
        if f'"{en}"' not in text:
            text = text.replace(
                '"Language": "Idioma",\n',
                f'"{en}": "{es}",\n    "Language": "Idioma",\n',
            )
    i18n.write_text(text, encoding="utf-8")

    # site_urls for clean paths (index.html folders already work)
    # schema
    schema = ROOT / "scripts" / "schema_markup.py"
    text = schema.read_text(encoding="utf-8")
    if "client-corner/index.html" not in text:
        text = text.replace(
            '    "customer-growth/index.html": {',
            '    "client-corner/index.html": {\n'
            '        "slug": "client-corner",\n'
            '        "name": "Client Corner",\n'
            '        "service_type": "Marketing Education",\n'
            '        "description": "Marketing Minute videos and client resources from YB Marketing for Pacific Northwest businesses.",\n'
            "    },\n"
            '    "crm-tutorials/index.html": {\n'
            '        "slug": "crm-tutorials",\n'
            '        "name": "CRM Tutorials",\n'
            '        "service_type": "Software Training",\n'
            '        "description": "Step-by-step video tutorials for YB Marketing\'s Customer Growth & Communication Tool.",\n'
            "    },\n"
            '    "customer-growth/index.html": {',
        )
        schema.write_text(text, encoding="utf-8")

    # sitemap root pages / collect
    sm = ROOT / "scripts" / "build-sitemap.py"
    text = sm.read_text(encoding="utf-8")
    if "client-corner/index.html" not in text:
        text = text.replace(
            '("customer-growth/index.html", "Customer Growth & Communication Tool"),\n]',
            '("customer-growth/index.html", "Customer Growth & Communication Tool"),\n'
            '    ("client-corner/index.html", "Client Corner"),\n'
            '    ("crm-tutorials/index.html", "CRM Tutorials"),\n]',
        )
        sm.write_text(text, encoding="utf-8")

    # vercel redirects
    vercel = ROOT / "vercel.json"
    text = vercel.read_text(encoding="utf-8")
    if "/client-corner" not in text or "/services/client-corner" not in text:
        text = text.replace(
            '{ "source": "/services/crm-services", "destination": "/customer-growth", "permanent": true },',
            '{ "source": "/services/crm-services", "destination": "/customer-growth", "permanent": true },\n'
            '    { "source": "/services/client-corner", "destination": "/client-corner", "permanent": true },\n'
            '    { "source": "/services/crm-tutorials", "destination": "/crm-tutorials", "permanent": true },',
        )
        vercel.write_text(text, encoding="utf-8")

    # site.js support for nav-insights
    site_js = ROOT / "js" / "site.js"
    text = site_js.read_text(encoding="utf-8")
    if "nav-insights" not in text:
        text = text.replace(
            ".nav-services, .nav-about",
            ".nav-services, .nav-about, .nav-insights",
        )
        text = text.replace(
            ".nav-services.is-open, .nav-about.is-open",
            ".nav-services.is-open, .nav-about.is-open, .nav-insights.is-open",
        )
        text = text.replace(
            "!e.target.closest('.nav-services') && !e.target.closest('.nav-about')",
            "!e.target.closest('.nav-services') && !e.target.closest('.nav-about') && !e.target.closest('.nav-insights')",
        )
        site_js.write_text(text, encoding="utf-8")

    # site.css
    css = ROOT / "site.css"
    text = css.read_text(encoding="utf-8")
    if ".nav-insights" not in text:
        text = text.replace(".nav-services,\n.nav-about {", ".nav-services,\n.nav-about,\n.nav-insights {")
        text = text.replace(".nav-services::before,\n.nav-about::before {", ".nav-services::before,\n.nav-about::before,\n.nav-insights::before {")
        text = text.replace(
            ".nav-about.is-open .nav-dd,\n.nav-about:hover .nav-dd,\n.nav-about:focus-within .nav-dd {",
            ".nav-about.is-open .nav-dd,\n.nav-about:hover .nav-dd,\n.nav-about:focus-within .nav-dd,\n"
            ".nav-insights.is-open .nav-dd,\n.nav-insights:hover .nav-dd,\n.nav-insights:focus-within .nav-dd {",
        )
        text = text.replace(
            ".nav-about.is-open .nav-svc-btn,\n.nav-about:hover .nav-svc-btn,\n.nav-about:focus-within .nav-svc-btn {",
            ".nav-about.is-open .nav-svc-btn,\n.nav-about:hover .nav-svc-btn,\n.nav-about:focus-within .nav-svc-btn,\n"
            ".nav-insights.is-open .nav-svc-btn,\n.nav-insights:hover .nav-svc-btn,\n.nav-insights:focus-within .nav-svc-btn {",
        )
        text = text.replace(
            ".nav-about.is-open .nav-chevron,\n.nav-about:hover .nav-chevron,\n.nav-about:focus-within .nav-chevron {",
            ".nav-about.is-open .nav-chevron,\n.nav-about:hover .nav-chevron,\n.nav-about:focus-within .nav-chevron,\n"
            ".nav-insights.is-open .nav-chevron,\n.nav-insights:hover .nav-chevron,\n.nav-insights:focus-within .nav-chevron {",
        )
        # add position rule
        if ".nav-insights {\n  position: relative;" not in text:
            text = text.replace(
                ".nav-about {\n  position: relative;\n}",
                ".nav-about {\n  position: relative;\n}\n\n.nav-insights {\n  position: relative;\n}",
            )
        css.write_text(text, encoding="utf-8")

    # Next.js
    links = ROOT / "next" / "lib" / "site-links.ts"
    text = links.read_text(encoding="utf-8")
    if "clientCorner" not in text:
        text = text.replace(
            'insights: "/insights",',
            'insights: "/insights",\n'
            '  clientCorner: "/client-corner",\n'
            '  crmTutorials: "/crm-tutorials",',
        )
        links.write_text(text, encoding="utf-8")

    # Reload nav snippet so new pages get Insights dropdown in header
    import importlib
    import insights_nav_snippet  # noqa: F401
    import site_nav_snippet
    importlib.reload(insights_nav_snippet)
    importlib.reload(site_nav_snippet)
    globals()["site_header_html"] = site_nav_snippet.site_header_html
    from site_footer_snippet import site_footer_html as _ftr
    globals()["site_footer_html"] = _ftr

    for slug, kwargs in [
        (
            "client-corner",
            dict(
                title="Client Corner | YB Marketing | 509-901-9735",
                meta="Marketing Minute videos and client resources from YB Marketing. Learn AI search, listings, reviews, Bing profiles, and Google Ads tips.",
                eyebrow="Client Resources",
                h1="Client Corner",
                lead="A marketing resource hub for YB Marketing clients — short Marketing Minute videos with practical tips you can use right away. Call 509-901-9735 to get started.",
                section_eyebrow="Marketing Minute",
                section_h2="Marketing Minute with Kevin Dean",
                section_lead="Quick videos on AI search, listings, reviews, and paid search — built for busy Pacific Northwest business owners.",
                videos=CLIENT_VIDEOS,
                cta_title="Need help putting these tips to work?",
                cta_copy="Talk with YB Marketing about SEO, Google Ads, listings, and the Customer Growth & Communication Tool.",
            ),
        ),
        (
            "crm-tutorials",
            dict(
                title="CRM Tutorials | YB Marketing | 509-901-9735",
                meta="Step-by-step video guides for YB Marketing's Customer Growth & Communication Tool — platform walkthrough, opportunities, and pipelines.",
                eyebrow="Training Videos",
                h1="CRM Tutorials",
                lead="Step-by-step video guides for the Customer Growth & Communication Tool — from a full platform walkthrough to opportunities and pipelines.",
                section_eyebrow="Learn the Tool",
                section_h2="Learn the Customer Growth & Communication Tool",
                section_lead="Watch these tutorials to get comfortable with the platform — from a full walkthrough to managing opportunities and pipelines.",
                videos=CRM_VIDEOS,
                cta_title="Need CRM help?",
                cta_copy="Our team can set up, train, and support your Customer Growth & Communication Tool so it actually gets used. Reach out anytime.",
            ),
        ),
    ]:
        out = ROOT / slug
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(page_shell(slug=slug, **kwargs), encoding="utf-8")
        print(f"wrote {slug}/index.html")


def patch_all_html() -> int:
    """Replace Insights link with Insights dropdown across static HTML."""
    # Patterns for desktop Insights link (various forms)
    patterns = [
        # Absolute EN
        (
            re.compile(r'<a href="/insights" class="nav-a"[^>]*>Insights</a>'),
            INSIGHTS_DROPDOWN_EN,
            False,
        ),
        (
            re.compile(r'<a href="/es/insights" class="nav-a"[^>]*>Ideas</a>'),
            INSIGHTS_DROPDOWN_ES,
            True,
        ),
        # Relative / bare Insights without class variants already covered
        (
            re.compile(r'<a href="[^"]*insights\.html" class="nav-a"[^>]*>Insights</a>'),
            INSIGHTS_DROPDOWN_EN,
            False,
        ),
    ]
    mobile_patterns = [
        (
            re.compile(r'<a href="/insights">Insights</a>'),
            MOBILE_INSIGHTS_EN,
        ),
        (
            re.compile(r'<a href="/es/insights">Ideas</a>'),
            MOBILE_INSIGHTS_ES,
        ),
        (
            re.compile(r'<a href="[^"]*insights\.html">Insights</a>'),
            MOBILE_INSIGHTS_EN,
        ),
    ]

    count = 0
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT).as_posix()
        if any(x in rel for x in ("node_modules/", "next/", "_next/", "partials/", "preview/")):
            continue
        text = path.read_text(encoding="utf-8")
        if 'id="navInsights"' in text:
            continue
        original = text
        is_es = rel.startswith("es/")

        for pattern, replacement, es_flag in patterns:
            if es_flag != is_es and pattern.pattern.startswith('<a href="/es'):
                continue
            if pattern.search(text):
                text = pattern.sub(replacement, text, count=1)
                break
        else:
            # try ES/EN regardless
            for pattern, replacement, _ in patterns:
                if pattern.search(text):
                    text = pattern.sub(replacement, text, count=1)
                    break

        for pattern, replacement in mobile_patterns:
            if pattern.search(text) and "mobileInsightsList" not in text:
                text = pattern.sub(replacement, text, count=1)
                break

        # Ensure CSS/JS selectors work on pages with inline styles mentioning only nav-about
        if 'id="navInsights"' in text and ".nav-insights" not in text:
            text = text.replace(".nav-services,.nav-about{", ".nav-services,.nav-about,.nav-insights{")
            text = text.replace(
                ".nav-svc-btn:hover,.nav-services:hover .nav-svc-btn,.nav-about:hover .nav-svc-btn{",
                ".nav-svc-btn:hover,.nav-services:hover .nav-svc-btn,.nav-about:hover .nav-svc-btn,.nav-insights:hover .nav-svc-btn{",
            )
            text = text.replace(
                ".nav-services:hover .nav-chevron,.nav-about:hover .nav-chevron{",
                ".nav-services:hover .nav-chevron,.nav-about:hover .nav-chevron,.nav-insights:hover .nav-chevron{",
            )
            text = text.replace(
                ".nav-services:hover .nav-dd,.nav-about:hover .nav-dd,",
                ".nav-services:hover .nav-dd,.nav-about:hover .nav-dd,.nav-insights:hover .nav-dd,",
            )
            text = text.replace(
                ".nav-services.is-open .nav-dd,.nav-about.is-open .nav-dd{",
                ".nav-services.is-open .nav-dd,.nav-about.is-open .nav-dd,.nav-insights.is-open .nav-dd{",
            )

        if text != original:
            path.write_text(text, encoding="utf-8")
            count += 1
    return count


def patch_next_header() -> None:
    header = ROOT / "next" / "components" / "layout" / "SiteHeader.tsx"
    if not header.exists():
        return
    text = header.read_text(encoding="utf-8")
    if "clientCorner" in text and "nav-insights" in text:
        return
    # Replace simple Insights link with dropdown similar to About
    old = """          <a href={siteLinks.insights} className="nav-a">
            Insights
          </a>"""
    new = """          <div className="nav-insights" id="navInsights">
            <button className="nav-svc-btn" type="button">
              Insights
              {chevronIcon}
            </button>
            <div className="nav-dd nav-dd-about">
              <div className="nav-dd-arrow" />
              <div className="nav-dd-about-inner">
                <div className="nav-dd-about-banner">
                  <span className="nav-dd-eyebrow">YB Marketing Insights</span>
                  <p className="nav-dd-banner-text">Articles, Marketing Minute &amp; CRM guides</p>
                </div>
                <div className="nav-dd-about-grid">
                  <a href={siteLinks.insights} className="dd-card">
                    <div className="dd-ic" style={{ background: "var(--wash-cyan)", color: "var(--yb-cyan)" }}>
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
                        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
                        <line x1="8" y1="7" x2="16" y2="7" />
                        <line x1="8" y1="11" x2="14" y2="11" />
                      </svg>
                    </div>
                    <div>
                      <span className="dd-name">Blog</span>
                      <span className="dd-desc">Marketing tips &amp; articles</span>
                    </div>
                  </a>
                  <a href={siteLinks.clientCorner} className="dd-card">
                    <div className="dd-ic" style={{ background: "var(--wash-violet)", color: "var(--yb-violet)" }}>
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <polygon points="23 7 16 12 23 17 23 7" />
                        <rect x="1" y="5" width="15" height="14" rx="2" ry="2" />
                      </svg>
                    </div>
                    <div>
                      <span className="dd-name">Client Corner</span>
                      <span className="dd-desc">Resources &amp; Marketing Minute</span>
                    </div>
                  </a>
                  <a href={siteLinks.crmTutorials} className="dd-card">
                    <div className="dd-ic" style={{ background: "var(--wash-blue)", color: "var(--yb-blue)" }}>
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <circle cx="12" cy="12" r="10" />
                        <polygon points="10 8 16 12 10 16 10 8" />
                      </svg>
                    </div>
                    <div>
                      <span className="dd-name">CRM Tutorials</span>
                      <span className="dd-desc">How-to videos for your CRM</span>
                    </div>
                  </a>
                </div>
              </div>
            </div>
          </div>"""
    if old in text:
        text = text.replace(old, new)
        # mobile insights expandable
        text = text.replace(
            '        <a href={siteLinks.insights}>Insights</a>\n',
            """        <a
          href="#"
          onClick={(e) => {
            e.preventDefault();
            const el = document.getElementById("mobileInsightsList");
            el?.classList.toggle("open");
          }}
          style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}
        >
          Insights <span>▾</span>
        </a>
        <div className="mobile-svc-list" id="mobileInsightsList">
          <a href={siteLinks.insights} className="mobile-about-row">
            <strong>Blog</strong>
            <span>Marketing tips &amp; articles</span>
          </a>
          <a href={siteLinks.clientCorner} className="mobile-about-row">
            <strong>Client Corner</strong>
            <span>Resources &amp; Marketing Minute</span>
          </a>
          <a href={siteLinks.crmTutorials} className="mobile-about-row">
            <strong>CRM Tutorials</strong>
            <span>How-to videos for your CRM</span>
          </a>
        </div>
""",
        )
        header.write_text(text, encoding="utf-8")
        print("patched Next.js SiteHeader")


def main() -> None:
    write_pages()
    patch_next_header()
    n = patch_all_html()
    print(f"patched Insights dropdown into {n} HTML files")


if __name__ == "__main__":
    main()
