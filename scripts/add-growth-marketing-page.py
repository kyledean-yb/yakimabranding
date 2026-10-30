#!/usr/bin/env python3
"""Build the Growth Marketing page (/growth-marketing)."""

from __future__ import annotations

import importlib.util
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

_spec = importlib.util.spec_from_file_location("ai_pages", ROOT / "scripts" / "add-ai-services-pages.py")
_ai = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ai)
PAGE_CSS, SCHEDULE = _ai.PAGE_CSS, _ai.SCHEDULE

SLUG = "growth-marketing"
TITLE = "Growth Marketing for Service Businesses | YB Marketing"
META = ("SEO, AI search, ads and social measured side by side in one live dashboard. "
        "Every month we show you what's working and move your budget toward it.")

ARROW = ('<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" '
         'stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>')
PHONE = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 '
         '4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 '
         '1-.45 2.11L7.91 8.96a16 16 0 0 0 6.07 6.07l1.08-.9a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 '
         '22 16.92z"/></svg>')

ICONS = {
    "website": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/>',
    "seo": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "ai": '<path d="M12 3l1.9 5.8L20 10l-6.1 1.2L12 17l-1.9-5.8L4 10l6.1-1.2z"/>',
    "ads": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "meta": '<path d="M3 11l18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "social": ('<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/>'
               '<line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>'),
}


def svg(name: str) -> str:
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round">{ICONS[name]}</svg>')


CHANNELS = [
    ("website", "Website", "Traffic, top pages and where visitors came from (Google Analytics)"),
    ("seo", "SEO", "Search impressions, clicks and keyword rankings (Search Console and rank tracking)"),
    ("ai", "AI search", "How often your business comes up in ChatGPT, Gemini and Google's AI Overviews"),
    ("ads", "Google Ads", "Spend, clicks, conversions and cost per lead"),
    ("meta", "Meta ads", "Spend and results from Facebook and Instagram ads"),
    ("social", "Organic social", "Reach and engagement on Facebook and Instagram"),
]

STEPS = [
    ("Unify", "We connect your website, SEO, AI search, ads and social data into one dashboard, so every channel "
              "is measured the same way and shown side by side."),
    ("Measure against your goals", "Before we look at a single number, we agree on what counts. For most "
     "businesses that's calls, booked jobs or revenue, not clicks or likes. Every channel gets judged against that."),
    ("Shift to what's working", "When one channel is producing and another isn't, we say so, and we move budget "
     "and effort toward the one that is."),
]

REVIEW = [
    ("What changed", "How each channel performed against your goals compared to last month"),
    ("What we did about it", "The changes we've already made, like a paused ad campaign, a new service page, "
     "or budget moved from one channel to another"),
    ("What we recommend next", "Where we think the next dollar or hour should go, and why"),
]

DEMO_ROWS = [
    ("website", "Website", "Visitors", "4,820", "+12%", "up"),
    ("seo", "SEO", "Search clicks", "1,940", "+18%", "up"),
    ("ai", "AI search", "AI answer mentions", "37", "+9", "up"),
    ("ads", "Google Ads", "Cost per lead", "$48", "-11%", "up"),
    ("meta", "Meta ads", "Cost per lead", "$71", "+6%", "down"),
    ("social", "Organic social", "Reach", "12,300", "+4%", "up"),
]

FAQS = [
    ("What do you mean by growth marketing?",
     "Running your marketing channels as one system instead of separate projects. We measure everything against "
     "the same goals and keep moving time and money toward what's producing results. The dashboard is how we see "
     "it; the monthly review is where the decisions happen."),
    ("How is this different from the reports I get now?",
     "Most reports cover one channel and describe what happened. Ours puts every channel side by side, measures "
     "them against your goals, and lists the changes we made and what we recommend next."),
    ("Which channels does it cover?",
     "SEO, AI search, Google Ads, Meta ads and organic social, plus your website traffic."),
    ("Can I see the dashboard whenever I want?",
     "Yes. You get your own login, so you don't have to wait for the monthly report."),
    ("What if a channel isn't working?",
     "We'll tell you, even when it's one we run. If the numbers say your budget does more somewhere else, "
     "that's our recommendation."),
    ("Who sees my data?",
     "You and our team. Your dashboard shows only your accounts."),
]

