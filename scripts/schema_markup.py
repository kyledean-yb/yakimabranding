"""JSON-LD structured data for YB Marketing static site."""

from __future__ import annotations

import json
import re
import subprocess
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://yakimabranding.com"
LOGO_URL = f"{SITE}/assets/yb-logo-color.png"
HOME_HERO_IMAGE = f"{SITE}/assets/team-photo.webp"

SCHEMA_MARKER_START = "<!-- yb-schema-start -->"
SCHEMA_MARKER_END = "<!-- yb-schema-end -->"
LD_JSON_RE = re.compile(
    r'<script type="application/ld\+json">.*?</script>\s*',
    re.DOTALL,
)
MARKER_BLOCK_RE = re.compile(
    re.escape(SCHEMA_MARKER_START) + r".*?" + re.escape(SCHEMA_MARKER_END) + r"\s*",
    re.DOTALL,
)

AGGREGATE_RATING = {
    "@type": "AggregateRating",
    "ratingValue": "5.0",
    "reviewCount": "43",
    "bestRating": "5",
}

TEAM_MEMBERS = [
    ("Jacob Ross", "Account Executive"),
    ("Kayelyn Aggett", "Social Media Manager"),
    ("Kevin Dean", "Owner"),
    ("Kirsten Gonzalez", "Marketing Administrator"),
    ("Kristin Sparling", "Account Executive"),
    ("Sophie Mann", "Account Executive"),
]

SERVICE_PAGES = {
    "services/branding.html": {
        "slug": "branding",
        "name": "Branding & Design",
        "service_type": "Brand Identity Design",
        "description": "Comprehensive brand strategy, logo design, and design systems for Pacific Northwest businesses.",
    },
    "services/content-creation.html": {
        "slug": "content-marketing",
        "name": "Content Marketing",
        "service_type": "Content Marketing",
        "description": "Website content, blog writing, press releases, email campaigns, and social media content for growing businesses.",
    },
    "services/google-ads.html": {
        "slug": "google-ads",
        "name": "Google Ads Management",
        "service_type": "Pay-Per-Click Advertising",
        "description": "Expert Google Ads management since 2005 — search, display, and Performance Max campaigns for Pacific Northwest businesses.",
    },
    "services/press-releases.html": {
        "slug": "press-releases",
        "name": "Press Releases",
        "service_type": "Press Release Writing & Distribution",
        "description": "Professional press release writing and distribution for Pacific Northwest businesses.",
    },
    "services/seo.html": {
        "slug": "seo",
        "name": "SEO & AI Optimization",
        "service_type": "Search Engine Optimization",
        "description": "Local SEO, technical SEO, keyword strategy, and AI search optimization for Pacific Northwest businesses.",
    },
    "services/social-media.html": {
        "slug": "social-media",
        "name": "Social Media Management",
        "service_type": "Social Media Marketing",
        "description": "Facebook, Instagram, and LinkedIn management with real growth strategies for Pacific Northwest businesses.",
    },
    "services/web-design.html": {
        "slug": "web-design",
        "name": "Web Design & Development",
        "service_type": "Web Design",
        "description": "Custom WordPress and Wix website design and development for Pacific Northwest businesses.",
    },
}

LOCAL_SERVICE_META = {
    "seo": {
        "folder": "seo",
        "name": "SEO & AI Optimization",
        "service_type": "Search Engine Optimization",
        "export": "seoLocations",
        "file": "seoLocations.js",
    },
    "google-ads": {
        "folder": "google-ads",
        "name": "Google Ads Management",
        "service_type": "Pay-Per-Click Advertising",
        "export": "googleAdsLocations",
        "file": "googleAdsLocations.js",
    },
    "web-design": {
        "folder": "web-design",
        "name": "Web Design & Development",
        "service_type": "Web Design",
        "export": "webDesignLocations",
        "file": "webDesignLocations.js",
    },
    "social-media": {
        "folder": "social-media",
        "name": "Social Media Management",
        "service_type": "Social Media Marketing",
        "export": "socialMediaLocations",
        "file": "socialMediaLocations.js",
    },
    "branding": {
        "folder": "branding",
        "name": "Branding & Design",
        "service_type": "Brand Identity Design",
        "export": "brandingLocations",
        "file": "brandingLocations.js",
    },
}

