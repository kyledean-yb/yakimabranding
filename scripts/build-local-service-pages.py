#!/usr/bin/env python3
"""Generate localized service landing pages (web design, Google Ads, social, branding)."""

import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "../"
PARTIALS = ROOT / "partials" / "local-service"

sys.path.insert(0, str(ROOT / "scripts"))
from service_local_config import PROCESS_STEPS, SERVICE_CONFIGS
from schema_markup import seo_head_html
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_staging_seo_snippet import STAGING_ROBOTS_META
from site_footer_snippet import site_footer_html
from site_nav_snippet import site_header_html

LOC_PIN = (
    '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'
    "</svg>"
)

BRAND_ACCordion_CSS = """
.brand-acc{display:flex;flex-direction:column;gap:10px;max-width:920px;margin:0 auto}
.brand-acc-item{background:#fff;border:1px solid var(--line);border-radius:var(--r-xl);overflow:hidden;box-shadow:0 2px 12px rgba(22,32,58,.05);scroll-margin-top:100px;transition:border-color 200ms,box-shadow 200ms}
.brand-acc-item.is-open{border-color:rgba(123,91,230,.35);box-shadow:0 8px 28px rgba(123,91,230,.12)}
.brand-acc-trigger{display:flex;align-items:center;gap:16px;width:100%;padding:20px 24px;background:transparent;border:none;cursor:pointer;text-align:left;font-family:var(--font-body)}
.brand-acc-trigger:hover{background:rgba(123,91,230,.04)}
.brand-acc-item.is-open .brand-acc-trigger{background:rgba(123,91,230,.06)}
.brand-acc-heading{flex:1;min-width:0}
.brand-acc-title{display:block;font-family:var(--font-display);font-weight:700;font-size:clamp(1rem,1.8vw,1.15rem);color:var(--ink);margin-top:5px;line-height:1.25}
.brand-acc-icon{width:32px;height:32px;border-radius:50%;background:var(--bg-mute);display:flex;align-items:center;justify-content:center;flex:none;color:var(--fg2);transition:transform 280ms ease,background 200ms,color 200ms}
.brand-acc-item.is-open .brand-acc-icon{background:var(--yb-violet);color:#fff;transform:rotate(45deg)}
.brand-acc-panel{max-height:0;overflow:hidden;transition:max-height 380ms cubic-bezier(.16,1,.3,1)}
.brand-acc-panel-inner{padding:0 24px 28px;border-top:1px solid var(--line)}
.brand-acc-content{display:grid;grid-template-columns:1fr 1fr;gap:32px;align-items:center;padding-top:24px}
.brand-acc-content--text{grid-template-columns:1fr;padding-top:20px}
.brand-block-num{width:32px;height:32px;border-radius:var(--r-md);background:var(--wash-violet);color:var(--yb-violet);font-family:var(--font-display);font-weight:800;font-size:14px;display:flex;align-items:center;justify-content:center;flex:none}
.brand-block-tag{font-weight:700;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--yb-violet)}
.brand-block-media{border-radius:var(--r-xl);overflow:hidden;background:var(--bg-soft);border:1px solid var(--line);box-shadow:0 8px 32px rgba(22,32,58,.08)}
.brand-block-media img{width:100%;height:auto;display:block}
.brand-block-copy p{color:var(--fg2);font-size:15.5px;line-height:1.8;margin:0 0 18px}
@media(max-width:900px){.brand-acc-content{grid-template-columns:1fr;gap:24px}.brand-acc-trigger{padding:18px 20px}.brand-acc-panel-inner{padding:0 20px 24px}}
"""


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def load_locations(config: dict) -> list[dict]:
    export_name = config["export_name"]
    data_file = config["data_file"]
    script = (
        f"import {{ {export_name} }} from './{data_file}';"
        f"process.stdout.write(JSON.stringify({export_name}));"
    )
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=ROOT / "data",
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def load_partial(name: str, prefix: str) -> str:
    text = (PARTIALS / name).read_text(encoding="utf-8")
    return text.replace("../", prefix)


