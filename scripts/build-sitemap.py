#!/usr/bin/env python3
"""Generate sitemap.html, XML sitemaps, and link footer Sitemap entries site-wide."""

import json
import re
import subprocess
import sys
from datetime import date, datetime
from html import escape, unescape
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from schema_markup import SERVICE_PAGES, SITE
from site_urls import page_href, clean_segment
from site_nav_snippet import site_header_html
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_staging_seo_snippet import STAGING_ROBOTS_META
from site_footer_snippet import site_footer_html
TITLE_RE = re.compile(r"<title>([^<]+)</title>", re.IGNORECASE)
CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]+)"', re.IGNORECASE)
SITEMAP_LINK_RE = re.compile(r'<a href="#">Sitemap</a>')
SITEMAP_LINKED_RE = re.compile(r'<a href="[^"]*sitemap(?:\.html)?">Sitemap</a>')

EXCLUDE_DIRS = {"preview", "partials", "ui_kits", "posts", "scripts", "assets", "js", "node_modules", "blog"}
POSTS_DATA = ROOT / "blog" / "data" / "posts.json"
ROOT_PAGES = [
    ("index.html", "Home"),
    ("about.html", "About Us"),
    ("insights.html", "Insights"),
    ("contact.html", "Contact"),
    ("washington-state-sales-tax.html", "Washington State Sales Tax Notice"),
    ("privacy-policy.html", "Privacy Policy"),
    ("sitemap.html", "Sitemap"),
]

SERVICE_LABELS = {
    "index.html": "Service",
}

SERVICE_INDEX_PAGES = [
    ("seo/index.html", "SEO Optimization"),
    ("google-ads/index.html", "Google Ads"),
    ("web-design/index.html", "Web Design"),
    ("social-media/index.html", "Social Media"),
    ("branding/index.html", "Branding & Design"),
    ("press-releases/index.html", "Press Releases"),
    ("content-marketing/index.html", "Content Marketing"),
]


def clean_title(raw: str) -> str:
    title = unescape(raw.strip())
    for suffix in (
        " — YB Marketing Insights",
        " — YB Marketing",
        " | YB Marketing",
    ):
        if title.endswith(suffix):
            title = title[: -len(suffix)].strip()
    return title


def page_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = TITLE_RE.search(text)
    if not match:
        return path.stem.replace("-", " ").title()
    return clean_title(match.group(1))


def is_public_page(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part.startswith(".") for part in rel.parts):
        return False
    if rel.parts[0] in EXCLUDE_DIRS:
        return False
    if rel.name == "blog.html":
        return False
    return True


def load_location_hubs() -> list[dict]:
    script = (
        "import { locationHubs } from './locationHubs.js';"
        "process.stdout.write(JSON.stringify(locationHubs));"
    )
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=ROOT / "data",
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


LOCAL_SERVICE_FOLDERS = [
    ("seo", "SEO"),
    ("google-ads", "Google Ads"),
    ("web-design", "Web Design"),
    ("social-media", "Social Media"),
    ("branding", "Branding"),
]


def location_group_links(slug: str, city: str, state: str) -> list[tuple[str, str]]:
    place = f"{city}, {state}"
    links = []
    for folder, service in LOCAL_SERVICE_FOLDERS:
        if not (ROOT / folder / f"{slug}.html").exists():
            continue
        links.append((page_href(f"{folder}/{slug}.html"), f"{service} in {place}"))
    return links