CITY_META = {
    "yakima-wa": ("Yakima", "WA", "Washington"),
    "ellensburg-wa": ("Ellensburg", "WA", "Washington"),
    "tri-cities-wa": ("Tri-Cities", "WA", "Washington"),
    "spokane-wa": ("Spokane", "WA", "Washington"),
    "boise-id": ("Boise", "ID", "Idaho"),
    "coeur-dalene-id": ("Coeur d'Alene", "ID", "Idaho"),
    "tacoma-wa": ("Tacoma", "WA", "Washington"),
    "vancouver-wa": ("Vancouver", "WA", "Washington"),
    "wenatchee-wa": ("Wenatchee", "WA", "Washington"),
    "walla-walla-wa": ("Walla Walla", "WA", "Washington"),
}

LOCATION_HUB_CITIES = {
    "boise-id": ("Boise", "ID"),
    "coeur-dalene-id": ("Coeur d'Alene", "ID"),
    "ellensburg-wa": ("Ellensburg", "WA"),
    "spokane-wa": ("Spokane", "WA"),
    "tacoma-wa": ("Tacoma", "WA"),
    "tri-cities-wa": ("Tri-Cities (Kennewick, Pasco & Richland)", "WA"),
    "vancouver-wa": ("Vancouver", "WA"),
    "walla-walla-wa": ("Walla Walla", "WA"),
    "wenatchee-wa": ("Wenatchee", "WA"),
    "yakima-wa": ("Yakima", "WA"),
}

GUEST_POST_SLUGS = {
    "effects-of-rain-on-asphalt",
    "pcba-design-for-manufacturability",
    "resolving-employee-disputes-before-you-are-sued",
    "signs-your-car-may-need-transmission-repair",
    "what-to-look-for-in-a-moving-company",
    "what-you-should-consider-when-installing-a-concrete-patio",
    "why-choose-gasoline-box-trucks-vs-diesel",
    "the-thermal-press-difference",
    "selecting-a-commercial-landscape-maintenance-company",
    "why-should-you-send-your-child-to-camp-mowglis-give-them-a-chance-to-unplug",
    "best-business-entity-for-franchisees",
}


def organization_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "YB Marketing",
        "alternateName": "Yakima Branding",
        "url": SITE,
        "logo": LOGO_URL,
        "description": "Award-winning digital marketing agency helping businesses grow through strategic branding, SEO, and comprehensive digital solutions.",
        "telephone": "+15099019735",
        "email": "info@yakimabranding.com",
        "foundingDate": "2004",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Yakima",
            "addressRegion": "WA",
            "addressCountry": "US",
        },
        "areaServed": [
            "Yakima, WA",
            "Ellensburg, WA",
            "Tri-Cities, WA",
            "Spokane, WA",
            "Boise, ID",
            "Coeur d'Alene, ID",
            "Tacoma, WA",
            "Vancouver, WA",
            "Wenatchee, WA",
            "Walla Walla, WA",
            "Pacific Northwest",
        ],
        "sameAs": [
            "https://www.facebook.com/yakimabranding",
            "https://www.instagram.com/yakimabranding",
            "https://www.linkedin.com/company/yakima-branding",
        ],
        "aggregateRating": AGGREGATE_RATING.copy(),
    }


def website_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "YB Marketing",
        "url": SITE,
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": f"{SITE}/insights?search={{search_term_string}}",
            },
            "query-input": "required name=search_term_string",
        },
    }


def global_schemas() -> list[dict]:
    return [organization_schema(), website_schema()]


def breadcrumb(items: list[tuple[int, str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": pos,
                "name": name,
                "item": url,
            }
            for pos, name, url in items
        ],
    }


def person_schema(name: str, job_title: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": name,
        "jobTitle": job_title,
        "worksFor": {"@type": "Organization", "name": "YB Marketing"},
        "url": f"{SITE}/about",
    }


def faq_schema(faqs: list[dict]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {"@type": "Answer", "text": item["a"]},
            }
            for item in faqs
        ],
    }


def service_schema(name: str, service_type: str, url: str, description: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "serviceType": service_type,
        "provider": {
            "@type": "LocalBusiness",
            "name": "YB Marketing",
            "url": SITE,
        },
        "areaServed": {"@type": "State", "name": "Pacific Northwest"},
        "url": url,
        "description": description,
    }


def webpage_schema(name: str, url: str, description: str | None = None, crumbs: list[tuple[int, str, str]] | None = None) -> dict:
    data: dict = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": name,
        "url": url,
    }
    if description:
        data["description"] = description
    if crumbs:
        data["breadcrumb"] = breadcrumb(crumbs)
    return data


@lru_cache(maxsize=1)
def load_posts() -> dict[str, dict]:
    path = ROOT / "blog" / "data" / "posts.json"
    if not path.exists():
        return {}
    posts = json.loads(path.read_text(encoding="utf-8"))
    return {p["slug"]: p for p in posts}


