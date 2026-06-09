"""HubSpot contact form embed for services/*.html pages."""

from typing import Optional

HS_PORTAL_ID = "243964841"
HS_REGION = "na2"
HS_EMBED_SCRIPT = f"https://js-na2.hsforms.net/forms/embed/{HS_PORTAL_ID}.js"
SERVICE_HS_FORM_ID = "6f398aa2-6690-4d5f-98e1-da96f49c633d"

SERVICE_SOURCE_LABELS = {
    "seo.html": "SEO Service Page",
    "google-ads.html": "Google Ads Service Page",
    "web-design.html": "Web Design Service Page",
    "social-media.html": "Social Media Service Page",
    "branding.html": "Branding Service Page",
    "content-creation.html": "Content Creation Service Page",
    "press-releases.html": "Press Releases Service Page",
}

SERVICE_THANK_YOU = {
    "seo.html": "thank-you-seo",
    "google-ads.html": "thank-you-google-ads",
    "web-design.html": "thank-you-web-design",
    "social-media.html": "thank-you-social-media",
    "branding.html": "thank-you-branding",
    "content-creation.html": "thank-you-content-creation",
    "press-releases.html": "thank-you-press-releases",
}


def service_thank_you_redirect(service_filename: str) -> str:
    return f"/services/{SERVICE_THANK_YOU.get(service_filename, 'thank-you-seo')}"


def service_hubspot_form_html(source: str, redirect: Optional[str] = None) -> str:
    redirect = redirect or "/thank-you"
    return f"""          <h3 style="font-size:20px;margin:0 0 20px">Send Us a Message</h3>
          <div class="yb-hs-form" data-source="{source}" data-redirect="{redirect}">
            <div class="hs-form-frame" data-region="{HS_REGION}" data-form-id="{SERVICE_HS_FORM_ID}" data-portal-id="{HS_PORTAL_ID}"></div>
          </div>
          <p class="yb-hs-form-footnote">We respond within 4 business hours. Your information is never shared.</p>"""