def schema_json(loc: dict, config: dict) -> tuple[str, str]:
    city = loc["city"]
    service_name = config["service_label"]
    local_business = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "YB Marketing",
        "url": "https://yakimabranding.com",
        "telephone": "+15099019735",
        "email": "info@yakimabranding.com",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": loc["schema"]["addressLocality"],
            "addressRegion": loc["schema"]["addressRegion"],
            "addressCountry": loc["schema"].get("addressCountry", "US"),
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
                "name": service_name,
                "item": f"https://yakimabranding.com/{config['folder']}",
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": f"{city} {service_name}",
                "item": loc["canonicalUrl"],
            },
        ],
    }
    return json.dumps(local_business, ensure_ascii=False), json.dumps(
        breadcrumb, ensure_ascii=False
    )


def render_faqs(loc: dict, accent: str) -> str:
    slug = loc["slug"]
    items = []
    for i, faq in enumerate(loc["faqs"], start=1):
        fid = f"{slug}-faq-{i}"
        items.append(
            f"""      <div class="faq-item" id="{fid}">
        <button class="faq-q" onclick="toggleFaq('{fid}', '{accent}')">
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


def render_process_steps(service_key: str) -> str:
    cards = []
    for label, body in PROCESS_STEPS[service_key]:
        cards.append(
            f"""      <div style="background:#fff;border-radius:var(--r-lg);padding:28px;border:1px solid var(--line);box-shadow:0 2px 8px rgba(22,32,58,.05)">
        <h3 style="font-family:var(--font-display);font-weight:800;font-size:16px;color:var(--ink);margin:0 0 12px;text-transform:uppercase;letter-spacing:.04em">{esc(label)}</h3>
        <p style="color:var(--fg2);font-size:14px;line-height:1.65;margin:0">{esc(body)}</p>
      </div>"""
        )
    return "\n".join(cards)


def render_hero_orbit(prefix: str, city: str, service_label: str, config: dict) -> str:
    return f"""    <div class="svc-hero-visual">
      <div class="hero-orbit hero-orbit--svc hero-orbit--features" style="{config['orbit_style']}">
        <div class="hero-orbit-bg" aria-hidden="true">
          <div class="hero-orbit-ring hero-orbit-ring--track"></div>
          <div class="hero-orbit-hub">
            <div class="hero-orbit-hub-art">
              <img src="{prefix}assets/{config['hub_image']}" alt="{esc(service_label)} in {esc(city)}">
            </div>
          </div>
        </div>
        <div class="hero-orbit-spin">
          <div class="hero-orbit-node" style="--i:0"><div class="hero-orbit-icon"><span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg></span></span></div></div>
          <div class="hero-orbit-node" style="--i:1"><div class="hero-orbit-icon"><span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg></span></span></div></div>
          <div class="hero-orbit-node" style="--i:2"><div class="hero-orbit-icon"><span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/></svg></span></span></div></div>
          <div class="hero-orbit-node" style="--i:3"><div class="hero-orbit-icon"><span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></span></span></div></div>
          <div class="hero-orbit-node" style="--i:4"><div class="hero-orbit-icon"><span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/></svg></span></span></div></div>
          <div class="hero-orbit-node" style="--i:5"><div class="hero-orbit-icon"><span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg></span></span></div></div>
        </div>
      </div>
    </div>"""


def what_we_do_section(loc: dict, config: dict, accent: str) -> str:
    if config["layout"] == "google-ads":
        block = loc["googleAdsIntro"]
        heading = block["heading"]
        intro = block["intro"]
        local = block["localParagraph"]
    else:
        block = loc["whatWeDo"]
        heading = block["heading"]
        intro = block["intro"]
        local = block["localParagraph"]
    return f"""
<section style="background:#fff">
  <div class="container">
    <div style="text-align:center;max-width:760px;margin:0 auto 20px">
      <span class="eyebrow" style="color:{accent}">What We Do</span>
      <h2 style="margin:14px 0 16px">{esc(heading)}</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">{esc(intro)}</p>
    </div>
    <p class="local-intro">{esc(local)}</p>
  </div>
</section>"""


def service_specific_sections(loc: dict, config: dict, prefix: str) -> str:
    layout = config["layout"]
    accent = config["accent"]
    parts = []

    if layout in ("web-design", "social-media"):
        features = load_partial(config["features_partial"], prefix)
        features = features.replace('style="color:#159468"', f'style="color:{accent}"')
        features = features.replace('style="color:#c77f12"', f'style="color:{accent}"')
        parts.append(f"""
<div class="wave-div" style="background:#ffffff"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,70 C480,0 960,0 1440,70 L1440,70 L0,70 Z" fill="#ffffff"/></svg></div>
<section style="background:#fff">
  <div class="container">
{features}
  </div>
</section>""")
        platforms = load_partial(config["platforms_partial"], prefix)
        platforms = platforms.replace('style="color:#159468"', f'style="color:{accent}"')
        platforms = platforms.replace('style="color:#c77f12"', f'style="color:{accent}"')
        parts.append(platforms)

    elif layout == "google-ads":
        included = load_partial(config["included_partial"], prefix)
        perfmax = load_partial(config["perfmax_partial"], prefix)
        parts.append(f"""
<div class="wave-div" style="background:#ffffff"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,70 C480,0 960,0 1440,70 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>
{included}
{perfmax}""")

    elif layout == "branding":
        accordion = load_partial(config["accordion_partial"], prefix)
        parts.append(f"""
<div class="wave-div" style="background:#ffffff"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,70 C480,0 960,0 1440,70 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>
<section style="background:var(--bg-soft);padding:72px 0">
  <div class="container">
{accordion}
  </div>
</section>""")

    return "\n".join(parts)


def render_page(loc: dict, config: dict) -> str:
    p = PREFIX
    city = loc["city"]
    slug = loc["slug"]
    service_key = config["layout"]
    accent = config["accent"]
    schema_head = seo_head_html(f"{config['folder']}/{slug}.html")
    header = site_header_html(p).strip()
    footer = site_footer_html(p).strip()
    faqs_html = render_faqs(loc, accent)
    signals_html = render_local_signals(loc["localSignals"])
    process_html = render_process_steps(service_key)
    orbit_html = render_hero_orbit(p, city, config["service_label"], config)
    contact_html = load_partial("contact-section.html", p).replace(
        'style="color:#159468"', f'style="color:{accent}"'
    ).replace('style="color:#FF6B57"', f'style="color:{accent}"')
    hero_aria = f'{config["service_label"]} in {city}'
    eyebrow = loc["hero"].get("eyebrow", config["service_label"].upper())

    extra_css = BRAND_ACCordion_CSS if service_key == "branding" else ""
    brand_script = (
        f'\n<script src="{p}js/brand-accordion.js" defer></script>'
        if service_key == "branding"
        else ""
    )

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
<link rel="stylesheet" href="{p}site.css">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--font-body);background:var(--bg);color:var(--fg1);-webkit-font-smoothing:antialiased;overflow-x:hidden}}
::selection{{background:var(--yb-blue);color:#fff}}
img{{display:block;max-width:100%}}
a{{color:inherit;text-decoration:none}}
.container{{width:100%;max-width:var(--container);margin:0 auto;padding:0 28px}}
section{{padding:88px 0}}
.eyebrow{{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-body);font-weight:700;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--yb-blue)}}
.eyebrow::before{{content:'';display:block;width:7px;height:7px;border-radius:50%;background:currentColor;flex:none}}
.btn{{display:inline-flex;align-items:center;gap:8px;border:none;cursor:pointer;font-family:var(--font-body);font-weight:700;font-size:15px;border-radius:var(--r-md);padding:13px 22px;transition:all 240ms;white-space:nowrap;line-height:1}}
.btn-grad{{background:var(--grad-brand);color:#fff;box-shadow:0 14px 30px -10px rgba(63,111,214,.45)}}
.btn-grad:hover{{transform:translateY(-2px);filter:brightness(1.06)}}
.btn-lg{{padding:16px 28px;font-size:16px}}
.btn-ghost-white{{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.35)}}
.btn-ghost-white:hover{{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.6)}}
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
.yb-lead{{color:var(--fg2);font-size:16px;line-height:1.75}}
{extra_css}
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
    <img src="{p}assets/yb-logo-white.png" alt="">
  </div>
  <div class="container svc-hero-inner">
    <div class="svc-hero-text">
      <span class="eyebrow" style="color:{accent}">{esc(eyebrow)}</span>
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
      <p style="margin-top:20px;font-size:14px"><a href="{p}{config['parent_href']}" style="color:var(--yb-cyan);font-weight:600">View all {esc(config['parent_name'])} services →</a></p>
    </div>
{orbit_html}
  </div>
</section>

<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 80" preserveAspectRatio="none" style="height:80px"><path d="M0,0 C360,80 1080,80 1440,0 L1440,80 L0,80 Z" fill="#ffffff"/></svg></div>

{what_we_do_section(loc, config, accent)}
{service_specific_sections(loc, config, p)}

<!-- WHY YB -->
<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div>
<div style="background:var(--grad-navy)">
<section style="position:relative;overflow:hidden;padding:88px 0">
  <div style="position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.6;pointer-events:none"></div>
  <div class="container" style="position:relative;max-width:820px">
    <span class="eyebrow" style="color:var(--yb-cyan)">{esc(config["why_eyebrow"])}</span>
    <h2 style="margin:14px 0 18px;color:#fff;font-size:clamp(1.8rem,2.6vw,2.4rem);line-height:1.12">{esc(loc["whyYb"]["heading"])}</h2>
    <p style="color:var(--fg2-on-dark);font-size:16px;line-height:1.75;margin:0 0 28px">{esc(loc["whyYb"]["body"])}</p>
    <a href="{p}contact.html" class="btn btn-grad">Let&rsquo;s Talk
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
      <span class="eyebrow" style="color:{accent}">Our Process</span>
      <h2 style="margin:14px 0 12px">{esc(config["process_title"])}</h2>
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px" class="why-tiles-grid">
{process_html}
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

<!-- FAQ -->
<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z" fill="#ffffff"/></svg></div>
<section style="background:#fff">
  <div class="container">
    <div style="text-align:center;max-width:700px;margin:0 auto 48px">
      <span class="eyebrow" style="color:{accent}">Common Questions</span>
      <h2 style="margin:14px 0 14px">{esc(city)} {esc(config['service_label'])} — Frequently Asked Questions</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">Answers to the questions we hear most often about {esc(config['service_label'].lower())} in {esc(city)}.</p>
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
    <h2 style="margin:14px 0 14px;color:#fff;font-size:clamp(1.8rem,2.6vw,2.4rem)">{esc(config["cta_heading"])}</h2>
    <p style="color:var(--fg2-on-dark);font-size:16px;margin-bottom:32px">{esc(config["cta_sub"])}</p>
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

<script src="{p}js/contact-forms.js" defer></script>
<script src="{p}js/newsletter-popup.js" defer></script>
<script src="{p}js/site.js"></script>
<script>
function toggleFaq(id, accent) {{
  var item = document.getElementById(id);
  if (!item) return;
  var btn = item.querySelector('.faq-q');
  var panel = item.querySelector('.faq-a');
  var open = btn.classList.contains('active');
  document.querySelectorAll('.faq-q.active').forEach(function(b) {{
    b.classList.remove('active');
    b.closest('.faq-item').querySelector('.faq-a').style.maxHeight = null;
    b.closest('.faq-item').style.removeProperty('--faq-ac');
  }});
  if (!open) {{
    btn.classList.add('active');
    item.style.setProperty('--faq-ac', accent);
    panel.style.maxHeight = panel.scrollHeight + 'px';
  }}
}}
</script>{brand_script}
</body>
</html>"""


def main() -> None:
    total = 0
    for service_key, config in SERVICE_CONFIGS.items():
        out_dir = ROOT / config["folder"]
        out_dir.mkdir(parents=True, exist_ok=True)
        locations = load_locations(config)
        for loc in locations:
            path = out_dir / f"{loc['slug']}.html"
            path.write_text(render_page(loc, config), encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)}")
            total += 1
    print(f"generated {total} local service pages")


if __name__ == "__main__":
    main()
