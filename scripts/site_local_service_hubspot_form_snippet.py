"""HubSpot contact form embed for localized service / location pages."""

import html

HS_PORTAL_ID = "243964841"
HS_REGION = "na2"
HS_EMBED_SCRIPT = f"https://js-na2.hsforms.net/forms/embed/{HS_PORTAL_ID}.js"
LOCAL_HS_FORM_ID = "485886f4-f11a-41e9-8311-ed6c5f3f2c68"

LOCAL_HS_FORM_PLACEHOLDER = "__LOCAL_HS_FORM__"


def location_thank_you_redirect(slug: str, *, from_locations_dir: bool = False) -> str:
    if from_locations_dir:
        return f"/locations/thank-you-{slug}"
    return f"/locations/thank-you-{slug}"


def local_hubspot_form_html(
    source: str,
    redirect: str = "/thank-you",
) -> str:
    return f"""          <div class="yb-hs-form" data-source="{html.escape(source)}" data-redirect="{html.escape(redirect)}">
            <div class="hs-form-frame" data-region="{HS_REGION}" data-form-id="{LOCAL_HS_FORM_ID}" data-portal-id="{HS_PORTAL_ID}"></div>
          </div>
          <p class="yb-hs-form-footnote">We respond by the next business day. Your information is never shared.</p>"""


def hubspot_script_tags(prefix: str) -> str:
    return (
        f'<script src="{prefix}js/hubspot-form.js" defer></script>\n'
        f'<script src="{HS_EMBED_SCRIPT}" defer></script>'
    )
