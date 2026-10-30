"""Per-page JSON-LD (@graph) and social meta, built from each page's own content.

Run scripts/patch-schema.py after any page generator to refresh every page.
"""

from __future__ import annotations

import html
import importlib.util
import json
import re
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://yakimabranding.com"
ORG_ID = f"{SITE}/#organization"
WEBSITE_ID = f"{SITE}/#website"
LOGO_ID = f"{SITE}/#logo"
LOGO_URL = f"{SITE}/assets/yb-logo-color.png"
OG_DEFAULT = f"{SITE}/assets/og-default.jpg"
OG_DEFAULT_SIZE = (1200, 630)
PHONE = "+1-509-901-9735"
EMAIL = "info@yakimabranding.com"
PACIFIC = ZoneInfo("America/Los_Angeles")
SAME_AS = [
    "https://www.facebook.com/yakimabranding",
    "https://www.instagram.com/yb.marketing_/",
    "https://www.linkedin.com/company/18939370",
]
RATING = {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "48", "bestRating": "5", "worstRating": "1"}

SEO_START = "<!-- yb-seo-start -->"
SEO_END = "<!-- yb-seo-end -->"

SKIP_DIRS = {"preview", "partials", "ui_kits", "posts", "scripts", "assets", "js", "node_modules",
             "next", "_next", "data", "scraps", "uploads", "wp-content", "emails"}

SERVICES = {
    "seo/index.html": "Search Engine Optimization",
    "seo/local-seo.html": "Local Search Engine Optimization",
    "seo/ai-search.html": "Generative Engine Optimization",
    "seo/technical-seo.html": "Technical Search Engine Optimization",
    "seo/website-migration.html": "Website Migration",
    "google-ads/index.html": "Pay-Per-Click Advertising",
    "web-design/index.html": "Web Design",
    "branding/index.html": "Brand Identity Design",
    "social-media/index.html": "Social Media Marketing",
    "content-marketing/index.html": "Content Marketing",
    "press-releases/index.html": "Press Release Writing and Distribution",
    "customer-growth/index.html": "Customer Relationship Management Software",
    "ai-for-business/index.html": "Artificial Intelligence Consulting",
    "ai-for-small-business/index.html": "Artificial Intelligence Consulting",
    "phx-hvac/index.html": "HVAC Marketing",
}
CATALOG = [
    ("SEO Services", "/seo"), ("Local SEO", "/seo/local-seo"), ("AI Search Optimization", "/seo/ai-search"),
    ("Technical SEO", "/seo/technical-seo"), ("Website Migrations", "/seo/website-migration"),
    ("Google Ads Management", "/google-ads"), ("Web Design", "/web-design"), ("Branding & Design", "/branding"),
    ("Social Media Marketing", "/social-media"), ("Content Marketing", "/content-marketing"),
    ("Press Releases", "/press-releases"), ("Customer Growth & Communication Tool", "/customer-growth"),
    ("AI for Business", "/ai-for-business"), ("AI for Small Business", "/ai-for-small-business"),
]
KNOWS_ABOUT = ["Search engine optimization", "Local SEO", "Generative engine optimization", "Google Ads",
               "Pay-per-click advertising", "Web design", "WordPress", "Branding", "Logo design",
               "Social media marketing", "Content marketing", "Press releases", "Marketing automation",
               "Artificial intelligence for business"]
LOCAL_FOLDERS = {"seo": "Search Engine Optimization", "google-ads": "Pay-Per-Click Advertising",
                 "web-design": "Web Design", "social-media": "Social Media Marketing",
                 "branding": "Brand Identity Design"}
