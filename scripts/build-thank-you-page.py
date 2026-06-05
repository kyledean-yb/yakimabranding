#!/usr/bin/env python3
"""Generate thank-you.html."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from reviews_section_snippet import reviews_section_html
from schema_markup import seo_head_html
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_staging_seo_snippet import STAGING_ROBOTS_META
from site_footer_snippet import site_footer_html
from site_nav_snippet import site_header_html

PREFIX = ""
header = site_header_html(PREFIX).strip()
footer = site_footer_html(PREFIX).strip()


def prepare_reviews_for_thank_you(raw: str) -> str:
    """Reviews partial assumes a navy section above and white below — adjust for thank-you layout."""
    text = raw.replace('src="../', f'src="{PREFIX}')
    # services section above is white, not navy
    text = text.replace(
        '<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>',
        '<div class="wave-div ty-wave-services-reviews"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>',
        1,
    )
    # footer below is navy, not white
    text = text.replace(
        '<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#ffffff"/></svg></div>',
        '<div class="wave-div ty-wave-reviews-footer"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div>',
        1,
    )
    return text


reviews = prepare_reviews_for_thank_you(reviews_section_html())
schema_head = seo_head_html("thank-you.html")

SERVICE_CARDS = [
    ("var(--yb-cyan)", "var(--wash-cyan)", "services/seo.html", "SEO & AI Optimization", "Rank higher on Google and AI search with a strategy built for your market.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'),
    ("var(--yb-coral)", "var(--wash-coral)", "services/google-ads.html", "Google Ads Management", "Drive qualified leads with campaigns managed by certified PPC specialists.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/></svg>'),
    ("#159468", "var(--wash-mint)", "services/web-design.html", "Web Design & Development", "Fast, conversion-focused websites built on WordPress, Wix, or custom stacks.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>'),
    ("#c77f12", "var(--wash-amber)", "services/social-media.html", "Social Media Management", "Grow your audience and turn followers into customers with consistent content.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/></svg>'),
    ("var(--yb-violet)", "var(--wash-violet)", "services/branding.html", "Branding & Design", "Logos, visual identity systems, and brand guidelines that stand out.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>'),
    ("var(--yb-violet)", "var(--wash-violet)", "services/content-creation.html", "Content Marketing", "Blog posts, copy, and content strategy that builds authority and converts.", '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>'),
]

service_cards_html = []
for accent, wash, href, title, desc, icon in SERVICE_CARDS:
    service_cards_html.append(
        f"""      <a href="{PREFIX}{href}" class="ty-svc-card">
        <div class="ty-svc-ic" style="background:{wash};color:{accent}">{icon}</div>
        <h3>{title}</h3>
        <p>{desc}</p>
        <span class="ty-svc-link" style="color:{accent}">Learn More <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span>
      </a>"""
    )

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{STAGING_ROBOTS_META}
<link rel="icon" href="{PREFIX}favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{PREFIX}favicon.png">
<title>Thank You | YB Marketing</title>
<meta name="description" content="Thank you for contacting YB Marketing. A member of our team will be in touch within 1 business day.">
<!-- TODO: Add Google Ads conversion tracking snippet here if running paid campaigns -->
<!-- TODO: Fire lead conversion event here — GA4: gtag('event', 'generate_lead') -->
<!-- TODO: Fire Meta Pixel lead event here — fbq('track', 'Lead') -->
<link rel="stylesheet" href="{PREFIX}colors_and_type.css">
<link rel="stylesheet" href="{PREFIX}site.css">
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
.ty-steps{{background:#fff;padding:88px 0}}
.ty-steps-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:40px}}
.ty-step{{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--r-lg);padding:28px}}
.ty-step-ic{{width:56px;height:56px;border-radius:var(--r-md);display:flex;align-items:center;justify-content:center;margin-bottom:18px}}
.ty-step h3{{font-family:var(--font-display);font-weight:800;font-size:15px;letter-spacing:.04em;text-transform:uppercase;color:var(--ink);margin:0 0 12px}}
.ty-step p{{font-size:14.5px;color:var(--fg2);line-height:1.65;margin:0}}
.ty-calendly{{background:var(--bg-soft);padding:88px 0}}
.ty-calendly-card{{background:#fff;border:1px solid var(--line);border-radius:var(--r-xl);padding:36px;box-shadow:var(--sh-sm);max-width:720px;margin:36px auto 0;text-align:center}}
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
</head>
<body>
{ACCESSIBE_BODY_SCRIPT}

{header}

<section class="ty-hero">
  <div class="ty-hero-mesh"></div>
  <div class="container" style="position:relative">
    <span class="eyebrow" style="color:var(--yb-coral)">Message Received</span>
    <h1>Thank You for<br><span class="ty-hero-accent">Contacting YB Marketing!</span></h1>
    <p class="ty-hero-lead">We've received your message and a member of our team will be in touch within 1 business day. We look forward to learning more about your business and how we can help you grow.</p>
    <p class="ty-hero-urgent">For urgent needs, please call us directly at <a href="tel:5099019735">(509) 901-9735</a> or email <a href="mailto:info@yakimabranding.com">info@yakimabranding.com</a></p>
    <a href="{PREFIX}index.html" class="btn btn-grad btn-lg">Return to Home
      <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
    </a>
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

<section class="ty-calendly" id="book">
  <div class="container" style="text-align:center">
    <h2 style="font-size:clamp(1.6rem,2.4vw,2rem);margin:0 0 12px">Don't Want to Wait? Book a Meeting Now.</h2>
    <p class="yb-lead" style="max-width:560px;margin:0 auto">Schedule your free 30-minute introduction call directly — no forms, no back and forth.</p>
    <div class="ty-calendly-card">
      <div style="width:56px;height:56px;background:var(--grad-brand);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 12px;font-family:var(--font-display);font-weight:800;font-size:22px;color:#fff">YB</div>
      <div style="font-size:12px;font-weight:600;color:var(--fg3);margin-bottom:4px">YB Marketing Team</div>
      <div style="font-weight:700;font-size:18px;color:var(--ink);margin-bottom:6px">Introduction Meeting</div>
      <div style="display:inline-flex;align-items:center;gap:6px;font-size:13px;color:var(--fg3);background:var(--bg-soft);border-radius:var(--r-pill);padding:5px 12px;border:1px solid var(--line);margin-bottom:16px">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        30 min · Free
      </div>
      <p style="font-size:13.5px;color:var(--fg2);margin-bottom:20px;line-height:1.6">An introduction meeting to learn more about your business, your goals, and how we can help you grow. No commitment required.</p>
      <!-- Replace with your actual Calendly inline embed -->
      <!-- <div class="calendly-inline-widget" data-url="https://calendly.com/yakimabranding/introduction-meeting" style="min-width:320px;height:630px;"></div>
           <script src="https://assets.calendly.com/assets/external/widget.js" async></script> -->
      <a href="https://calendly.com/yakimabranding" target="_blank" rel="noopener" class="btn btn-grad" style="width:100%;max-width:360px;justify-content:center;padding:15px">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>
        Schedule on Calendly
      </a>
      <p style="text-align:center;font-size:11.5px;color:var(--fg3);margin-top:10px">Replace the button above with a Calendly inline embed when your link is ready.</p>
    </div>
  </div>
</section>

<section class="ty-services">
  <div class="container">
    <div style="text-align:center;max-width:640px;margin:0 auto">
      <span class="eyebrow" style="color:var(--yb-blue)">Explore Our Services</span>
      <h2 style="margin:14px 0 0;font-size:clamp(1.8rem,2.6vw,2.4rem)">While You Wait, Explore What YB Can Do For You</h2>
    </div>
    <div class="ty-svc-grid">
{chr(10).join(service_cards_html)}
    </div>
  </div>
</section>

{reviews}

{footer}

<script>
if (typeof window !== 'undefined') {{
  window.history.replaceState(null, '', '{PREFIX}thank-you.html');
}}
// Optional: redirect to homepage after 60 seconds
// setTimeout(function() {{ window.location.href = '{PREFIX}index.html'; }}, 60000);
</script>
<script src="{PREFIX}js/newsletter-popup.js" defer></script>
<script src="{PREFIX}js/chat-widget.js" defer></script>
<script src="{PREFIX}js/site.js" defer></script>
</body>
</html>
"""

(ROOT / "thank-you.html").write_text(html, encoding="utf-8")
print("wrote thank-you.html")