EXTRA_CSS = """
.gm-sec-head{text-align:center;max-width:720px;margin:0 auto 48px}
.gm-sec-head p{color:var(--fg2);font-size:16px;line-height:1.75}
.gm-prose{max-width:720px;margin:0 auto}
.gm-prose p{color:var(--fg2);font-size:17px;line-height:1.8;margin-bottom:18px}
.gm-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.gm-review{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.gm-note{text-align:center;color:var(--ink);font-weight:600;font-size:16px;margin-top:32px}
.gm-dash{max-width:900px;margin:0 auto;background:#fff;border:1px solid var(--line);border-radius:var(--r-xl);box-shadow:0 24px 60px -24px rgba(22,32,58,.25);overflow:hidden}
.gm-dash-bar{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:16px 22px;border-bottom:1px solid var(--line);background:var(--bg-soft)}
.gm-dash-bar strong{font-family:var(--font-display);color:var(--ink);font-size:15px}
.gm-tag{font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--fg3);background:#fff;border:1px solid var(--line);border-radius:999px;padding:4px 10px}
.gm-row{display:grid;grid-template-columns:1.3fr 1.2fr .8fr .7fr;align-items:center;gap:12px;padding:14px 22px;border-bottom:1px solid var(--line);font-size:14px;color:var(--fg2)}
.gm-row:last-child{border-bottom:none}
.gm-row--head{font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--fg3);padding-top:12px;padding-bottom:12px}
.gm-ch{display:flex;align-items:center;gap:10px;font-weight:700;color:var(--ink)}
.gm-ch-ic{width:30px;height:30px;border-radius:var(--r-sm);background:var(--wash-blue);color:var(--yb-blue);display:flex;align-items:center;justify-content:center;flex:none}
.gm-ch-ic svg{width:16px;height:16px}
.gm-val{font-family:var(--font-display);font-weight:800;color:var(--ink);font-size:16px}
.gm-delta{font-weight:700;font-size:13px;border-radius:999px;padding:3px 9px;justify-self:start}
.gm-delta--up{background:var(--wash-mint);color:#159468}
.gm-delta--down{background:var(--wash-coral);color:var(--yb-coral)}
.gm-caption{text-align:center;color:var(--fg2);font-size:15px;max-width:640px;margin:18px auto 0}
.gm-ask{max-width:900px;margin:64px auto 0;display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}
.gm-ask h3{font-size:22px;margin-bottom:12px}
.gm-ask p{color:var(--fg2);font-size:16px;line-height:1.75}
.gm-chat{background:#fff;border:1px solid var(--line);border-radius:var(--r-xl);padding:22px;box-shadow:0 12px 32px -12px rgba(22,32,58,.18);display:grid;gap:12px}
.gm-bubble{border-radius:16px;padding:12px 16px;font-size:14.5px;line-height:1.6;max-width:90%}
.gm-bubble--q{justify-self:end;background:var(--grad-brand);color:#fff;border-bottom-right-radius:4px}
.gm-bubble--a{justify-self:start;background:var(--bg-soft);color:var(--fg1);border-bottom-left-radius:4px}
.gm-result{max-width:900px;margin:0 auto;background:#fff;border:1px solid var(--line);border-radius:var(--r-xl);padding:32px;display:grid;grid-template-columns:auto 1fr;gap:32px;align-items:center}
.gm-stats{display:flex;gap:28px}
.gm-stat strong{display:block;font-family:var(--font-display);font-size:34px;font-weight:800;background:var(--grad-brand);-webkit-background-clip:text;background-clip:text;color:transparent;line-height:1.1}
.gm-stat span{font-size:13px;color:var(--fg2)}
.gm-result p{color:var(--fg2);font-size:16px;line-height:1.7;margin-bottom:12px}
.gm-result a{color:var(--yb-blue);font-weight:700}
@media(max-width:900px){.gm-steps,.gm-review,.gm-ask,.gm-result{grid-template-columns:1fr}.gm-stats{flex-wrap:wrap}}
@media(max-width:640px){.gm-row{grid-template-columns:1.4fr 1fr .8fr}.gm-row>:nth-child(2){display:none}}
"""

