#!/usr/bin/env python3
"""Fetch YB Marketing blog posts via WP REST API and generate static HTML."""

import html
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from about_nav_snippet import about_nav_shell
from schema_markup import seo_head_html
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_tracking_snippet import ATTRIBUTER_FOOTER_BLOCK, GTM_BODY_NOSCRIPT_BLOCK, TRACKING_HEAD_BLOCK
from site_staging_seo_snippet import STAGING_ROBOTS_META
from site_footer_snippet import site_footer_html
from blog_intro_snippet import intro_block_for_build, updated_meta_for_build

def about_nav_block(prefix: str) -> str:
    return about_nav_shell(prefix).strip()

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "blog" / "posts"
DATA_FILE = ROOT / "blog" / "data" / "posts.json"
API = "https://www.yakimabranding.com/wp-json/wp/v2"
BLOG_INDEX_PREFIX = ""  # insights.html at site root
POST_PREFIX = "../../"  # blog/posts/*.html → site root

WAVE_HERO_TO_SOFT = (
    '<div class="wave-div wave-from-navy wave-to-soft">'
    '<svg viewBox="0 0 1440 70" preserveAspectRatio="none">'
    '<path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z"/></svg></div>'
)
WAVE_HERO_TO_WHITE = (
    '<div class="wave-div wave-from-navy wave-to-white">'
    '<svg viewBox="0 0 1440 70" preserveAspectRatio="none">'
    '<path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z"/></svg></div>'
)
WAVE_FOOTER_FROM_SOFT = (
    '<div class="wave-div wave-to-footer wave-from-soft">'
    '<svg viewBox="0 0 1440 70" preserveAspectRatio="none">'
    '<path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z"/></svg></div>'
)
WAVE_FOOTER_FROM_WHITE = (
    '<div class="wave-div wave-to-footer wave-from-white">'
    '<svg viewBox="0 0 1440 70" preserveAspectRatio="none">'
    '<path d="M0,70 C360,0 1080,0 1440,70 L1440,70 L0,70 Z"/></svg></div>'
)

ARROW_SM = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
ARROW_MD = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'

# Filter topics aligned with YB service lines (audited per post slug)
BLOG_TOPICS = [
    ("all", "All Posts"),
    ("seo", "SEO"),
    ("google-ads", "Google Ads"),
    ("social-media", "Social Media"),
    ("web-design", "Web Design"),
    ("content", "Content"),
    ("strategy", "Strategy"),
    ("news", "News"),
    ("general", "General"),
]

TOPIC_LABELS = {tid: label for tid, label in BLOG_TOPICS if tid != "all"}

# Manual audit: primary topic per slug (overrides WP categories)
SLUG_TOPIC = {
    "yb-marketing-announces-strategic-acquisition-of-encite-branding-marketing-creative": "news",
    "why-local-businesses-need-seo-how-you-can-help-them": "seo",
    "everything-businesses-need-to-know-about-seo": "seo",
    "5-paid-search-tactics-to-help-you-generate-leads": "google-ads",
    "how-did-this-restaurants-pay-per-click-campaign-improve-so-drastically": "google-ads",
    "types-of-facebook-ads": "google-ads",
    "so-youre-thinking-about-social-media-management": "social-media",
    "an-introverts-guide-to-using-social-media": "social-media",
    "social-media-platforms": "social-media",
    "recap-common-social-media-mistakes-every-business-should-avoid": "social-media",
    "social-media-management-vs-growth": "social-media",
    "5-major-myths": "social-media",
    "five-social-media-post-ideas-for-when-youre-in-a-rut": "social-media",
    "what-is-a-hashtag": "social-media",
    "ways-to-increase-followers": "social-media",
    "7-ways-to-convert-social-media-followers-into-paying-customers": "social-media",
    "evolution-social-media": "social-media",
    "what-is-a-landing-page-why-is-it-important": "web-design",
    "how-to-create-a-portfolio-website-for-your-small-business": "web-design",
    "5-creative-ways-to-enhance-your-website-using-video": "web-design",
    "how-often-should-you-run-content-audits-and-update-your-site": "web-design",
    "how-to-create-content-for-every-stage-in-the-buyers-journey": "content",
    "in-house-marketing-vs-agency-marketing": "strategy",
    "digital-marketing-is-an-investment-not-an-expense": "strategy",
    "why-you-should-be-using-customer-satisfaction-surveys": "strategy",
    "3-ways-to-close-more-internet-leads": "strategy",
    "what-drives-consumer-spending": "strategy",
    "resolving-employee-disputes-before-you-are-sued": "strategy",
    "best-business-entity-for-franchisees": "strategy",
    "what-you-should-consider-when-installing-a-concrete-patio": "general",
    "the-thermal-press-difference": "general",
    "why-should-you-send-your-child-to-camp-mowglis-give-them-a-chance-to-unplug": "general",
    "signs-your-car-may-need-transmission-repair": "general",
    "what-to-look-for-in-a-moving-company": "general",
    "effects-of-rain-on-asphalt": "general",
    "pcba-design-for-manufacturability": "general",
    "selecting-a-commercial-landscape-maintenance-company": "general",
    "why-choose-gasoline-box-trucks-vs-diesel": "general",
}


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "YB-Marketing-Blog-Builder/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode()), resp.headers


