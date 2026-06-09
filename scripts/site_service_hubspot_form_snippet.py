"""HubSpot contact form embed for services/*.html pages."""

from typing import Optional

HS_PORTAL_ID = "243964841"
HS_REGION = "na2"
HS_EMBED_SCRIPT = f"https://js-na2.hsforms.net/forms/embed/{HS_PORTAL_ID}.js"
SERVICE_HS_FORM_ID = "6f398aa2-6690-4d5f-98e1-da96f49c633d"

SERVICE_SOURCE_LABELS = {
    "index.html": "Service Page",
    "seo.html": "SEO Service Page",
    "google-ads.html": "Google Ads Service Page",
    "web-design.html": "Web Design Service Page",
    "social-media.html": "Social Media Service Page",
    "branding.html": "Branding Service Page",
    "content-creation.html": "Content Creation Service Page",
    "press-releases.html": "Press Releases Service Page",
}

SERVICE_SOURCE_BY_FOLDER = {
    "seo": "SEO Service Page",
    "google-ads": "Google Ads Service Page",
    "web-design": "Web Design Service Page",
    "social-media": "Social Media Service Page",
    "branding": "Branding Service Page",
    "content-marketing": "Content Creation Service Page",
    "press-releases": "Press Releases Service Page",
}

SERVICE_THANK_YOU = {
    "seo": "thank-you-seo",
    "google-ads": "thank-you-google-ads",
    "web-design": "thank-you-web-design",
    "social-media": "thank-you-social-media",
    "branding": "thank-you-branding",
    "content-creation": "thank-you-content-creation",
    "content-marketing": "thank-you-content-creation",
    "press-releases": "thank-you-press-releases",
}


def service_thank_you_redirect(service_filename: str, folder: str = "") -> str:
    slug = folder or service_filename.replace(".html", "")
    thank_you = SERVICE_THANK_YOU.get(slug, "thank-you-seo")
    return f"/services/{thank_you}"


def service_hubspot_form_html(source: str, redirect: Optional[str] = None) -> str:
    redirect = redirect or "/thank-you"
    return f"""          <h3 style="font-size:20px;margin:0 0 20px">Send Us a Message</h3>
          <div class="yb-hs-form" data-source="{source}" data-redirect="{redirect}">
            <div class="hs-form-frame" data-region="{HS_REGION}" data-form-id="{SERVICE_HS_FORM_ID}" data-portal-id="{HS_PORTAL_ID}"></div>
          </div>
          <p class="yb-hs-form-footnote">We respond within 4 business hours. Your information is never shared.</p>"""