WAVE_DOWN = ('<div class="wave-div" style="background:{a}"><svg viewBox="0 0 1440 70" preserveAspectRatio="none">'
             '<path d="M0,70 C480,0 960,0 1440,70 L1440,70 L0,70 Z" fill="{b}"/></svg></div>')
WAVE_UP = ('<div class="wave-div" style="background:{a}"><svg viewBox="0 0 1440 70" preserveAspectRatio="none">'
           '<path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="{b}"/></svg></div>')
WHITE, SOFT = "#ffffff", "#F6F8FC"


def orbit() -> str:
    nodes = "\n".join(
        f'          <div class="hero-orbit-node" style="--i:{i}"><div class="hero-orbit-icon" aria-label="{label}">'
        f'<span class="hero-orbit-pill"><span class="hero-orbit-pill-ic">{svg(key)}</span></span></div></div>'
        for i, (key, label, _) in enumerate(CHANNELS)
    )
    return f"""    <div class="svc-hero-visual">
      <div class="hero-orbit hero-orbit--svc hero-orbit--features" style="--orbit-feat-wash:var(--wash-blue);--orbit-feat-color:var(--yb-blue);--orbit-feat-glow:rgba(63,111,214,0.22)">
        <div class="hero-orbit-bg" aria-hidden="true">
          <div class="hero-orbit-ring hero-orbit-ring--track"></div>
          <div class="hero-orbit-hub">
            <div class="hero-orbit-hub-art">
              <img src="../assets/yb-logo-white.png" alt="YB Marketing growth marketing dashboard">
            </div>
          </div>
        </div>
        <div class="hero-orbit-spin">
{nodes}
        </div>
      </div>
    </div>"""


def feat(key: str, title: str, desc: str) -> str:
    return f"""      <div class="feat-card">
        <div class="feat-ic" style="background:var(--wash-blue);color:var(--yb-blue)">{svg(key)}</div>
        <div class="feat-title">{title}</div>
        <div class="feat-desc">{desc}</div>
      </div>"""


def card(title: str, desc: str, num: str = "") -> str:
    head = f'<div class="step-num">{num}</div>' if num else ""
    return f'      <div class="step">{head}<h3>{title}</h3><p>{desc}</p></div>'


def faq_item(q: str, a: str) -> str:
    return (f'      <div class="faq-item"><button class="faq-q" type="button" style="--faq-ac:var(--yb-blue)">'
            f'{q}<span class="faq-icon">+</span></button>'
            f'<div class="faq-a"><div class="faq-a-inner">{a}</div></div></div>')


def demo() -> str:
    rows = "\n".join(
        f'      <div class="gm-row"><span class="gm-ch"><span class="gm-ch-ic">{svg(k)}</span>{name}</span>'
        f'<span>{metric}</span><span class="gm-val">{val}</span>'
        f'<span class="gm-delta gm-delta--{trend}">{delta}</span></div>'
        for k, name, metric, val, delta, trend in DEMO_ROWS
    )
    return f"""    <div class="gm-dash" role="img" aria-label="Example dashboard showing every marketing channel side by side, with sample data">
      <div class="gm-dash-bar"><strong>All channels · This month vs last month</strong><span class="gm-tag">Sample data</span></div>
      <div class="gm-row gm-row--head"><span>Channel</span><span>Measured by</span><span>This month</span><span>Change</span></div>
{rows}
    </div>"""


