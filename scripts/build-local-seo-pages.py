#!/usr/bin/env python3
"""Generate localized SEO landing pages from data/seoLocations.js."""

import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "seo"
DATA_FILE = ROOT / "data" / "seoLocations.js"
PREFIX = "../"
PARTIALS = ROOT / "partials" / "local-service"

sys.path.insert(0, str(ROOT / "scripts"))
from reviews_section_snippet import reviews_section_html
from schema_markup import seo_head_html
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_local_service_hubspot_form_snippet import (
    LOCAL_HS_FORM_PLACEHOLDER,
    hubspot_script_tags,
    local_hubspot_form_html,
    location_thank_you_redirect,
)
from site_staging_seo_snippet import STAGING_ROBOTS_META
from seo_vs_ppc_section_snippet import seo_vs_ppc_section_html
from site_footer_snippet import site_footer_html
from site_nav_snippet import site_header_html

FEAT_ICONS = [
    '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    '<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/>',
    '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
    '<path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>',
    '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>',
]

LOC_PIN = (
    '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'
    "</svg>"
)

HERO_ORBIT_NODES = [
    ("Personalization", '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>'),
    ("Visibility", '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>'),
    ("Spread the Word", '<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/>'),
    ("Google's Friend", '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>'),
    ("Increase Keywords", '<path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>'),
    ("Increase Traffic", '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>'),
]


def render_hero_orbit(prefix: str, city: str) -> str:
    nodes = []
    for i, (label, icon) in enumerate(HERO_ORBIT_NODES):
        nodes.append(
            f"""          <div class="hero-orbit-node" style="--i:{i}">
            <div class="hero-orbit-icon" aria-label="{esc(label)}">
              <span class="hero-orbit-pill">
                <span class="hero-orbit-pill-ic">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{icon}</svg>
                </span>
              </span>
            </div>
          </div>"""
        )
    nodes_html = "\n".join(nodes)
    return f"""    <div class="svc-hero-visual">
      <div class="hero-orbit hero-orbit--svc hero-orbit--features" style="--orbit-feat-wash:var(--wash-cyan);--orbit-feat-color:var(--yb-cyan);--orbit-feat-glow:rgba(43,196,240,0.22)">
        <div class="hero-orbit-bg" aria-hidden="true">
          <div class="hero-orbit-ring hero-orbit-ring--track"></div>
          <div class="hero-orbit-hub">
            <div class="hero-orbit-hub-art">
              <img src="{prefix}assets/svc-hub-seo.webp" alt="SEO services in {esc(city)}">
            </div>
          </div>
        </div>
        <div class="hero-orbit-spin">
{nodes_html}
        </div>
      </div>
    </div>"""


def load_locations() -> list[dict]:
    script = (
        "import { seoLocations } from './seoLocations.js';"
        "process.stdout.write(JSON.stringify(seoLocations));"
    )
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=ROOT / "data",
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def schema_json(loc: dict) -> tuple[str, str]:
    locality = loc["schema"]["addressLocality"]
    region = loc["schema"]["addressRegion"]
    country = loc["schema"]["addressCountry"]
    city = loc["city"]
    local_business = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "YB Marketing",
        "url": "https://yakimabranding.com",
        "telephone": "+15099019735",
        "email": "info@yakimabranding.com",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": locality,
            "addressRegion": region,
            "addressCountry": country,
        },
        "areaServed": city,
        "description": loc["metaDescription"],
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://yakimabranding.com",
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "SEO",
                "item": "https://yakimabranding.com/services/seo.html",
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": f"{city} SEO",
                "item": loc["canonicalUrl"],
            },
        ],
    }
    return json.dumps(local_business, ensure_ascii=False), json.dumps(
        breadcrumb, ensure_ascii=False
    )


def load_partial(name: str, prefix: str) -> str:
    text = (PARTIALS / name).read_text(encoding="utf-8")
    return text.replace("../", prefix)