def fetch_all_posts():
    posts = []
    page = 1
    while True:
        url = f"{API}/posts?per_page=100&page={page}&_embed"
        batch, headers = fetch_json(url)
        posts.extend(batch)
        total_pages = int(headers.get("X-WP-TotalPages", 1))
        if page >= total_pages:
            break
        page += 1
    return posts


def strip_html(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def format_date(iso):
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%B %d, %Y")
    except ValueError:
        return ""


def reading_time(content_html):
    words = len(strip_html(content_html).split())
    return max(1, round(words / 200))


def get_featured_url(post):
    embed = post.get("_embedded", {})
    media = embed.get("wp:featuredmedia") or []
    if media and media[0].get("source_url"):
        return media[0]["source_url"]
    return ""


def get_categories(post):
    embed = post.get("_embedded", {})
    terms = embed.get("wp:term") or []
    cats = []
    for group in terms:
        for term in group:
            if term.get("taxonomy") == "category":
                cats.append(term.get("name", "Blog"))
    return cats or ["Blog"]


def assign_topic(post):
    """Return primary filter topic id for a post."""
    slug = post["slug"]
    if slug in SLUG_TOPIC:
        return SLUG_TOPIC[slug]

    title_l = html.unescape(post["title"]["rendered"]).lower()
    blob = title_l + " " + slug.replace("-", " ") + " " + " ".join(get_categories(post)).lower()

    rules = [
        ("news", ("acquisition", "announces", "press release", "einpresswire")),
        ("google-ads", ("google ads", "paid search", "ppc", "pay-per-click", "adwords", "facebook ads")),
        ("seo", ("seo", "search engine optimization", "search engine marketing", "ranking", "organic search")),
        ("social-media", ("social media", "facebook", "instagram", "linkedin", "hashtag", "follower")),
        ("web-design", ("web design", "website", "wordpress", "wix", "landing page", "portfolio site")),
        ("content", ("content marketing", "buyer's journey", "blogging", "content audit", "copywriting")),
    ]
    for topic_id, keys in rules:
        if any(k in blob for k in keys):
            return topic_id

    wp_cats = [c.lower() for c in get_categories(post)]
    if "social media" in wp_cats:
        return "social-media"
    if "services" in wp_cats:
        return "seo"

    return "strategy"


def pick_service_cta(post, prefix=POST_PREFIX):
    """Return (title, desc, btn, href) for accent sidebar card."""
    title_l = html.unescape(post["title"]["rendered"]).lower()
    slug = post["slug"]
    checks = [
        (("google ads", "paid search", "ppc", "adwords"), "Need Better Google Ads?",
         "Learn how YB Marketing helps businesses improve Google Ads results with a strategy-first approach.",
         "View Google Ads Services", f"{prefix}services/google-ads.html"),
        (("seo", "search engine"), "Need Stronger SEO?",
         "Rank higher locally and nationally with a custom SEO plan built around your services and markets.",
         "View SEO Services", f"{prefix}services/seo.html"),
        (("social media", "facebook", "instagram", "linkedin", "hashtag"), "Grow Your Social Presence?",
         "Build real follower growth and engagement with a strategy tailored to your brand and audience.",
         "View Social Media Services", f"{prefix}services/social-media.html"),
        (("web design", "website", "wordpress", "wix", "landing page"), "Need a Better Website?",
         "Get a site designed to reflect your brand, load fast, and convert visitors into leads.",
         "View Web Design Services", f"{prefix}services/web-design.html"),
        (("content", "blog", "writing"), "Need Content That Converts?",
         "YB creates blogs, service pages, and campaigns that educate buyers and support SEO.",
         "View Content Services", f"{prefix}services/content-creation.html"),
        (("press release",), "Get Your Story Published?",
         "Professional press releases and distribution to help journalists notice your news.",
         "View Press Release Services", f"{prefix}services/press-releases.html"),
    ]
    blob = title_l + " " + slug.replace("-", " ")
    for keys, t, d, b, h in checks:
        if any(k in blob for k in keys):
            return t, d, b, h
    return (
        "Need Better Google Ads?",
        "Learn how YB Marketing helps improve Google Ads results with a strategy-first approach.",
        "View Google Ads Services",
        f"{prefix}services/google-ads.html",
    )


def rewrite_content(content, slug_map):
    """Point internal yakimabranding post links to local pages."""
    def repl(m):
        path = m.group(1).rstrip("/").split("/")[-1] or m.group(1).rstrip("/").split("/")[-2]
        if path in slug_map:
            return f'href="{slug_map[path]}.html"'
        return m.group(0)

    content = re.sub(
        r'href="https?://(?:www\.)?yakimabranding\.com/([^"#?]+)/?"',
        repl,
        content,
        flags=re.I,
    )
    content = re.sub(r"<!--more-->", "", content)
    content = re.sub(r'class="wp-block-paragraph"', 'class="wp-block-paragraph blog-p"', content)
    # Bold-only lines from WordPress → real headings
    content = re.sub(
        r'<p class="[^"]*">\s*<strong>([^<]+)</strong>\s*</p>',
        r"<h2>\1</h2>",
        content,
        flags=re.I,
    )
    content = re.sub(
        r'<p class="[^"]*">\s*<strong><mark[^>]*>([^<]+)</mark></strong>\s*</p>',
        r"<h2>\1</h2>",
        content,
        flags=re.I,
    )
    # wp headings
    content = re.sub(
        r'<h2 class="wp-block-heading[^"]*">',
        "<h2>",
        content,
        flags=re.I,
    )
    content = re.sub(
        r'<h3 class="wp-block-heading[^"]*">',
        "<h3>",
        content,
        flags=re.I,
    )
    return content


def sidebar_html(prefix, accent):
    t, d, b, h = accent
    return f"""
<aside class="blog-sidebar" aria-label="Related actions">
  <div class="sidebar-card">
    <h3>Ready to Grow?</h3>
    <p>Talk with YB Marketing about a strategy built around your business goals.</p>
    <a href="{prefix}contact.html" class="btn btn-grad">{ARROW_SM} Get Started</a>
  </div>
  <div class="sidebar-card sidebar-card-ghost">
    <h3>Explore Our Services</h3>
    <p>SEO, Google Ads, web design, branding, social media, and content marketing under one strategy.</p>
    <a href="{prefix}index.html#services" class="btn">{ARROW_SM} View Services</a>
  </div>
  <div class="sidebar-card sidebar-card-accent">
    <h3>{html.escape(t)}</h3>
    <p>{html.escape(d)}</p>
    <a href="{h}" class="btn">{ARROW_SM} {html.escape(b)}</a>
  </div>
</aside>"""


def header_nav(prefix, active_blog=False):
    blog_style = ' style="color:var(--yb-blue)"' if active_blog else ""
    return f"""
<div class="header top" id="header">
  <div class="container header-inner">
    <a class="logo" href="{prefix}index.html">
      <img src="{prefix}assets/yb-logo-color.png" alt="YB Marketing logo" style="width:44px;height:44px">
      <span class="logo-text">YB <span>Marketing</span></span>
    </a>
    <nav class="nav">
      <a href="{prefix}index.html" class="nav-a">Home</a>
      {about_nav_block(prefix)}
      <div class="nav-services" id="navServices">
        <button class="nav-svc-btn" type="button">Services
          <svg class="nav-chevron" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
        <div class="nav-dd">
          <div class="nav-dd-arrow"></div>
          <div class="nav-dd-grid">
            <a href="{prefix}services/web-design.html" class="dd-card"><div class="dd-ic" style="background:var(--wash-mint);color:#159468"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg></div><div><span class="dd-name">Web Design</span><span class="dd-desc">WordPress, Wix &amp; custom sites</span></div></a>
            <a href="{prefix}services/social-media.html" class="dd-card"><div class="dd-ic" style="background:var(--wash-amber);color:#c77f12"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/></svg></div><div><span class="dd-name">Social Media</span><span class="dd-desc">Grow your following</span></div></a>
            <a href="{prefix}services/google-ads.html" class="dd-card"><div class="dd-ic" style="background:var(--wash-coral);color:var(--yb-coral)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/></svg></div><div><span class="dd-name">Google Ads</span><span class="dd-desc">PPC that converts</span></div></a>
            <a href="{prefix}services/seo.html" class="dd-card"><div class="dd-ic" style="background:var(--wash-cyan);color:var(--yb-cyan)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div><div><span class="dd-name">SEO</span><span class="dd-desc">Rank higher on Google</span></div></a>
            <a href="{prefix}services/press-releases.html" class="dd-card"><div class="dd-ic" style="background:var(--wash-pink);color:var(--yb-pink)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2z"/></svg></div><div><span class="dd-name">Press Releases</span><span class="dd-desc">Get published</span></div></a>
            <a href="{prefix}services/content-creation.html" class="dd-card"><div class="dd-ic" style="background:var(--wash-violet);color:var(--yb-violet)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg></div><div><span class="dd-name">Content &amp; Blogging</span><span class="dd-desc">Copy that converts</span></div></a>
          </div>
        </div>
      </div>
      <a href="{prefix}insights.html" class="nav-a"{blog_style}>Insights</a>
      <a href="{prefix}contact.html" class="nav-a">Contact</a>
    </nav>
    <div class="btn-hdr" style="display:flex;align-items:center;gap:8px">
      <a href="tel:5099019735" class="btn" style="background:#fff;color:var(--yb-blue);border:1.5px solid var(--line-strong);padding:11px 16px;font-size:14px">509-901-9735</a>
      <a href="{prefix}contact.html" class="btn btn-grad">Get Started</a>
    </div>
    <button class="hamburger" id="hamburger" type="button" aria-label="Open menu"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
  </div>
  <div class="mobile-menu" id="mobileMenu">
    <a href="{prefix}index.html">Home</a>
    <a href="#" onclick="document.getElementById('mobileAboutList').classList.toggle('open');return false" style="display:flex;justify-content:space-between;align-items:center">About <span>▾</span></a>
    <div class="mobile-svc-list" id="mobileAboutList">
      <a href="{prefix}about.html" class="mobile-about-row"><strong>About Us</strong><span>Meet our team &amp; our story</span></a>
      <a href="{prefix}washington-state-sales-tax.html" class="mobile-about-row"><strong>WA Sales Tax Notice</strong><span>Oct 2025 tax updates for WA businesses</span></a>
    </div>
    <a href="{prefix}insights.html"{blog_style}>Insights</a>
    <a href="{prefix}contact.html">Contact</a>
  </div>
</div>"""


def blog_filters_html(total):
    buttons = []
    for tid, label in BLOG_TOPICS:
        active = " is-active" if tid == "all" else ""
        buttons.append(
            f'<button type="button" class="blog-filter{active}" data-filter="{tid}" '
            f'aria-pressed="{"true" if tid == "all" else "false"}">{html.escape(label)}</button>'
        )
    return f"""
<div class="blog-filters-wrap">
  <p class="blog-filters-label">Browse by topic</p>
  <div class="blog-filters" role="group" aria-label="Filter articles by topic">
    {''.join(buttons)}
  </div>
  <p class="blog-filter-status" id="blogFilterStatus" aria-live="polite">Showing all {total} articles</p>
</div>"""


def page_shell(prefix, title, desc, body, active_blog=False, extra_head="", extra_script="", footer_wave=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{STAGING_ROBOTS_META}
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="stylesheet" href="{prefix}colors_and_type.css">
<link rel="stylesheet" href="{prefix}site.css">
<link rel="stylesheet" href="{prefix}blog.css">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
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
.nav-services{{position:relative}}
.nav-svc-btn{{display:flex;align-items:center;gap:5px;font-weight:600;font-size:15px;padding:8px 14px;border-radius:var(--r-sm);background:none;border:none;cursor:pointer;font-family:var(--font-body)}}
.nav-dd{{position:absolute;top:calc(100% + 10px);left:50%;transform:translateX(-50%);width:660px;background:#fff;border-radius:var(--r-xl);box-shadow:var(--sh-lg);padding:16px;opacity:0;pointer-events:none;z-index:200}}
.nav-services:hover .nav-dd,.nav-services.is-open .nav-dd{{opacity:1;pointer-events:all}}
.nav-dd-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}}
.dd-card{{display:flex;gap:11px;padding:12px;border-radius:var(--r-md)}}
.dd-card:hover{{background:var(--bg-soft)}}
.dd-name{{font-weight:700;font-size:13px;display:block}}
.dd-desc{{font-size:11.5px;color:var(--fg3)}}
.btn{{display:inline-flex;align-items:center;gap:8px;border:none;cursor:pointer;font-family:var(--font-body);font-weight:700;font-size:15px;border-radius:var(--r-md);padding:13px 22px}}
.btn-grad{{background:var(--grad-brand);color:#fff;box-shadow:var(--sh-blue)}}
.hamburger{{display:none;background:none;border:none;cursor:pointer}}
.mobile-menu{{display:none;border-top:1px solid var(--line);background:#fff;padding:12px 28px}}
.mobile-menu a{{display:block;padding:14px 0;font-weight:600;border-bottom:1px solid var(--line)}}
.mobile-menu.open{{display:block}}
@media(max-width:900px){{.nav,.btn-hdr{{display:none}}.hamburger{{display:flex}}.nav-dd{{display:none}}}}
</style>
{extra_head}
{TRACKING_HEAD_BLOCK}
</head>
<body class="blog-page">
{GTM_BODY_NOSCRIPT_BLOCK}
{ACCESSIBE_BODY_SCRIPT}
{header_nav(prefix, active_blog)}
{body}
{footer_wave}
{site_footer_html(prefix)}
<script src="{prefix}js/newsletter-popup.js" defer></script>
<script src="{prefix}js/chat-widget.js" defer></script>
<script src="{prefix}js/site.js" defer></script>
<script>
document.getElementById('hamburger')?.addEventListener('click', function () {{
  document.getElementById('mobileMenu')?.classList.toggle('open');
}});
</script>
{extra_script}
{ATTRIBUTER_FOOTER_BLOCK}
</body>
</html>"""


def build():
    print("Fetching posts from WordPress API…")
    raw_posts = fetch_all_posts()
    raw_posts.sort(key=lambda p: p["date"], reverse=True)

    slug_map = {p["slug"]: p["slug"] for p in raw_posts}
    entries = []

    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    for post in raw_posts:
        slug = post["slug"]
        title = html.unescape(post["title"]["rendered"])
        content = rewrite_content(post["content"]["rendered"], slug_map)
        excerpt = strip_html(post["excerpt"]["rendered"])[:220]
        if excerpt.endswith("[…]") or excerpt.endswith("[...]"):
            excerpt = excerpt.rsplit(" ", 1)[0] + "…"
        image = get_featured_url(post)
        cats = get_categories(post)
        date_str = format_date(post["date"])
        rt = reading_time(post["content"]["rendered"])
        accent = pick_service_cta(post, POST_PREFIX)

        topic = assign_topic(post)
        topic_label = TOPIC_LABELS.get(topic, "Strategy")
        cat_html = (
            f'<span class="post-cat post-cat--{html.escape(topic)}">{html.escape(topic_label)}</span>'
            + "".join(
                f'<span class="post-cat post-cat-wp">{html.escape(c)}</span>'
                for c in cats[:2]
                if c.lower() not in ("blog", topic_label.lower())
            )
        )

        img_block = ""
        if image:
            img_block = f'<div class="post-hero-img"><img src="{html.escape(image)}" alt="{html.escape(title)}" loading="lazy"></div>'

        intro_block = intro_block_for_build(content, title, excerpt, slug)
        updated_meta = updated_meta_for_build(slug)

        body = f"""
<section class="blog-hero">
  <div class="blog-hero-mesh"></div>
  <div class="hero-logo-overlay hero-logo-overlay--center" aria-hidden="true">
    <img src="{POST_PREFIX}assets/yb-logo-white.png" alt="">
  </div>
  <div class="container blog-hero-inner">
    <span class="eyebrow" style="color:var(--yb-cyan)">YB Marketing Insights</span>
    <h1 style="color:#fff;font-size:clamp(1.6rem,3vw,2.2rem)">{html.escape(title)}</h1>
  </div>
</section>
{WAVE_HERO_TO_WHITE}
<section class="blog-article">
  <div class="container blog-layout">
    <article class="blog-main">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="{POST_PREFIX}insights.html">Insights</a><span>/</span><span>{html.escape(title[:50])}{'…' if len(title) > 50 else ''}</span>
      </nav>
      {img_block}
      <header class="post-header">
        <div class="post-cats">{cat_html}</div>
        <h1>{html.escape(title)}</h1>
        <div class="post-meta"><span>{date_str}</span><span>{rt} min read</span><span>YB Marketing</span>{updated_meta}</div>
      </header>
{intro_block}
      <div class="blog-prose">{content}</div>
    </article>
    {sidebar_html(POST_PREFIX, accent)}
  </div>
</section>
"""

        desc = excerpt or strip_html(content)[:160]
        page = page_shell(
            POST_PREFIX,
            f"{title} — YB Marketing Insights",
            desc,
            body,
            footer_wave=WAVE_FOOTER_FROM_WHITE,
            extra_head=seo_head_html(f"blog/posts/{slug}.html"),
        )
        out = POSTS_DIR / f"{slug}.html"
        out.write_text(page, encoding="utf-8")

        entries.append({
            "slug": slug,
            "title": title,
            "excerpt": excerpt,
            "date": post["date"],
            "dateFormatted": date_str,
            "image": image,
            "categories": cats,
            "topic": topic,
            "topicLabel": TOPIC_LABELS.get(topic, "Strategy"),
            "readingTime": rt,
        })
        print(f"  · {slug}.html")

    DATA_FILE.write_text(json.dumps(entries, indent=2), encoding="utf-8")

    cards = []
    for i, e in enumerate(entries):
        img = e["image"] or "../assets/blog-1.webp"
        topic = e.get("topic", "strategy")
        topic_label = e.get("topicLabel", TOPIC_LABELS.get(topic, "Strategy"))
        cards.append(f"""
      <a href="blog/posts/{e['slug']}.html" class="blog-card" data-topic="{html.escape(topic)}">
        <div class="blog-card-thumb"><img src="{html.escape(img)}" alt="{html.escape(e['title'])}" loading="lazy"></div>
        <div class="blog-card-body">
          <span class="blog-card-cat blog-card-cat--{html.escape(topic)}">{html.escape(topic_label)}</span>
          <h2>{html.escape(e['title'])}</h2>
          <p>{html.escape(e['excerpt'])}</p>
          <div class="blog-card-meta"><span>{e['readingTime']} min read</span></div>
          <span class="blog-card-link">Read Article {ARROW_MD}</span>
        </div>
      </a>""")

    index_body = f"""
<section class="blog-hero">
  <div class="blog-hero-mesh"></div>
  <div class="hero-logo-overlay hero-logo-overlay--center" aria-hidden="true">
    <img src="assets/yb-logo-white.png" alt="">
  </div>
  <div class="container blog-hero-inner">
    <span class="eyebrow" style="color:var(--yb-cyan)">Insights &amp; Resources</span>
    <h1>Marketing Insights</h1>
    <p>Digital marketing tips, SEO guides, social media strategies, and business growth advice from our team.</p>
  </div>
</section>
{WAVE_HERO_TO_SOFT}
<section class="blog-listing">
  <div class="container">
    {blog_filters_html(len(entries))}
    <div class="blog-layout">
      <div class="blog-main">
        <div class="blog-card-grid" id="blogCardGrid">
          {''.join(cards)}
        </div>
        <p class="blog-filter-empty" id="blogFilterEmpty" hidden>No articles in this category yet. Try another filter.</p>
      </div>
      {sidebar_html(BLOG_INDEX_PREFIX, pick_service_cta(raw_posts[0], BLOG_INDEX_PREFIX))}
    </div>
  </div>
</section>
"""
    filter_script = """
<script src="js/blog-filter.js" defer></script>"""
    (ROOT / "insights.html").write_text(
        page_shell(
            BLOG_INDEX_PREFIX,
            "Insights — YB Marketing",
            "Digital marketing insights from YB Marketing.",
            index_body,
            active_blog=True,
            extra_head=seo_head_html("insights.html"),
            extra_script=filter_script,
            footer_wave=WAVE_FOOTER_FROM_SOFT,
        ),
        encoding="utf-8",
    )
    redirect = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=insights.html">
<link rel="canonical" href="insights.html">
<title>Redirecting to Insights — YB Marketing</title>
<script>location.replace("insights.html");</script>
{TRACKING_HEAD_BLOCK}
</head>
<body>
{GTM_BODY_NOSCRIPT_BLOCK}
<p><a href="insights.html">Continue to Insights</a></p>
{ATTRIBUTER_FOOTER_BLOCK}
</body>
</html>
"""
    (ROOT / "blog.html").write_text(redirect, encoding="utf-8")
    print(f"\nGenerated insights.html + {len(entries)} posts in blog/posts/")


if __name__ == "__main__":
    build()
