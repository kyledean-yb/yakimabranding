#!/usr/bin/env python3
"""Create AI for Business + AI for Small Business pages; wire general page into nav/home."""

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

GENERAL_SLUG = "ai-for-business"
SMB_SLUG = "ai-for-small-business"

ICON_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M12 2a4 4 0 0 1 4 4v1h1a3 3 0 0 1 0 6h-.5"/>'
    '<path d="M8 7V6a4 4 0 0 1 7.2-2.4"/>'
    '<path d="M7.5 13H7a3 3 0 0 1 0-6h1"/>'
    '<path d="M8 13v3a4 4 0 0 0 8 0v-3"/>'
    '<circle cx="9" cy="17" r="1"/><circle cx="15" cy="17" r="1"/>'
    "</svg>"
)

PAGE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--font-body);background:var(--bg);color:var(--fg1);-webkit-font-smoothing:antialiased;overflow-x:hidden}
::selection{background:var(--yb-blue);color:#fff}
img{display:block;max-width:100%}
a{color:inherit;text-decoration:none}
.container{width:100%;max-width:var(--container);margin:0 auto;padding:0 28px}
section{padding:88px 0}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-body);font-weight:700;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--yb-blue)}
.eyebrow::before{content:'';display:block;width:7px;height:7px;border-radius:50%;background:currentColor;flex:none}
.header{position:sticky;top:0;z-index:50;transition:all 240ms cubic-bezier(.4,0,.2,1)}
.header.solid{background:rgba(255,255,255,.88);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}
.header.top{background:rgba(255,255,255,.6);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid transparent}
.header-inner{display:flex;align-items:center;justify-content:space-between;height:72px}
.logo{display:flex;align-items:center;gap:11px}
.logo img{width:44px;height:44px}
.logo-text{font-family:var(--font-display);font-weight:800;font-size:22px;letter-spacing:-.02em;color:var(--ink)}
.logo-text span{color:var(--yb-blue)}
.nav{display:flex;align-items:center;gap:2px}
.nav-a{font-weight:600;font-size:15px;color:var(--fg1);padding:8px 14px;border-radius:var(--r-sm);transition:all 240ms;display:inline-block}
.nav-a:hover{background:var(--bg-soft);color:var(--yb-blue)}
.nav-services,.nav-about,.nav-insights{position:relative}
.nav-svc-btn{display:flex;align-items:center;gap:5px;font-weight:600;font-size:15px;color:var(--fg1);padding:8px 14px;border-radius:var(--r-sm);transition:all 240ms;background:none;border:none;cursor:pointer;font-family:var(--font-body)}
.nav-svc-btn:hover,.nav-services:hover .nav-svc-btn,.nav-about:hover .nav-svc-btn,.nav-insights:hover .nav-svc-btn{background:var(--bg-soft);color:var(--yb-blue)}
.nav-chevron{transition:transform 240ms;flex:none;color:currentColor}
.nav-services:hover .nav-chevron,.nav-about:hover .nav-chevron,.nav-insights:hover .nav-chevron{transform:rotate(180deg)}
.nav-dd{position:absolute;top:calc(100% + 10px);left:50%;transform:translateX(-50%) translateY(-10px) scale(.97);opacity:0;pointer-events:none;transition:opacity 200ms ease 150ms,transform 220ms cubic-bezier(.16,1,.3,1) 150ms;width:720px;background:#fff;border-radius:var(--r-xl);box-shadow:0 24px 64px -16px rgba(22,32,58,.22),0 0 0 1px rgba(22,32,58,.07);padding:16px;z-index:200}
.nav-services:hover .nav-dd,.nav-about:hover .nav-dd,.nav-insights:hover .nav-dd,.nav-services.is-open .nav-dd,.nav-about.is-open .nav-dd,.nav-insights.is-open .nav-dd{opacity:1;transform:translateX(-50%) translateY(0) scale(1);pointer-events:all;transition:opacity 150ms ease,transform 180ms cubic-bezier(.16,1,.3,1)}
.nav-dd-arrow{position:absolute;top:-5px;left:50%;transform:translateX(-50%) rotate(45deg);width:10px;height:10px;background:#fff;border-top:1px solid rgba(22,32,58,.08);border-left:1px solid rgba(22,32,58,.08)}
.nav-dd-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.dd-card{display:flex;align-items:flex-start;gap:11px;padding:12px;border-radius:var(--r-md);transition:background 150ms ease}
.dd-card:hover{background:var(--bg-soft)}
.dd-ic{width:36px;height:36px;border-radius:var(--r-sm);display:flex;align-items:center;justify-content:center;flex:none}
.dd-ic svg{width:18px;height:18px}
.dd-name{font-weight:700;font-size:13px;color:var(--ink);margin-bottom:2px;display:block;line-height:1.3}
.dd-desc{font-size:11.5px;color:var(--fg3);line-height:1.4}
.btn{display:inline-flex;align-items:center;gap:8px;border:none;cursor:pointer;font-family:var(--font-body);font-weight:700;font-size:15px;border-radius:var(--r-md);padding:13px 22px;transition:all 240ms;white-space:nowrap;line-height:1}
.btn-grad{background:var(--grad-brand);color:#fff;box-shadow:0 14px 30px -10px rgba(63,111,214,.45)}
.btn-grad:hover{transform:translateY(-2px);filter:brightness(1.06)}
.btn-ghost-white{background:rgba(255,255,255,.12);color:#fff;border:1.5px solid rgba(255,255,255,.28)}
.btn-ghost-white:hover{background:rgba(255,255,255,.22);transform:translateY(-2px)}
.btn-lg{padding:16px 28px;font-size:16px}
.hamburger{display:none;background:none;border:none;cursor:pointer;padding:6px;align-items:center;justify-content:center}
.mobile-menu{display:none;border-top:1px solid var(--line);background:#fff;padding:12px 28px 20px}
.mobile-menu a,.mobile-menu button{display:block;padding:14px 0;border-bottom:1px solid var(--line);font-weight:600;font-size:17px;color:var(--ink);width:100%;text-align:left;background:none;border:none;font-family:var(--font-body);cursor:pointer}
.mobile-svc-list{display:none;padding:8px 0 8px 16px}
.mobile-svc-list.open{display:block}
.mobile-svc-list a{font-size:15px;padding:10px 0;color:var(--fg2)}
.svc-hero{position:relative;overflow:hidden;background:var(--grad-navy);padding:80px 0 100px}
.svc-hero-mesh{position:absolute;inset:0;background-image:var(--grad-mesh);pointer-events:none}
.svc-hero-inner{position:relative;display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:center}
.svc-hero h1{margin:16px 0 20px;font-size:clamp(2.1rem,3.8vw,3.4rem);color:#fff;line-height:1.08}
.hero-lead{margin:0 0 32px;color:var(--fg2-on-dark);max-width:540px;font-size:clamp(1rem,1.3vw,1.2rem);line-height:1.6}
.svc-hero-actions{display:flex;gap:14px;flex-wrap:wrap}
.feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.feat-card{background:#fff;border-radius:var(--r-lg);padding:26px;border:1px solid var(--line);box-shadow:0 2px 8px rgba(22,32,58,.06);transition:all 240ms}
.feat-card:hover{transform:translateY(-4px);box-shadow:0 12px 32px -8px rgba(22,32,58,.14)}
.feat-ic{width:48px;height:48px;border-radius:var(--r-md);display:flex;align-items:center;justify-content:center;margin-bottom:16px}
.feat-ic svg{width:22px;height:22px}
.feat-title{font-family:var(--font-display);font-weight:700;font-size:16px;color:var(--ink);margin-bottom:7px}
.feat-desc{font-size:14px;color:var(--fg2);line-height:1.6}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.step{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:22px}
.step-num{font-family:var(--font-display);font-weight:800;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--yb-blue);margin-bottom:10px}
.step h3{font-size:16px;margin:0 0 8px;color:var(--ink)}
.step p{font-size:14px;color:var(--fg2);line-height:1.6;margin:0}
.svc-cta{background:var(--grad-navy);position:relative;overflow:hidden;padding:80px 0}
.svc-cta-mesh{position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.7}
.svc-cta-inner{position:relative;text-align:center;max-width:680px;margin:0 auto}
.svc-cta h2{color:#fff;margin-bottom:14px}
.svc-cta p{color:var(--fg2-on-dark);font-size:16px;margin-bottom:32px}
.svc-cta-btns{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.wave-div{position:relative;overflow:hidden;line-height:0;font-size:0}
.wave-div svg{display:block;width:100%;height:70px}
.footer{background:var(--grad-navy);color:#fff;position:relative;overflow:hidden;padding:64px 0 28px}
.footer-mesh{position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.5;pointer-events:none}
.footer-grid{position:relative;display:grid;grid-template-columns:1.7fr 1fr 1fr 1.4fr;gap:40px;margin-bottom:42px}
.footer-brand p{color:var(--fg2-on-dark);font-size:14px;max-width:280px;margin:14px 0 18px}
.footer-col h4{font-family:var(--font-display);font-size:14px;font-weight:700;margin-bottom:14px;letter-spacing:.04em;color:#fff}
.footer-col ul{list-style:none;display:grid;gap:10px}
.footer-col a{color:var(--fg2-on-dark);font-size:14px;transition:color 240ms}
.footer-col a:hover{color:#fff}
.footer-bottom{position:relative;border-top:1px solid rgba(255,255,255,.12);padding-top:22px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;color:var(--fg2-on-dark);font-size:13px}
.social-btn{width:38px;height:38px;border-radius:var(--r-sm);background:rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;color:#fff;transition:background 240ms}
.social-btn:hover{background:var(--yb-blue)}
.faq-item{border-bottom:1px solid var(--line)}
.faq-q{display:flex;justify-content:space-between;align-items:center;padding:20px 0;cursor:pointer;font-weight:700;font-size:15.5px;color:var(--ink);gap:16px;background:none;border:none;width:100%;text-align:left;font-family:var(--font-body);transition:color 200ms}
.faq-q:hover{color:var(--yb-blue)}
.faq-q.active{color:var(--faq-ac,var(--yb-blue))}
.faq-icon{width:28px;height:28px;border-radius:50%;background:var(--bg-mute);display:flex;align-items:center;justify-content:center;flex:none;transition:background 200ms,transform 200ms;color:var(--fg2)}
.faq-q.active .faq-icon{background:var(--faq-ac,var(--yb-blue));color:#fff;transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height 320ms cubic-bezier(.16,1,.3,1)}
.faq-a-inner{padding-bottom:20px;font-size:15px;color:var(--fg2);line-height:1.75}
.footer-socials{display:flex;gap:10px;margin-top:12px}
@media(max-width:1100px){.nav,.btn-hdr{display:none}.hamburger{display:flex}.nav-dd{display:none}.mobile-menu.open{display:block}}
@media(max-width:900px){.svc-hero-inner{grid-template-columns:1fr}.svc-hero-visual{display:none}.feat-grid,.steps{grid-template-columns:1fr 1fr}.footer-grid{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.feat-grid,.steps,.footer-grid{grid-template-columns:1fr}section{padding:60px 0}}
"""

SCHEDULE = """        <p class="yb-schedule-intro" style="font-weight:700;margin-bottom:14px">Choose who you'd like to meet with</p>
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
        </div>"""

ORBIT = f"""    <div class="svc-hero-visual">
      <div class="hero-orbit hero-orbit--svc hero-orbit--features" style="--orbit-feat-wash:var(--wash-violet);--orbit-feat-color:var(--yb-violet);--orbit-feat-glow:rgba(124,92,252,0.22)">
        <div class="hero-orbit-bg" aria-hidden="true">
          <div class="hero-orbit-ring hero-orbit-ring--track"></div>
          <div class="hero-orbit-hub">
            <div class="hero-orbit-hub-art">
              <img src="../assets/yb-logo-white.png" alt="YB Marketing AI services">
            </div>
          </div>
        </div>
        <div class="hero-orbit-spin">
          <div class="hero-orbit-node" style="--i:0"><div class="hero-orbit-icon" aria-label="Content"><span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg></span></span></div></div>
          <div class="hero-orbit-node" style="--i:1"><div class="hero-orbit-icon" aria-label="Voice"><span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg></span></span></div></div>
          <div class="hero-orbit-node" style="--i:2"><div class="hero-orbit-icon" aria-label="Automation"><span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg></span></span></div></div>
          <div class="hero-orbit-node" style="--i:3"><div class="hero-orbit-icon" aria-label="Chat"><span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></span></span></div></div>
          <div class="hero-orbit-node" style="--i:4"><div class="hero-orbit-icon" aria-label="Data"><span class="hero-orbit-pill"><span class="hero-orbit-pill-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg></span></span></div></div>
          <div class="hero-orbit-node" style="--i:5"><div class="hero-orbit-icon" aria-label="Training"><span class="hero-orbit-pill"><span class="hero-orbit-pill-ic">{ICON_SVG}</span></span></div></div>
        </div>
      </div>
    </div>"""


def faq_item(q: str, a: str) -> str:
    return (
        f'<div class="faq-item"><button class="faq-q" type="button" style="--faq-ac:var(--yb-violet)">'
        f"{q}<span class=\"faq-icon\">+</span></button>"
        f'<div class="faq-a"><div class="faq-a-inner">{a}</div></div></div>'
    )


def feat(title: str, desc: str, svg: str) -> str:
    return f"""      <div class="feat-card">
        <div class="feat-ic" style="background:var(--wash-violet);color:var(--yb-violet)">{svg}</div>
        <div class="feat-title">{title}</div>
        <div class="feat-desc">{desc}</div>
      </div>"""


def build_page(
    *,
    slug: str,
    title: str,
    meta: str,
    eyebrow: str,
    h1: str,
    lead: str,
    body_html: str,
    form_source: str,
    thank_you: str,
    interest: str,
) -> str:
    prefix = "../"
    header = site_header_html(prefix, current_path=f"/{slug}").strip()
    footer = site_footer_html(prefix, current_path=f"/{slug}").strip()
    form = lead_form_html(form_source, redirect=thank_you, default_interest=interest)
    seo = seo_head_html(f"{slug}/index.html")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="../favicon.png" type="image/png">
<link rel="apple-touch-icon" href="../favicon.png">
{STAGING_ROBOTS_META}
<title>{title} | YB Marketing | 509-901-9735</title>
<meta name="description" content="{meta}">
<link rel="stylesheet" href="../colors_and_type.css">
<link rel="stylesheet" href="../insights.css">
<link rel="stylesheet" href="../lead-form.css">
<style>{PAGE_CSS}</style>
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
      <span class="eyebrow" style="color:var(--yb-cyan)">{eyebrow}</span>
      <h1>{h1}</h1>
      <p class="hero-lead">{lead}</p>
      <div class="svc-hero-actions">
        <a href="/contact" class="btn btn-grad btn-lg">Get Started Today
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </a>
        <a href="#how-it-works" class="btn btn-ghost-white">How it works</a>
      </div>
    </div>
{ORBIT}
  </div>
</section>

<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 80" preserveAspectRatio="none" style="height:80px"><path d="M0,0 C360,80 1080,80 1440,0 L1440,80 L0,80 Z" fill="#ffffff"/></svg></div>

{body_html}

<section style="background:#fff" id="contact">
  <div class="container">
    <div style="text-align:center;max-width:720px;margin:0 auto 40px">
      <span class="eyebrow">Get Started</span>
      <h2 style="margin:14px 0 12px">Book a Meeting or Send Us a Message</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">Grab a free 30 minute intro call, or send a note and we'll get back to you.</p>
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
    <span class="eyebrow" style="color:var(--yb-cyan)">Work with us</span>
    <h2 style="margin:14px 0 14px;color:#fff;font-size:clamp(1.8rem,2.6vw,2.4rem)">Ready to put AI to work in your marketing?</h2>
    <p style="color:var(--fg2-on-dark);font-size:16px;margin-bottom:32px">Connect with us and we will map out practical next steps for your team.</p>
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


def general_body() -> str:
    feats = [
        feat(
            "Content & Social Media",
            "Generate blog posts, captions, ad copy, emails, and content calendars, then turn one strong piece into several formats your team can publish.",
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>',
        ),
        feat(
            "Voice & Lead Handling",
            "AI voice agents can answer calls around the clock, qualify leads, and route opportunities so after hours inquiries do not turn into missed revenue.",
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>',
        ),
        feat(
            "Automations & Follow Ups",
            "Send an SMS after a form fill, schedule reminders and confirmations, and keep nurture sequences moving so leads do not sit unanswered.",
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>',
        ),
        feat(
            "Customer Engagement & Sales",
            "Chatbots engage website visitors in real time, answer common questions, handle basic objections, and guide people toward booking a call or appointment.",
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
        ),
        feat(
            "Data & Optimization",
            "Track patterns across ads, site traffic, and messaging, then use those insights to adjust campaigns and put budget where it performs best.",
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        ),
        feat(
            "Training & Support",
            "We train your team on the tools we set up, leave clear instructions, and stay available to refine workflows as your needs change.",
            ICON_SVG,
        ),
    ]
    faqs = [
        faq_item(
            "What is AI for Business at YB Marketing?",
            "Practical guidance and setup for AI tools that help with content, follow up, chat, voice agents, and everyday marketing tasks, without unnecessary complexity.",
        ),
        faq_item(
            "Do I need to be technical to use AI?",
            "No. We focus on tools and workflows your team can actually run, with clear training and guardrails.",
        ),
        faq_item(
            "Can AI help with website content?",
            "Yes. AI can speed up drafts and outlines, while we keep brand voice, accuracy, and SEO quality in check.",
        ),
        faq_item(
            "Do you build chatbots or voice agents?",
            "Yes. We can help design and deploy assistants that answer common questions and capture leads.",
        ),
        faq_item(
            "Will AI replace our marketing team?",
            "No. AI works best as a multiplier. It helps with faster drafts, better follow up, and clearer reporting alongside human strategy.",
        ),
        faq_item(
            "How do you keep AI accurate and on brand?",
            "We set prompts, review workflows, and approve messaging so outputs stay aligned with your brand and offers.",
        ),
        faq_item(
            "How quickly can we start using AI?",
            "Many teams see useful workflows within weeks once goals and tools are chosen.",
        ),
        faq_item(
            "Is AI support ongoing?",
            "Yes. We can train your team, refine automations, and adjust as tools and needs change.",
        ),
    ]
    return f"""
<section style="background:#fff">
  <div class="container">
    <div style="max-width:760px;margin:0 auto;text-align:center">
      <span class="eyebrow">Why AI</span>
      <h2 style="margin:14px 0 16px">If you're not using AI, you're already behind.</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75;margin-bottom:16px">Most owners know AI is the future, but figuring out how to use it can feel overwhelming. We close that gap with simple tools that streamline operations, boost engagement, and drive real results.</p>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">AI acts like a force multiplier: less repetitive work, faster response times, and consistent communication across every channel.</p>
    </div>
  </div>
</section>

<div class="wave-div" style="background:#ffffff"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,70 C480,0 960,0 1440,70 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>

<section style="background:var(--bg-soft)">
  <div class="container">
    <div style="text-align:center;max-width:700px;margin:0 auto 52px">
      <span class="eyebrow">What AI unlocks</span>
      <h2 style="margin:14px 0 16px">Practical tools your team can use</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">Clear applications for marketing and sales, without the overwhelm.</p>
    </div>
    <div class="feat-grid">
{''.join(feats)}
    </div>
  </div>
</section>

<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#ffffff"/></svg></div>

<section style="background:#fff" id="how-it-works">
  <div class="container">
    <div style="text-align:center;max-width:700px;margin:0 auto 48px">
      <span class="eyebrow">How it works</span>
      <h2 style="margin:14px 0 16px">Guidance, setup, and support</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">We start with your goals, choose tools that fit, get them running, and train your team so the systems stick.</p>
    </div>
    <div class="steps">
      <div class="step"><div class="step-num">01</div><h3>Review your goals</h3><p>We look at your current marketing, tools, and where time or leads are getting lost.</p></div>
      <div class="step"><div class="step-num">02</div><h3>Recommend tools</h3><p>You get a short list of AI uses that fit your business, with a clear reason for each one.</p></div>
      <div class="step"><div class="step-num">03</div><h3>Set up and connect</h3><p>We connect the tools to your site, CRM, or ad accounts and test them with real examples from your business.</p></div>
      <div class="step"><div class="step-num">04</div><h3>Train and refine</h3><p>Your team learns the workflows, and we stay available to adjust prompts and automations as results come in.</p></div>
    </div>
  </div>
</section>

<div class="wave-div" style="background:#ffffff"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,70 C480,0 960,0 1440,70 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>

<section style="background:var(--bg-soft)" id="faq">
  <div class="container" style="max-width:820px">
    <div style="text-align:center;margin-bottom:40px">
      <span class="eyebrow">FAQ</span>
      <h2 style="margin:14px 0 12px">Frequently Asked Questions</h2>
      <p style="color:var(--fg2);font-size:15px;line-height:1.7">Answers to the questions we hear most often about our AI for Business services.</p>
    </div>
    <div class="faq-list">
{''.join(faqs)}
    </div>
    <p style="margin:28px 0 0;text-align:center;color:var(--fg2);font-size:14px">Running a smaller team? See our page on <a href="/ai-for-small-business" style="color:var(--yb-blue);font-weight:700">AI for small businesses</a>.</p>
  </div>
</section>

<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#ffffff"/></svg></div>
"""


def smb_body() -> str:
    feats = [
        feat(
            "Content & Social Media",
            "Draft blog posts, captions, emails, and ad copy faster so a lean team can stay visible without spending whole evenings writing from scratch.",
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>',
        ),
        feat(
            "Voice & Lead Handling",
            "When you cannot answer every call, AI voice tools cover common questions, take messages, and pass warm leads to you instead of sending people to a competitor.",
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>',
        ),
        feat(
            "Automations & Follow Ups",
            "Form fills and chat inquiries get a timely text or email so follow up happens even when your day is packed with jobs.",
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>',
        ),
        feat(
            "Customer Engagement & Sales",
            "Website chat can answer FAQs, collect contact info, and help visitors book a call without needing someone glued to the inbox.",
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
        ),
        feat(
            "Data & Optimization",
            "See which ads, pages, and messages are pulling their weight so you can spend with more confidence and less guesswork.",
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        ),
        feat(
            "Training & Support",
            "We set tools up for the size of your team, show you how to run them, and leave instructions you can follow when we are not on the call.",
            ICON_SVG,
        ),
    ]
    faqs = [
        faq_item(
            "What is AI consulting for a small business?",
            "Working with someone who knows the tools, looks at how your business runs, and helps you set up a few AI workflows that save time or catch more leads.",
        ),
        faq_item(
            "Why should a busy owner spend time on this?",
            "Because repetitive marketing tasks eat hours you could spend on customers. Automating drafts and follow up frees time without hiring another full time person.",
        ),
        faq_item(
            "Where should a small business start with AI?",
            "Start where the pain is loudest: unanswered leads, thin content calendars, or the same FAQ typed out over and over. We begin there, not with every new tool on the market.",
        ),
        faq_item(
            "What does an AI consultant actually do?",
            "Review your processes, recommend software that fits your budget, set it up, train whoever will use it, and stick around long enough to fix what breaks.",
        ),
        faq_item(
            "How much does this cost?",
            "It depends on scope. A single automation is different from a full content and follow up setup. We quote after we understand what you need.",
        ),
        faq_item(
            "How fast will we see results?",
            "Many owners notice less busywork within a few weeks of launch. Bigger returns show up once the new habits stick and leads stop slipping.",
        ),
        faq_item(
            "Can you build chatbots or voice agents for us?",
            "Yes, for practical jobs like answering FAQs, booking requests, and drafting replies, connected to tools you already use.",
        ),
        faq_item(
            "Do you only work with Pacific Northwest businesses?",
            "We are based in Yakima and work across the region, but remote setups work fine if you want the same practical approach from elsewhere.",
        ),
    ]
    return f"""
<section style="background:#fff">
  <div class="container">
    <div style="max-width:760px;margin:0 auto;text-align:center">
      <span class="eyebrow">For small businesses</span>
      <h2 style="margin:14px 0 16px">If you're not using AI, you're already behind.</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75;margin-bottom:16px">Most small business owners know AI is the future, but figuring out how to use it with a lean team can feel overwhelming. We close that gap with practical tools that save time, catch more leads, and keep marketing consistent.</p>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">AI acts like a force multiplier for a small staff: less repetitive work, faster response times, and steadier communication when you cannot be everywhere at once.</p>
    </div>
  </div>
</section>

<div class="wave-div" style="background:#ffffff"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,70 C480,0 960,0 1440,70 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>

<section style="background:var(--bg-soft)">
  <div class="container">
    <div style="text-align:center;max-width:700px;margin:0 auto 52px">
      <span class="eyebrow">What AI unlocks</span>
      <h2 style="margin:14px 0 16px">Practical tools sized for a small team</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">The same kinds of AI applications larger companies use, set up so you can run them without a full marketing department.</p>
    </div>
    <div class="feat-grid">
{''.join(feats)}
    </div>
  </div>
</section>

<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#ffffff"/></svg></div>

<section style="background:#fff" id="how-it-works">
  <div class="container">
    <div style="text-align:center;max-width:700px;margin:0 auto 48px">
      <span class="eyebrow">How it works</span>
      <h2 style="margin:14px 0 16px">Guidance, setup, and support</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">Short conversations, clear recommendations, and setups you can see working before we call the project done.</p>
    </div>
    <div class="steps">
      <div class="step"><div class="step-num">01</div><h3>Review your goals</h3><p>We learn how you get leads today, what slips through, and which tasks take more time than they should.</p></div>
      <div class="step"><div class="step-num">02</div><h3>Recommend tools</h3><p>You get one or two AI uses with a budget and timeline, not a pitch to do everything at once.</p></div>
      <div class="step"><div class="step-num">03</div><h3>Set up and connect</h3><p>We connect tools to your website, inbox, or CRM and test them with your real offers and FAQs.</p></div>
      <div class="step"><div class="step-num">04</div><h3>Train and refine</h3><p>You leave with a working system and notes your team can follow. Ongoing help is available if you want it.</p></div>
    </div>
  </div>
</section>

<div class="wave-div" style="background:#ffffff"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,70 C480,0 960,0 1440,70 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>

<section style="background:var(--bg-soft)" id="faq">
  <div class="container" style="max-width:820px">
    <div style="text-align:center;margin-bottom:40px">
      <span class="eyebrow">FAQ</span>
      <h2 style="margin:14px 0 12px">Frequently Asked Questions</h2>
      <p style="color:var(--fg2);font-size:15px;line-height:1.7">Answers to questions small business owners ask before they start.</p>
    </div>
    <div class="faq-list">
{''.join(faqs)}
    </div>
    <p style="margin:28px 0 0;text-align:center;color:var(--fg2);font-size:14px">Need the broader overview? Visit <a href="/ai-for-business" style="color:var(--yb-blue);font-weight:700">AI for Business</a>.</p>
  </div>
</section>

<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#ffffff"/></svg></div>
"""


DD_CARD = (
    f'<a href="/{GENERAL_SLUG}" class="dd-card"><div class="dd-ic" style="background:var(--wash-violet);'
    f'color:var(--yb-violet)">{ICON_SVG}</div><div><span class="dd-name">AI for Business</span>'
    f'<span class="dd-desc">Practical AI for marketing teams</span></div></a>'
)
FOOTER_LI = f'<li><a href="/{GENERAL_SLUG}">AI for Business</a></li>'

HOME_CARD = f"""
      <div class="svc-card" style="--ac:var(--yb-violet)">
        <div class="svc-img"><img src="assets/svc-content.webp" alt="AI for Business"></div>
        <div class="svc-chip" style="background:var(--wash-violet);color:var(--yb-violet)">
          {ICON_SVG}
        </div>
        <h3 class="yb-h3">AI for Business</h3>
        <p>Practical AI guidance, training, and support so your team can draft content, follow up faster, and catch more leads.</p>
        <ul class="svc-feats">
          <li><span class="feat-check" style="background:var(--wash-violet);color:var(--yb-violet)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></span>Content &amp; Social</li>
          <li><span class="feat-check" style="background:var(--wash-violet);color:var(--yb-violet)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></span>Automations &amp; Follow Up</li>
          <li><span class="feat-check" style="background:var(--wash-violet);color:var(--yb-violet)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></span>Chat &amp; Voice Agents</li>
          <li><span class="feat-check" style="background:var(--wash-violet);color:var(--yb-violet)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></span>Training &amp; Support</li>
        </ul>
        <a href="/{GENERAL_SLUG}" class="svc-link" style="color:var(--yb-violet)">Learn More <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></a>
      </div>
"""


def patch_nav_footer_sources() -> None:
    nav = ROOT / "scripts" / "site_nav_snippet.py"
    text = nav.read_text(encoding="utf-8")
    if GENERAL_SLUG not in text:
        pattern = re.compile(
            r"(<a href=\"\{page_href_lang\('services/customer-growth\.html', lang\)\}\" class=\"dd-card\">.*?</a>)",
            re.S,
        )
        card = (
            f'<a href="{{page_href_lang(\'services/{GENERAL_SLUG}.html\', lang)}}" class="dd-card">'
            f'<div class="dd-ic" style="background:var(--wash-violet);color:var(--yb-violet)">{ICON_SVG}</div>'
            f'<div><span class="dd-name">{{t("AI for Business", lang)}}</span>'
            f'<span class="dd-desc">{{t("Practical AI for marketing teams", lang)}}</span></div></a>'
        )
        text2, n = pattern.subn(r"\1\n            " + card, text, count=1)
        if n:
            nav.write_text(text2, encoding="utf-8")
            print("patched site_nav_snippet.py")
        else:
            print("nav customer-growth card not found")

    foot = ROOT / "scripts" / "site_footer_snippet.py"
    text = foot.read_text(encoding="utf-8")
    if GENERAL_SLUG not in text:
        old = (
            '<li><a href="{page_href_lang(\'services/customer-growth.html\', lang)}">'
            '{t("Customer Growth & Communication Tool", lang)}</a></li>'
        )
        if old in text:
            insert = (
                old
                + "\n          <li><a href=\"{page_href_lang('services/"
                + GENERAL_SLUG
                + ".html', lang)}\">{t(\"AI for Business\", lang)}</a></li>"
            )
            foot.write_text(text.replace(old, insert, 1), encoding="utf-8")
            print("patched site_footer_snippet.py")
        else:
            print("footer marker not found")

    urls = ROOT / "scripts" / "site_urls.py"
    text = urls.read_text(encoding="utf-8")
    if f'"{GENERAL_SLUG}.html"' not in text:
        text = text.replace(
            '"customer-growth.html": "customer-growth",',
            '"customer-growth.html": "customer-growth",\n'
            f'    "{GENERAL_SLUG}.html": "{GENERAL_SLUG}",\n'
            f'    "{SMB_SLUG}.html": "{SMB_SLUG}",',
        )
        urls.write_text(text, encoding="utf-8")
        print("patched site_urls.py")

    lead = ROOT / "scripts" / "site_lead_form_snippet.py"
    text = lead.read_text(encoding="utf-8")
    if "ai-for-business" not in text:
        text = text.replace(
            '("customer-growth", "Customer Growth & Communication Tool"),\n'
            '    ("video-animation", "Video Animation"),',
            '("customer-growth", "Customer Growth & Communication Tool"),\n'
            '    ("ai-for-business", "AI for Business"),\n'
            '    ("ai-for-small-business", "AI for Small Business"),\n'
            '    ("video-animation", "Video Animation"),',
        )
        text = text.replace(
            '"Customer Growth": "customer-growth",\n'
            '    "Video": "video-animation",',
            '"Customer Growth": "customer-growth",\n'
            '    "AI for Business": "ai-for-business",\n'
            '    "AI for Small": "ai-for-small-business",\n'
            '    "Video": "video-animation",',
        )
        lead.write_text(text, encoding="utf-8")
        print("patched site_lead_form_snippet.py")

    vercel = ROOT / "vercel.json"
    text = vercel.read_text(encoding="utf-8")
    if "ai-services" not in text:
        needle = '{ "source": "/services/crm-tutorials", "destination": "/crm-tutorials", "permanent": true },'
        add = (
            needle
            + '\n    { "source": "/services/ai-services", "destination": "/ai-for-business", "permanent": true },'
            + '\n    { "source": "/services/ai-for-business", "destination": "/ai-for-business", "permanent": true },'
            + '\n    { "source": "/services/ai-for-small-business", "destination": "/ai-for-small-business", "permanent": true },'
        )
        if needle in text:
            vercel.write_text(text.replace(needle, add, 1), encoding="utf-8")
            print("patched vercel.json")

    schema = ROOT / "scripts" / "schema_markup.py"
    text = schema.read_text(encoding="utf-8")
    if f'"{GENERAL_SLUG}/index.html"' not in text:
        text = text.replace(
            '    "customer-growth/index.html": {\n'
            '        "slug": "customer-growth",\n'
            '        "name": "Customer Growth & Communication Tool",\n'
            '        "service_type": "Customer Relationship Management",\n'
            '        "description": "Lead management, centralized messaging, automation, and customer follow up for Pacific Northwest businesses.",\n'
            "    },\n}",
            '    "customer-growth/index.html": {\n'
            '        "slug": "customer-growth",\n'
            '        "name": "Customer Growth & Communication Tool",\n'
            '        "service_type": "Customer Relationship Management",\n'
            '        "description": "Lead management, centralized messaging, automation, and customer follow up for Pacific Northwest businesses.",\n'
            "    },\n"
            f'    "{GENERAL_SLUG}/index.html": {{\n'
            f'        "slug": "{GENERAL_SLUG}",\n'
            '        "name": "AI for Business",\n'
            '        "service_type": "Artificial Intelligence Consulting",\n'
            '        "description": "Practical AI guidance, training, and setup for marketing teams ,  content drafts, follow up, chat, and voice tools.",\n'
            "    },\n"
            f'    "{SMB_SLUG}/index.html": {{\n'
            f'        "slug": "{SMB_SLUG}",\n'
            '        "name": "AI for Small Business",\n'
            '        "service_type": "Artificial Intelligence Consulting",\n'
            '        "description": "AI consulting for small businesses ,  save time, catch more leads, and keep marketing consistent without enterprise complexity.",\n'
            "    },\n}",
        )
        schema.write_text(text, encoding="utf-8")
        print("patched schema_markup.py")

    sm = ROOT / "scripts" / "build-sitemap.py"
    text = sm.read_text(encoding="utf-8")
    if f"{GENERAL_SLUG}/index.html" not in text:
        text = text.replace(
            '("customer-growth/index.html", "Customer Growth & Communication Tool"),\n]',
            '("customer-growth/index.html", "Customer Growth & Communication Tool"),\n'
            f'    ("{GENERAL_SLUG}/index.html", "AI for Business"),\n'
            f'    ("{SMB_SLUG}/index.html", "AI for Small Business"),\n]',
        )
        sm.write_text(text, encoding="utf-8")
        print("patched build-sitemap.py")


def patch_html_files() -> int:
    n = 0
    for path in ROOT.rglob("*.html"):
        if any(x in path.as_posix() for x in ("node_modules", "next/", "_next/")):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if f'href="/{GENERAL_SLUG}"' in text and "AI for Business" in text:
            continue
        orig = text
        # Desktop dropdown after customer-growth
        m = re.search(
            r'(<a href="/(?:es/)?customer-growth" class="dd-card">.*?</a>)',
            text,
            re.S,
        )
        if m and f'href="/{GENERAL_SLUG}"' not in text[m.start() : m.end() + 400]:
            card = DD_CARD
            if "/es/" in m.group(1):
                card = DD_CARD.replace(f'href="/{GENERAL_SLUG}"', f'href="/es/{GENERAL_SLUG}"')
            text = text[: m.end()] + "\n            " + card + text[m.end() :]

        # Footer services list
        fm = re.search(
            r'(<li><a href="/(?:es/)?customer-growth"[^>]*>[^<]*</a></li>)',
            text,
        )
        if fm and f'href="/{GENERAL_SLUG}"' not in text[fm.start() : fm.end() + 200]:
            li = FOOTER_LI
            if "/es/" in fm.group(1):
                li = f'<li><a href="/es/{GENERAL_SLUG}">AI for Business</a></li>'
            text = text[: fm.end()] + "\n          " + li + text[fm.end() :]

        # Interest select
        if 'value="customer-growth"' in text and 'value="ai-for-business"' not in text:
            text = text.replace(
                '<option value="customer-growth">Customer Growth &amp; Communication Tool</option>',
                '<option value="customer-growth">Customer Growth &amp; Communication Tool</option>\n'
                '<option value="ai-for-business">AI for Business</option>\n'
                '<option value="ai-for-small-business">AI for Small Business</option>',
            )
            text = text.replace(
                '<option value="customer-growth" selected>Customer Growth &amp; Communication Tool</option>',
                '<option value="customer-growth" selected>Customer Growth &amp; Communication Tool</option>\n'
                '<option value="ai-for-business">AI for Business</option>\n'
                '<option value="ai-for-small-business">AI for Small Business</option>',
            )

        if text != orig:
            path.write_text(text, encoding="utf-8")
            n += 1
    return n


def patch_homepage() -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    if "AI for Business</h3>" in text or 'yb-h3">AI for Business' in text:
        print("homepage already has AI card")
        return
    needle = (
        '        <a href="/customer-growth" class="svc-link" style="color:var(--yb-blue)">Learn More '
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" '
        'stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/>'
        '<polyline points="12 5 19 12 12 19"/></svg></a>\n      </div>\n\n    </div>\n    <div class="svc-cta">'
    )
    if needle not in text:
        print("homepage marker not found")
        return
    replacement = (
        '        <a href="/customer-growth" class="svc-link" style="color:var(--yb-blue)">Learn More '
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" '
        'stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/>'
        '<polyline points="12 5 19 12 12 19"/></svg></a>\n      </div>\n'
        + HOME_CARD
        + "\n    </div>\n    <div class=\"svc-cta\">"
    )
    path.write_text(text.replace(needle, replacement, 1), encoding="utf-8")
    print("patched homepage AI card")


def main() -> None:
    general_kwargs = dict(
        slug=GENERAL_SLUG,
        title="AI for Business Services",
        meta="YB Marketing provides practical AI guidance, training, and support for businesses across the country, including content, follow up, chatbots, and voice tools. Call 509-901-9735 to get started.",
        eyebrow="AI Services",
        h1="Work smarter.<br>Grow faster.",
        lead="Practical AI guidance, training, and support so you make informed marketing decisions without added confusion.",
        body_html=general_body(),
        form_source="AI for Business Service Page",
        thank_you="/thank-you",
        interest="ai-for-business",
    )
    smb_kwargs = dict(
        slug=SMB_SLUG,
        title="AI for Small Business Services",
        meta="YB Marketing helps small businesses across the country use AI for content, follow up, chat, and voice tools that save time and catch more leads. Call 509-901-9735 to get started.",
        eyebrow="AI for Small Business",
        h1="Work smarter.<br>Grow faster.",
        lead="Practical AI guidance, training, and support sized for a small team, so you make better marketing decisions without adding confusion.",
        body_html=smb_body(),
        form_source="AI for Small Business Service Page",
        thank_you="/thank-you",
        interest="ai-for-small-business",
    )

    for slug, kwargs in ((GENERAL_SLUG, general_kwargs), (SMB_SLUG, smb_kwargs)):
        out = ROOT / slug
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(build_page(**kwargs), encoding="utf-8")
        print(f"wrote {slug}/index.html")

    patch_nav_footer_sources()
    # Rebuild pages once so headers include new nav from snippet
    import importlib
    import site_nav_snippet
    import site_footer_snippet
    importlib.reload(site_nav_snippet)
    importlib.reload(site_footer_snippet)
    global site_header_html, site_footer_html
    from site_nav_snippet import site_header_html as site_header_html
    from site_footer_snippet import site_footer_html as site_footer_html

    general_kwargs["body_html"] = general_body()
    smb_kwargs["body_html"] = smb_body()
    (ROOT / GENERAL_SLUG / "index.html").write_text(build_page(**general_kwargs), encoding="utf-8")
    (ROOT / SMB_SLUG / "index.html").write_text(build_page(**smb_kwargs), encoding="utf-8")

    patched = patch_html_files()
    print(f"patched {patched} html files for nav/footer/interest")
    patch_homepage()


if __name__ == "__main__":
    main()