TEAM = {
    "kevin": ("Kevin Dean", "Owner", "Propietario"),
    "jacob": ("Jacob Ross", "Account Executive", "Ejecutivo de cuentas"),
    "sophie": ("Sophie Mann", "Account Executive", "Ejecutiva de cuentas"),
    "kirsten": ("Kirsten Gonzalez", "Marketing Administrator", "Administradora de marketing"),
    "kayelyn": ("Kayelyn Aggett", "Social Media Manager", "Gerente de redes sociales"),
}
SECTION_NAMES = {
    "about": ("About", "Nosotros"), "about/case-studies": ("Case Studies", "Casos de éxito"),
    "locations": ("Locations", "Ubicaciones"), "insights": ("Insights", "Perspectivas"),
    "seo": ("SEO Services", "Servicios de SEO"), "google-ads": ("Google Ads", "Google Ads"),
    "web-design": ("Web Design", "Diseño web"), "branding": ("Branding & Design", "Marca y diseño"),
    "social-media": ("Social Media", "Redes sociales"),
}
STATES = {"WA": "Washington", "ID": "Idaho", "OR": "Oregon", "CA": "California", "CO": "Colorado",
          "AZ": "Arizona", "IL": "Illinois"}
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July",
                                       "August", "September", "October", "November", "December"], 1)}


def _load_module(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@lru_cache(maxsize=1)
def location_data() -> dict[str, dict]:
    mod = _load_module("yb_locations", "add-location-pages.py")
    data = {r["slug"]: {**r, "kind": "region"} for r in mod.REGIONS}
    data.update({c["slug"]: {**c, "kind": "city"} for c in mod.CITIES})
    return data


@lru_cache(maxsize=1)
def reviews() -> list[tuple[str, str]]:
    src = (ROOT / "scripts" / "add-reviews-page.py").read_text(encoding="utf-8")
    start = src.index("REVIEWS = [")
    ns: dict = {}
    exec(src[start:src.index("\n]\n", start) + 3], ns)
    return list(ns["REVIEWS"])


@lru_cache(maxsize=1)
def posts() -> dict[str, dict]:
    data = json.loads((ROOT / "blog" / "data" / "posts.json").read_text(encoding="utf-8"))
    return {p["slug"]: p for p in data}


def is_public(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if any(p.startswith(".") for p in parts):
        return False
    if parts[0] in SKIP_DIRS or (parts[0] == "es" and len(parts) > 1 and parts[1] in SKIP_DIRS):
        return False
    return True


def clean_path(base_rel: str) -> str:
    """Repo path without es/ prefix → URL path ('' for home)."""
    if base_rel == "index.html":
        return ""
    if base_rel.startswith("blog/posts/"):
        return "insights/" + base_rel[len("blog/posts/"):-5]
    if base_rel.endswith("/index.html"):
        return base_rel[: -len("/index.html")]
    return base_rel[:-5]


def url_for(path: str, lang: str) -> str:
    if lang == "es":
        return f"{SITE}/es/{path}".rstrip("/") if path else f"{SITE}/es"
    return f"{SITE}/{path}" if path else f"{SITE}/"


def es_file_for(base_rel: str) -> Path:
    return ROOT / "es" / base_rel


def abs_url(src: str, page_rel: str) -> str:
    if src.startswith("http"):
        return src
    if src.startswith("/"):
        return SITE + src
    base = Path(page_rel).parent
    parts: list[str] = []
    for part in (base / src).as_posix().split("/"):
        if part == "..":
            if parts:
                parts.pop()
        elif part and part != ".":
            parts.append(part)
    return f"{SITE}/" + "/".join(parts)


def text_of(node) -> str:
    return re.sub(r"\s+", " ", node.get_text(" ", strip=True)).strip() if node else ""


def short_title(title: str) -> str:
    t = title.split(" | ")[0]
    t = re.sub(r"\s*(?:[—–-]|:)\s+YB Marketing.*$", "", t)
    return t.strip()


def iso_pacific(raw: str) -> str:
    dt = datetime.fromisoformat(raw[:19]) if "T" in raw else datetime.fromisoformat(raw[:10])
    return dt.replace(tzinfo=PACIFIC).isoformat()


def extract_faqs(soup: BeautifulSoup) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for item in soup.select(".faq-item"):
        q = item.select_one(".faq-q")
        a = item.select_one(".faq-a-inner") or item.select_one(".faq-a")
        if q:
            for icon in q.select(".faq-icon"):
                icon.extract()
        out.append((text_of(q), text_of(a)))
    for item in soup.select(".team-faq-item"):
        out.append((text_of(item.select_one(".team-faq-q")), text_of(item.select_one(".team-faq-a"))))
    for det in soup.select(".lc-faq details"):
        summary = det.find("summary")
        q = text_of(summary)
        if summary:
            summary.extract()
        out.append((q, text_of(det)))
    seen, faqs = set(), []
    for q, a in out:
        if q and a and q not in seen:
            seen.add(q)
            faqs.append((q, a))
    return faqs


def organization(full: bool, lang: str, with_reviews: bool = False) -> dict:
    org: dict = {
        "@type": "ProfessionalService",
        "@id": ORG_ID,
        "name": "YB Marketing",
        "alternateName": "Yakima Branding",
        "url": f"{SITE}/",
        "logo": {"@type": "ImageObject", "@id": LOGO_ID, "url": LOGO_URL, "contentUrl": LOGO_URL, "caption": "YB Marketing"},
        "image": OG_DEFAULT,
        "telephone": PHONE,
        "email": EMAIL,
        "address": {"@type": "PostalAddress", "addressLocality": "Yakima", "addressRegion": "WA", "addressCountry": "US"},
        "areaServed": {"@type": "Country", "name": "United States"},
        "priceRange": "$$",
        "sameAs": SAME_AS,
    }
    if not full:
        return org
    org.update({
        "description": "YB Marketing has been based in Yakima, Washington since 2004 and helps businesses across the country with marketing, website design, SEO, advertising, and branding.",
        "foundingDate": "2004",
        "foundingLocation": {"@type": "Place", "name": "Yakima, Washington"},
        "contactPoint": [{
            "@type": "ContactPoint", "contactType": "sales", "telephone": PHONE, "email": EMAIL,
            "areaServed": "US", "availableLanguage": ["English"],
        }],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "09:00", "closes": "17:00",
        }],
        "knowsAbout": KNOWS_ABOUT,
        "aggregateRating": RATING,
        "employee": [
            {"@type": "Person", "@id": f"{SITE}/about/{slug}#person", "name": name, "jobTitle": title,
             "url": f"{SITE}/about/{slug}"}
            for slug, (name, title, _) in TEAM.items()
        ],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Marketing services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "@id": f"{SITE}{path}#service", "name": name, "url": f"{SITE}{path}"}}
                for name, path in CATALOG
            ],
        },
    })
    if with_reviews:
        org["review"] = [
            {"@type": "Review", "author": {"@type": "Person", "name": name}, "reviewBody": body,
             "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"},
             "publisher": {"@type": "Organization", "name": "Google"}}
            for name, body in reviews()
        ]
    return org


