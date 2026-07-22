"""Service FAQ blocks for location hub pages."""

from __future__ import annotations

import html
import json

from site_urls import page_href

FAQ_ICON = (
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/>'
    '<line x1="5" y1="12" x2="19" y2="12"/></svg>'
)

FAQ_CSS = """
.faq-item{border-bottom:1px solid var(--line)}
.faq-q{display:flex;justify-content:space-between;align-items:center;padding:20px 0;cursor:pointer;font-weight:700;font-size:15.5px;color:var(--ink);gap:16px;background:none;border:none;width:100%;text-align:left;font-family:var(--font-body);transition:color 200ms}
.faq-q:hover{color:var(--yb-blue)}
.faq-q.active{color:var(--faq-ac,var(--yb-blue))}
.faq-icon{width:28px;height:28px;border-radius:50%;background:var(--bg-mute);display:flex;align-items:center;justify-content:center;flex:none;transition:background 200ms,transform 200ms;color:var(--fg2)}
.faq-q.active .faq-icon{background:var(--faq-ac,var(--yb-blue));color:#fff;transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height 320ms cubic-bezier(.16,1,.3,1)}
.faq-a-inner{padding-bottom:20px;font-size:15px;color:var(--fg2);line-height:1.75}
.faq-a-inner a{color:var(--yb-blue);font-weight:700;text-decoration:underline;text-underline-offset:2px}
.faq-a-inner a:hover{color:var(--yb-blue-600)}
"""

FAQ_JS = """
function toggleFaq(id, accent) {
  var item = document.getElementById(id);
  if (!item) return;
  var btn = item.querySelector('.faq-q');
  var panel = item.querySelector('.faq-a');
  var isOpen = btn.classList.contains('active');
  document.querySelectorAll('.faq-q.active').forEach(function(b) {
    b.classList.remove('active');
    b.closest('.faq-item').querySelector('.faq-a').style.maxHeight = null;
    b.closest('.faq-item').style.removeProperty('--faq-ac');
  });
  if (!isOpen) {
    btn.classList.add('active');
    item.style.setProperty('--faq-ac', accent || 'var(--yb-blue)');
    panel.style.maxHeight = panel.scrollHeight + 'px';
  }
}
"""

SERVICE_FAQS = [
    {
        "folder": "seo",
        "label": "SEO",
        "accent": "#2BC4F0",
        "question": "Do you offer SEO in {place}?",
        "answer": (
            "Yes. YB Marketing provides local SEO for {place} businesses — including Google Business "
            "Profile optimization, local keyword targeting, technical SEO, and content that helps you "
            "rank in search and Maps."
        ),
    },
    {
        "folder": "google-ads",
        "label": "Google Ads",
        "accent": "#FF6B57",
        "question": "Do you manage Google Ads in {place}?",
        "answer": (
            "Yes. We manage Google Ads campaigns for {place} businesses with keyword strategy, "
            "conversion tracking, and ongoing optimization so your ad spend reaches the right local customers."
        ),
    },
    {
        "folder": "web-design",
        "label": "Web Design",
        "accent": "#159468",
        "question": "Do you design websites for businesses in {place}?",
        "answer": (
            "Yes. We build custom, mobile-ready websites for {place} businesses that are fast, "
            "SEO-friendly, and designed to convert visitors into leads."
        ),
    },
    {
        "folder": "social-media",
        "label": "Social Media",
        "accent": "#c77f12",
        "question": "Do you provide social media management in {place}?",
        "answer": (
            "Yes. Our team creates and manages social content that reflects {city}'s local market "
            "and helps {place} businesses build engagement and brand awareness."
        ),
    },
    {
        "folder": "branding",
        "label": "Branding",
        "accent": "#7B5BE6",
        "question": "Do you offer branding services in {place}?",
        "answer": (
            "Yes. We develop brand identities — logos, visual systems, and messaging — built for "
            "{place} businesses that want to stand out in their market."
        ),
    },
]


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def place_label(city: str, state: str) -> str:
    return f"{city}, {state}"


def location_service_faqs(city: str, state: str, slug: str) -> list[dict]:
    """Return FAQ items with plain-text answers (for schema) and HTML answers (for page)."""
    place = place_label(city, state)
    items = []
    for svc in SERVICE_FAQS:
        href = page_href(f"{svc['folder']}/{slug}.html")
        link_label = f"{svc['label']} in {place}"
        answer_plain = svc["answer"].format(place=place, city=city)
        answer_html = (
            f"{esc(answer_plain)} "
            f'<a href="{esc(href)}">Learn more about {esc(link_label)}</a>.'
        )
        items.append(
            {
                "q": svc["question"].format(place=place, city=city),
                "a": f"{answer_plain} Learn more about {link_label}: https://yakimabranding.com{href}",
                "a_html": answer_html,
                "href": href,
                "label": link_label,
                "accent": svc["accent"],
                "folder": svc["folder"],
            }
        )
    return items


def render_faq_items(faqs: list[dict], slug: str) -> str:
    blocks = []
    for i, faq in enumerate(faqs, start=1):
        fid = f"{slug}-faq-{i}"
        blocks.append(
            f"""      <div class="faq-item" id="{fid}">
        <button class="faq-q" type="button" onclick="toggleFaq('{fid}', '{faq['accent']}')">
          {esc(faq["q"])}
          <span class="faq-icon">{FAQ_ICON}</span>
        </button>
        <div class="faq-a"><div class="faq-a-inner">{faq["a_html"]}</div></div>
      </div>"""
        )
    return "\n".join(blocks)


def render_faq_section(city: str, state: str, slug: str) -> str:
    place = place_label(city, state)
    faqs = location_service_faqs(city, state, slug)
    return f"""
<!-- LOCATION SERVICE FAQ -->
<section style="background:#fff" id="faq" data-location-faq="1">
  <div class="container">
    <div style="text-align:center;max-width:700px;margin:0 auto 48px">
      <span class="eyebrow" style="color:var(--yb-blue)">Common Questions</span>
      <h2 style="margin:14px 0 14px">{esc(place)} Digital Marketing — Frequently Asked Questions</h2>
      <p style="color:var(--fg2);font-size:16px;line-height:1.75">Answers about our SEO, Google Ads, web design, social media, and branding services in {esc(place)}.</p>
    </div>
    <div style="max-width:760px;margin:0 auto;border-top:1px solid var(--line)">
{render_faq_items(faqs, slug)}
    </div>
  </div>
</section>
"""


def faq_schema_script(city: str, state: str, slug: str) -> str:
    faqs = location_service_faqs(city, state, slug)
    schema = {
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
    return (
        '<script type="application/ld+json">'
        + json.dumps(schema, ensure_ascii=False)
        + "</script>"
    )
