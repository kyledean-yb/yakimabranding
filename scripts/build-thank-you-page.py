#!/usr/bin/env python3
"""Generate thank-you pages (general, home, contact, per-service, per-location)."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from reviews_section_snippet import reviews_section_html
from schema_markup import seo_head_html
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_tracking_snippet import ATTRIBUTER_FOOTER_BLOCK, GTM_BODY_NOSCRIPT_BLOCK, TRACKING_HEAD_BLOCK
from site_staging_seo_snippet import THANK_YOU_ROBOTS_META
from site_footer_snippet import site_footer_html
from site_nav_snippet import site_header_html
from site_schedule_grid_snippet import thank_you_calendly_section_html
from site_thank_you_lead_snippet import thank_you_lead_script_html

SERVICE_PAGES = [
    ("seo", "SEO", "seo.html"),
    ("google-ads", "Google Ads", "google-ads.html"),
    ("web-design", "Web Design", "web-design.html"),
    ("social-media", "Social Media", "social-media.html"),
    ("branding", "Branding", "branding.html"),
    ("content-creation", "Content Marketing", "content-creation.html"),
    ("press-releases", "Press Releases", "press-releases.html"),
]

SERVICE_CARDS = [
    ("var(--yb-cyan)", "var(--wash-cyan)", "services/seo.html", "SEO & AI Optimization", "Rank higher on Google and AI search with a strategy built for your market.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'),
    ("var(--yb-coral)", "var(--wash-coral)", "services/google-ads.html", "Google Ads Management", "Drive qualified leads with campaigns managed by certified PPC specialists.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/></svg>'),
    ("#159468", "var(--wash-mint)", "services/web-design.html", "Web Design & Development", "Fast, conversion-focused websites built on WordPress, Wix, or custom stacks.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>'),
    ("#c77f12", "var(--wash-amber)", "services/social-media.html", "Social Media Management", "Grow your audience and turn followers into customers with consistent content.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/></svg>'),
    ("var(--yb-violet)", "var(--wash-violet)", "services/branding.html", "Branding & Design", "Logos, visual identity systems, and brand guidelines that stand out.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>'),
    ("var(--yb-violet)", "var(--wash-violet)", "services/content-creation.html", "Content Marketing", "Blog posts, copy, and content strategy that builds authority and converts.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>'),
]


def load_location_hubs() -> list[dict]:
    script = """
    import { locationHubs } from './data/locationHubs.js';
    console.log(JSON.stringify(locationHubs.map((l) => ({ slug: l.slug, city: l.city }))));
    """
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def prepare_reviews_for_thank_you(raw: str, prefix: str) -> str:
    """Reviews partial assumes a navy section above and white below — adjust for thank-you layout."""
    text = raw.replace('src="../', f'src="{prefix}')
    text = text.replace(
        '<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>',
        '<div class="wave-div ty-wave-services-reviews"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>',
        1,
    )
    text = text.replace(
        '<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#ffffff"/></svg></div>',
        '<div class="wave-div ty-wave-reviews-footer"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div>',
        1,
    )
    return text


def service_cards_html(prefix: str) -> str:
    cards = []
    for accent, wash, href, title, desc, icon in SERVICE_CARDS:
        cards.append(
            f"""      <a href="{prefix}{href}" class="ty-svc-card">
        <div class="ty-svc-ic" style="background:{wash};color:{accent}">{icon}</div>
        <h3>{title}</h3>
        <p>{desc}</p>
        <span class="ty-svc-link" style="color:{accent}">Learn More <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span>
      </a>"""
        )
    return "\n".join(cards)


def build_thank_you_html(variant: dict) -> str:
    prefix = variant["prefix"]
    schema_head = seo_head_html(variant["schema_path"])
    header = site_header_html(prefix).strip()
    footer = site_footer_html(prefix).strip()
    reviews = prepare_reviews_for_thank_you(reviews_section_html(), prefix)
    calendly_section = thank_you_calendly_section_html(prefix)
    cards = service_cards_html(prefix)

    return f"""<!DOCTYPE html>