def website() -> dict:
    return {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "url": f"{SITE}/",
        "name": "Yakima Branding",
        "alternateName": ["YB Marketing", "yakimabranding.com"],
        "publisher": {"@id": ORG_ID},
        "inLanguage": ["en-US", "es-US"],
    }


def breadcrumbs(path: str, lang: str, page_name: str, url: str,
                parents: list[tuple[str, str]] | None = None) -> dict | None:
    home = "Inicio" if lang == "es" else "Home"
    items = [(home, url_for("", lang))]
    segs = path.split("/") if path else []
    for i in range(1, len(segs)):
        sub = "/".join(segs[:i])
        if sub not in SECTION_NAMES:
            continue
        exists = (ROOT / f"{sub}.html").exists() or (ROOT / sub / "index.html").exists() or sub == "insights"
        if exists:
            items.append((SECTION_NAMES[sub][1 if lang == "es" else 0], url_for(sub, lang)))
    items.extend(parents or [])
    if path:
        items.append((page_name, url))
    if len(items) < 2:
        return None
    return {
        "@type": "BreadcrumbList",
        "@id": f"{url}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": name, "item": item_url}
            for i, (name, item_url) in enumerate(items, 1)
        ],
    }


def place_for_location(loc: dict) -> dict:
    state = {"@type": "State", "name": loc["state"]}
    if loc["kind"] == "city":
        return {"@type": "City", "name": loc["name"], "containedInPlace": state}
    return {
        "@type": "Place",
        "name": loc["name"],
        "containedInPlace": state,
        "containsPlace": [{"@type": "City", "name": c} for c in loc.get("cities", [])],
    }


