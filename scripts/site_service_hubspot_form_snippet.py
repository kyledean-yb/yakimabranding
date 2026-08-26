"""Contact form embed for service hub pages (GoHighLevel webhook)."""

from typing import Optional

from site_lead_form_snippet import service_lead_form_html

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
    return service_lead_form_html(source, redirect)
