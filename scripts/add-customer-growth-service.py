#!/usr/bin/env python3
"""Add Customer Growth & Communication Tool service page and nav entry sitewide."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from schema_markup import seo_head_html
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_footer_snippet import site_footer_html
from site_lead_form_snippet import lead_form_html
from site_nav_snippet import site_header_html
from site_staging_seo_snippet import STAGING_ROBOTS_META
from site_tracking_snippet import ATTRIBUTER_FOOTER_BLOCK, GTM_BODY_NOSCRIPT_BLOCK, TRACKING_HEAD_BLOCK

SLUG = "customer-growth"
LABEL = "Customer Growth & Communication Tool"
DESC = "CRM, messaging & automation"
ICON_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>'
    '<circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/>'
    '<path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
)
# Users icon for CRM / team relationships
DD_CARD_EN = (
    f'<a href="/{SLUG}" class="dd-card"><div class="dd-ic" style="background:var(--wash-blue);'
    f'color:var(--yb-blue)">{ICON_SVG}</div><div><span class="dd-name">{LABEL}</span>'
    f'<span class="dd-desc">{DESC}</span></div></a>'
)
DD_CARD_ES = (
    f'<a href="/es/{SLUG}" class="dd-card"><div class="dd-ic" style="background:var(--wash-blue);'
    f'color:var(--yb-blue)">{ICON_SVG}</div><div><span class="dd-name">Herramienta de crecimiento '
    f'y comunicación</span><span class="dd-desc">CRM, mensajería y automatización</span></div></a>'
)
# Relative-path variants used in older generated nav
DD_CARD_REL = (
    f'<a href="{{prefix}}services/{SLUG}.html" class="dd-card"><div class="dd-ic" '
    f'style="background:var(--wash-blue);color:var(--yb-blue)">{ICON_SVG}</div>'
    f'<div><span class="dd-name">{LABEL}</span><span class="dd-desc">{DESC}</span></div></a>'
)

FOOTER_LI_EN = f'<li><a href="/{SLUG}">{LABEL}</a></li>'
FOOTER_LI_ES = (
    f'<li><a href="/es/{SLUG}">Herramienta de crecimiento y comunicación</a></li>'
)

# Marker: insert after Content & Blogging card
AFTER_CONTENT_MARKERS = [
    # Absolute clean URLs (current site)
    re.compile(
        r'(<a href="/content-marketing" class="dd-card">.*?</a>)',
        re.S,
    ),
    re.compile(
        r'(<a href="/es/content-marketing" class="dd-card">.*?</a>)',
        re.S,
    ),
    # Relative services paths (blog builder / older pages)
    re.compile(
        r'(<a href="[^"]*services/content-creation\.html" class="dd-card">.*?</a>)',
        re.S,
    ),
]

FOOTER_AFTER = re.compile(
    r'(<li><a href="[^"]*(?:content-marketing|content-creation)[^"]*"[^>]*>[^<]*(?:Content Marketing|Marketing de contenidos)[^<]*</a></li>)',
    re.I,
)


def build_service_page() -> str:
    prefix = "../"
    header = site_header_html(prefix, current_path=f"/{SLUG}").strip()
    footer = site_footer_html(prefix, current_path=f"/{SLUG}").strip()
    form = lead_form_html(
        "Customer Growth Service Page",
        redirect="/services/thank-you-customer-growth",
        default_interest="customer-growth",
    )
    seo = seo_head_html(f"{SLUG}/index.html")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="../favicon.png" type="image/png">
<link rel="apple-touch-icon" href="../favicon.png">
{STAGING_ROBOTS_META}
<title>Customer Growth &amp; Communication Tool | YB Marketing | 509-901-9735</title>
<meta name="description" content="Organize every lead, centralize every conversation, and automate follow-up with YB Marketing's Customer Growth &amp; Communication Tool — CRM, messaging, and automation for Pacific Northwest businesses.">
<link rel="stylesheet" href="../colors_and_type.css">
<link rel="stylesheet" href="../insights.css">
<link rel="stylesheet" href="../lead-form.css">
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
.header{{position:sticky;top:0;z-index:50;transition:all 240ms cubic-bezier(.4,0,.2,1)}}
.header.solid{{background:rgba(255,255,255,.88);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}}
.header.top{{background:rgba(255,255,255,.6);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid transparent}}
.header-inner{{display:flex;align-items:center;justify-content:space-between;height:72px}}
.logo{{display:flex;align-items:center;gap:11px}}
.logo img{{width:44px;height:44px}}
.logo-text{{font-family:var(--font-display);font-weight:800;font-size:22px;letter-spacing:-.02em;color:var(--ink)}}
.logo-text span{{color:var(--yb-blue)}}
.nav{{display:flex;align-items:center;gap:2px}}
.nav-a{{font-weight:600;font-size:15px;color:var(--fg1);padding:8px 14px;border-radius:var(--r-sm);transition:all 240ms;display:inline-block}}
.nav-a:hover{{background:var(--bg-soft);color:var(--yb-blue)}}
.nav-services,.nav-about{{position:relative}}
.nav-svc-btn{{display:flex;align-items:center;gap:5px;font-weight:600;font-size:15px;color:var(--fg1);padding:8px 14px;border-radius:var(--r-sm);transition:all 240ms;background:none;border:none;cursor:pointer;font-family:var(--font-body)}}
.nav-svc-btn:hover,.nav-services:hover .nav-svc-btn,.nav-about:hover .nav-svc-btn{{background:var(--bg-soft);color:var(--yb-blue)}}
.nav-chevron{{transition:transform 240ms;flex:none;color:currentColor}}
.nav-services:hover .nav-chevron,.nav-about:hover .nav-chevron{{transform:rotate(180deg)}}
.nav-dd{{position:absolute;top:calc(100% + 10px);left:50%;transform:translateX(-50%) translateY(-10px) scale(.97);opacity:0;pointer-events:none;transition:opacity 200ms ease 150ms,transform 220ms cubic-bezier(.16,1,.3,1) 150ms;width:720px;background:#fff;border-radius:var(--r-xl);box-shadow:0 24px 64px -16px rgba(22,32,58,.22),0 0 0 1px rgba(22,32,58,.07);padding:16px;z-index:200}}
.nav-services:hover .nav-dd,.nav-about:hover .nav-dd,.nav-services.is-open .nav-dd,.nav-about.is-open .nav-dd{{opacity:1;transform:translateX(-50%) translateY(0) scale(1);pointer-events:all;transition:opacity 150ms ease,transform 180ms cubic-bezier(.16,1,.3,1)}}
.nav-dd-arrow{{position:absolute;top:-5px;left:50%;transform:translateX(-50%) rotate(45deg);width:10px;height:10px;background:#fff;border-top:1px solid rgba(22,32,58,.08);border-left:1px solid rgba(22,32,58,.08)}}
.nav-dd-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}}
.dd-card{{display:flex;align-items:flex-start;gap:11px;padding:12px;border-radius:var(--r-md);transition:background 150ms ease}}
.dd-card:hover{{background:var(--bg-soft)}}
.dd-ic{{width:36px;height:36px;border-radius:var(--r-sm);display:flex;align-items:center;justify-content:center;flex:none}}
.dd-ic svg{{width:18px;height:18px}}
.dd-name{{font-weight:700;font-size:13px;color:var(--ink);margin-bottom:2px;display:block;line-height:1.3}}
.dd-desc{{font-size:11.5px;color:var(--fg3);line-height:1.4}}
.btn{{display:inline-flex;align-items:center;gap:8px;border:none;cursor:pointer;font-family:var(--font-body);font-weight:700;font-size:15px;border-radius:var(--r-md);padding:13px 22px;transition:all 240ms;white-space:nowrap;line-height:1}}
.btn-grad{{background:var(--grad-brand);color:#fff;box-shadow:0 14px 30px -10px rgba(63,111,214,.45)}}
.btn-grad:hover{{transform:translateY(-2px);filter:brightness(1.06)}}
.btn-ghost-white{{background:rgba(255,255,255,.12);color:#fff;border:1.5px solid rgba(255,255,255,.28)}}
.btn-ghost-white:hover{{background:rgba(255,255,255,.22);transform:translateY(-2px)}}
.btn-lg{{padding:16px 28px;font-size:16px}}
.hamburger{{display:none;background:none;border:none;cursor:pointer;padding:6px;align-items:center;justify-content:center}}
.mobile-menu{{display:none;border-top:1px solid var(--line);background:#fff;padding:12px 28px 20px}}
.mobile-menu a,.mobile-menu button{{display:block;padding:14px 0;border-bottom:1px solid var(--line);font-weight:600;font-size:17px;color:var(--ink);width:100%;text-align:left;background:none;border:none;font-family:var(--font-body);cursor:pointer}}
.mobile-svc-list{{display:none;padding:8px 0 8px 16px}}
.mobile-svc-list.open{{display:block}}
.mobile-svc-list a{{font-size:15px;padding:10px 0;color:var(--fg2)}}
.svc-hero{{position:relative;overflow:hidden;background:var(--grad-navy);padding:80px 0 100px}}
.svc-hero-mesh{{position:absolute;inset:0;background-image:var(--grad-mesh);pointer-events:none}}
.svc-hero-inner{{position:relative;display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:center}}
.svc-hero h1{{margin:16px 0 20px;font-size:clamp(2.1rem,3.8vw,3.4rem);color:#fff;line-height:1.08}}
.hero-lead{{margin:0 0 32px;color:var(--fg2-on-dark);max-width:540px;font-size:clamp(1rem,1.3vw,1.2rem);line-height:1.6}}
.svc-hero-actions{{display:flex;gap:14px;flex-wrap:wrap}}
.feat-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
.feat-card{{background:#fff;border-radius:var(--r-lg);padding:26px;border:1px solid var(--line);box-shadow:0 2px 8px rgba(22,32,58,.06);transition:all 240ms}}
.feat-card:hover{{transform:translateY(-4px);box-shadow:0 12px 32px -8px rgba(22,32,58,.14)}}
.feat-ic{{width:48px;height:48px;border-radius:var(--r-md);display:flex;align-items:center;justify-content:center;margin-bottom:16px}}
.feat-ic svg{{width:22px;height:22px}}
.feat-title{{font-family:var(--font-display);font-weight:700;font-size:16px;color:var(--ink);margin-bottom:7px}}
.feat-desc{{font-size:14px;color:var(--fg2);line-height:1.6}}
.pain-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}}
.pain-card{{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:20px 16px;text-align:center}}
.pain-card strong{{display:block;font-size:14px;color:var(--ink);margin-bottom:6px;line-height:1.35}}
.pain-card span{{font-size:13px;color:var(--fg2);line-height:1.45}}
.svc-cta{{background:var(--grad-navy);position:relative;overflow:hidden;padding:80px 0}}
.svc-cta-mesh{{position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.7}}
.svc-cta-inner{{position:relative;text-align:center;max-width:680px;margin:0 auto}}
.svc-cta h2{{color:#fff;margin-bottom:14px}}
.svc-cta p{{color:var(--fg2-on-dark);font-size:16px;margin-bottom:32px}}
.svc-cta-btns{{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}}
.wave-div{{position:relative;overflow:hidden;line-height:0;font-size:0}}
.wave-div svg{{display:block;width:100%;height:70px}}
.footer{{background:var(--grad-navy);color:#fff;position:relative;overflow:hidden;padding:64px 0 28px}}
.footer-mesh{{position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.5;pointer-events:none}}
.footer-grid{{position:relative;display:grid;grid-template-columns:1.7fr 1fr 1fr 1.4fr;gap:40px;margin-bottom:42px}}
.footer-brand p{{color:var(--fg2-on-dark);font-size:14px;max-width:280px;margin:14px 0 18px}}
.footer-col h4{{font-family:var(--font-display);font-size:14px;font-weight:700;margin-bottom:14px;letter-spacing:.04em;color:#fff}}
.footer-col ul{{list-style:none;display:grid;gap:10px}}
.footer-col a{{color:var(--fg2-on-dark);font-size:14px;transition:color 240ms}}
.footer-col a:hover{{color:#fff}}
.footer-bottom{{position:relative;border-top:1px solid rgba(255,255,255,.12);padding-top:22px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;color:var(--fg2-on-dark);font-size:13px}}
.social-btn{{width:38px;height:38px;border-radius:var(--r-sm);background:rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;color:#fff;transition:background 240ms}}
.social-btn:hover{{background:var(--yb-blue)}}
.faq-item{{border-bottom:1px solid var(--line)}}
.faq-q{{display:flex;justify-content:space-between;align-items:center;padding:20px 0;cursor:pointer;font-weight:700;font-size:15.5px;color:var(--ink);gap:16px;background:none;border:none;width:100%;text-align:left;font-family:var(--font-body);transition:color 200ms}}
.faq-q:hover{{color:var(--yb-blue)}}
.faq-q.active{{color:var(--faq-ac,var(--yb-blue))}}
.faq-icon{{width:28px;height:28px;border-radius:50%;background:var(--bg-mute);display:flex;align-items:center;justify-content:center;flex:none;transition:background 200ms,transform 200ms;color:var(--fg2)}}
.faq-q.active .faq-icon{{background:var(--faq-ac,var(--yb-blue));color:#fff;transform:rotate(45deg)}}
.faq-a{{max-height:0;overflow:hidden;transition:max-height 320ms cubic-bezier(.16,1,.3,1)}}
.faq-a-inner{{padding-bottom:20px;font-size:15px;color:var(--fg2);line-height:1.75}}
.footer-socials{{display:flex;gap:10px;margin-top:12px}}
@media(max-width:1100px){{.nav,.btn-hdr{{display:none}}.hamburger{{display:flex}}.nav-dd{{display:none}}.mobile-menu.open{{display:block}}}}
@media(max-width:900px){{.svc-hero-inner{{grid-template-columns:1fr}}.svc-hero-visual{{display:none}}.feat-grid{{grid-template-columns:1fr 1fr}}.pain-grid{{grid-template-columns:1fr 1fr}}.footer-grid{{grid-template-columns:1fr 1fr}}}}
@media(max-width:640px){{.feat-grid,.pain-grid,.footer-grid{{grid-template-columns:1fr}}section{{padding:60px 0}}}}
</style>
<link rel="stylesheet" href="../site.css">
{seo}
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
      <span class="eyebrow" style="color:var(--yb-cyan)">CRM &amp; Automation</span>
      <h1>Customer Growth &amp;<br><span style="background:linear-gradient(135deg,var(--yb-cyan),var(--yb-blue));-webkit-background-clip:text;background-clip:text;color:transparent">Communication Tool</span></h1>
      <p class="hero-lead">Organize every lead, centralize every conversation, and automate the follow-up that turns interest into customers — all in one tool.</p>
      <div class="svc-hero-actions">
        <a href="/contact" class="btn btn-grad btn-lg">Get Started Today
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </a>
        <a href="tel:5099019735" class="btn btn-ghost-white">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 16 0 0 0 6.07 6.07l1.08-.9a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          509-901-9735
        </a>
      </div>
    </div>
    <div class="svc-hero-visual">
      <div class="hero-orbit hero-orbit--svc hero-orbit--features" style="--orbit-feat-wash:var(--wash-blue);--orbit-feat-color:var(--yb-blue);--orbit-feat-glow:rgba(63,111,214,0.22)">
        <div class="hero-orbit-bg" aria-hidden="true">
          <div class="hero-orbit-ring hero-orbit-ring--track"></div>
          <div class="hero-orbit-hub">
            <div class="hero-orbit-hub-art">
              <img src="../assets/yb-logo-white.png" alt="YB Marketing Customer Growth and Communication Tool">
            </div>
          </div>
        </div>
        <div class="hero-orbit-spin">
          <div class="hero-orbit-node" style="--i:0">
            <div class="hero-orbit-icon" aria-label="Lead Management">
              <span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></span></span>
            </div>
          </div>
          <div class="hero-orbit-node" style="--i:1">
            <div class="hero-orbit-icon" aria-label="Sales Pipeline">
              <span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg></span></span>
            </div>
          </div>
          <div class="hero-orbit-node" style="--i:2">
            <div class="hero-orbit-icon" aria-label="Email &amp; SMS">
              <span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></span></span>
            </div>
          </div>
          <div class="hero-orbit-node" style="--i:3">
            <div class="hero-orbit-icon" aria-label="Automation">
              <span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg></span></span>
            </div>
          </div>
          <div class="hero-orbit-node" style="--i:4">
            <div class="hero-orbit-icon" aria-label="Landing Pages">
              <span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg></span></span>
            </div>
          </div>
          <div class="hero-orbit-node" style="--i:5">
            <div class="hero-orbit-icon" aria-label="Analytics">
              <span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg></span></span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 80" preserveAspectRatio="none" style="height:80px"><path d="M0,0 C360,80 1080,80 1440,0 L1440,80 L0,80 Z" fill="#ffffff"/></svg></div>

<section style="background:#fff">
  <div class="container">
    <div style="text-align:center;max-width:720px;margin:0 auto 44px">
      <span class="eyebrow">Everyday Friction</span>
      <h2 style="margin:14px 0 16px">Turn business problems into a clearer path to growth</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">YB Marketing's Customer Growth &amp; Communication Tool brings lead management, communication, automation, and customer follow-up together so your team can move faster without adding more disconnected tools.</p>
    </div>
    <div class="pain-grid">
      <div class="pain-card"><strong>Repetitive tasks?</strong><span>Save up to 10+ hours a week</span></div>
      <div class="pain-card"><strong>No time for reviews?</strong><span>Automate review &amp; referral requests</span></div>
      <div class="pain-card"><strong>Feeling disorganized?</strong><span>Manage every customer in one place</span></div>
      <div class="pain-card"><strong>Missed calls?</strong><span>Never lose a hot lead</span></div>
      <div class="pain-card"><strong>Slow follow-up?</strong><span>Respond the moment a lead acts</span></div>
    </div>
  </div>
</section>

<div class="wave-div" style="background:#ffffff"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,70 C480,0 960,0 1440,70 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>

<section style="background:var(--bg-soft)">
  <div class="container">
    <div style="text-align:center;max-width:700px;margin:0 auto 52px">
      <span class="eyebrow">Inside the Tool</span>
      <h2 style="margin:14px 0 16px">A full CRM at the core</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">One practical place to capture leads, see every conversation, track opportunities, and keep follow-up moving.</p>
    </div>
    <div class="feat-grid">
      <div class="feat-card">
        <div class="feat-ic" style="background:var(--wash-blue);color:var(--yb-blue)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg></div>
        <div class="feat-title">Easily Manage Every Lead</div>
        <div class="feat-desc">Drag-and-drop deal tracking so you always know where each lead stands.</div>
      </div>
      <div class="feat-card">
        <div class="feat-ic" style="background:var(--wash-blue);color:var(--yb-blue)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></div>
        <div class="feat-title">Centralized Inbox</div>
        <div class="feat-desc">SMS, email, Facebook, Instagram DMs, and live chat — all in one feed.</div>
      </div>
      <div class="feat-card">
        <div class="feat-ic" style="background:var(--wash-blue);color:var(--yb-blue)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg></div>
        <div class="feat-title">Automatic Follow-Up</div>
        <div class="feat-desc">Instantly respond when a lead takes action — no manual follow-up needed.</div>
      </div>
      <div class="feat-card">
        <div class="feat-ic" style="background:var(--wash-blue);color:var(--yb-blue)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 16 0 0 0 6.07 6.07l1.08-.9a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg></div>
        <div class="feat-title">Missed-Call Text Back</div>
        <div class="feat-desc">Automatically texts any missed caller so you never lose a hot lead.</div>
      </div>
      <div class="feat-card">
        <div class="feat-ic" style="background:var(--wash-blue);color:var(--yb-blue)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></div>
        <div class="feat-title">Email &amp; SMS Marketing</div>
        <div class="feat-desc">Build campaigns and automatic follow-up that nurture leads and keep customers engaged.</div>
      </div>
      <div class="feat-card">
        <div class="feat-ic" style="background:var(--wash-blue);color:var(--yb-blue)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div>
        <div class="feat-title">Reputation Management</div>
        <div class="feat-desc">Request reviews automatically, monitor ratings, and respond more efficiently.</div>
      </div>
    </div>
  </div>
</section>

<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#ffffff"/></svg></div>

<section style="background:#fff">
  <div class="container">
    <div style="text-align:center;max-width:700px;margin:0 auto 52px">
      <span class="eyebrow">Grow With You</span>
      <h2 style="margin:14px 0 16px">Start with the tool. Add what your business needs.</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">Replace multiple subscriptions while keeping room to add marketing, scheduling, reputation, and AI tools as your needs grow.</p>
    </div>
    <div class="feat-grid">
      <div class="feat-card">
        <div class="feat-title">Forms &amp; Funnels</div>
        <div class="feat-desc">Capture leads from your website and send every submission directly into the Customer Growth &amp; Communication Tool.</div>
      </div>
      <div class="feat-card">
        <div class="feat-title">Appointment Scheduling</div>
        <div class="feat-desc">Let customers book online, send reminders, and sync appointments to their contact record.</div>
      </div>
      <div class="feat-card">
        <div class="feat-title">Voice &amp; Chatbot AI</div>
        <div class="feat-desc">Answer common questions, qualify inquiries, respond to reviews, capture caller details, and book appointments.</div>
      </div>
      <div class="feat-card">
        <div class="feat-title">Invoices &amp; Contracts</div>
        <div class="feat-desc">Create, send, sign, store, and manage invoices, contracts, and important documents in one place.</div>
      </div>
      <div class="feat-card">
        <div class="feat-title">Built for One-Person Businesses</div>
        <div class="feat-desc">If you're a one-person team, our tool and support can help you run your business like you have a full team behind you.</div>
      </div>
      <div class="feat-card">
        <div class="feat-title">Personalized Support</div>
        <div class="feat-desc">Monthly support included in each plan. We train you, customize the setup, and help manage marketing workflows.</div>
      </div>
    </div>
  </div>
</section>

<div class="wave-div" style="background:#ffffff"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,70 C480,0 960,0 1440,70 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>

<section style="background:var(--bg-soft)" id="faq">
  <div class="container" style="max-width:820px">
    <div style="text-align:center;margin-bottom:40px">
      <span class="eyebrow">FAQs</span>
      <h2 style="margin:14px 0 12px">Answers about the Customer Growth &amp; Communication Tool</h2>
      <p style="color:var(--fg2);font-size:15px;line-height:1.7">Also known as a CRM — we use a clearer name so the purpose is obvious from day one.</p>
    </div>
    <div class="faq-list">
      <div class="faq-item"><button class="faq-q" type="button" style="--faq-ac:var(--yb-blue)">What is YB Marketing's Customer Growth &amp; Communication Tool?<span class="faq-icon">+</span></button><div class="faq-a"><div class="faq-a-inner">It is our all-in-one platform for managing leads, conversations, follow-up, and customer engagement. In industry terms, it is a CRM (customer relationship management) system.</div></div></div>
      <div class="faq-item"><button class="faq-q" type="button" style="--faq-ac:var(--yb-blue)">What is a CRM?<span class="faq-icon">+</span></button><div class="faq-a"><div class="faq-a-inner">A CRM helps you organize leads, track conversations, and follow up so fewer opportunities fall through the cracks. Our Customer Growth &amp; Communication Tool is that CRM — plus messaging, automation, scheduling, and more in one place.</div></div></div>
      <div class="faq-item"><button class="faq-q" type="button" style="--faq-ac:var(--yb-blue)">Who is this tool for?<span class="faq-icon">+</span></button><div class="faq-a"><div class="faq-a-inner">It is built for local businesses and one-person teams that need a clear place for contacts, pipelines, tasks, and marketing tools without enterprise complexity.</div></div></div>
      <div class="faq-item"><button class="faq-q" type="button" style="--faq-ac:var(--yb-blue)">Can you help set up the tool?<span class="faq-icon">+</span></button><div class="faq-a"><div class="faq-a-inner">Yes. We help configure your pipeline, import contacts, connect forms and ads, and train your team so the system matches how you actually sell.</div></div></div>
      <div class="faq-item"><button class="faq-q" type="button" style="--faq-ac:var(--yb-blue)">Does it work with our website and ads?<span class="faq-icon">+</span></button><div class="faq-a"><div class="faq-a-inner">Yes. We can connect form fills, call tracking, and ad leads so new inquiries land in your Customer Growth &amp; Communication Tool with the right context.</div></div></div>
      <div class="faq-item"><button class="faq-q" type="button" style="--faq-ac:var(--yb-blue)">Can you automate follow-ups?<span class="faq-icon">+</span></button><div class="faq-a"><div class="faq-a-inner">Yes. We can set reminders, email and text sequences, and task automations so leads get timely follow-up without manual busywork.</div></div></div>
      <div class="faq-item"><button class="faq-q" type="button" style="--faq-ac:var(--yb-blue)">Do you offer ongoing support?<span class="faq-icon">+</span></button><div class="faq-a"><div class="faq-a-inner">Yes. Monthly support is included in each plan so your team has help when questions come up after launch.</div></div></div>
    </div>
  </div>
</section>

<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#ffffff"/></svg></div>

<section style="background:#fff" id="contact">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start" class="why-main-grid">
      <div>
        <span class="eyebrow">Book a Meeting</span>
        <h2 style="margin:14px 0 14px">See how the tool fits your business</h2>
        <p style="color:var(--fg2);font-size:16px;line-height:1.75;margin-bottom:24px">An introduction meeting to learn more about your business, your goals, and how we can help you grow. No commitment required.</p>
        <p class="yb-schedule-intro" style="font-weight:700;margin-bottom:14px">Choose who you'd like to meet with</p>
        <div class="yb-schedule-grid">
          <div class="yb-schedule-card yb-schedule-card--split">
            <img src="../assets/jacob-headshot.webp" alt="Jacob Ross" class="yb-schedule-card__photo" width="64" height="64" loading="lazy">
            <span class="yb-schedule-card__info">
              <span class="yb-schedule-card__name">Jacob Ross</span>
              <a href="https://link.bluesoftwebsites.com/widget/booking/lRk0w69pQF0RRze2xKqx" target="_blank" rel="noopener noreferrer" class="yb-schedule-card__cta">Schedule Call</a>
              <a href="/about/jacob" class="yb-schedule-card__meet">Meet Jacob</a>
            </span>
          </div>
          <div class="yb-schedule-card yb-schedule-card--split">
            <img src="../assets/kevin-headshot.webp" alt="Kevin Dean" class="yb-schedule-card__photo" width="64" height="64" loading="lazy">
            <span class="yb-schedule-card__info">
              <span class="yb-schedule-card__name">Kevin Dean</span>
              <a href="https://link.bluesoftwebsites.com/widget/booking/UFZzPYN4w4sYMXsTvGHP" target="_blank" rel="noopener noreferrer" class="yb-schedule-card__cta">Schedule Call</a>
              <a href="/about/kevin" class="yb-schedule-card__meet">Meet Kevin</a>
            </span>
          </div>
          <div class="yb-schedule-card yb-schedule-card--split">
            <img src="../assets/sophie-headshot.webp" alt="Sophie Mann" class="yb-schedule-card__photo" width="64" height="64" loading="lazy">
            <span class="yb-schedule-card__info">
              <span class="yb-schedule-card__name">Sophie Mann</span>
              <a href="https://link.bluesoftwebsites.com/widget/booking/dwvAN8VTyHIbsbW3OLUF" target="_blank" rel="noopener noreferrer" class="yb-schedule-card__cta">Schedule Call</a>
              <a href="/about/sophie" class="yb-schedule-card__meet">Meet Sophie</a>
            </span>
          </div>
        </div>
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
    <span class="eyebrow" style="color:var(--yb-cyan)">Ready to Grow?</span>
    <h2 style="margin:14px 0 14px;color:#fff;font-size:clamp(1.8rem,2.6vw,2.4rem)">Organize leads. Automate follow-up.</h2>
    <p style="color:var(--fg2-on-dark);font-size:16px;margin-bottom:32px">See how YB Marketing's Customer Growth &amp; Communication Tool can centralize communication and keep opportunities moving.</p>
    <div class="svc-cta-btns">
      <a href="/contact" class="btn btn-grad btn-lg">Get Started Today</a>
      <a href="tel:5099019735" class="btn btn-ghost-white btn-lg">509-901-9735</a>
    </div>
  </div>
</div>
</div>

{footer}

<script src="../js/newsletter-popup.js" defer></script>
<script src="../js/chat-widget.js" defer></script>
<script src="../js/hero-orbit.js" defer></script>
<script src="../js/site.js" defer></script>
<script src="../js/lead-form-config.js" defer></script>
<script src="../js/lead-form.js" defer></script>
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
      b.closest('.faq-item').querySelector('.faq-a').style.maxHeight = null;
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


def patch_html_files() -> tuple[int, int]:
    nav_patched = 0
    footer_patched = 0
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT).as_posix()
        if any(
            part in rel
            for part in (
                "node_modules/",
                "next/",
                "_next/",
                "partials/",
                "preview/",
                "ui_kits/",
            )
        ):
            continue
        text = path.read_text(encoding="utf-8")
        if "customer-growth" in text and LABEL in text:
            # May still need footer
            pass
        original = text
        is_es = rel.startswith("es/")

        # Skip if already has clean absolute customer-growth dd-card
        has_nav = f'href="/{SLUG}"' in text and LABEL in text
        if is_es:
            has_nav = f'href="/es/{SLUG}"' in text and (
                "Herramienta de crecimiento" in text or LABEL in text
            )

        if not has_nav:
            card = DD_CARD_ES if is_es else DD_CARD_EN
            for pattern in AFTER_CONTENT_MARKERS:
                if pattern.search(text):
                    text, n = pattern.subn(r"\1\n            " + card, text, count=1)
                    if n:
                        nav_patched += 1
                        break
            else:
                # Relative path pages (blog builder style)
                if 'services/content-creation.html" class="dd-card"' in text:
                    # Determine prefix from the content-creation href
                    m = re.search(
                        r'href="([^"]*)services/content-creation\.html" class="dd-card">.*?</a>',
                        text,
                        re.S,
                    )
                    if m:
                        prefix = m.group(1)
                        card_rel = DD_CARD_REL.format(prefix=prefix)
                        text = text.replace(m.group(0), m.group(0) + "\n            " + card_rel, 1)
                        nav_patched += 1

        # Footer services list
        footer_marker = (
            f'<li><a href="/es/{SLUG}">' if is_es else f'<li><a href="/{SLUG}">'
        )
        if footer_marker not in text and FOOTER_AFTER.search(text):
            li = FOOTER_LI_ES if is_es else FOOTER_LI_EN
            text2, n = FOOTER_AFTER.subn(r"\1\n          " + li, text, count=1)
            if n:
                text = text2
                footer_patched += 1

        if text != original:
            path.write_text(text, encoding="utf-8")
    return nav_patched, footer_patched


def patch_source_files() -> None:
    # site_urls.py
    urls = ROOT / "scripts" / "site_urls.py"
    text = urls.read_text(encoding="utf-8")
    if f'"{SLUG}.html"' not in text:
        text = text.replace(
            '"web-design.html": "web-design",\n}',
            f'"web-design.html": "web-design",\n    "{SLUG}.html": "{SLUG}",\n}}',
        )
        urls.write_text(text, encoding="utf-8")

    # site_nav_snippet.py
    nav = ROOT / "scripts" / "site_nav_snippet.py"
    text = nav.read_text(encoding="utf-8")
    if SLUG not in text:
        marker = "services/content-creation.html', lang)}\" class=\"dd-card\">"
        idx = text.find(marker)
        if idx != -1:
            end = text.find("</a>", idx) + 4
            insert = (
                "\n            <a href=\"{page_href_lang('services/"
                + SLUG
                + ".html', lang)}\" class=\"dd-card\"><div class=\"dd-ic\" style=\"background:var(--wash-blue);color:var(--yb-blue)\">"
                + ICON_SVG
                + '</div><div><span class="dd-name">{t("'
                + LABEL
                + '", lang)}</span><span class="dd-desc">{t("'
                + DESC
                + '", lang)}</span></div></a>'
            )
            text = text[:end] + insert + text[end:]
            nav.write_text(text, encoding="utf-8")

    # site_footer_snippet.py
    foot = ROOT / "scripts" / "site_footer_snippet.py"
    text = foot.read_text(encoding="utf-8")
    if SLUG not in text:
        text = text.replace(
            '<li><a href="{page_href_lang(\'services/content-creation.html\', lang)}">{t("Content Marketing", lang)}</a></li>',
            '<li><a href="{page_href_lang(\'services/content-creation.html\', lang)}">{t("Content Marketing", lang)}</a></li>\n'
            f'          <li><a href="{{page_href_lang(\'services/{SLUG}.html\', lang)}}">{{t("{LABEL}", lang)}}</a></li>',
        )
        foot.write_text(text, encoding="utf-8")

    # site_i18n.py
    i18n = ROOT / "scripts" / "site_i18n.py"
    text = i18n.read_text(encoding="utf-8")
    if LABEL not in text:
        text = text.replace(
            '"Copy that converts": "Textos que convierten",\n',
            '"Copy that converts": "Textos que convierten",\n'
            f'    "{LABEL}": "Herramienta de crecimiento y comunicación",\n'
            f'    "{DESC}": "CRM, mensajería y automatización",\n',
        )
        i18n.write_text(text, encoding="utf-8")

    # schema_markup.py
    schema = ROOT / "scripts" / "schema_markup.py"
    text = schema.read_text(encoding="utf-8")
    if f'"{SLUG}/index.html"' not in text:
        text = text.replace(
            '    "web-design/index.html": {\n'
            '        "slug": "web-design",\n'
            '        "name": "Web Design & Development",\n'
            '        "service_type": "Web Design",\n'
            '        "description": "Custom WordPress and Wix website design and development for Pacific Northwest businesses.",\n'
            "    },\n}",
            '    "web-design/index.html": {\n'
            '        "slug": "web-design",\n'
            '        "name": "Web Design & Development",\n'
            '        "service_type": "Web Design",\n'
            '        "description": "Custom WordPress and Wix website design and development for Pacific Northwest businesses.",\n'
            "    },\n"
            f'    "{SLUG}/index.html": {{\n'
            f'        "slug": "{SLUG}",\n'
            f'        "name": "{LABEL}",\n'
            '        "service_type": "Customer Relationship Management",\n'
            '        "description": "Lead management, centralized messaging, automation, and customer follow-up for Pacific Northwest businesses.",\n'
            "    },\n}",
        )
        schema.write_text(text, encoding="utf-8")

    # build-sitemap.py SERVICE_INDEX_PAGES
    sm = ROOT / "scripts" / "build-sitemap.py"
    text = sm.read_text(encoding="utf-8")
    if f"{SLUG}/index.html" not in text:
        text = text.replace(
            '("content-marketing/index.html", "Content Marketing"),\n]',
            '("content-marketing/index.html", "Content Marketing"),\n'
            f'    ("{SLUG}/index.html", "{LABEL}"),\n]',
        )
        sm.write_text(text, encoding="utf-8")

    # lead form interests
    lead = ROOT / "scripts" / "site_lead_form_snippet.py"
    text = lead.read_text(encoding="utf-8")
    if SLUG not in text:
        text = text.replace(
            '("press-releases", "Press Releases"),\n',
            '("press-releases", "Press Releases"),\n'
            f'    ("{SLUG}", "{LABEL}"),\n',
        )
        text = text.replace(
            '"Press": "press-releases",\n',
            '"Press": "press-releases",\n'
            f'    "Customer Growth": "{SLUG}",\n',
        )
        lead.write_text(text, encoding="utf-8")

    # service form mapping
    svc_form = ROOT / "scripts" / "site_service_hubspot_form_snippet.py"
    text = svc_form.read_text(encoding="utf-8")
    if SLUG not in text:
        text = text.replace(
            '"press-releases.html": "Press Releases Service Page",\n}',
            '"press-releases.html": "Press Releases Service Page",\n'
            f'    "{SLUG}.html": "Customer Growth Service Page",\n}}',
        )
        text = text.replace(
            '"press-releases": "Press Releases Service Page",\n}',
            '"press-releases": "Press Releases Service Page",\n'
            f'    "{SLUG}": "Customer Growth Service Page",\n}}',
        )
        text = text.replace(
            '"press-releases": "thank-you-press-releases",\n}',
            '"press-releases": "thank-you-press-releases",\n'
            f'    "{SLUG}": "thank-you-{SLUG}",\n}}',
        )
        svc_form.write_text(text, encoding="utf-8")

    # vercel redirects
    vercel = ROOT / "vercel.json"
    text = vercel.read_text(encoding="utf-8")
    if f"/services/{SLUG}" not in text:
        text = text.replace(
            '{ "source": "/services/content-creation", "destination": "/content-marketing", "permanent": true },',
            '{ "source": "/services/content-creation", "destination": "/content-marketing", "permanent": true },\n'
            f'    {{ "source": "/services/{SLUG}.html", "destination": "/{SLUG}", "permanent": true }},\n'
            f'    {{ "source": "/services/{SLUG}", "destination": "/{SLUG}", "permanent": true }},\n'
            f'    {{ "source": "/crm-services", "destination": "/{SLUG}", "permanent": true }},\n'
            f'    {{ "source": "/services/crm-services", "destination": "/{SLUG}", "permanent": true }},',
        )
        vercel.write_text(text, encoding="utf-8")

    # Next.js links
    links = ROOT / "next" / "lib" / "site-links.ts"
    if links.exists():
        text = links.read_text(encoding="utf-8")
        if "customerGrowth" not in text:
            text = text.replace(
                'contentMarketing: "/content-marketing",',
                'contentMarketing: "/content-marketing",\n'
                f'  customerGrowth: "/{SLUG}",',
            )
            links.write_text(text, encoding="utf-8")

    nav_tsx = ROOT / "next" / "lib" / "nav-services.tsx"
    if nav_tsx.exists():
        text = nav_tsx.read_text(encoding="utf-8")
        if "customerGrowth" not in text:
            insert = f"""
  {{
    href: siteLinks.customerGrowth,
    name: "{LABEL}",
    desc: "{DESC}",
    wash: "var(--wash-blue)",
    color: "var(--yb-blue)",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
        <circle cx="9" cy="7" r="4" />
        <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
        <path d="M16 3.13a4 4 0 0 1 0 7.75" />
      </svg>
    ),
  }},