@lru_cache(maxsize=1)
def load_location_hubs() -> dict[str, dict]:
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
    hubs = json.loads(result.stdout)
    return {h["slug"]: h for h in hubs}


def _load_js_export(export_name: str, file_name: str) -> list[dict]:
    script = (
        f"import {{ {export_name} }} from './{file_name}';"
        f"process.stdout.write(JSON.stringify({export_name}));"
    )
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=ROOT / "data",
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


@lru_cache(maxsize=1)
def load_local_service_locations() -> dict[tuple[str, str], dict]:
    index: dict[tuple[str, str], dict] = {}
    for key, meta in LOCAL_SERVICE_META.items():
        rows = _load_js_export(meta["export"], meta["file"])
        for row in rows:
            index[(meta["folder"], row["slug"])] = row
    return index


def localized_service_schemas(service_key: str, city_slug: str) -> list[dict]:
    meta = LOCAL_SERVICE_META[service_key]
    loc = load_local_service_locations().get((meta["folder"], city_slug))
    city, state, state_full = CITY_META[city_slug]
    url = f"{SITE}/{meta['folder']}/{city_slug}"
    service_name = meta["name"]
    schemas = [
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": f"{service_name} in {city}, {state}",
            "serviceType": meta["service_type"],
            "provider": {
                "@type": "LocalBusiness",
                "name": "YB Marketing",
                "url": SITE,
                "telephone": "+15099019735",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "Yakima",
                    "addressRegion": "WA",
                    "addressCountry": "US",
                },
            },
            "areaServed": {
                "@type": "City",
                "name": city,
                "containedInPlace": {"@type": "State", "name": state_full},
            },
            "url": url,
        },
        breadcrumb(
            [
                (1, "Home", SITE),
                (2, service_name, f"{SITE}/{service_key}"),
                (3, f"{service_name} in {city}", url),
            ]
        ),
    ]
    if loc and loc.get("faqs"):
        schemas.append(faq_schema(loc["faqs"]))
    return schemas


def blog_posting_schema(post: dict, guest: bool = False) -> dict:
    slug = post["slug"]
    date = post.get("date", "")
    if date and "T" not in date and len(date) == 10:
        date_iso = f"{date}T00:00:00"
    elif date:
        date_iso = date.split(".")[0]
    else:
        date_iso = "PLACEHOLDER — add publish date"
    image = post.get("image") or "PLACEHOLDER — add featured image URL"
    data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "url": f"{SITE}/insights/{slug}",
        "datePublished": date_iso,
        "dateModified": date_iso,
        "author": {"@type": "Organization", "name": "YB Marketing", "url": SITE},
        "publisher": {
            "@type": "Organization",
            "name": "YB Marketing",
            "logo": {"@type": "ImageObject", "url": LOGO_URL},
        },
        "image": image,
        "description": post.get("excerpt", ""),
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{SITE}/insights/{slug}"},
        "breadcrumb": breadcrumb(
            [
                (1, "Home", SITE),
                (2, "Insights", f"{SITE}/insights"),
                (3, post["title"], f"{SITE}/insights/{slug}"),
            ]
        ),
    }
    if guest:
        data["_comment"] = "Guest post — verify author attribution"
    return data