def render_features(features: list[dict]) -> str:
    cards = []
    for i, feat in enumerate(features):
        icon = FEAT_ICONS[i % len(FEAT_ICONS)]
        cards.append(
            f"""      <div class="feat-card">
        <div class="feat-ic" style="background:var(--wash-cyan);color:var(--yb-cyan)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{icon}</svg>
        </div>
        <div class="feat-title">{esc(feat["title"])}</div>
        <div class="feat-desc">{esc(feat["body"])}</div>
      </div>"""
        )
    return "\n".join(cards)


def render_faqs(loc: dict) -> str:
    slug = loc["slug"]
    items = []
    for i, faq in enumerate(loc["faqs"], start=1):
        fid = f"{slug}-faq-{i}"
        items.append(
            f"""      <div class="faq-item" id="{fid}">
        <button class="faq-q" onclick="toggleFaq('{fid}', '#2BC4F0')">
          {esc(faq["q"])}
          <span class="faq-icon"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></span>
        </button>
        <div class="faq-a"><div class="faq-a-inner">{esc(faq["a"])}</div></div>
      </div>"""
        )
    return "\n".join(items)


def render_local_signals(signals: list[str]) -> str:
    chips = "".join(
        f'<span class="loc-chip">{LOC_PIN}{esc(s)}</span>' for s in signals
    )
    return f"""        <div class="locations-track">
          <div class="locations-set">{chips}</div>
          <div class="locations-set" aria-hidden="true">{chips}</div>
        </div>"""


def render_page(loc: dict) -> str:
    p = PREFIX
    city = loc["city"]
    slug = loc["slug"]
    schema_head = seo_head_html(f"seo/{slug}.html")
    header = site_header_html(p).strip()
    footer = site_footer_html(p).strip()
    features_html = render_features(loc["features"])
    faqs_html = render_faqs(loc)
    signals_html = render_local_signals(loc["localSignals"])
    reviews_html = reviews_section_html()
    hero_aria = f'SEO services in {city}'
    orbit_html = render_hero_orbit(p, city)
    contact_html = (
        load_partial("contact-section.html", p)
        .replace('style="color:#159468"', 'style="color:#2BC4F0"')
        .replace(
            LOCAL_HS_FORM_PLACEHOLDER,
            local_hubspot_form_html(
                f"SEO in {city}",
                redirect=location_thank_you_redirect(slug),
            ),
        )
    )
    seo_vs_ppc_html = seo_vs_ppc_section_html(p)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{STAGING_ROBOTS_META}
