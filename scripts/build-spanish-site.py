#!/usr/bin/env python3
"""Generate /es/ Spanish mirror of the static site via machine translation + cache.

Phases:
  1) Extract unique translatable strings from all English HTML
  2) Translate missing cache entries (batched / rate-limited)
  3) Render /es/** pages applying cache + Spanish chrome
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from site_footer_snippet import site_footer_html  # noqa: E402
from site_i18n import (  # noqa: E402
    SITE,
    absolute_asset_url,
    clean_path_from_file,
    hreflang_links,
    rewrite_internal_href_to_es,
)
from site_nav_snippet import site_header_html  # noqa: E402

CACHE_PATH = ROOT / "data" / "i18n" / "es-cache.json"
ES_ROOT = ROOT / "es"

EXCLUDE_DIRS = {
    "preview",
    "partials",
    "ui_kits",
    "posts",
    "scripts",
    "assets",
    "js",
    "node_modules",
    "next",
    "es",
    "_next",
    "data",
    "wp-content",
}

SKIP_PARENT_TAGS = {"script", "style", "noscript", "code", "pre", "svg"}
ATTRS_TO_TRANSLATE = ("alt", "title", "aria-label", "placeholder")
PROTECT_TOKENS = [
    "YB Marketing",
    "Yakima Branding",
    "Google Ads",
    "Google Business Profile",
    "WordPress",
    "Wix",
    "HubSpot",
    "Pacific Northwest",
    "LinkedIn",
    "Facebook",
    "Instagram",
    "SEO",
    "PPC",
    "AI",
    "CWU",
    "Hoopfest",
    "Bloomsday",
]

HEADER_RE = re.compile(
    r'<div class="header top" id="header">[\s\S]*?<div class="mobile-menu" id="mobileMenu">[\s\S]*?</div>\s*</div>',
    re.DOTALL,
)
FOOTER_RE = re.compile(r'<footer class="footer">.*?</footer>', re.DOTALL)
HREFLANG_RE = re.compile(
    r'<link\b[^>]*\bhreflang=["\'][^"\']+["\'][^>]*/?>\s*',
    re.I,
)
CANONICAL_RE = re.compile(r'(<link rel="canonical" href=")[^"]+(")', re.I)
HTML_LANG_RE = re.compile(r'(<html[^>]*\slang=")[^"]+(")', re.I)

PHONE_RE = re.compile(r"\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
URL_RE = re.compile(r"https?://[^\s<>\"]+")


def load_cache() -> dict[str, str]:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict[str, str]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def is_public_page(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part.startswith(".") for part in rel.parts):
        return False
    if rel.parts[0] in EXCLUDE_DIRS:
        return False
    return True


def prefix_for_es(rel_en: str) -> str:
    parts = Path(rel_en).parts
    return "../" * len(parts)


def about_active_for(path: Path) -> str | None:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "about.html":
        return "about"
    if "case-studies" in rel:
        return "case-studies"
    if "washington-state-sales-tax" in rel:
        return "tax"
    if rel.startswith("about/") and "thank-you" not in rel:
        return "about"
    return None


def should_skip_text(text: str) -> bool:
    s = text.strip()
    if not s:
        return True
    if len(s) <= 1 and not s.isalpha():
        return True
    if re.fullmatch(r"[\d\s\W_]+", s):
        return True
    return False


def protect(text: str) -> tuple[str, list[str]]:
    held: list[str] = []
    out = text

    def stash(match: re.Match[str]) -> str:
        held.append(match.group(0))
        return f"⟦{len(held) - 1}⟧"

    out = URL_RE.sub(stash, out)
    out = EMAIL_RE.sub(stash, out)
    out = PHONE_RE.sub(stash, out)
    for token in sorted(PROTECT_TOKENS, key=len, reverse=True):
        if token in out:
            held.append(token)
            out = out.replace(token, f"⟦{len(held) - 1}⟧")
    return out, held


def unprotect(text: str, held: list[str]) -> str:
    out = text
    for i, val in enumerate(held):
        out = out.replace(f"⟦{i}⟧", val)
        out = out.replace(f"[[{i}]]", val)
    return out


def _chunk(text: str, size: int) -> list[str]:
    if len(text) <= size:
        return [text]
    parts: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            split = text.rfind(". ", start, end)
            if split > start + size // 2:
                end = split + 1
        parts.append(text[start:end])
        start = end
    return parts


class Translator:
    def __init__(self, cache: dict[str, str], dry_run: bool = False):
        self.cache = cache
        self.dry_run = dry_run
        self._client = None

    def _ensure_client(self):
        if self._client is None:
            from deep_translator import GoogleTranslator

            self._client = GoogleTranslator(source="en", target="es")
        return self._client

    def get(self, text: str) -> str:
        if should_skip_text(text):
            return text
        return self.cache.get(text, text)

    def translate_one(self, text: str) -> str:
        if should_skip_text(text):
            return text
        if text in self.cache:
            return self.cache[text]
        if self.dry_run:
            self.cache[text] = f"[ES] {text}"
            return self.cache[text]

        protected, held = protect(text)
        client = self._ensure_client()
        parts: list[str] = []
        for chunk in _chunk(protected, 4500):
            for attempt in range(6):
                try:
                    parts.append(client.translate(chunk))
                    break
                except Exception as exc:  # noqa: BLE001
                    wait = min(8.0, 1.2 * (attempt + 1))
                    print(f"  retry {attempt + 1}: {exc}")
                    time.sleep(wait)
            else:
                parts.append(chunk)
            time.sleep(0.03)
        result = unprotect("".join(parts), held)
        self.cache[text] = result
        return result

    def fill_missing(self, strings: set[str]) -> None:
        missing = sorted(s for s in strings if s not in self.cache and not should_skip_text(s))
        print(f"Translating {len(missing)} unique strings ({len(self.cache)} cached)...")
        for i, s in enumerate(missing, 1):
            self.translate_one(s)
            if i % 20 == 0:
                save_cache(self.cache)
                print(f"  {i}/{len(missing)}")
        save_cache(self.cache)
        print(f"Translation complete. cache={len(self.cache)}")


def collect_strings_from_json(script_text: str, out: set[str]) -> None:
    try:
        data = json.loads(script_text)
    except json.JSONDecodeError:
        return

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in {"@type", "@context", "@id", "url", "item", "telephone", "email", "image", "logo"}:
                    continue
                if k in {"name", "description", "text", "headline", "jobTitle"} and isinstance(v, str):
                    if not should_skip_text(v):
                        out.add(v.strip())
                else:
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)


def collect_strings_from_html(html: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    found: set[str] = set()
    if soup.title and soup.title.string and not should_skip_text(soup.title.string):
        found.add(soup.title.string.strip())
    for meta in soup.find_all("meta", attrs={"name": True}):
        if meta.get("name", "").lower() == "description" and meta.get("content"):
            if not should_skip_text(meta["content"]):
                found.add(meta["content"].strip())
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        if script.string:
            collect_strings_from_json(script.string, found)
    for tag in soup.find_all(True):
        if tag.name in SKIP_PARENT_TAGS:
            continue
        for attr in ATTRS_TO_TRANSLATE:
            if tag.has_attr(attr) and isinstance(tag[attr], str) and not should_skip_text(tag[attr]):
                found.add(tag[attr].strip())
    for node in soup.find_all(string=True):
        if isinstance(node, Comment):
            continue
        parent = node.parent
        if not isinstance(parent, Tag) or parent.name in SKIP_PARENT_TAGS:
            continue
        if parent.find_parent(SKIP_PARENT_TAGS):
            continue
        core = str(node).strip()
        if not should_skip_text(core):
            found.add(core)
    return found


def translate_json_ld(script_text: str, tr: Translator) -> str:
    try:
        data = json.loads(script_text)
    except json.JSONDecodeError:
        return script_text

    def walk(node):
        if isinstance(node, dict):
            for k, v in list(node.items()):
                if k in {"@type", "@context", "@id", "url", "item", "telephone", "email", "image", "logo"}:
                    continue
                if k in {"name", "description", "text", "headline", "jobTitle"} and isinstance(v, str):
                    node[k] = tr.get(v.strip()) if v.strip() in tr.cache else tr.get(v)
                else:
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)
    return json.dumps(data, ensure_ascii=False)


def apply_translations(soup: BeautifulSoup, tr: Translator) -> None:
    if soup.title and soup.title.string:
        soup.title.string = tr.get(soup.title.string.strip())
    for meta in soup.find_all("meta", attrs={"name": True}):
        if meta.get("name", "").lower() == "description" and meta.get("content"):
            meta["content"] = tr.get(meta["content"].strip())
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        if script.string:
            script.string = translate_json_ld(script.string, tr)
    for tag in soup.find_all(True):
        if tag.name in SKIP_PARENT_TAGS:
            continue
        for attr in ATTRS_TO_TRANSLATE:
            if tag.has_attr(attr) and isinstance(tag[attr], str) and tag[attr].strip():
                tag[attr] = tr.get(tag[attr].strip())
    for node in list(soup.find_all(string=True)):
        if isinstance(node, Comment):
            continue
        parent = node.parent
        if not isinstance(parent, Tag) or parent.name in SKIP_PARENT_TAGS:
            continue
        if parent.find_parent(SKIP_PARENT_TAGS):
            continue
        text = str(node)
        core = text.strip()
        if should_skip_text(core):
            continue
        leading = text[: len(text) - len(text.lstrip())]
        trailing = text[len(text.rstrip()) :]
        node.replace_with(NavigableString(leading + tr.get(core) + trailing))


def rewrite_links(soup: BeautifulSoup, source_file: Path) -> None:
    for tag in soup.find_all(["a", "link", "area"]):
        href = tag.get("href")
        if not href:
            continue
        rel = (tag.get("rel") or [])
        if isinstance(rel, str):
            rel = [rel]
        if tag.name == "link" and "alternate" in rel:
            continue
        if not href.startswith(("/", "#", "http", "mailto", "tel", "javascript", "data")):
            abs_href = absolute_asset_url(href, source_file)
            if abs_href.endswith(".html"):
                from site_urls import absolute_clean_url

                try:
                    clean = absolute_clean_url(abs_href.lstrip("/"))
                    tag["href"] = rewrite_internal_href_to_es(clean)
                except Exception:  # noqa: BLE001
                    tag["href"] = rewrite_internal_href_to_es(abs_href)
            else:
                tag["href"] = abs_href
        else:
            tag["href"] = rewrite_internal_href_to_es(href)

    for tag in soup.find_all(["img", "script", "source", "iframe"]):
        for attr in ("src", "data-src"):
            val = tag.get(attr)
            if val and not val.startswith(("http", "//", "data:", "/")):
                tag[attr] = absolute_asset_url(val, source_file)

    for tag in soup.find_all("link"):
        href = tag.get("href")
        if href and not href.startswith(("http", "//", "/", "data:")):
            tag["href"] = absolute_asset_url(href, source_file)


def restamp_chrome(html: str, rel_en: str, source_en: Path) -> str:
    current = clean_path_from_file(source_en)
    prefix = prefix_for_es(rel_en)
    about = about_active_for(source_en)
    header = site_header_html(prefix, about, lang="es", current_path=current).strip()
    footer = site_footer_html(prefix, lang="es", current_path=current).strip()
    out = html
    if HEADER_RE.search(out):
        out = HEADER_RE.sub(header, out, count=1)
    if FOOTER_RE.search(out):
        out = FOOTER_RE.sub(footer, out, count=1)
    return out


def finalize_head(html: str, current_clean: str) -> str:
    out = HREFLANG_RE.sub("", html)
    links = hreflang_links(current_clean)
    canonical = f"{SITE}/es/{current_clean}" if current_clean else f"{SITE}/es"

    if HTML_LANG_RE.search(out):
        out = HTML_LANG_RE.sub(r"\1es\2", out, count=1)
    else:
        out = out.replace("<html", '<html lang="es"', 1)

    if CANONICAL_RE.search(out):
        out = CANONICAL_RE.sub(rf"\1{canonical}\2", out, count=1)
    else:
        out = out.replace("</head>", f'<link rel="canonical" href="{canonical}">\n</head>', 1)

    out = out.replace("</head>", links + "\n</head>", 1)
    return out


def process_page(path: Path, tr: Translator) -> Path:
    rel = path.relative_to(ROOT).as_posix()
    out_path = ES_ROOT / rel
    out_path.parent.mkdir(parents=True, exist_ok=True)
    raw = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw, "html.parser")
    apply_translations(soup, tr)
    rewrite_links(soup, path)
    html = str(soup)
    # html.parser sometimes emits a stray "HTML" token before <html>
    html = re.sub(
        r"^(?:<!DOCTYPE html>\s*)?HTML\s*",
        "<!DOCTYPE html>\n",
        html,
        count=1,
        flags=re.I,
    )
    if not html.lstrip().lower().startswith("<!doctype"):
        html = "<!DOCTYPE html>\n" + html
    # Drop accidental "HTML" leftovers before the root element
    html = re.sub(r"(<!DOCTYPE html>\s*)HTML(?=\s*(?:<!--|<html\b))", r"\1", html, count=1, flags=re.I)
    html = restamp_chrome(html, rel, path)
    html = finalize_head(html, clean_path_from_file(path))
    out_path.write_text(html, encoding="utf-8")
    return out_path


def iter_pages():
    for path in sorted(ROOT.rglob("*.html")):
        if is_public_page(path):
            yield path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--only", type=str, default="")
    parser.add_argument("--skip-translate", action="store_true", help="Only render from cache")
    args = parser.parse_args()

    cache = load_cache()
    tr = Translator(cache, dry_run=args.dry_run)
    pages = list(iter_pages())
    if args.only:
        pages = [p for p in pages if args.only in p.relative_to(ROOT).as_posix()]
    if args.limit:
        pages = pages[: args.limit]

    print(f"Pages: {len(pages)}")
    if not args.skip_translate:
        all_strings: set[str] = set()
        for i, path in enumerate(pages, 1):
            html = path.read_text(encoding="utf-8", errors="replace")
            all_strings |= collect_strings_from_html(html)
            if i % 40 == 0:
                print(f"  extracted from {i}/{len(pages)} pages ({len(all_strings)} unique)")
        print(f"Unique strings: {len(all_strings)}")
        tr.fill_missing(all_strings)

    print(f"Rendering {len(pages)} Spanish pages → {ES_ROOT}/")
    for i, path in enumerate(pages, 1):
        rel = path.relative_to(ROOT).as_posix()
        process_page(path, tr)
        if i % 25 == 0 or i == len(pages):
            print(f"  rendered {i}/{len(pages)} ({rel})")

    save_cache(tr.cache)
    print("done")


if __name__ == "__main__":
    main()
