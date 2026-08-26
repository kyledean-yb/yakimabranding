"""GoHighLevel webhook lead form HTML for YB Marketing static pages."""

from __future__ import annotations

import html
import re

INTEREST_OPTIONS = [
    ("web-design", "Web Design"),
    ("seo", "SEO"),
    ("google-ads", "Google Ads"),
    ("branding", "Branding & Design"),
    ("social-media", "Social Media"),
    ("content-marketing", "Content Marketing"),
    ("press-releases", "Press Releases"),
    ("video-animation", "Video Animation"),
    ("other", "Not sure / Other"),
]

DEFAULT_INTEREST_BY_SOURCE = {
    "SEO": "seo",
    "Google Ads": "google-ads",
    "Web Design": "web-design",
    "Social Media": "social-media",
    "Branding": "branding",
    "Content": "content-marketing",
    "Press": "press-releases",
    "Video": "video-animation",
}


def default_interest_for_source(source: str) -> str:
    for key, value in DEFAULT_INTEREST_BY_SOURCE.items():
        if key.lower() in source.lower():
            return value
    return ""


def _field_id(source: str, field: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", source.lower()).strip("-")[:24] or "lead"
    return f"yb-{slug}-{field}"


def interest_options_html(default: str = "") -> str:
    lines = [
        '<option value="" disabled'
        + ("" if default else " selected")
        + ">What are you interested in?</option>"
    ]
    for value, label in INTEREST_OPTIONS:
        selected = " selected" if value == default else ""
        lines.append(
            f'<option value="{html.escape(value)}"{selected}>{html.escape(label)}</option>'
        )
    return "\n".join(lines)


def lead_form_html(
    source: str,
    redirect: str = "/thank-you",
    *,
    submit_label: str = "Get Started Today",
    default_interest: str = "",
) -> str:
    interest_default = default_interest or default_interest_for_source(source)
    fid = lambda field: _field_id(source, field)
    src = html.escape(source)
    redir = html.escape(redirect)
    return f"""          <form class="yb-lead-form" action="#" method="post" data-source="{src}" data-redirect="{redir}" novalidate>
            <div class="yb-lead-form__row">
              <div class="yb-lead-form__field">
                <label for="{fid("name")}">Name *</label>
                <input id="{fid("name")}" name="name" type="text" autocomplete="name" required placeholder="Your name">
              </div>
              <div class="yb-lead-form__field">
                <label for="{fid("email")}">Email *</label>
                <input id="{fid("email")}" name="email" type="email" autocomplete="email" required placeholder="you@company.com">
              </div>
            </div>
            <div class="yb-lead-form__row">
              <div class="yb-lead-form__field">
                <label for="{fid("phone")}">Phone *</label>
                <input id="{fid("phone")}" name="phone" type="tel" autocomplete="tel" required placeholder="(509) 555-0100">
              </div>
              <div class="yb-lead-form__field">
                <label for="{fid("company")}">Company or URL</label>
                <input id="{fid("company")}" name="company" type="text" autocomplete="organization" placeholder="yourcompany.com">
              </div>
            </div>
            <div class="yb-lead-form__field">
              <label for="{fid("interest")}">I'm interested in *</label>
              <div class="yb-lead-form__select-wrap">
                <select id="{fid("interest")}" name="interest" required>
{interest_options_html(interest_default)}
                </select>
              </div>
            </div>
            <div class="yb-lead-form__field">
              <label for="{fid("message")}">How can we help?</label>
              <textarea id="{fid("message")}" name="message" rows="4" placeholder="Tell us about your goals…"></textarea>
            </div>
            <input type="hidden" name="source" value="{src}">
            <input type="hidden" name="page_url" value="">
            <button type="submit" class="btn btn-grad yb-lead-form__submit">{html.escape(submit_label)}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            </button>
            <p class="yb-lead-form__status" hidden aria-live="polite"></p>
          </form>
          <p class="yb-lead-form-footnote">We respond by the next business day. Your information is never shared.</p>"""


def lead_form_script_tags(prefix: str = "") -> str:
    return (
        f'<link rel="stylesheet" href="{prefix}lead-form.css">\n'
        f'<script src="{prefix}js/lead-form-config.js" defer></script>\n'
        f'<script src="{prefix}js/lead-form.js" defer></script>'
    )


def local_lead_form_html(source: str, redirect: str = "/thank-you") -> str:
    return lead_form_html(source, redirect)


def service_lead_form_html(source: str, redirect: str = "/thank-you") -> str:
    return lead_form_html(source, redirect)