"""
            text = text.replace(
                '    href: siteLinks.contentMarketing,',
                insert + '    href: siteLinks.contentMarketing,',
            )
            # Wait - that puts it BEFORE content marketing. Better after content marketing block.
            # Fix: undo and insert after content marketing entry instead
            text = nav_tsx.read_text(encoding="utf-8")
            if "customerGrowth" not in text:
                # insert before closing ]; of NAV_SERVICES
                text = text.replace(
                    """    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M12 20h9" />
        <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
      </svg>
    ),
  },
];""",
                    """    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M12 20h9" />
        <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
      </svg>
    ),
  },
  {
    href: siteLinks.customerGrowth,
    name: "Customer Growth & Communication Tool",
    desc: "CRM, messaging & automation",
    wash: "var(--wash-blue)",
    color: "var(--yb-blue)",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
        <circle cx="9" cy="7" r="4" />
        <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
        <path d="M16 3.13a4 4 0 0 1 0 7.75" />
      </svg>
    ),
  },
];""",
                )
                nav_tsx.write_text(text, encoding="utf-8")

    # build-blog.py hardcoded nav
    blog = ROOT / "scripts" / "build-blog.py"
    text = blog.read_text(encoding="utf-8")
    if SLUG not in text:
        marker = 'services/content-creation.html" class="dd-card">'
        idx = text.find(marker)
        if idx != -1:
            end = text.find("</a>", idx) + 4
            insert = (
                '\n            <a href="{prefix}services/'
                + SLUG
                + '.html" class="dd-card"><div class="dd-ic" style="background:var(--wash-blue);color:var(--yb-blue)">'
                + ICON_SVG
                + f'</div><div><span class="dd-name">{LABEL}</span><span class="dd-desc">{DESC}</span></div></a>'
            )
            # Only first occurrence in header_nav - there may be f-string with prefix
            # Find Content & Blogging block more carefully
            pattern = re.compile(
                r'(<a href="\{prefix\}services/content-creation\.html" class="dd-card">.*?</a>)',
                re.S,
            )
            text2, n = pattern.subn(
                r"\1\n            <a href=\"{prefix}services/"
                + SLUG
                + '.html" class="dd-card"><div class="dd-ic" style="background:var(--wash-blue);color:var(--yb-blue)">'
                + ICON_SVG
                + f'</div><div><span class="dd-name">{LABEL}</span><span class="dd-desc">{DESC}</span></div></a>',
                text,
                count=1,
            )
            if n:
                blog.write_text(text2, encoding="utf-8")


def create_thank_you_stub() -> None:
    """Minimal thank-you redirect page under services/."""
    src = ROOT / "services" / "thank-you-press-releases.html"
    dest = ROOT / "services" / f"thank-you-{SLUG}.html"
    if not src.exists() or dest.exists():
        return
    text = src.read_text(encoding="utf-8")
    text = text.replace("Press Releases", LABEL)
    text = text.replace("press-releases", SLUG)
    text = text.replace("/press-releases", f"/{SLUG}")
    dest.write_text(text, encoding="utf-8")
    print(f"wrote {dest.relative_to(ROOT)}")


def main() -> None:
    out_dir = ROOT / SLUG
    out_dir.mkdir(parents=True, exist_ok=True)
    page = build_service_page()
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote {SLUG}/index.html")

    patch_source_files()
    print("patched source snippets / config")

    create_thank_you_stub()

    nav_n, foot_n = patch_html_files()
    print(f"patched nav in ~{nav_n} files, footer in ~{foot_n} files")


if __name__ == "__main__":
    main()
