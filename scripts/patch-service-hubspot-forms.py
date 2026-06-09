#!/usr/bin/env python3
"""Replace placeholder contact forms on main service pages with HubSpot embed."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from site_service_hubspot_form_snippet import (
    HS_EMBED_SCRIPT,
    SERVICE_SOURCE_BY_FOLDER,
    service_hubspot_form_html,
    service_thank_you_redirect,
)

SERVICE_DIRS = [
    "seo",
    "google-ads",
    "web-design",
    "social-media",
    "branding",
    "content-marketing",
    "press-releases",
]

CONTACT_CARD_FORM_RE = re.compile(
    r'\s*<h3 style="font-size:20px;margin:0 0 20px">Send Us a Message</h3>\s*'
    r'(?:<form class="yb-contact-form" action="#" method="post">.*?</form>|'
    r'<div class="yb-hs-form"[^>]*>\s*'
    r'<div class="hs-form-frame"[^>]*></div>\s*'
    r'</div>\s*'
    r'<p class="yb-hs-form-footnote">[^<]*</p>)',
    re.DOTALL,
)


def inject_hubspot_scripts(text: str, prefix: str) -> str:
    hubspot_js = f'<script src="{prefix}js/hubspot-form.js"></script>'
    embed_js = f'<script src="{HS_EMBED_SCRIPT}" defer></script>'
    if hubspot_js in text and embed_js in text:
        return text
    if f'<script src="{prefix}js/contact-forms.js"' in text:
        return text.replace(
            f'<script src="{prefix}js/contact-forms.js"',
            f"{hubspot_js}\n{embed_js}\n<script src=\"{prefix}js/contact-forms.js\"",
            1,
        )
    if f'<script src="{prefix}js/site.js"' in text:
        return text.replace(
            f'<script src="{prefix}js/site.js"',
            f"{hubspot_js}\n{embed_js}\n<script src=\"{prefix}js/site.js\"",
            1,
        )
    return text.replace("</body>", f"{hubspot_js}\n{embed_js}\n</body>", 1)


def patch_service_page(path: Path, folder: str) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    source = SERVICE_SOURCE_BY_FOLDER.get(folder, f"{folder.replace('-', ' ').title()} Service Page")
    redirect = service_thank_you_redirect(path.name, folder=folder)
    form_html = service_hubspot_form_html(source, redirect=redirect)

    if not CONTACT_CARD_FORM_RE.search(text):
        return False

    text = CONTACT_CARD_FORM_RE.sub("\n" + form_html, text, count=1)
    text = inject_hubspot_scripts(text, "../")
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    patched = 0
    for folder in SERVICE_DIRS:
        path = ROOT / folder / "index.html"
        if not path.exists():
            continue
        if patch_service_page(path, folder):
            patched += 1
            print(f"patched {folder}/index.html")
    print(f"patched {patched} service pages")


if __name__ == "__main__":
    main()