def collect_pages() -> tuple[
    dict[str, list[tuple[str, str]]],
    list[tuple[str, str, list[tuple[str, str]]]],
    list[tuple[str, str]],
]:
    compact: dict[str, list[tuple[str, str]]] = {
        "Main Pages": [],
        "Services": [],
        "Team": [],
    }
    local_groups: list[tuple[str, str, list[tuple[str, str]]]] = []
    insights: list[tuple[str, str]] = []

    for loc in sorted(load_location_hubs(), key=lambda item: item["slug"]):
        city = loc["city"]
        state = loc["state"]
        slug = loc["slug"]
        group_title = f"Digital Marketing Agency in {city}, {state}"
        hub_href = page_href(f"locations/{slug}.html")
        local_groups.append((group_title, hub_href, location_group_links(slug, city, state)))

    for href, label in ROOT_PAGES:
        if href == "sitemap.html":
            continue
        compact["Main Pages"].append((page_href(href), label))

    for rel, label in SERVICE_INDEX_PAGES:
        if (ROOT / rel).exists():
            compact["Services"].append((page_href(rel), label))

    for path in sorted((ROOT / "about").glob("*.html")):
        if "thank-you" in path.name:
            continue
        href = page_href(f"about/{path.name}")
        compact["Team"].append((href, page_title(path)))

    for path in sorted((ROOT / "blog" / "posts").glob("*.html")):
        href = page_href(f"blog/posts/{path.name}")
        insights.append((href, page_title(path)))

    return compact, local_groups, insights


def is_sitemap_page(path: Path) -> bool:
    if not is_public_page(path):
        return False
    rel = path.relative_to(ROOT).as_posix()
    if "thank-you" in rel:
        return False
    if rel == "blog.html":
        return False
    return True


def normalize_canonical(href: str) -> str:
    href = href.strip()
    if href.startswith("http"):
        return href.rstrip("/") if not href.endswith(".com/") else href
    if href.startswith("/"):
        return f"{SITE}{href.rstrip('/')}"
    return f"{SITE}/{href.rstrip('/')}"