def body() -> str:
    channels = "\n".join(feat(*c) for c in CHANNELS)
    steps = "\n".join(card(t, d, f"Step {i}") for i, (t, d) in enumerate(STEPS, 1))
    review = "\n".join(card(t, d) for t, d in REVIEW)
    faqs = "\n".join(faq_item(q, a) for q, a in FAQS)
    return f"""<section style="background:#fff">
  <div class="container">
    <div class="gm-sec-head" style="margin-bottom:28px">
      <span class="eyebrow">The problem</span>
      <h2 style="margin:14px 0 0">Every channel says it's working</h2>
    </div>
    <div class="gm-prose">
      <p>Your ads report says ads are working. Your SEO report says SEO is working. Social says the same. Each one is measured on its own terms, by the people running it, and nobody lines them up next to each other.</p>
      <p>So you end up deciding where to spend based on whichever report was most convincing that month, not on which channel actually brought in customers.</p>
    </div>
  </div>
</section>

{WAVE_DOWN.format(a=WHITE, b=SOFT)}

<section style="background:var(--bg-soft)">
  <div class="container">
    <div class="gm-sec-head">
      <span class="eyebrow">One dashboard</span>
      <h2 style="margin:14px 0 16px">All your marketing in one place</h2>
      <p>We connect every channel we run for you to one live dashboard. You can log in any time and see the same numbers we see.</p>
    </div>
    <div class="feat-grid">
{channels}
    </div>
  </div>
</section>

{WAVE_UP.format(a=SOFT, b=WHITE)}

<section style="background:#fff" id="how-it-works">
  <div class="container">
    <div class="gm-sec-head">
      <span class="eyebrow">How it works</span>
      <h2 style="margin:14px 0 0">Unify. Measure. Shift.</h2>
    </div>
    <div class="gm-steps">
{steps}
    </div>
  </div>
</section>

{WAVE_DOWN.format(a=WHITE, b=SOFT)}

<section style="background:var(--bg-soft)">
  <div class="container">
    <div class="gm-sec-head">
      <span class="eyebrow">The monthly review</span>
      <h2 style="margin:14px 0 16px">Every month, a report that ends in decisions</h2>
      <p>Once a month you get a report built from the dashboard. It doesn't stop at what happened. It covers:</p>
    </div>
    <div class="gm-review">
{review}
    </div>
    <p class="gm-note">You'll always know what we changed and why, without having to ask.</p>
  </div>
</section>

{WAVE_UP.format(a=SOFT, b=WHITE)}

<section style="background:#fff" id="see-it">
  <div class="container">
    <div class="gm-sec-head">
      <span class="eyebrow">See it</span>
      <h2 style="margin:14px 0 0">Your numbers, not a PDF</h2>
    </div>
{demo()}
    <p class="gm-caption">Live data from every channel. Log in whenever you want, not just when the report arrives.</p>
    <div class="gm-ask">
      <div>
        <h3>Ask your data a question</h3>
        <p>Type a question in plain English, like "How did organic traffic compare to last month?" or "What did we spend on Google Ads in October?", and get the answer straight from your own numbers.</p>
      </div>
      <div class="gm-chat" role="img" aria-label="Example question and answer, with sample data">
        <div class="gm-bubble gm-bubble--q">What did we spend on Google Ads in October?</div>
        <div class="gm-bubble gm-bubble--a">You spent $2,140 on Google Ads in October, 6% less than September. It brought in 44 leads at about $48 each.</div>
        <span class="gm-tag" style="justify-self:start">Sample data</span>
      </div>
    </div>
  </div>
</section>

{WAVE_DOWN.format(a=WHITE, b=SOFT)}

<section style="background:var(--bg-soft)">
  <div class="container">
    <div class="gm-sec-head">
      <span class="eyebrow">Results</span>
      <h2 style="margin:14px 0 0">What happens when you can see everything at once</h2>
    </div>
    <div class="gm-result">
      <div class="gm-stats">
        <div class="gm-stat"><strong>+112%</strong><span>Organic traffic</span></div>
        <div class="gm-stat"><strong>+204%</strong><span>Page one keywords</span></div>
      </div>
      <div>
        <p>A Bay Area electrical contractor grew organic traffic 112% year over year and page one keywords 204%, and started showing up in AI search results for the first time.</p>
        <a href="/about/case-studies/local-electrical-contractor-seo-growth">Read the case study →</a>
      </div>
    </div>
  </div>
</section>

{WAVE_UP.format(a=SOFT, b=WHITE)}

<section style="background:#fff" id="faq">
  <div class="container" style="max-width:820px">
    <div style="text-align:center;margin-bottom:40px">
      <span class="eyebrow">FAQ</span>
      <h2 style="margin:14px 0 0">Questions we get a lot</h2>
    </div>
    <div class="faq-list">
{faqs}
    </div>
  </div>
</section>

{WAVE_DOWN.format(a=WHITE, b=SOFT)}"""


