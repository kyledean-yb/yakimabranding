#!/usr/bin/env python3
"""Replace <footer> blocks with the shared site footer snippet. Safe to re-run."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from site_footer_snippet import site_footer_html
from site_i18n import clean_path_from_file

FOOTER_RE = re.compile(r'<footer class="footer">.*?</footer>', re.DOTALL)
SWITCHER_RE = re.compile(r'<div class="lang-switch lang-switch--footer".*?</div>', re.DOTALL)
EXCLUDE_DIRS = {"preview", "partials", "ui_kits", "posts", "scripts", "assets", "js", "node_modules", "next", "scraps"}
FOOTER_STYLE_RE = re.compile(r'<style id="yb-footer-layout">.*?</style>\n?', re.DOTALL)


def footer_layout_css() -> str:
    css = (ROOT / "site.css").read_text(encoding="utf-8")
    start = css.index("/* footer-layout:start")
    end = css.index("/* footer-layout:end */")
    return css[css.index("*/", start) + 2:end].strip()


def with_footer_style(text: str, css: str) -> str:
    text = FOOTER_STYLE_RE.sub("", text)
    if "site.css" in text:
        return text
    return text.replace("</head>", f'<style id="yb-footer-layout">\n{css}\n</style>\n</head>', 1)


def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth


def is_public_page(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part.startswith(".") for part in rel.parts):
        return False
    if rel.parts[0] in EXCLUDE_DIRS:
        return False
    return True


def main() -> None:
    patched = 0
    skipped = 0
    css = footer_layout_css()
    for path in sorted(ROOT.rglob("*.html")):
        if not is_public_page(path):
            continue
        text = path.read_text(encoding="utf-8")
        m = FOOTER_RE.search(text)
        if not m:
            continue
        rel = path.relative_to(ROOT)
        lang = "es" if rel.parts[0] == "es" else "en"
        old_switcher = SWITCHER_RE.search(m.group(0))
        new_footer = site_footer_html(
            prefix_for(path),
            lang=lang,
            current_path=clean_path_from_file(path),
            switcher=old_switcher.group(0) if old_switcher else None,
        ).strip()
        updated = with_footer_style(text[: m.start()] + new_footer + text[m.end():], css)
        if updated == text:
            skipped += 1
            continue
        path.write_text(updated, encoding="utf-8")
        patched += 1

    print(f"patched {patched} footers ({skipped} unchanged)")


if __name__ == "__main__":
    main()
