#!/usr/bin/env python3
"""Generate team-member thank-you pages (about/thank-you-{slug}.html)."""

from __future__ import annotations

import html
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

_spec = importlib.util.spec_from_file_location(
    "build_thank_you_page", ROOT / "scripts" / "build-thank-you-page.py"
)
_build_ty = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_build_ty)

ROOT_PREFIX = _build_ty.PREFIX
prepare_reviews_for_thank_you = _build_ty.prepare_reviews_for_thank_you
service_cards_html = _build_ty.service_cards_html
from reviews_section_snippet import reviews_section_html
from schema_markup import seo_head_html
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_footer_snippet import site_footer_html
from site_nav_snippet import site_header_html
from site_staging_seo_snippet import STAGING_ROBOTS_META

ABOUT_PREFIX = "../"
ABOUT_DIR = ROOT / "about"

TEAM_MEMBERS = [
    {
        "slug": "jacob",
        "name": "Jacob Ross",
        "short": "Jacob",
        "role": "Account Executive",
        "photo": "jacob-headshot.webp",
        "calendly": "https://calendly.com/jacobybmarketing",
        "email": "jacob@yakimabranding.com",
        "phone": "5092031007",
        "phone_display": "(509) 203-1007",
        "lead": (
            "Digital marketing expert and self-proclaimed grill master — "
            "building memorable brands with data-driven campaigns."
        ),
        "bio": (
            "Jacob believes good is never enough when greatness is within reach. "
            "With more than four years of digital marketing sales experience, he brings "
            "the best ingredients to every project so each client's brand stands out and stays memorable."
        ),
        "interests": ["Website", "SEO", "Google Ads", "Social Media"],
        "profile_href": "jacob.html",
    },
    {
        "slug": "kevin",
        "name": "Kevin Dean",
        "short": "Kevin",
        "role": "Owner",
        "photo": "kevin-headshot.webp",
        "calendly": "https://calendly.com/kdean-wsi",
        "email": "kevin@yakimabranding.com",
        "phone": "5099019735",
        "phone_display": "(509) 901-9735",
        "lead": (
            "Certified advertising professional and SEO expert leading YB Marketing with a focus "
            "on superior service, clear communication, and measurable ROI."
        ),
        "bio": (
            "Kevin specializes in helping businesses grow through better utilization of the Internet "
            "to generate leads and increase visibility. With an MBA, senior management experience, "
            "and advanced marketing skills, he works with our team to find opportunities for increasing "
            "online branding, lead generation, and overall return on investment."
        ),
        "interests": ["SEO", "Google Ads", "Web Strategy", "Branding"],
        "profile_href": "kevin.html",
    },
    {
        "slug": "kristin",
        "name": "Kristin Sparling",
        "short": "Kristin",
        "role": "Account Executive",
        "photo": "kristin-headshot.webp",
        "calendly": "https://calendly.com/kristin-sparling/connect",
        "email": "kristin@yakimabranding.com",
        "phone": "5099401799",
        "phone_display": "(509) 940-1799",
        "lead": (
            "Strategy-first account executive helping Pacific Northwest businesses grow "
            "with tailored digital marketing plans."
        ),
        "bio": (
            "Kristin brings strategic insight and hands-on expertise from over three years in digital marketing. "
            "She is committed to understanding each client's story, identifying their goals, and developing "
            "tailored marketing plans that drive measurable growth across Washington."
        ),
        "interests": ["Website", "Social Media", "SEO", "Google Ads", "Graphic Design"],
        "profile_href": "kristin.html",
    },
    {
        "slug": "sophie",
        "name": "Sophie Mann",
        "short": "Sophie",
        "role": "Account Executive",
        "photo": "sophie-headshot.webp",
        "calendly": "https://calendly.com/sophie-yakimabranding/30min",
        "email": "sophie@yakimabranding.com",
        "phone": "3039556979",
        "phone_display": "(303) 955-6979",
        "lead": (
            "Strategic communications specialist with deep expertise in education and manufacturing — "
            "now serving clients from Chicago."
        ),
        "bio": (
            "Sophie thrives on building lasting partnerships and turning big ideas into smart, measurable campaigns. "
            "With seven-plus years in agency life, she helps brands sharpen their voice and connect with the audiences "
            "that matter most — from content strategy to creative direction."
        ),
        "interests": ["Content Strategy", "Social Media", "Branding", "Creative Direction"],
        "profile_href": "sophie.html",
    },
]