def build_page(rel: str, raw: str) -> dict | None:
    """Return {'graph': [...], 'meta': {...}} or None for pages to skip."""
    if 'http-equiv="refresh"' in raw[:4000]:
        return None
    raw = STRIP_RES[0].sub("", raw)
    soup = BeautifulSoup(raw, "html.parser")
    lang = "es" if rel.startswith("es/") else "en"
    base_rel = rel[3:] if lang == "es" else rel
    path = clean_path(base_rel)

    canon_tag = soup.find("link", rel="canonical")
    url = canon_tag["href"].rstrip("/") if canon_tag and canon_tag.get("href") else url_for(path, lang)
    if url == SITE:
        url = f"{SITE}/"

    title_tag = soup.find("title")
    title = html.unescape(title_tag.get_text().strip()) if title_tag else short_title(path or "YB Marketing")
    desc_tag = soup.find("meta", attrs={"name": "description"})
    desc = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""
    h1 = text_of(soup.find("h1"))
    name = short_title(title)
    lang_code = "es-US" if lang == "es" else "en-US"
    page_id = f"{url}#webpage"
    stem = Path(base_rel).stem
    noindex = bool(soup.find("meta", attrs={"name": "robots", "content": re.compile("noindex")}))

    image_url, image_size, og_type = OG_DEFAULT, OG_DEFAULT_SIZE, "website"
    page_types: list[str] = ["WebPage"]
    extra: list[dict] = []
    page_extra: dict = {}
    full_org, org_reviews = False, False
    published = None
    crumb_name = name
    crumb_parents: list[tuple[str, str]] = []

    if base_rel == "index.html":
        full_org = True
        page_extra["about"] = {"@id": ORG_ID}
    elif base_rel == "about.html":
        page_types = ["AboutPage"]
        full_org = True
        page_extra["mainEntity"] = {"@id": ORG_ID}
    elif base_rel == "contact.html":
        page_types = ["ContactPage"]
        full_org = True
        page_extra["mainEntity"] = {"@id": ORG_ID}
    elif base_rel == "reviews.html":
        full_org, org_reviews = True, True
        page_extra["mainEntity"] = {"@id": ORG_ID}
    elif base_rel == "insights.html":
        page_types = ["CollectionPage"]
        blog_posts = []
        for slug, p in sorted(posts().items(), key=lambda kv: kv[1]["date"], reverse=True):
            if lang == "es" and not (ROOT / "es" / "blog" / "posts" / f"{slug}.html").exists():
                continue
            post_url = url_for(f"insights/{slug}", lang)
            blog_posts.append({"@type": "BlogPosting", "@id": f"{post_url}#article", "headline": p["title"],
                               "url": post_url, "datePublished": iso_pacific(p["date"])})
        extra.append({"@type": "Blog", "@id": f"{url}#blog", "name": name, "url": url, "description": desc,
                      "publisher": {"@id": ORG_ID}, "inLanguage": lang_code, "blogPost": blog_posts})
        page_extra["mainEntity"] = {"@id": f"{url}#blog"}
    elif base_rel.startswith("blog/posts/"):
        post = posts().get(stem, {})
        og_type = "article"
        if post.get("image"):
            image_url, image_size = abs_url(post["image"], base_rel), None
        published = iso_pacific(post["date"]) if post.get("date") else None
        modified = published
        upd = soup.select_one(".post-updated")
        m = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})", text_of(upd))
        if m:
            modified = datetime(int(m.group(2)), MONTHS[m.group(1)], 1, tzinfo=PACIFIC).isoformat()
        crumb_name = h1 or name
        prose = soup.select_one(".blog-prose")
        article = {
            "@type": "BlogPosting",
            "@id": f"{url}#article",
            "isPartOf": {"@id": url_for("insights", lang) + "#blog"},
            "mainEntityOfPage": {"@id": page_id},
            "headline": (h1 or name)[:110],
            "description": desc,
            "image": {"@id": f"{url}#primaryimage"},
            "author": {"@type": "Organization", "@id": ORG_ID, "name": "YB Marketing", "url": f"{SITE}/"},
            "publisher": {"@id": ORG_ID},
            "inLanguage": lang_code,
        }
        if published:
            article["datePublished"] = published
            article["dateModified"] = modified if modified and modified > published else published
            page_extra["datePublished"] = article["datePublished"]
            page_extra["dateModified"] = article["dateModified"]
        if post.get("topicLabel"):
            article["articleSection"] = post["topicLabel"]
        if post.get("categories"):
            article["keywords"] = [c for c in post["categories"] if c != "Blog"] or post["categories"]
        if prose:
            article["wordCount"] = len(text_of(prose).split())
        if post.get("readingTime"):
            article["timeRequired"] = f"PT{post['readingTime']}M"
        extra.append(article)
    elif base_rel == "about/case-studies/index.html":
        page_types = ["CollectionPage"]
        items = []
        for i, f in enumerate(sorted((ROOT / "about" / "case-studies").glob("*.html")), 1):
            if f.name == "index.html":
                continue
            target = (ROOT / "es" / "about" / "case-studies" / f.name) if lang == "es" else f
            if not target.exists():
                target = f
            t = BeautifulSoup(target.read_text(encoding="utf-8"), "html.parser").find("title")
            items.append({"@type": "ListItem", "position": len(items) + 1,
                          "url": url_for(f"about/case-studies/{f.stem}", lang if target != f else "en"),
                          "name": short_title(html.unescape(t.get_text())) if t else f.stem})
        extra.append({"@type": "ItemList", "@id": f"{url}#list", "itemListElement": items, "numberOfItems": len(items)})
        page_extra["mainEntity"] = {"@id": f"{url}#list"}
    elif base_rel.startswith("about/case-studies/"):
        og_type = "article"
        crumb_name = h1 or name
        extra.append({
            "@type": "Article",
            "@id": f"{url}#article",
            "mainEntityOfPage": {"@id": page_id},
            "headline": (h1 or name)[:110],
            "description": desc,
            "image": {"@id": f"{url}#primaryimage"},
            "author": {"@type": "Organization", "@id": ORG_ID, "name": "YB Marketing", "url": f"{SITE}/"},
            "publisher": {"@id": ORG_ID},
            "articleSection": "Case Study" if lang == "en" else "Caso de éxito",
            "inLanguage": lang_code,
        })
    elif base_rel.startswith("about/") and stem in TEAM:
        page_types = ["ProfilePage"]
        og_type = "profile"
        person_name, job_en, job_es = TEAM[stem]
        crumb_name = person_name
        img = soup.find("img", alt=person_name)
        person = {
            "@type": "Person",
            "@id": f"{SITE}/about/{stem}#person",
            "name": person_name,
            "jobTitle": job_es if lang == "es" else job_en,
            "worksFor": {"@id": ORG_ID},
            "url": url,
            "description": desc,
        }
        if img and img.get("src"):
            image_url, image_size = abs_url(img["src"], rel), None
            person["image"] = image_url
        extra.append(person)
        page_extra["mainEntity"] = {"@id": person["@id"]}
    elif base_rel == "locations/index.html":
        page_types = ["CollectionPage"]
        items = []
        for slug, loc in location_data().items():
            items.append({"@type": "ListItem", "position": len(items) + 1,
                          "url": url_for(f"locations/{slug}", "en"), "name": loc["name"]})
        extra.append({"@type": "ItemList", "@id": f"{url}#list", "itemListElement": items, "numberOfItems": len(items)})
        page_extra["mainEntity"] = {"@id": f"{url}#list"}
    elif base_rel.startswith("locations/") and stem in location_data() and "thank-you" not in stem:
        loc = location_data()[stem]
        crumb_name = loc["name"]
        parent = location_data().get(loc.get("region") or "")
        if parent:
            parent_rel = f"locations/{parent['slug']}"
            parent_lang = lang if (ROOT / ("es/" if lang == "es" else "") / f"{parent_rel}.html").exists() else "en"
            crumb_parents = [(parent["name"], url_for(parent_rel, parent_lang))]
        extra.append({
            "@type": "Service",
            "@id": f"{url}#service",
            "name": name,
            "serviceType": "Digital Marketing",
            "description": desc,
            "provider": {"@id": ORG_ID},
            "areaServed": place_for_location(loc),
            "url": url,
        })
        page_extra["about"] = {"@id": f"{url}#service"}
    elif base_rel.startswith("locations/") and "thank-you" not in stem:
        m = re.match(r"(.+?),? (WA|ID|OR)\b", h1 or name)
        area = {"@type": "City", "name": m.group(1).split(" in ")[-1].strip(), "containedInPlace": {"@type": "State", "name": STATES[m.group(2)]}} if m else {"@type": "Country", "name": "United States"}
        extra.append({"@type": "Service", "@id": f"{url}#service", "name": name, "serviceType": "Digital Marketing",
                      "description": desc, "provider": {"@id": ORG_ID}, "areaServed": area, "url": url})
        page_extra["about"] = {"@id": f"{url}#service"}
    elif base_rel in SERVICES:
        area = {"@type": "Country", "name": "United States"}
        if base_rel.startswith("phx-hvac/"):
            area = {"@type": "City", "name": "Phoenix", "containedInPlace": {"@type": "State", "name": "Arizona"}}
        extra.append({
            "@type": "Service",
            "@id": f"{SITE}/{path}#service" if lang == "en" else f"{url}#service",
            "name": name,
            "serviceType": SERVICES[base_rel],
            "description": desc,
            "provider": {"@id": ORG_ID},
            "areaServed": area,
            "url": url,
        })
        page_extra["about"] = {"@id": extra[-1]["@id"]}
    elif base_rel.split("/")[0] in LOCAL_FOLDERS and base_rel.count("/") == 1 and "thank-you" not in stem:
        m = re.match(r"(.+)-([a-z]{2})$", stem)
        if m:
            loc = location_data().get(stem)
            city = loc["name"] if loc else m.group(1).replace("-", " ").title()
            state = STATES.get(m.group(2).upper(), m.group(2).upper())
            extra.append({
                "@type": "Service",
                "@id": f"{url}#service",
                "name": name,
                "serviceType": LOCAL_FOLDERS[base_rel.split("/")[0]],
                "description": desc,
                "provider": {"@id": ORG_ID},
                "areaServed": {"@type": "City", "name": city, "containedInPlace": {"@type": "State", "name": state}},
                "url": url,
            })
            page_extra["about"] = {"@id": f"{url}#service"}
    elif base_rel in ("client-corner/index.html", "crm-tutorials/index.html"):
        page_types = ["CollectionPage"]

    faqs = [] if noindex else extract_faqs(soup)
    if faqs:
        page_types = page_types + ["FAQPage"]
        page_extra["mainEntity"] = [
            {"@type": "Question", "@id": f"{url}#faq-{i}", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for i, (q, a) in enumerate(faqs, 1)
        ]

    crumb = None if noindex else breadcrumbs(path, lang, crumb_name, url, crumb_parents)
    webpage = {
        "@type": page_types[0] if len(page_types) == 1 else page_types,
        "@id": page_id,
        "url": url,
        "name": title,
        "isPartOf": {"@id": WEBSITE_ID},
        "inLanguage": lang_code,
        "primaryImageOfPage": {"@id": f"{url}#primaryimage"},
        "image": {"@id": f"{url}#primaryimage"},
    }
    if desc:
        webpage["description"] = desc
    if crumb:
        webpage["breadcrumb"] = {"@id": crumb["@id"]}
    webpage.update(page_extra)

    image_node = {"@type": "ImageObject", "@id": f"{url}#primaryimage", "url": image_url, "contentUrl": image_url,
                  "inLanguage": lang_code}
    if image_size:
        image_node["width"], image_node["height"] = image_size

    graph = [organization(full_org, lang, org_reviews), website(), webpage, image_node] + extra
    if crumb:
        graph.append(crumb)

    en_path = ROOT / base_rel
    es_path = es_file_for(base_rel)
    alternates = {}
    if en_path.exists() and es_path.exists():
        alternates = {"en": url_for(path, "en"), "es": url_for(path, "es")}

    meta = {
        "url": url,
        "title": title,
        "description": desc,
        "image": image_url,
        "image_size": image_size,
        "image_alt": h1 or name,
        "type": og_type,
        "locale": "es_US" if lang == "es" else "en_US",
        "alternates": alternates,
        "published": published,
        "has_canonical": bool(canon_tag),
        "has_hreflang": bool(soup.find("link", rel="alternate", hreflang=True)),
    }
    return {"graph": graph, "meta": meta}


def meta_tags(meta: dict) -> list[str]:
    e = lambda v: html.escape(v, quote=True)
    tags = []
    if not meta["has_canonical"]:
        tags.append(f'<link rel="canonical" href="{e(meta["url"])}">')
    if meta["alternates"] and not meta["has_hreflang"]:
        en, es = meta["alternates"]["en"], meta["alternates"]["es"]
        tags += [f'<link rel="alternate" hreflang="en" href="{e(en)}">',
                 f'<link rel="alternate" hreflang="es" href="{e(es)}">',
                 f'<link rel="alternate" hreflang="x-default" href="{e(en)}">']
    tags += [
        '<meta property="og:site_name" content="Yakima Branding">',
        f'<meta property="og:type" content="{meta["type"]}">',
        f'<meta property="og:url" content="{e(meta["url"])}">',
        f'<meta property="og:title" content="{e(meta["title"])}">',
    ]
    if meta["description"]:
        tags.append(f'<meta property="og:description" content="{e(meta["description"])}">')
    tags.append(f'<meta property="og:image" content="{e(meta["image"])}">')
    if meta["image_size"]:
        tags += [f'<meta property="og:image:width" content="{meta["image_size"][0]}">',
                 f'<meta property="og:image:height" content="{meta["image_size"][1]}">']
    tags.append(f'<meta property="og:image:alt" content="{e(meta["image_alt"])}">')
    tags.append(f'<meta property="og:locale" content="{meta["locale"]}">')
    if meta["alternates"]:
        other = "en_US" if meta["locale"] == "es_US" else "es_US"
        tags.append(f'<meta property="og:locale:alternate" content="{other}">')
    if meta["published"]:
        tags.append(f'<meta property="article:published_time" content="{meta["published"]}">')
    tags += [
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{e(meta["title"])}">',
    ]
    if meta["description"]:
        tags.append(f'<meta name="twitter:description" content="{e(meta["description"])}">')
    tags.append(f'<meta name="twitter:image" content="{e(meta["image"])}">')
    return tags


STRIP_RES = [
    re.compile(r"<!-- yb-seo-start -->.*?<!-- yb-seo-end -->\s*", re.S),
    re.compile(r"<!-- yb-schema-start -->.*?<!-- yb-schema-end -->\s*", re.S),
    re.compile(r'<script type="application/ld\+json">.*?</script>\s*', re.S),
    re.compile(r'<meta\b[^>]*\b(?:property|name)="(?:og|twitter|article):[^"]*"[^>]*>\s*'),
]


CANONICAL_RE = re.compile(r'<link\b[^>]*\brel="canonical"[^>]*>\s*')


def apply_to_html(raw: str, data: dict) -> str:
    out = raw
    for rx in STRIP_RES:
        out = rx.sub("", out)
    canon = list(CANONICAL_RE.finditer(out))
    for m in reversed(canon[1:]):
        out = out[: m.start()] + out[m.end():]
    graph = json.dumps({"@context": "https://schema.org", "@graph": data["graph"]}, ensure_ascii=False, separators=(",", ":"))
    graph = graph.replace("</", "<\\/")
    block = "\n".join([SEO_START, *meta_tags(data["meta"]),
                       f'<script type="application/ld+json">{graph}</script>', SEO_END]) + "\n"
    return out.replace("</head>", block + "</head>", 1) if "</head>" in out else out