def build_page() -> str:
    prefix = "../"
    header = site_header_html(prefix, current_path=f"/{SLUG}").strip()
    footer = site_footer_html(prefix, current_path=f"/{SLUG}").strip()
    form = lead_form_html("Growth Marketing Page", redirect="/thank-you", default_interest="growth-marketing")
    seo = seo_head_html(f"{SLUG}/index.html")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="../favicon.png" type="image/png">
<link rel="apple-touch-icon" href="../favicon.png">
{STAGING_ROBOTS_META}
<title>{TITLE}</title>
<meta name="description" content="{META}">
<link rel="stylesheet" href="../colors_and_type.css">
<link rel="stylesheet" href="../insights.css">
<link rel="stylesheet" href="../lead-form.css">
<style>{PAGE_CSS}{EXTRA_CSS}</style>
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
      <span class="eyebrow" style="color:var(--yb-cyan)">Growth marketing</span>
      <h1>Stop guessing which marketing is working</h1>
      <p class="hero-lead">Most agencies manage each channel in its own lane, with its own report. We pull SEO, AI search, ads and social into one live dashboard, measure all of it against the goals you set, and move your budget to where the results are.</p>
      <div class="svc-hero-actions">
        <a href="#contact" class="btn btn-grad btn-lg">Book a walkthrough
          {ARROW}
        </a>
        <a href="tel:5099019735" class="btn btn-ghost-white">
          {PHONE}
          509-901-9735
        </a>
      </div>
    </div>
{orbit()}
  </div>
</section>

<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 80" preserveAspectRatio="none" style="height:80px"><path d="M0,0 C360,80 1080,80 1440,0 L1440,80 L0,80 Z" fill="#ffffff"/></svg></div>

{body()}

<section style="background:var(--bg-soft)" id="contact">
  <div class="container">
    <div style="text-align:center;max-width:720px;margin:0 auto 40px">
      <span class="eyebrow">Get Started</span>
      <h2 style="margin:14px 0 12px">Book a Meeting or Send Us a Message</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">Pick a time with one of us below, or send a note and we'll get back to you.</p>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start" class="why-main-grid">
      <div>
{SCHEDULE}
      </div>
      <div style="background:#fff;border-radius:var(--r-xl);padding:28px;box-shadow:var(--sh-sm);border:1px solid var(--line)">
        <h3 style="font-size:20px;margin:0 0 20px">Send Us a Message</h3>
{form}
      </div>
    </div>
  </div>
</section>

<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div>
<div style="background:var(--grad-navy)">
<div class="svc-cta">
  <div class="svc-cta-mesh"></div>
  <div class="container svc-cta-inner">
    <h2 style="margin:0 0 14px;color:#fff;font-size:clamp(1.8rem,2.6vw,2.4rem)">See all your marketing in one place</h2>
    <p style="color:var(--fg2-on-dark);font-size:16px;margin-bottom:32px">Book a 30-minute walkthrough. We'll show you the dashboard, talk through your goals, and point out what we'd look at first in your channels.</p>
    <div class="svc-cta-btns">
      <a href="#contact" class="btn btn-grad btn-lg">Book a walkthrough</a>
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


def main() -> None:
    out = ROOT / SLUG / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_page(), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
