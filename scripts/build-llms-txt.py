#!/usr/bin/env python3
"""Write /llms.txt (site index for AI assistants) and /llms-full.txt (page text), per llmstxt.org.

Re-run after adding or changing pages.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from seo_graph import SITE, extract_faqs, location_data, short_title  # noqa: E402

SECTIONS = [
    ("Services", [
        "seo/index.html", "seo/local-seo.html", "seo/ai-search.html", "seo/technical-seo.html",
        "seo/website-migration.html", "google-ads/index.html", "web-design/index.html", "branding/index.html",
        "social-media/index.html", "content-marketing/index.html", "press-releases/index.html",
        "customer-growth/index.html",
    ]),
    ("AI Services", ["ai-for-business/index.html", "ai-for-small-business/index.html"]),
    ("Company", ["about.html", "reviews.html", "about/case-studies/index.html", "contact.html",
                 "about/kevin.html", "about/jacob.html", "about/sophie.html", "about/kirsten.html",
                 "about/kayelyn.html"]),
    ("Case Studies", "about/case-studies/*.html"),
    ("Locations", "locations"),
    ("Resources", ["insights.html", "client-corner/index.html", "crm-tutorials/index.html"]),
]
FULL_TEXT_SECTIONS = {"Services", "AI Services", "Company", "Case Studies", "Locations"}
STRIP_SELECTORS = ["script", "style", "noscript", "svg", "header", "nav", "footer", "form", "iframe",
                   ".svr", ".mega-menu", ".mobile-menu", ".footer", ".chat-widget", "[aria-hidden=true]",
                   ".faq-list", ".faq-item", ".lc-faq", ".team-faq-item", ".cta-band", ".booking"]


def url_for(rel: str) -> str:
    if rel == "index.html":
        return f"{SITE}/"
    if rel.endswith("/index.html"):
        return f"{SITE}/{rel[:-11]}"
    return f"{SITE}/{rel[:-5]}"


def page_info(rel: str) -> tuple[str, str, BeautifulSoup]:
    soup = BeautifulSoup((ROOT / rel).read_text(encoding="utf-8"), "html.parser")
    title = short_title(html.unescape(soup.title.get_text().strip())) if soup.title else rel
    title = re.sub(r"\s+[—–]\s+", ", ", title)
    desc_tag = soup.find("meta", attrs={"name": "description"})
    desc = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""
    return title, desc, soup


def section_pages(spec) -> list[str]:
    if spec == "locations":
        return ["locations/index.html"] + [
            f"locations/{slug}.html" for slug in location_data() if (ROOT / "locations" / f"{slug}.html").exists()
        ]
    if isinstance(spec, str):
        base = Path(spec).parent
        return [f"{base.as_posix()}/{p.name}" for p in sorted((ROOT / base).glob(Path(spec).name)) if p.name != "index.html"]
    return [rel for rel in spec if (ROOT / rel).exists()]


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def page_markdown(rel: str) -> str:
    title, desc, soup = page_info(rel)
    faqs = extract_faqs(BeautifulSoup((ROOT / rel).read_text(encoding="utf-8"), "html.parser"))
    body = soup.find("main") or soup.body or soup
    for sel in STRIP_SELECTORS:
        for node in body.select(sel):
            node.decompose()
    lines: list[str] = []
    last = None
    for node in body.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
        if node.find_parent(["li"]) and node.name != "li":
            continue
        text = clean(node.get_text(" ", strip=True))
        if not text or text == last or len(text) < 3:
            continue
        last = text
        if node.name in ("h1", "h2", "h3", "h4"):
            level = {"h1": "##", "h2": "###", "h3": "####", "h4": "####"}[node.name]
            lines.append(f"\n{level} {text}\n")
        elif node.name == "li":
            lines.append(f"- {text}")
        else:
            lines.append(text)
    out = [f"# {title}", f"URL: {url_for(rel)}"]
    if desc:
        out.append(f"> {html.unescape(desc)}")
    out.append("\n".join(lines).strip())
    if faqs:
        out.append("\n### Frequently Asked Questions\n")
        out.extend(f"**{q}**\n{a}\n" for q, a in faqs)
    return "\n\n".join(out).strip()


def build_index() -> str:
    _, home_desc, _ = page_info("index.html")
    parts = [
        "# YB Marketing (Yakima Branding)",
        "",
        "> YB Marketing is a digital marketing agency based in Yakima, Washington since 2004. "
        "We help businesses across the United States with SEO, AI search optimization, Google Ads, "
        "website design, branding, social media, content, and AI tools for business.",
        "",
        "- Phone: (509) 901-9735",
        "- Email: info@yakimabranding.com",
        "- Office: Yakima, Washington, USA. Clients nationwide; meetings by phone, Zoom, or in person in Yakima.",
        "- Rating: 5.0 from 48 Google reviews",
        "- Founded: 2004",
        "- Languages: English site, with a Spanish version at https://yakimabranding.com/es",
        "- Full page text for AI assistants: https://yakimabranding.com/llms-full.txt",
        "",
    ]
    for name, spec in SECTIONS:
        parts.append(f"## {name}\n")
        for rel in section_pages(spec):
            title, desc, _ = page_info(rel)
            line = f"- [{title}]({url_for(rel)})"
            if desc:
                line += f": {html.unescape(desc)}"
            parts.append(line)
        parts.append("")
    posts = sorted(json.loads((ROOT / "blog" / "data" / "posts.json").read_text(encoding="utf-8")),
                   key=lambda p: p["date"], reverse=True)
    parts.append("## Optional\n")
    parts.append(f"- [Sitemap]({SITE}/sitemap.xml): Every page and article on the site")
    for p in posts:
        excerpt = clean(html.unescape(p.get("excerpt", ""))).rstrip("…").strip()
        parts.append(f"- [{p['title']}]({SITE}/insights/{p['slug']}): {excerpt}" if excerpt else f"- [{p['title']}]({SITE}/insights/{p['slug']})")
    return "\n".join(parts).strip() + "\n"


def build_full() -> str:
    parts = [
        "# YB Marketing (Yakima Branding): full site text",
        "",
        "> Plain text of the main pages on https://yakimabranding.com for AI assistants. "
        "See https://yakimabranding.com/llms.txt for the index.",
        "",
        page_markdown("index.html"),
    ]
    for name, spec in SECTIONS:
        if name not in FULL_TEXT_SECTIONS:
            continue
        for rel in section_pages(spec):
            parts.append("\n---\n")
            parts.append(page_markdown(rel))
    return re.sub(r"\n{3,}", "\n\n", "\n".join(parts)).strip() + "\n"


def main() -> None:
    index = build_index()
    full = build_full()
    (ROOT / "llms.txt").write_text(index, encoding="utf-8")
    (ROOT / "llms-full.txt").write_text(full, encoding="utf-8")
    print(f"wrote llms.txt ({len(index):,} chars) and llms-full.txt ({len(full):,} chars)")


if __name__ == "__main__":
    main()
