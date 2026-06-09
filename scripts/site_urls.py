"""Clean URL helpers for YB Marketing static site."""

from __future__ import annotations

from pathlib import Path
from typing import Optional
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]

SERVICE_FILE_SLUGS = {
    "branding.html": "branding",
    "content-creation.html": "content-marketing",
    "google-ads.html": "google-ads",
    "press-releases.html": "press-releases",
    "seo.html": "seo",
    "social-media.html": "social-media",
    "web-design.html": "web-design",
}

SPECIAL_PATHS = {
    "index.html": "",
    "washington-state-sales-tax.html": "washington-state-sales-tax-notice",
}


def clean_segment(rel_path: str) -> str:
    """Map a repo-relative .html path to a clean URL path (no leading slash)."""
    rel_path = rel_path.replace("\\", "/").lstrip("/")
    if not rel_path:
        return ""

    if rel_path in SPECIAL_PATHS:
        return SPECIAL_PATHS[rel_path]

    if rel_path.startswith("services/"):
        name = rel_path.rsplit("/", 1)[-1]
        if name.startswith("thank-you-"):
            return f"services/{name.replace('.html', '')}"
        slug = SERVICE_FILE_SLUGS.get(name, name.replace(".html", ""))
        return slug

    if rel_path.startswith("blog/posts/"):
        slug = rel_path.replace("blog/posts/", "").replace(".html", "")
        return f"insights/{slug}"

    if rel_path.startswith("posts/"):
        slug = rel_path.replace("posts/", "").replace(".html", "")
        return f"insights/{slug}"

    return rel_path.replace(".html", "")


def page_href(path: str, anchor: Optional[str] = None) -> str:
    """Absolute clean URL for internal page links."""
    segment = clean_segment(path)
    frag = f"#{anchor.lstrip('#')}" if anchor else ""
    return ("/" if segment == "" else f"/{segment}") + frag


def href(prefix: str, path: str, anchor: Optional[str] = None) -> str:
    """Backward-compatible alias — internal links are always absolute."""
    _ = prefix
    return page_href(path, anchor)


def absolute_clean_url(rel_path: str) -> str:
    segment = clean_segment(rel_path)
    return "/" if segment == "" else f"/{segment}"


def resolve_href_to_absolute(href_value: str, source_file: Path) -> str:
    """Resolve a relative or absolute internal href to an absolute clean URL."""
    parsed = urlsplit(href_value)
    if not parsed.path or parsed.path.startswith("//"):
        return href_value

    skip_prefixes = ("http:", "https:", "mailto:", "tel:", "javascript:")
    lower = href_value.lower()
    if any(lower.startswith(p) for p in skip_prefixes):
        return href_value

    if parsed.path.startswith("/"):
        rel = parsed.path.lstrip("/")
    else:
        source_dir = source_file.parent.relative_to(ROOT)
        rel = (source_dir / parsed.path).resolve().relative_to(ROOT.resolve()).as_posix()

    clean = absolute_clean_url(rel)
    return urlunsplit(("", "", clean, parsed.query, parsed.fragment))


def patch_html_href(href_value: str, source_file: Path) -> str:
    if ".html" not in href_value:
        return href_value
    if href_value.startswith("#"):
        return href_value
    lower = href_value.lower()
    if lower.startswith(("http://", "https://", "mailto:", "tel:", "javascript:")):
        return href_value
    return resolve_href_to_absolute(href_value, source_file)