def schemas_for_rel_path(rel: str) -> tuple[list[dict], str, str]:
    """Return (schema objects, type summary, notes)."""
    rel = rel.replace("\\", "/")
    notes = ""
    page_schemas: list[dict] = []

    if rel == "index.html":
        page_schemas.extend(
            [
                {
                    "@context": "https://schema.org",
                    "@type": "LocalBusiness",
                    "name": "YB Marketing",
                    "image": HOME_HERO_IMAGE,
                    "url": SITE,
                    "telephone": "+15099019735",
                    "email": "info@yakimabranding.com",
                    "priceRange": "$$",
                    "address": {
                        "@type": "PostalAddress",
                        "addressLocality": "Yakima",
                        "addressRegion": "WA",
                        "addressCountry": "US",
                    },
                    "geo": {"@type": "GeoCoordinates", "latitude": 46.6021, "longitude": -120.5059},
                    "openingHoursSpecification": {
                        "@type": "OpeningHoursSpecification",
                        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                        "opens": "09:00",
                        "closes": "17:00",
                    },
                    "aggregateRating": AGGREGATE_RATING.copy(),
                },
                webpage_schema(
                    "YB Marketing — Digital Marketing Agency | Yakima, WA",
                    SITE,
                    "Award-winning digital marketing agency helping businesses grow through strategic branding, SEO, and comprehensive digital solutions. Rooted in Yakima, WA.",
                    [(1, "Home", SITE)],
                ),
            ]
        )
        return global_schemas() + page_schemas, "Organization, WebSite, LocalBusiness, WebPage", notes

    if rel == "about.html":
        page_schemas.append(
            {
                "@context": "https://schema.org",
                "@type": "AboutPage",
                "name": "About YB Marketing | Yakima Branding",
                "url": f"{SITE}/about",
                "description": "Meet the YB Marketing team. We are a dedicated digital marketing agency rooted in Yakima, WA, serving businesses across the Pacific Northwest.",
                "breadcrumb": breadcrumb(
                    [(1, "Home", SITE), (2, "About", f"{SITE}/about")]
                ),
            }
        )
        page_schemas.extend(person_schema(n, t) for n, t in TEAM_MEMBERS)
        return global_schemas() + page_schemas, "Organization, WebSite, AboutPage, Person ×6", notes

    if rel == "insights.html":
        page_schemas.append(
            {
                "@context": "https://schema.org",
                "@type": "Blog",
                "name": "YB Marketing Insights",
                "url": f"{SITE}/insights",
                "description": "Marketing insights, strategies, and guides for growing businesses from the YB Marketing team.",
                "publisher": {
                    "@type": "Organization",
                    "name": "YB Marketing",
                    "logo": {"@type": "ImageObject", "url": LOGO_URL},
                },
                "breadcrumb": breadcrumb(
                    [(1, "Home", SITE), (2, "Insights", f"{SITE}/insights")]
                ),
            }
        )
        return global_schemas() + page_schemas, "Organization, WebSite, Blog", notes

    if rel == "contact.html":
        page_schemas.append(
            {
                "@context": "https://schema.org",
                "@type": "ContactPage",
                "name": "Contact YB Marketing",
                "url": f"{SITE}/contact",
                "description": "Get in touch with YB Marketing. Schedule a free 30-minute consultation or send us a message. We serve businesses across the Pacific Northwest.",
                "breadcrumb": breadcrumb(
                    [(1, "Home", SITE), (2, "Contact", f"{SITE}/contact")]
                ),
            }
        )
        return global_schemas() + page_schemas, "Organization, WebSite, ContactPage", notes

    if rel == "washington-state-sales-tax.html":
        page_schemas.append(
            webpage_schema(
                "Washington State Sales Tax Notice | YB Marketing",
                f"{SITE}/washington-state-sales-tax-notice",
                crumbs=[
                    (1, "Home", SITE),
                    (2, "Washington State Sales Tax Notice", f"{SITE}/washington-state-sales-tax-notice"),
                ],
            )
        )
        notes = "Canonical URL uses /washington-state-sales-tax-notice per spec; file is washington-state-sales-tax.html"
        return global_schemas() + page_schemas, "Organization, WebSite, WebPage", notes

    if rel == "privacy-policy.html":
        page_schemas.append(
            webpage_schema(
                "Privacy Policy | YB Marketing",
                f"{SITE}/privacy-policy",
                crumbs=[
                    (1, "Home", SITE),
                    (2, "Privacy Policy", f"{SITE}/privacy-policy"),
                ],
            )
        )
        return global_schemas() + page_schemas, "Organization, WebSite, WebPage", notes

    if rel == "thank-you.html":
        page_schemas.append(
            {
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": "Thank You | YB Marketing",
                "url": f"{SITE}/thank-you",
                "noIndex": True,
            }
        )
        return global_schemas() + page_schemas, "Organization, WebSite, WebPage (noindex)", notes

    if rel == "sitemap.html":
        page_schemas.append(
            webpage_schema(
                "Sitemap | YB Marketing",
                f"{SITE}/sitemap",
                crumbs=[(1, "Home", SITE), (2, "Sitemap", f"{SITE}/sitemap")],
            )
        )
        return global_schemas() + page_schemas, "Organization, WebSite, WebPage", notes

    if rel in SERVICE_PAGES:
        svc = SERVICE_PAGES[rel]
        url = f"{SITE}/{svc['slug']}"
        page_schemas.extend(
            [
                service_schema(svc["name"], svc["service_type"], url, svc["description"]),
                breadcrumb(
                    [
                        (1, "Home", SITE),
                        (2, "Services", f"{SITE}/services"),
                        (3, svc["name"], url),
                    ]
                ),
                webpage_schema(svc["name"], url, svc["description"]),
            ]
        )
        return global_schemas() + page_schemas, "Organization, WebSite, Service, WebPage, BreadcrumbList", notes

    if rel.startswith("locations/") and rel.endswith(".html"):
        slug = Path(rel).stem
        city, state = LOCATION_HUB_CITIES.get(slug, (slug, "WA"))
        url = f"{SITE}/locations/{slug}"
        hub = load_location_hubs().get(slug, {})
        desc = hub.get(
            "metaDescription",
            f"YB Marketing provides full-service digital marketing for {city} businesses — SEO, Google Ads, web design, social media, and branding.",
        )
        page_schemas.extend(
            [
                {
                    "@context": "https://schema.org",
                    "@type": "LocalBusiness",
                    "name": f"YB Marketing — {city} Digital Marketing",
                    "url": url,
                    "telephone": "+15099019735",
                    "email": "info@yakimabranding.com",
                    "address": {
                        "@type": "PostalAddress",
                        "addressLocality": city.split(" (")[0],
                        "addressRegion": state,
                        "addressCountry": "US",
                    },
                    "areaServed": {"@type": "City", "name": city.split(" (")[0]},
                    "description": desc,
                    "aggregateRating": AGGREGATE_RATING.copy(),
                },
                webpage_schema(
                    f"Digital Marketing Agency in {city}, {state} | YB Marketing",
                    url,
                    desc,
                ),
                breadcrumb(
                    [
                        (1, "Home", SITE),
                        (2, "Locations", f"{SITE}/locations"),
                        (3, f"Digital Marketing Agency in {city}, {state}", url),
                    ]
                ),
            ]
        )
        return global_schemas() + page_schemas, "Organization, WebSite, LocalBusiness, WebPage, BreadcrumbList", notes

    for service_key, meta in LOCAL_SERVICE_META.items():
        prefix = f"{meta['folder']}/"
        if rel.startswith(prefix) and rel.endswith(".html"):
            city_slug = Path(rel).stem
            if city_slug not in CITY_META:
                break
            page_schemas.extend(localized_service_schemas(service_key, city_slug))
            types = "Organization, WebSite, Service, BreadcrumbList"
            if any(s.get("@type") == "FAQPage" for s in page_schemas):
                types += ", FAQPage"
            return global_schemas() + page_schemas, types, notes

    if rel.startswith("blog/posts/") and rel.endswith(".html"):
        slug = Path(rel).stem
        post = load_posts().get(slug)
        if post:
            guest = slug in GUEST_POST_SLUGS
            if guest:
                notes = "Guest post — verify author attribution"
            page_schemas.append(blog_posting_schema(post, guest=guest))
            label = "BlogPosting"
            if guest:
                label += " (guest)"
            return global_schemas() + page_schemas, f"Organization, WebSite, {label}", notes
        notes = "Blog post not found in posts.json"
        return global_schemas(), "Organization, WebSite", notes

    if rel.startswith("about/") and rel.endswith(".html"):
        name_part = Path(rel).stem.replace("-", " ").title()
        page_schemas.append(
            webpage_schema(
                f"{name_part} | YB Marketing Team",
                f"{SITE}/{rel.replace('.html', '')}",
                crumbs=[
                    (1, "Home", SITE),
                    (2, "About", f"{SITE}/about"),
                    (3, name_part, f"{SITE}/{rel.replace('.html', '')}"),
                ],
            )
        )
        return global_schemas() + page_schemas, "Organization, WebSite, WebPage", notes

    title_guess = Path(rel).stem.replace("-", " ").title()
    page_schemas.append(
        webpage_schema(
            f"{title_guess} | YB Marketing",
            f"{SITE}/{rel.replace('.html', '')}",
        )
    )
    notes = "Fallback WebPage schema"
    return global_schemas() + page_schemas, "Organization, WebSite, WebPage", notes


def render_schema_head(schemas: list[dict]) -> str:
    lines = [SCHEMA_MARKER_START]
    for schema in schemas:
        payload = {k: v for k, v in schema.items() if k != "_comment"}
        lines.append(
            f'<script type="application/ld+json">{json.dumps(payload, ensure_ascii=False, separators=(",", ":"))}</script>'
        )
    lines.append(SCHEMA_MARKER_END)
    return "\n".join(lines) + "\n"


def inject_schema_into_html(html: str, schemas: list[dict]) -> str:
    html = MARKER_BLOCK_RE.sub("", html)
    html = LD_JSON_RE.sub("", html)
    block = render_schema_head(schemas)
    if "</head>" not in html:
        return html
    return html.replace("</head>", block + "</head>", 1)


def seo_head_html(rel_path: str) -> str:
    """SeoHead-equivalent: JSON-LD block for a page relative path."""
    schemas, _, _ = schemas_for_rel_path(rel_path.replace("\\", "/"))
    return render_schema_head(schemas)