CAL_ICON = (
    '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2.2" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/>'
    '<line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/>'
    '<line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>'
)


def member_calendly_section(member: dict) -> str:
    name = html.escape(member["name"])
    short = html.escape(member["short"])
    calendly = html.escape(member["calendly"])
    photo = html.escape(f"{ABOUT_PREFIX}assets/{member['photo']}")
    return f"""<section class="ty-calendly" id="book">
  <div class="container" style="text-align:center">
    <h2 style="font-size:clamp(1.6rem,2.4vw,2rem);margin:0 0 12px">Don't Want to Wait? Book a Meeting with {short}.</h2>
    <p class="yb-lead" style="max-width:560px;margin:0 auto 36px">Schedule your free 30-minute introduction call directly — no forms, no back and forth.</p>
    <div class="ty-calendly-card ty-calendly-card--member">
      <div class="ty-member-calendly-intro">
        <img src="{photo}" alt="{name}" class="ty-member-calendly-photo" width="88" height="88" loading="lazy">
        <div class="ty-member-calendly-meta">YB Marketing · {name}</div>
        <div class="ty-member-calendly-title">Introduction Meeting</div>
        <div class="ty-member-calendly-duration">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          30 min · Free
        </div>
        <p class="ty-member-calendly-desc">Book time to discuss your business and how YB Marketing can help you grow.</p>
      </div>
      <a href="{calendly}" class="btn btn-grad ty-member-calendly-btn" target="_blank" rel="noopener">Book a Meeting with {short} {CAL_ICON}</a>
    </div>
  </div>
</section>"""


def member_about_section(member: dict) -> str:
    short = html.escape(member["short"])
    bio = html.escape(member["bio"])
    lead = html.escape(member["lead"])
    interests = "".join(
        f'<span class="ty-member-interest">{html.escape(item)}</span>'
        for item in member["interests"]
    )
    profile = html.escape(member["profile_href"])
    return f"""<section class="ty-member-about">
  <div class="container">
    <div class="ty-member-about-grid">
      <div>
        <span class="eyebrow" style="color:var(--yb-blue)">About {short}</span>
        <h2 style="margin:14px 0 16px;font-size:clamp(1.6rem,2.4vw,2rem)">Your YB Marketing contact</h2>
        <p class="ty-member-about-lead">{lead}</p>
        <p class="ty-member-about-bio">{bio}</p>
        <a href="{profile}" class="btn btn-grad" style="margin-top:8px">View {short}'s Profile
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </a>
      </div>
      <div class="ty-member-about-side">
        <h3 style="font-size:15px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:var(--ink);margin:0 0 14px">Interested in?</h3>
        <div class="ty-member-interests">{interests}</div>
      </div>
    </div>
  </div>
</section>"""


def build_team_thank_you_html(member: dict) -> str:
    p = ABOUT_PREFIX
    filename = f"about/thank-you-{member['slug']}.html"
    schema_head = seo_head_html(filename)
    header = site_header_html(p).strip()
    footer = site_footer_html(p).strip()
    reviews = prepare_reviews_for_thank_you(reviews_section_html()).replace(
        f'src="{ROOT_PREFIX}', f'src="{p}'
    )

    name = html.escape(member["name"])
    short = html.escape(member["short"])
    role = html.escape(member["role"])
    photo = html.escape(f"{p}assets/{member['photo']}")
    email = html.escape(member["email"])
    phone_display = html.escape(member["phone_display"])
    phone = html.escape(member["phone"])
    profile = html.escape(member["profile_href"])
    history_path = f"thank-you-{member['slug']}.html"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{STAGING_ROBOTS_META}