<html lang="en" data-yb-lead-source="{variant["lead_source"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{THANK_YOU_ROBOTS_META}
<link rel="icon" href="{prefix}favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{prefix}favicon.png">
<title>{variant["title"]}</title>
<meta name="description" content="Thank you for contacting YB Marketing. A member of our team will be in touch within 1 business day.">
<!-- TODO: Add Google Ads conversion tracking snippet here if running paid campaigns -->
<link rel="stylesheet" href="{prefix}colors_and_type.css">
<link rel="stylesheet" href="{prefix}site.css">
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
.ty-hero{{background:var(--grad-navy);position:relative;overflow:hidden;padding:100px 0 88px;text-align:center}}
.ty-hero-mesh{{position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.65;pointer-events:none}}
.ty-hero h1{{font-family:var(--font-display);font-weight:800;font-size:clamp(2.2rem,4vw,3.4rem);color:#fff;line-height:1.08;margin:18px 0}}
.ty-hero-accent{{background:var(--grad-brand);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.ty-hero-lead{{color:var(--fg2-on-dark);font-size:clamp(1rem,1.4vw,1.12rem);line-height:1.7;max-width:640px;margin:0 auto 24px}}
.ty-hero-urgent{{color:rgba(255,255,255,.75);font-size:14.5px;line-height:1.65;max-width:560px;margin:0 auto 32px}}
.ty-hero-urgent a{{color:var(--yb-cyan);font-weight:600}}
.ty-hero-actions{{display:flex;flex-wrap:wrap;gap:12px;justify-content:center}}
.ty-steps{{background:#fff;padding:88px 0}}
.ty-steps-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:40px}}
.ty-step{{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--r-lg);padding:28px}}
.ty-step-ic{{width:56px;height:56px;border-radius:var(--r-md);display:flex;align-items:center;justify-content:center;margin-bottom:18px}}
.ty-step h3{{font-family:var(--font-display);font-weight:800;font-size:15px;letter-spacing:.04em;text-transform:uppercase;color:var(--ink);margin:0 0 12px}}
.ty-step p{{font-size:14.5px;color:var(--fg2);line-height:1.65;margin:0}}
.ty-calendly{{background:var(--bg-soft);padding:88px 0}}
.ty-calendly-card{{background:#fff;border:1px solid var(--line);border-radius:var(--r-xl);padding:36px;box-shadow:var(--sh-sm);max-width:720px;margin:36px auto 0;text-align:center}}
.ty-calendly-card--schedule{{max-width:640px;text-align:left}}
.ty-calendly-card--schedule .yb-schedule-intro{{margin-top:0}}
.ty-services{{background:#fff;padding:88px 0}}
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
}}
@media(max-width:900px){{
  .ty-hero{{padding:72px 0 64px}}
  .ty-steps,.ty-calendly,.ty-services{{padding:64px 0}}
  .ty-steps-grid{{grid-template-columns:1fr}}
  .ty-svc-grid{{grid-template-columns:1fr}}
  .reviews-bg{{padding-top:64px!important}}
}}
@media(max-width:640px){{
  .container{{padding:0 20px}}
  .ty-hero{{padding:56px 0 48px}}
  .ty-hero-urgent{{font-size:13px;padding:0 4px}}
  .ty-calendly-card{{padding:24px 20px}}
  .rv-scroll-card{{width:min(300px,calc(100vw - 48px))}}
}}
</style>
{schema_head}
{TRACKING_HEAD_BLOCK}
</head>
<body>
{GTM_BODY_NOSCRIPT_BLOCK}
{ACCESSIBE_BODY_SCRIPT}

{header}

<section class="ty-hero">
  <div class="ty-hero-mesh"></div>
  <div class="container" style="position:relative">
    <span class="eyebrow" style="color:var(--yb-coral)">Message Received</span>
    <h1>Thank You for<br><span class="ty-hero-accent">Contacting YB Marketing!</span></h1>
    <p class="ty-hero-lead">We've received your message and a member of our team will be in touch within 1 business day. We look forward to learning more about your business and how we can help you grow.</p>
    <p class="ty-hero-urgent">For urgent needs, please call us directly at <a href="tel:5099019735">(509) 901-9735</a> or email <a href="mailto:info@yakimabranding.com">info@yakimabranding.com</a></p>
    <div class="ty-hero-actions">
      <a href="{variant["cta_href"]}" class="btn btn-grad btn-lg">{variant["cta_label"]}
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
      </a>
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
        <h3>We Review Your Message</h3>
        <p>A real member of the YB team — not a bot — reviews every inquiry personally and routes it to the right specialist for your needs.</p>
      </div>
      <div class="ty-step">
        <div class="ty-step-ic" style="background:var(--wash-cyan);color:var(--yb-cyan)">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 16 0 0 0 6.07 6.07l1.08-.9a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        </div>
        <h3>We Reach Out Within 1 Business Day</h3>
        <p>Expect a call or email from our team within 1 business day. If you'd like to skip the wait, book a 30-minute intro call directly using the link below.</p>
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

{calendly_section}

<section class="ty-services">
  <div class="container">
    <div style="text-align:center;max-width:640px;margin:0 auto">
      <span class="eyebrow" style="color:var(--yb-blue)">Explore Our Services</span>
      <h2 style="margin:14px 0 0;font-size:clamp(1.8rem,2.6vw,2.4rem)">While You Wait, Explore What YB Can Do For You</h2>
    </div>
    <div class="ty-svc-grid">
{cards}
    </div>
  </div>
</section>

{reviews}

{footer}

<script>
if (typeof window !== 'undefined') {{
  window.history.replaceState(null, '', '{variant["history_path"]}');
}}
</script>
<script src="{prefix}js/newsletter-popup.js" defer></script>
<script src="{prefix}js/chat-widget.js" defer></script>
<script src="{prefix}js/site.js" defer></script>
{thank_you_lead_script_html(prefix)}
{ATTRIBUTER_FOOTER_BLOCK}
</body>
</html>
"""


def all_variants() -> list[dict]:
    variants = [
        {
            "output": ROOT / "thank-you.html",
            "schema_path": "thank-you.html",
            "prefix": "",
            "title": "Thank You | YB Marketing",
            "history_path": "thank-you.html",
            "lead_source": "general",
            "cta_href": "index.html",
            "cta_label": "Return to Home",
        },
        {
            "output": ROOT / "thank-you-home.html",
            "schema_path": "thank-you-home.html",
            "prefix": "",
            "title": "Thank You | YB Marketing",
            "history_path": "thank-you-home.html",
            "lead_source": "home",
            "cta_href": "index.html",
            "cta_label": "Return to Home",
        },
        {
            "output": ROOT / "thank-you-contact.html",
            "schema_path": "thank-you-contact.html",
            "prefix": "",
            "title": "Thank You for Contacting Us | YB Marketing",
            "history_path": "thank-you-contact.html",
            "lead_source": "contact",
            "cta_href": "contact.html",
            "cta_label": "Return to Contact",
        },
    ]

    for key, label, service_file in SERVICE_PAGES:
        filename = f"thank-you-{key}.html"
        variants.append(
            {
                "output": ROOT / "services" / filename,
                "schema_path": f"services/{filename}",
                "prefix": "../",
                "title": f"Thank You | {label} | YB Marketing",
                "history_path": filename,
                "lead_source": f"service_{key}",
                "cta_href": service_file,
                "cta_label": f"Return to {label}",
            }
        )

    for hub in load_location_hubs():
        slug = hub["slug"]
        city = hub["city"]
        filename = f"thank-you-{slug}.html"
        variants.append(
            {
                "output": ROOT / "locations" / filename,
                "schema_path": f"locations/{filename}",
                "prefix": "../",
                "title": f"Thank You | {city} | YB Marketing",
                "history_path": filename,
                "lead_source": f"location_{slug}",
                "cta_href": f"{slug}.html",
                "cta_label": f"Return to {city}",
            }
        )

    return variants


def main() -> None:
    for variant in all_variants():
        html = build_thank_you_html(variant)
        variant["output"].parent.mkdir(parents=True, exist_ok=True)
        variant["output"].write_text(html, encoding="utf-8")
        print(f"wrote {variant['output'].relative_to(ROOT)}")


if __name__ == "__main__":
    main()
