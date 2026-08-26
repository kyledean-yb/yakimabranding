#!/usr/bin/env python3
"""Replace HubSpot embed forms with GoHighLevel webhook lead forms sitewide."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from site_lead_form_snippet import lead_form_html, lead_form_script_tags

HS_FORM_BLOCK_RE = re.compile(
    r'<div class="yb-hs-form"[^>]*data-source="([^"]*)"[^>]*data-redirect="([^"]*)"[^>]*>\s*'
    r'<div class="hs-form-frame"[^>]*></div>\s*</div>\s*'
    r'<p class="yb-hs-form-footnote">[^<]*</p>',
    re.DOTALL,
)

HS_FORM_BLOCK_RE_ALT = re.compile(
    r'<div class="yb-hs-form"[^>]*data-redirect="([^"]*)"[^>]*data-source="([^"]*)"[^>]*>\s*'
    r'<div class="hs-form-frame"[^>]*></div>\s*</div>\s*'
    r'<p class="yb-hs-form-footnote">[^<]*</p>',
    re.DOTALL,
)

HUBSPOT_SCRIPTS_RE = re.compile(
    r'<script src="[^"]*hubspot-form\.js" defer></script>\s*'
    r'<script src="https://js-na2\.hsforms\.net/forms/embed/243964841\.js" defer></script>\s*',
    re.MULTILINE,
)

LEAD_CSS_RE = re.compile(r'<link rel="stylesheet" href="[^"]*lead-form\.css">\s*')
LEAD_SCRIPTS_RE = re.compile(
    r'<script src="[^"]*lead-form-config\.js" defer></script>\s*'
    r'<script src="[^"]*lead-form\.js" defer></script>\s*',
    re.MULTILINE,
)


def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "/" if depth == 0 else "../" * depth


def replace_hs_block(match: re.Match[str], source_idx: int, redirect_idx: int) -> str:
    source = match.group(source_idx)
    redirect = match.group(redirect_idx)
    submit = "Send Message" if "Contact" in source or "Profile" in source else "Get Started Today"
    return lead_form_html(source, redirect, submit_label=submit)


def inject_lead_assets(text: str, prefix: str) -> str:
    assets = lead_form_script_tags(prefix)
    if "lead-form.js" in text:
        return text
    text = HUBSPOT_SCRIPTS_RE.sub("", text)
    if f'<script src="{prefix}js/site.js"' in text:
        return text.replace(
            f'<script src="{prefix}js/site.js"',
            f"{assets}\n<script src=\"{prefix}js/site.js\"",
            1,
        )
    if "</body>" in text:
        return text.replace("</body>", f"{assets}\n</body>", 1)
    return text


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "hs-form-frame" not in text and "hubspot-form.js" not in text:
        return False
    original = text

    def sub_primary(m: re.Match[str]) -> str:
        return replace_hs_block(m, 1, 2)

    def sub_alt(m: re.Match[str]) -> str:
        return replace_hs_block(m, 2, 1)

    text = HS_FORM_BLOCK_RE.sub(sub_primary, text)
    text = HS_FORM_BLOCK_RE_ALT.sub(sub_alt, text)
    text = inject_lead_assets(text, prefix_for(path))

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    patched = 0
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in path.parts for part in ("preview", "ui_kits", "posts", "node_modules", "next")):
            continue
        if patch_file(path):
            patched += 1
            print(f"patched {path.relative_to(ROOT)}")
    print(f"patched {patched} files")


if __name__ == "__main__":
    main()