<link rel="icon" href="{p}favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{p}favicon.png">
<title>{esc(loc["titleTag"])}</title>
<meta name="description" content="{esc(loc["metaDescription"])}">
<link rel="canonical" href="{esc(loc["canonicalUrl"])}">
<link rel="stylesheet" href="{p}colors_and_type.css">
<link rel="stylesheet" href="{p}insights.css">
<link rel="stylesheet" href="{p}site.css">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--font-body);background:var(--bg);color:var(--fg1);-webkit-font-smoothing:antialiased;overflow-x:hidden}}
img{{display:block;max-width:100%}}
a{{color:inherit;text-decoration:none}}
.container{{width:100%;max-width:var(--container);margin:0 auto;padding:0 28px}}
section{{padding:88px 0}}
.eyebrow{{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-body);font-weight:700;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--yb-blue)}}
.eyebrow::before{{content:'';display:block;width:7px;height:7px;border-radius:50%;background:currentColor;flex:none}}
.btn{{display:inline-flex;align-items:center;gap:8px;border:none;cursor:pointer;font-family:var(--font-body);font-weight:700;font-size:15px;border-radius:var(--r-md);padding:13px 22px;transition:all 240ms;white-space:nowrap;line-height:1}}
.btn-grad{{background:var(--grad-brand);color:#fff;box-shadow:0 14px 30px -10px rgba(63,111,214,.45)}}
.btn-grad:hover{{transform:translateY(-2px);filter:brightness(1.06)}}
.btn-ghost-white{{background:rgba(255,255,255,.12);color:#fff;border:1.5px solid rgba(255,255,255,.28)}}
.btn-ghost-white:hover{{background:rgba(255,255,255,.22);transform:translateY(-2px)}}
.btn-lg{{padding:16px 28px;font-size:16px}}
.svc-hero{{position:relative;overflow:hidden;background:var(--grad-navy);padding:80px 0 100px}}
.svc-hero-mesh{{position:absolute;inset:0;background-image:var(--grad-mesh);pointer-events:none}}
.svc-hero-inner{{position:relative;display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:center}}
.svc-hero-text .eyebrow::before{{background:currentColor}}
.svc-hero h1{{margin:16px 0 14px;font-family:var(--font-display);font-weight:800;font-size:clamp(2rem,3.6vw,3.2rem);color:#fff;line-height:1.08}}
.svc-hero-sub{{color:var(--yb-cyan);font-family:var(--font-display);font-weight:700;font-size:clamp(1.05rem,1.6vw,1.25rem);margin-bottom:18px}}
.hero-lead{{margin:0 0 32px;color:var(--fg2-on-dark);max-width:540px;font-size:clamp(1rem,1.3vw,1.15rem);line-height:1.7}}
.svc-hero-actions{{display:flex;gap:14px;flex-wrap:wrap}}
.svc-hero-visual{{position:relative}}
.feat-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
.feat-card{{background:#fff;border-radius:var(--r-lg);padding:26px;border:1px solid var(--line);box-shadow:0 2px 8px rgba(22,32,58,.06);transition:all 240ms}}
.feat-card:hover{{transform:translateY(-4px);box-shadow:0 12px 32px -8px rgba(22,32,58,.14)}}
.feat-ic{{width:48px;height:48px;border-radius:var(--r-md);display:flex;align-items:center;justify-content:center;margin-bottom:16px}}
.feat-ic svg{{width:22px;height:22px}}
.feat-title{{font-family:var(--font-display);font-weight:700;font-size:16px;color:var(--ink);margin-bottom:7px}}
.feat-desc{{font-size:14px;color:var(--fg2);line-height:1.6}}
.local-intro{{max-width:820px;margin:32px auto 0;color:var(--fg2);font-size:16px;line-height:1.75;text-align:left}}
.svc-cta{{background:var(--grad-navy);position:relative;overflow:hidden;padding:80px 0}}
.svc-cta-mesh{{position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.7}}
.svc-cta-inner{{position:relative;text-align:center;max-width:680px;margin:0 auto}}
.svc-cta h2{{color:#fff;margin-bottom:14px}}
.svc-cta p{{color:var(--fg2-on-dark);font-size:16px;margin-bottom:32px}}
.svc-cta-btns{{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}}
.wave-div{{position:relative;overflow:hidden;line-height:0;font-size:0}}
.wave-div svg{{display:block;width:100%;height:70px}}
.faq-item{{border-bottom:1px solid var(--line)}}
.faq-q{{display:flex;justify-content:space-between;align-items:center;padding:20px 0;cursor:pointer;font-weight:700;font-size:15.5px;color:var(--ink);gap:16px;background:none;border:none;width:100%;text-align:left;font-family:var(--font-body);transition:color 200ms}}
.faq-q:hover{{color:var(--yb-blue)}}
.faq-q.active{{color:var(--faq-ac,var(--yb-blue))}}
.faq-icon{{width:28px;height:28px;border-radius:50%;background:var(--bg-mute);display:flex;align-items:center;justify-content:center;flex:none;transition:background 200ms,transform 200ms;color:var(--fg2)}}
.faq-q.active .faq-icon{{background:var(--faq-ac,var(--yb-blue));color:#fff;transform:rotate(45deg)}}
.faq-a{{max-height:0;overflow:hidden;transition:max-height 320ms cubic-bezier(.16,1,.3,1)}}
.faq-a-inner{{padding-bottom:20px;font-size:15px;color:var(--fg2);line-height:1.75}}
.locations-track{{display:flex;width:max-content;animation:loc-scroll 35s linear infinite;gap:0}}
.locations-track:hover{{animation-play-state:paused}}
.locations-set{{display:flex;gap:12px;padding-right:12px}}
.loc-chip{{display:inline-flex;align-items:center;gap:7px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);color:rgba(255,255,255,.85);font-size:13px;font-weight:600;letter-spacing:.03em;padding:7px 16px;border-radius:var(--r-pill);white-space:nowrap;font-family:var(--font-display)}}
.loc-chip svg{{opacity:.6;flex:none}}
@keyframes loc-scroll{{from{{transform:translateX(0)}}to{{transform:translateX(-50%)}}}}
.reviews-bg{{background:var(--bg-soft)}}
.reviews-scroll-track{{display:flex;width:max-content;animation:rv-scroll 50s linear infinite;gap:22px}}
.reviews-scroll-track:hover{{animation-play-state:paused}}
.reviews-scroll-set{{display:flex;gap:22px}}
.rv-scroll-card{{width:320px;background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:22px;box-shadow:var(--sh-sm);flex:none;display:flex;flex-direction:column}}
@keyframes rv-scroll{{from{{transform:translateX(0)}}to{{transform:translateX(-50%)}}}}
@media(prefers-reduced-motion:reduce){{.reviews-scroll-track{{animation:none}}}}
.footer{{background:var(--grad-navy);color:#fff;position:relative;overflow:hidden;padding:64px 0 28px}}
.footer-mesh{{position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.5;pointer-events:none}}
.footer-grid{{position:relative;display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr 1.1fr;gap:40px;margin-bottom:42px}}
.footer-brand p{{color:var(--fg2-on-dark);font-size:14px;max-width:280px;margin:14px 0 18px}}
.footer-col h4{{font-family:var(--font-display);font-size:14px;font-weight:700;margin-bottom:14px;letter-spacing:.04em;color:#fff}}
.footer-col ul{{list-style:none;display:grid;gap:10px}}
.footer-col a{{color:var(--fg2-on-dark);font-size:14px;transition:color 240ms}}
.footer-col a:hover{{color:#fff}}
.footer-bottom{{position:relative;border-top:1px solid rgba(255,255,255,.12);padding-top:22px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;color:var(--fg2-on-dark);font-size:13px}}
.footer-socials{{display:flex;gap:10px;margin-top:12px}}
.social-btn{{width:38px;height:38px;border-radius:var(--r-sm);background:rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;color:#fff;transition:background 240ms}}
.social-btn:hover{{background:var(--yb-blue)}}
@media(max-width:900px){{.svc-hero-inner{{grid-template-columns:1fr}}.svc-hero-visual{{display:none}}.feat-grid{{grid-template-columns:1fr 1fr}}.why-main-grid{{grid-template-columns:1fr !important}}.why-tiles-grid{{grid-template-columns:1fr 1fr !important}}}}
@media(max-width:640px){{.feat-grid{{grid-template-columns:1fr}}.footer-grid{{grid-template-columns:1fr}}section{{padding:60px 0}}}}
</style>
{schema_head}</head>
<body>
{ACCESSIBE_BODY_SCRIPT}

{header}

<!-- HERO -->
<section class="svc-hero" aria-label="{esc(hero_aria)}">
  <div class="svc-hero-mesh"></div>
  <div class="hero-logo-overlay hero-logo-overlay--left" aria-hidden="true">
    <img src="{p}assets/yb-logo-white.png" alt="YB Marketing logo serving {esc(city)}">
  </div>
  <div class="container svc-hero-inner">
    <div class="svc-hero-text">
      <span class="eyebrow" style="color:#2BC4F0">{esc(city)} SEO Services</span>
      <h1>{esc(loc["hero"]["headline"])}</h1>
      <p class="svc-hero-sub">{esc(loc["hero"]["subheadline"])}</p>
      <p class="hero-lead">{esc(loc["hero"]["body"])}</p>
      <div class="svc-hero-actions">
        <a href="{p}contact.html" class="btn btn-grad btn-lg">Get Started Today
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </a>
        <a href="tel:5099019735" class="btn btn-ghost-white btn-lg">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 16 0 0 0 6.07 6.07l1.08-.9a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          509-901-9735
        </a>
      </div>
      <p style="margin-top:20px;font-size:14px"><a href="{p}services/seo.html" style="color:var(--yb-cyan);font-weight:600">View all SEO services →</a></p>
    </div>
{orbit_html}
  </div>
</section>

<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 80" preserveAspectRatio="none" style="height:80px"><path d="M0,0 C360,80 1080,80 1440,0 L1440,80 L0,80 Z" fill="#ffffff"/></svg></div>

<!-- WHAT IS SEO -->
<section style="background:#fff">
  <div class="container">
    <div style="text-align:center;max-width:760px;margin:0 auto 20px">
      <span class="eyebrow" style="color:#2BC4F0">What We Do</span>
      <h2 style="margin:14px 0 16px">{esc(loc["whatIsSeo"]["heading"])}</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">{esc(loc["whatIsSeo"]["intro"])}</p>
    </div>
    <p class="local-intro">{esc(loc["whatIsSeo"]["localParagraph"])}</p>
    <div class="feat-grid" style="margin-top:52px">
{features_html}
    </div>
  </div>
</section>

{seo_vs_ppc_html}

<!-- WHY YB -->
<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div>
<div style="background:var(--grad-navy)">
<section style="position:relative;overflow:hidden;padding:88px 0">
  <div style="position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.6;pointer-events:none"></div>
  <div class="container" style="position:relative;max-width:820px">
    <span class="eyebrow" style="color:var(--yb-cyan)">Why YB for SEO</span>
    <h2 style="margin:14px 0 18px;color:#fff;font-size:clamp(1.8rem,2.6vw,2.4rem);line-height:1.12">{esc(loc["whyYb"]["heading"])}</h2>
    <p style="color:var(--fg2-on-dark);font-size:16px;line-height:1.75;margin:0 0 28px">{esc(loc["whyYb"]["body"])}</p>
    <a href="{p}contact.html" class="btn btn-grad">Let's Talk
      <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
    </a>
  </div>
</section>
</div>

<!-- PROCESS -->
<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>
<section style="background:var(--bg-soft)">
  <div class="container">
    <div style="text-align:center;max-width:640px;margin:0 auto 44px">
      <span class="eyebrow" style="color:#2BC4F0">Our Process</span>
      <h2 style="margin:14px 0 12px">How We Get You Ranking</h2>
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px" class="why-tiles-grid">
      <div style="background:#fff;border-radius:var(--r-lg);padding:28px;border:1px solid var(--line);box-shadow:0 2px 8px rgba(22,32,58,.05)">
        <h3 style="font-family:var(--font-display);font-weight:800;font-size:16px;color:var(--ink);margin:0 0 12px;text-transform:uppercase;letter-spacing:.04em">SEO Site Audit</h3>
        <p style="color:var(--fg2);font-size:14px;line-height:1.65;margin:0">We start with a free review of your rankings, technical health, content gaps, and local visibility.</p>
      </div>
      <div style="background:#fff;border-radius:var(--r-lg);padding:28px;border:1px solid var(--line);box-shadow:0 2px 8px rgba(22,32,58,.05)">
        <h3 style="font-family:var(--font-display);font-weight:800;font-size:16px;color:var(--ink);margin:0 0 12px;text-transform:uppercase;letter-spacing:.04em">Keyword &amp; Content Plan</h3>
        <p style="color:var(--fg2);font-size:14px;line-height:1.65;margin:0">Together we map the searches that matter most and build pages and content that answer them clearly.</p>
      </div>
      <div style="background:#fff;border-radius:var(--r-lg);padding:28px;border:1px solid var(--line);box-shadow:0 2px 8px rgba(22,32,58,.05)">
        <h3 style="font-family:var(--font-display);font-weight:800;font-size:16px;color:var(--ink);margin:0 0 12px;text-transform:uppercase;letter-spacing:.04em">Rankings That Drive Leads</h3>
        <p style="color:var(--fg2);font-size:14px;line-height:1.65;margin:0">With ongoing optimization, reporting, and refinement, we help you climb in Google and turn visibility into calls and form fills.</p>
      </div>
    </div>
  </div>
</section>

<!-- LOCAL SIGNALS -->
<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div>
<div style="background:var(--grad-navy)">
<section style="padding:56px 0">
  <div class="container">
    <p style="color:rgba(255,255,255,.45);font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;margin:0 0 16px;text-align:center">Serving {esc(city)} &amp; Surrounding Areas</p>
    <div style="overflow:hidden;border-radius:var(--r-lg)">
{signals_html}
    </div>
  </div>
</section>
</div>

{reviews_html}

<!-- FAQ -->
<section style="background:#fff">
  <div class="container">
    <div style="text-align:center;max-width:700px;margin:0 auto 48px">
      <span class="eyebrow" style="color:#2BC4F0">Common Questions</span>
      <h2 style="margin:14px 0 14px">{esc(city)} SEO — Frequently Asked Questions</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">Answers to the questions we hear most often about SEO in {esc(city)}.</p>
    </div>
    <div style="max-width:760px;margin:0 auto;border-top:1px solid var(--line)">
{faqs_html}
    </div>
  </div>
</section>

{contact_html}

<!-- CTA -->
<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div>
<div style="background:var(--grad-navy)">
<div class="svc-cta">
  <div class="svc-cta-mesh"></div>
  <div class="container svc-cta-inner">
    <span class="eyebrow" style="color:var(--yb-cyan)">Ready to Grow?</span>
    <h2 style="margin:14px 0 14px;color:#fff;font-size:clamp(1.8rem,2.6vw,2.4rem)">Let&rsquo;s Talk About Your Goals</h2>
    <p style="color:var(--fg2-on-dark);font-size:16px;margin-bottom:32px">Schedule a free consultation and let our team build a custom strategy for your business.</p>
    <div class="svc-cta-btns">
      <a href="{p}contact.html" class="btn btn-grad btn-lg">Get Started Today</a>
      <a href="tel:5099019735" class="btn btn-ghost-white btn-lg">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 16 0 0 0 6.07 6.07l1.08-.9a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        509-901-9735
      </a>
    </div>
  </div>
</div>
</div>

{footer}

{hubspot_script_tags(p)}
<script src="{p}js/newsletter-popup.js" defer></script>
<script src="{p}js/chat-widget.js" defer></script>
<script src="{p}js/site.js"></script>
<script>
function toggleFaq(id, accent) {{
  document.documentElement.style.setProperty('--faq-ac', accent || 'var(--yb-blue)');
  var item = document.getElementById(id);
  if (!item) return;
  var btn = item.querySelector('.faq-q');
  var ans = item.querySelector('.faq-a');
  var open = btn.classList.contains('active');
  document.querySelectorAll('.faq-q.active').forEach(function(b) {{
    b.classList.remove('active');
    var a = b.closest('.faq-item').querySelector('.faq-a');
    if (a) a.style.maxHeight = '0';
  }});
  if (!open) {{
    btn.classList.add('active');
    ans.style.maxHeight = ans.scrollHeight + 'px';
  }}
}}
</script>
</body>
</html>
"""


def main() -> None:
    if not DATA_FILE.exists():
        raise SystemExit(f"Missing {DATA_FILE}")
    OUT_DIR.mkdir(exist_ok=True)
    locations = load_locations()
    for loc in locations:
        out = OUT_DIR / f"{loc['slug']}.html"
        out.write_text(render_page(loc), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")
    print(f"generated {len(locations)} local SEO pages")


if __name__ == "__main__":
    main()