<link rel="icon" href="{p}favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{p}favicon.png">
<title>Thank You — {name} | YB Marketing</title>
<meta name="description" content="Thank you for contacting {name} at YB Marketing. {short} will be in touch within 1 business day.">
<link rel="stylesheet" href="{p}colors_and_type.css">
<link rel="stylesheet" href="{p}site.css">
<link rel="stylesheet" href="{p}team-profile.css">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--font-body);background:var(--bg);color:var(--fg1);-webkit-font-smoothing:antialiased;overflow-x:hidden}}
a{{color:inherit;text-decoration:none}}
.container{{width:100%;max-width:var(--container);margin:0 auto;padding:0 28px}}
.eyebrow{{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-size:13px;letter-spacing:.14em;text-transform:uppercase}}
.eyebrow::before{{content:'';width:7px;height:7px;border-radius:50%;background:currentColor;flex:none}}
.btn{{display:inline-flex;align-items:center;gap:8px;border:none;cursor:pointer;font-family:var(--font-body);font-weight:700;font-size:15px;border-radius:var(--r-md);padding:13px 22px;transition:all 240ms;text-decoration:none;line-height:1}}
.btn-grad{{background:var(--grad-brand);color:#fff;box-shadow:0 14px 30px -10px rgba(63,111,214,.45)}}
.btn-grad:hover{{transform:translateY(-2px);filter:brightness(1.06)}}
.btn-lg{{padding:16px 28px;font-size:16px}}
.wave-div{{position:relative;overflow:hidden;line-height:0;font-size:0}}
.wave-div svg{{display:block;width:100%;height:70px}}
.ty-hero{{background:var(--grad-navy);position:relative;overflow:hidden;padding:88px 0 72px}}
.ty-hero-mesh{{position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.65;pointer-events:none}}
.ty-hero-member-grid{{position:relative;display:grid;grid-template-columns:140px 1fr;gap:32px;align-items:center;max-width:880px;margin:0 auto}}
.ty-hero-photo{{width:140px;height:140px;border-radius:50%;object-fit:cover;border:4px solid rgba(255,255,255,.18);box-shadow:0 18px 40px rgba(0,0,0,.25)}}
.ty-hero-copy{{text-align:left}}
.ty-hero-copy h1{{font-family:var(--font-display);font-weight:800;font-size:clamp(2rem,3.6vw,3rem);color:#fff;line-height:1.08;margin:14px 0 8px}}
.ty-hero-accent{{background:var(--grad-brand);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.ty-hero-role{{color:var(--yb-cyan);font-weight:700;font-size:15px;margin:0 0 14px}}
.ty-hero-lead{{color:var(--fg2-on-dark);font-size:clamp(1rem,1.35vw,1.1rem);line-height:1.7;margin:0 0 18px;max-width:560px}}
.ty-hero-urgent{{color:rgba(255,255,255,.75);font-size:14.5px;line-height:1.65;margin:0 0 22px}}
.ty-hero-urgent a{{color:var(--yb-cyan);font-weight:600}}
.ty-hero-actions{{display:flex;flex-wrap:wrap;gap:12px}}
.ty-steps{{background:#fff;padding:88px 0}}
.ty-steps-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:40px}}
.ty-step{{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--r-lg);padding:28px}}
.ty-step-ic{{width:56px;height:56px;border-radius:var(--r-md);display:flex;align-items:center;justify-content:center;margin-bottom:18px}}
.ty-step h3{{font-family:var(--font-display);font-weight:800;font-size:15px;letter-spacing:.04em;text-transform:uppercase;color:var(--ink);margin:0 0 12px}}
.ty-step p{{font-size:14.5px;color:var(--fg2);line-height:1.65;margin:0}}
.ty-calendly{{background:var(--bg-soft);padding:88px 0}}
.ty-calendly-card{{background:#fff;border:1px solid var(--line);border-radius:var(--r-xl);padding:36px;box-shadow:var(--sh-sm);max-width:720px;margin:36px auto 0;text-align:center}}
.ty-calendly-card--member{{max-width:520px}}
.ty-member-calendly-intro{{display:flex;flex-direction:column;align-items:center;text-align:center;margin-bottom:22px}}
.ty-member-calendly-photo{{width:88px;height:88px;border-radius:50%;object-fit:cover;margin-bottom:14px;border:3px solid var(--line)}}
.ty-member-calendly-meta{{font-size:12px;font-weight:600;color:var(--fg3);margin-bottom:4px}}
.ty-member-calendly-title{{font-weight:700;font-size:18px;color:var(--ink);margin-bottom:8px}}
.ty-member-calendly-duration{{display:inline-flex;align-items:center;gap:6px;font-size:13px;color:var(--fg3);background:var(--bg-soft);border-radius:var(--r-pill);padding:5px 12px;border:1px solid var(--line);margin-bottom:14px}}
.ty-member-calendly-desc{{font-size:13.5px;color:var(--fg2);line-height:1.6;max-width:360px;margin:0 auto}}
.ty-member-calendly-btn{{width:100%;max-width:360px;justify-content:center;padding:15px;margin:0 auto}}
.ty-member-about{{background:#fff;padding:88px 0}}
.ty-member-about-grid{{display:grid;grid-template-columns:1.4fr .8fr;gap:40px;align-items:start}}
.ty-member-about-lead{{font-size:16px;color:var(--fg2);line-height:1.7;margin:0 0 14px}}
.ty-member-about-bio{{font-size:15px;color:var(--fg2);line-height:1.7;margin:0 0 18px}}
.ty-member-about-side{{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--r-xl);padding:28px}}
.ty-member-interests{{display:flex;flex-wrap:wrap;gap:10px}}
.ty-member-interest{{display:inline-flex;padding:8px 14px;border-radius:var(--r-pill);background:var(--wash-coral);color:var(--yb-coral);font-size:13px;font-weight:700}}
.ty-services{{background:var(--bg-soft);padding:88px 0}}
.ty-svc-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:40px}}
.ty-svc-card{{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:24px;box-shadow:var(--sh-xs);transition:transform 240ms,box-shadow 240ms;text-decoration:none;color:inherit;display:flex;flex-direction:column;height:100%}}
.ty-svc-card:hover{{transform:translateY(-4px);box-shadow:var(--sh-md)}}
.ty-svc-ic{{width:48px;height:48px;border-radius:var(--r-md);display:flex;align-items:center;justify-content:center;margin-bottom:14px}}
.ty-svc-ic svg{{width:22px;height:22px}}
.ty-svc-card h3{{font-size:16px;color:var(--ink);margin:0 0 8px;line-height:1.35}}
.ty-svc-card p{{font-size:14px;color:var(--fg2);line-height:1.6;margin:0 0 16px;flex:1}}
.ty-svc-link{{font-size:13px;font-weight:700;display:inline-flex;align-items:center;gap:5px;margin-top:auto}}
.ty-wave-services-reviews{{background:#ffffff}}
.ty-wave-reviews-footer{{background:#F6F8FC}}
.reviews-bg{{background:var(--bg-soft)}}
.reviews-scroll-track{{display:flex;width:max-content;animation:rv-scroll 50s linear infinite;gap:22px}}
.reviews-scroll-track:hover{{animation-play-state:paused}}
.reviews-scroll-set{{display:flex;gap:22px}}
.rv-scroll-card{{width:320px;background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:22px;box-shadow:var(--sh-sm);flex:none;display:flex;flex-direction:column}}
@keyframes rv-scroll{{from{{transform:translateX(0)}}to{{transform:translateX(-50%)}}}}
@media(prefers-reduced-motion:reduce){{.reviews-scroll-track{{animation:none}}}}
@media(max-width:1024px){{
  .ty-svc-grid{{grid-template-columns:repeat(2,1fr)}}
  .ty-steps-grid{{grid-template-columns:1fr 1fr}}
  .ty-member-about-grid{{grid-template-columns:1fr}}
}}
@media(max-width:900px){{
  .ty-hero{{padding:72px 0 64px}}
  .ty-hero-member-grid{{grid-template-columns:1fr;text-align:center;justify-items:center}}
  .ty-hero-copy{{text-align:center}}
  .ty-hero-actions{{justify-content:center}}
  .ty-steps,.ty-calendly,.ty-services,.ty-member-about{{padding:64px 0}}
  .ty-steps-grid{{grid-template-columns:1fr}}
  .ty-svc-grid{{grid-template-columns:1fr}}
  .reviews-bg{{padding-top:64px!important}}
}}
@media(max-width:640px){{
  .container{{padding:0 20px}}
  .ty-hero{{padding:56px 0 48px}}
  .ty-hero-photo{{width:120px;height:120px}}
  .ty-calendly-card{{padding:24px 20px}}
  .rv-scroll-card{{width:min(300px,calc(100vw - 48px))}}
}}
</style>
{schema_head}
</head>
<body>
{ACCESSIBE_BODY_SCRIPT}

{header}

<section class="ty-hero">
  <div class="ty-hero-mesh"></div>
  <div class="container ty-hero-member-grid">
    <img src="{photo}" alt="{name}" class="ty-hero-photo" width="140" height="140" loading="eager">
    <div class="ty-hero-copy">
      <span class="eyebrow" style="color:var(--yb-coral)">Message Received</span>
      <h1>Thank You for<br><span class="ty-hero-accent">Reaching Out to {short}!</span></h1>
      <p class="ty-hero-role">{role} · YB Marketing</p>
      <p class="ty-hero-lead">{short} received your message and will be in touch within 1 business day. We look forward to learning more about your business and how we can help you grow.</p>
      <p class="ty-hero-urgent">For urgent needs, call <a href="tel:{phone}">{phone_display}</a> or email <a href="mailto:{email}">{email}</a></p>
      <div class="ty-hero-actions">
        <a href="{profile}" class="btn btn-grad btn-lg">Back to {short}'s Profile
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </a>
      </div>
    </div>
  </div>
</section>

<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z" fill="#ffffff"/></svg></div>

<section class="ty-steps">
  <div class="container">
    <div style="text-align:center;max-width:640px;margin:0 auto">
      <span class="eyebrow" style="color:var(--yb-blue)">What to Expect</span>
      <h2 style="margin:14px 0 0;font-size:clamp(1.8rem,2.6vw,2.4rem)">Here's What Happens Next</h2>
    </div>
    <div class="ty-steps-grid">
      <div class="ty-step">
        <div class="ty-step-ic" style="background:var(--wash-blue);color:var(--yb-blue)">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        </div>
        <h3>{short} Reviews Your Message</h3>
        <p>{short} personally reviews every inquiry and routes it to the right specialist on our team for your needs.</p>
      </div>
      <div class="ty-step">
        <div class="ty-step-ic" style="background:var(--wash-cyan);color:var(--yb-cyan)">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 16 0 0 0 6.07 6.07l1.08-.9a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        </div>
        <h3>We Reach Out Within 1 Business Day</h3>
        <p>Expect a call or email from {short} within 1 business day. Prefer to skip the wait? Book a 30-minute intro call below.</p>
      </div>
      <div class="ty-step">
        <div class="ty-step-ic" style="background:var(--wash-mint);color:var(--yb-mint)">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
        </div>
        <h3>We Build Your Custom Strategy</h3>
        <p>Once we connect, we'll start with a free audit of your website and marketing channels — and build a strategy tailored to your business and goals.</p>
      </div>
    </div>
  </div>
</section>

{member_calendly_section(member)}

{member_about_section(member)}

<section class="ty-services">
  <div class="container">
    <div style="text-align:center;max-width:640px;margin:0 auto">
      <span class="eyebrow" style="color:var(--yb-blue)">Explore Our Services</span>
      <h2 style="margin:14px 0 0;font-size:clamp(1.8rem,2.6vw,2.4rem)">While You Wait, Explore What YB Can Do For You</h2>
    </div>
    <div class="ty-svc-grid">
{chr(10).join(service_cards_html).replace(f'href="{ROOT_PREFIX}', f'href="{p}')}
    </div>
  </div>
</section>

{reviews}

{footer}

<script>
if (typeof window !== 'undefined') {{
  window.history.replaceState(null, '', '{history_path}');
}}
</script>
<script src="{p}js/newsletter-popup.js" defer></script>
<script src="{p}js/chat-widget.js" defer></script>
<script src="{p}js/site.js" defer></script>
</body>
</html>
"""


def main() -> None:
    ABOUT_DIR.mkdir(parents=True, exist_ok=True)
    for member in TEAM_MEMBERS:
        out = ABOUT_DIR / f"thank-you-{member['slug']}.html"
        out.write_text(build_team_thank_you_html(member), encoding="utf-8")
        print(f"wrote about/thank-you-{member['slug']}.html")


if __name__ == "__main__":
    main()