def public_url_for_page(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    match = CANONICAL_RE.search(text)
    if match:
        return normalize_canonical(match.group(1))

    if rel == "index.html":
        return f"{SITE}/"
    if rel in SERVICE_PAGES:
        return f"{SITE}/{SERVICE_PAGES[rel]['slug']}"
    if rel == "washington-state-sales-tax.html":
        return f"{SITE}/washington-state-sales-tax-notice"

    return f"{SITE}/{rel.replace('.html', '')}"


def page_sitemap_meta(rel: str) -> tuple[str, str]:
    if rel == "index.html":
        return "weekly", "1.0"
    if rel in SERVICE_PAGES:
        return "monthly", "0.9"
    if rel in {"about.html", "contact.html", "insights.html"}:
        return "monthly", "0.9"
    if rel.startswith("services/"):
        return "monthly", "0.9"
    if rel.startswith("locations/") or rel.split("/")[0] in {
        "seo",
        "google-ads",
        "web-design",
        "social-media",
        "branding",
    }:
        return "monthly", "0.8"
    if rel.startswith("about/"):
        return "monthly", "0.6"
    if rel in {"privacy-policy.html", "washington-state-sales-tax.html"}:
        return "yearly", "0.3"
    if rel == "sitemap.html":
        return "monthly", "0.2"
    return "monthly", "0.7"


def collect_page_urls() -> list[tuple[str, str, str, Optional[str]]]:
    entries: list[tuple[str, str, str, str | None]] = []
    seen: set[str] = set()

    for path in sorted(ROOT.rglob("*.html")):
        if not is_sitemap_page(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        url = public_url_for_page(path)
        if url in seen:
            continue
        seen.add(url)
        changefreq, priority = page_sitemap_meta(rel)
        entries.append((url, changefreq, priority, None))

    entries.sort(key=lambda item: item[0])
    return entries


def load_posts_data() -> list[dict]:
    if not POSTS_DATA.exists():
        return []
    return json.loads(POSTS_DATA.read_text(encoding="utf-8"))


def post_lastmod(post: dict) -> str:
    raw = post.get("date", "")
    if not raw:
        return date.today().isoformat()
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return raw[:10]


def collect_post_urls() -> list[tuple[str, str, str, str]]:
    entries = []
    for post in sorted(load_posts_data(), key=lambda item: item.get("date", ""), reverse=True):
        slug = post["slug"]
        entries.append(
            (
                f"{SITE}/insights/{slug}",
                "monthly",
                "0.6",
                post_lastmod(post),
            )
        )
    return entries


def render_url_entry(
    url: str,
    changefreq: str,
    priority: str,
    lastmod: Optional[str] = None,
) -> str:
    lastmod_line = f"\n    <lastmod>{lastmod}</lastmod>" if lastmod else ""
    return f"""  <url>
    <loc>{escape(url)}</loc>{lastmod_line}
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""


def build_urlset_xml(entries: list[tuple[str, str, str, Optional[str]]]) -> str:
    body = "\n".join(
        render_url_entry(url, changefreq, priority, lastmod)
        for url, changefreq, priority, lastmod in entries
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
"""


def build_sitemap_index(lastmods: dict[str, str]) -> str:
    sitemaps = "\n".join(
        f"""  <sitemap>
    <loc>{escape(f"{SITE}/{name}")}</loc>
    <lastmod>{lastmod}</lastmod>
  </sitemap>"""
        for name, lastmod in sorted(lastmods.items())
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemaps}
</sitemapindex>
"""


def write_xml_sitemaps() -> None:
    page_entries = collect_page_urls()
    post_entries = collect_post_urls()

    pages_path = ROOT / "sitemap-pages.xml"
    posts_path = ROOT / "sitemap-posts.xml"
    index_path = ROOT / "sitemap.xml"

    pages_path.write_text(build_urlset_xml(page_entries), encoding="utf-8")
    posts_path.write_text(build_urlset_xml(post_entries), encoding="utf-8")

    today = date.today().isoformat()
    post_lastmods = [entry[3] for entry in post_entries if entry[3]]
    index_path.write_text(
        build_sitemap_index(
            {
                "sitemap-pages.xml": today,
                "sitemap-posts.xml": max(post_lastmods) if post_lastmods else today,
            }
        ),
        encoding="utf-8",
    )

    print(f"wrote {pages_path.relative_to(ROOT)} ({len(page_entries)} URLs)")
    print(f"wrote {posts_path.relative_to(ROOT)} ({len(post_entries)} URLs)")
    print(f"wrote {index_path.relative_to(ROOT)} (index)")


def render_link_list(links: list[tuple[str, str]], list_class: str = "") -> str:
    cls = f' class="{list_class}"' if list_class else ""
    items = "\n".join(
        f'          <li><a href="{escape(href)}">{escape(label)}</a></li>'
        for href, label in links
    )
    return f"        <ul{cls}>\n{items}\n        </ul>"


def render_compact_section(title: str, links: list[tuple[str, str]]) -> str:
    return f"""      <div class="sitemap-col">
        <h2>{escape(title)}</h2>
{render_link_list(links)}
      </div>"""


def render_local_section(groups: list[tuple[str, str, list[tuple[str, str]]]]) -> str:
    subgroups = []
    for title, hub_href, links in groups:
        subgroups.append(
            f"""        <div class="sitemap-subgroup">
          <h3><a href="{escape(hub_href)}">{escape(title)}</a></h3>
{render_link_list(links)}
        </div>"""
        )
    body = "\n".join(subgroups)
    return f"""      <div class="sitemap-section sitemap-section--full">
        <h2>Locations</h2>
        <div class="sitemap-local-grid">
{body}
        </div>
      </div>"""


def render_insights_section(links: list[tuple[str, str]]) -> str:
    return f"""      <div class="sitemap-section sitemap-section--full">
        <h2>Insights</h2>
{render_link_list(links, "sitemap-insights-list")}
      </div>"""


def build_sitemap_html(
    compact: dict[str, list[tuple[str, str]]],
    local_groups: list[tuple[str, str, list[tuple[str, str]]]],
    insights: list[tuple[str, str]],
) -> str:
    compact_blocks = "\n".join(
        render_compact_section(title, links) for title, links in compact.items() if links
    )
    local_block = render_local_section(local_groups)
    insights_block = render_insights_section(insights)
    total = sum(len(links) for links in compact.values()) + sum(
        len(links) for _, _, links in local_groups
    ) + len(insights) + 1
    header = site_header_html("").strip()
    footer = site_footer_html("").strip()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{STAGING_ROBOTS_META}
<link rel="icon" href="favicon.png" type="image/png">
<link rel="apple-touch-icon" href="favicon.png">
<title>Sitemap — YB Marketing</title>
<meta name="description" content="Browse every page on the YB Marketing website — services, team profiles, insights, and more.">
<link rel="stylesheet" href="colors_and_type.css">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--font-body);background:var(--bg);color:var(--fg1);-webkit-font-smoothing:antialiased;overflow-x:hidden}}
::selection{{background:var(--yb-blue);color:#fff}}
img{{display:block;max-width:100%}}
a{{color:inherit;text-decoration:none}}
.container{{width:100%;max-width:var(--container);margin:0 auto;padding:0 28px}}
.eyebrow{{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-body);font-weight:700;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--yb-blue)}}
.eyebrow::before{{content:'';display:block;width:7px;height:7px;border-radius:50%;background:currentColor;flex:none}}
.btn{{display:inline-flex;align-items:center;gap:8px;border:none;cursor:pointer;font-family:var(--font-body);font-weight:700;font-size:15px;border-radius:var(--r-md);padding:13px 22px;transition:all 240ms;white-space:nowrap;line-height:1}}
.btn-grad{{background:var(--grad-brand);color:#fff;box-shadow:0 14px 30px -10px rgba(63,111,214,.45)}}
.btn-grad:hover{{transform:translateY(-2px);filter:brightness(1.06)}}
.sitemap-hero{{position:relative;overflow:hidden;background:var(--grad-navy);padding:72px 0 88px}}
.sitemap-hero-mesh{{position:absolute;inset:0;background-image:var(--grad-mesh);pointer-events:none}}
.sitemap-hero h1{{font-family:var(--font-display);font-weight:800;font-size:clamp(2rem,3.6vw,3.2rem);color:#fff;line-height:1.1;margin:18px 0 20px;max-width:820px}}
.sitemap-hero p{{color:var(--fg2-on-dark);font-size:clamp(1rem,1.3vw,1.12rem);line-height:1.75;max-width:820px}}
.sitemap-main{{padding:72px 0 96px}}
.sitemap-grid{{display:flex;flex-direction:column;gap:52px}}
.sitemap-compact{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:40px 56px}}
.sitemap-section h2,.sitemap-col h2{{font-family:var(--font-display);font-size:1.15rem;font-weight:800;color:var(--ink);margin-bottom:16px;padding-bottom:10px;border-bottom:2px solid var(--line)}}
.sitemap-section ul,.sitemap-col ul{{list-style:none;display:grid;gap:10px}}
.sitemap-section a,.sitemap-col a{{color:var(--yb-blue);font-size:15px;font-weight:600;line-height:1.45;transition:color 200ms}}
.sitemap-section a:hover,.sitemap-col a:hover{{color:var(--ink)}}
.sitemap-local-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px 24px;margin-top:8px}}
.sitemap-locations-intro{{color:var(--fg2);font-size:15px;line-height:1.65;margin:-4px 0 28px;max-width:820px}}
.sitemap-locations-intro a{{color:var(--yb-blue);font-weight:700}}
.sitemap-subgroup{{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--r-lg);padding:20px 22px}}
.sitemap-subgroup ul{{gap:8px}}
.sitemap-subgroup a{{font-size:14px}}
.sitemap-subgroup h3{{font-family:var(--font-display);font-size:1rem;font-weight:800;color:var(--ink);margin:0 0 14px;letter-spacing:.01em;line-height:1.35}}
.sitemap-subgroup h3 a{{color:inherit;text-decoration:none;transition:color 200ms}}
.sitemap-subgroup h3 a:hover{{color:var(--yb-blue)}}
.sitemap-insights-list{{display:block;columns:3;column-gap:48px}}
.sitemap-insights-list li{{break-inside:avoid;margin-bottom:10px}}
.sitemap-count{{margin-top:36px;padding:18px 22px;border-radius:var(--r-lg);background:var(--bg-soft);border:1px solid var(--line);color:var(--fg2);font-size:14px}}
@media(max-width:900px){{.sitemap-compact{{grid-template-columns:1fr}}.sitemap-local-grid{{grid-template-columns:1fr}}.sitemap-insights-list{{columns:2}}}}
@media(max-width:640px){{.sitemap-insights-list{{columns:1}}}}
</style>
<link rel="stylesheet" href="site.css">
</head>
<body>
{ACCESSIBE_BODY_SCRIPT}

{header}

<section class="sitemap-hero">
  <div class="sitemap-hero-mesh"></div>
  <div class="hero-logo-overlay hero-logo-overlay--left" aria-hidden="true">
    <img src="assets/yb-logo-white.png" alt="">
  </div>
  <div class="container" style="position:relative;z-index:2">
    <span class="eyebrow" style="color:var(--yb-cyan)">Sitemap</span>
    <h1>Yakima Branding Digital Marketing Agency</h1>
    <p>It&rsquo;s our goal to help you identify your company&rsquo;s marketing strengths and find the most creative way to highlight the benefits that set you apart from the competition. At Yakima Branding, we offer a comprehensive approach. We specialize in all-in-one solutions. That means we help you every step of the way to make sure your brand&rsquo;s value is upheld and your marketing approach is consistent and effective, across all platforms and deliverables.</p>
  </div>
</section>

<main class="sitemap-main">
  <div class="container">
    <div class="sitemap-grid">
      <div class="sitemap-compact">
{compact_blocks}
      </div>
{local_block}
{insights_block}
    </div>
    <p class="sitemap-count">{total} pages listed on this sitemap.</p>
  </div>
</main>

{footer}

<script src="js/newsletter-popup.js" defer></script>
<script src="js/chat-widget.js" defer></script>
<script src="js/site.js"></script>
</body>
</html>
"""


def patch_footer_sitemap_link(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    prefix = sitemap_prefix_for(path)
    replacement = f'<a href="{page_href("sitemap.html")}">Sitemap</a>'

    if SITEMAP_LINKED_RE.search(text):
        updated, n = SITEMAP_LINKED_RE.subn(replacement, text, count=1)
    elif SITEMAP_LINK_RE.search(text):
        updated, n = SITEMAP_LINK_RE.subn(replacement, text, count=1)
    else:
        return False

    if n:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def patch_snippet() -> None:
    snippet_path = ROOT / "scripts" / "site_footer_snippet.py"
    text = snippet_path.read_text(encoding="utf-8")
    if '<a href="/sitemap">Sitemap</a>' in text:
        return
    updated = text.replace(
        '<a href="{p}sitemap.html">Sitemap</a>',
        '<a href="/sitemap">Sitemap</a>',
    )
    snippet_path.write_text(updated, encoding="utf-8")


def patch_cta_footer() -> None:
    path = ROOT / "ui_kits" / "website" / "CTAFooter.jsx"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    updated = text.replace(
        '<a href="#" onClick={e=>e.preventDefault()} style={{ color: \'var(--fg2-on-dark)\', textDecoration: \'none\' }}>Sitemap</a>',
        '<a href="/sitemap" style={{ color: \'var(--fg2-on-dark)\', textDecoration: \'none\' }}>Sitemap</a>',
    )
    path.write_text(updated, encoding="utf-8")


def sitemap_prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth


def main() -> None:
    compact, local_groups, insights = collect_pages()
    sitemap_path = ROOT / "sitemap.html"
    sitemap_path.write_text(
        build_sitemap_html(compact, local_groups, insights), encoding="utf-8"
    )
    print(f"wrote {sitemap_path.relative_to(ROOT)}")

    write_xml_sitemaps()

    patched = 0
    for path in sorted(ROOT.rglob("*.html")):
        if not is_public_page(path):
            continue
        if patch_footer_sitemap_link(path):
            patched += 1
            print(f"linked footer in {path.relative_to(ROOT)}")

    patch_snippet()
    patch_cta_footer()
    print(f"patched {patched} footer links")


if __name__ == "__main__":
    main()
