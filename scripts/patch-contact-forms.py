#!/usr/bin/env python3
"""Add contact-forms.js and wrap legacy contact panels in yb-contact-form."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

CONTACT_FORM_WRAP = (
    '<h3 style="font-size:20px;margin:0 0 20px">Send Us a Message</h3>\n'
    '          <form class="yb-contact-form" action="#" method="post">\n'
    '          <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px">'
)
CONTACT_FORM_WRAP_OLD = (
    '<h3 style="font-size:20px;margin:0 0 20px">Send Us a Message</h3>\n'
    '          <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px">'
)
CONTACT_FORM_CLOSE = (
    '          <button type="submit" class="btn btn-grad" style="width:100%;justify-content:center;padding:15px;font-size:15px">Send Message'
)
CONTACT_FORM_CLOSE_OLD = (
    '          <button class="btn btn-grad" style="width:100%;justify-content:center;padding:15px;font-size:15px">Send Message'
)

CTA_FORM_OPEN = (
    '    <form class="yb-contact-form yb-cta-modal-form" action="#" method="post" '
    'style="padding:24px 28px 30px;display:grid;gap:14px">\n'
)
CTA_FORM_CLOSE = '      <button type="submit" class="btn btn-grad" style="width:100%;justify-content:center;padding:15px">Send Message</button>\n    </form>'

SCRIPT_TAG = '<script src="{prefix}js/contact-forms.js" defer></script>'


def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth


def inject_script(text: str, prefix: str) -> str:
    tag = SCRIPT_TAG.format(prefix=prefix)
    if "contact-forms.js" in text:
        return text
    if '<script src="' in text and "site.js" in text:
        return text.replace(
            f'<script src="{prefix}js/site.js"',
            f"{tag}\n<script src=\"{prefix}js/site.js\"",
            1,
        )
    return text.replace("</body>", f"{tag}\n</body>", 1)


def wrap_inline_contact_panels(text: str) -> str:
    if CONTACT_FORM_WRAP_OLD not in text:
        return text
    text = text.replace(CONTACT_FORM_WRAP_OLD, CONTACT_FORM_WRAP)
    text = text.replace(CONTACT_FORM_CLOSE_OLD, CONTACT_FORM_CLOSE)
    broken = (
        '          <button type="submit" class="btn btn-grad" style="width:100%;justify-content:center;padding:15px;font-size:15px">Send Message\n'
        "          </form>\n"
        '            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>\n'
        "          </button>"
    )
    fixed = (
        '          <button type="submit" class="btn btn-grad" style="width:100%;justify-content:center;padding:15px;font-size:15px">Send Message\n'
        '            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>\n'
        "          </button>\n"
        "          </form>"
    )
    text = text.replace(broken, fixed)
    # Close any form still missing </form> after a proper submit button
    if '<form class="yb-contact-form"' in text and broken not in text:
        needle = (
            '            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>\n'
            "          </button>\n"
            "        </div>"
        )
        replacement = needle.replace(
            "          </button>\n        </div>",
            "          </button>\n          </form>\n        </div>",
        )
        if needle in text and replacement not in text:
            text = text.replace(needle, replacement, 1)
    return text


def wrap_cta_modal(text: str) -> str:
    if 'id="ctaModal"' not in text or "yb-cta-modal-form" in text:
        return text
    old = (
        '    <div style="padding:24px 28px 30px;display:grid;gap:14px">\n'
        '      <div><label style="display:block;font-size:12.5px;font-weight:700;color:var(--fg2);margin-bottom:6px">Full Name</label>'
    )
    new = (
        '    <form class="yb-contact-form yb-cta-modal-form" action="#" method="post" '
        'style="padding:24px 28px 30px;display:grid;gap:14px">\n'
        '      <div><label style="display:block;font-size:12.5px;font-weight:700;color:var(--fg2);margin-bottom:6px">Full Name</label>'
    )
    if old in text:
        text = text.replace(old, new, 1)
        text = text.replace(
            '      <button class="btn btn-grad" style="width:100%;justify-content:center;padding:15px">Send Message</button>\n'
            "    </div>\n"
            "  </div>\n"
            "</div>",
            CTA_FORM_CLOSE + "\n  </div>\n</div>",
            1,
        )
    return text


def patch_contact_html(text: str) -> str:
    old = (
        '        <h3 style="font-size:22px;margin:0 0 24px;color:var(--ink)">Send Us a Message</h3>\n'
        "        <div style=\"display:grid;gap:16px\">"
    )
    new = (
        '        <h3 style="font-size:22px;margin:0 0 24px;color:var(--ink)">Send Us a Message</h3>\n'
        '        <form class="yb-contact-form" action="#" method="post" style="display:grid;gap:16px">'
    )
    if old in text and 'class="yb-contact-form"' not in text:
        text = text.replace(old, new, 1)
        text = text.replace(
            '          <button class="btn btn-grad" style="width:100%;justify-content:center;padding:15px;font-size:15px">\n'
            "            Send Message",
            '          <button type="submit" class="btn btn-grad" style="width:100%;justify-content:center;padding:15px;font-size:15px">\n'
            "            Send Message",
            1,
        )
        text = text.replace(
            '          <p style="font-size:12.5px;color:var(--fg3);text-align:center">We respond by the next business day. Your information is never shared.</p>\n'
            "        </div>",
            '          <p style="font-size:12.5px;color:var(--fg3);text-align:center">We respond by the next business day. Your information is never shared.</p>\n'
            "        </form>",
            1,
        )
    return text


def patch_index_html(text: str) -> str:
    text = text.replace(
        '<form id="contactForm" onsubmit="submitContactForm(event)" style="display:grid;gap:16px">',
        '<form id="contactForm" class="yb-contact-form" action="#" method="post" style="display:grid;gap:16px">',
    )
    old_modal = '    <div class="modal-form" id="modalForm">\n      <div class="field">'
    new_modal = (
        '    <form class="modal-form yb-contact-form" id="modalForm" action="#" method="post">\n'
        "      <div class=\"field\">"
    )
    if old_modal in text:
        text = text.replace(old_modal, new_modal, 1)
        text = text.replace(
            '      <button class="btn btn-grad" style="justify-content:center;width:100%" onclick="submitForm()">Send Message',
            '      <button type="submit" class="btn btn-grad" style="justify-content:center;width:100%">Send Message',
            1,
        )
        text = text.replace(
            "      </button>\n    </div>\n    <div class=\"modal-success\"",
            "      </button>\n    </form>\n    <div class=\"modal-success\"",
            1,
        )
    text = re.sub(
        r"function submitForm\(\) \{[^}]+\}\n",
        "",
        text,
    )
    text = text.replace(
        "function submitContactForm(e){e.preventDefault();document.getElementById('contactForm').style.display='none';document.getElementById('formSuccess').style.display='block';}",
        "",
    )
    return text


def main() -> None:
    patched = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if rel.parts[0] in {"preview", "partials", "ui_kits", "posts"}:
            continue
        text = path.read_text(encoding="utf-8")
        if "Send Message" not in text and 'id="contactForm"' not in text:
            continue
        original = text
        prefix = prefix_for(path)
        text = inject_script(text, prefix)
        if path.name == "index.html":
            text = patch_index_html(text)
        if path.name == "contact.html":
            text = patch_contact_html(text)
        text = wrap_inline_contact_panels(text)
        text = wrap_cta_modal(text)
        if text != original:
            path.write_text(text, encoding="utf-8")
            patched += 1
            print(f"patched {rel}")
    print(f"patched {patched} files")


if __name__ == "__main__":
    main()
