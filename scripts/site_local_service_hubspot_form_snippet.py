"""Contact form embed for localized service / location pages (GoHighLevel webhook)."""

from site_lead_form_snippet import lead_form_script_tags, local_lead_form_html

LOCAL_HS_FORM_PLACEHOLDER = "__LOCAL_HS_FORM__"


def location_thank_you_redirect(slug: str, *, from_locations_dir: bool = False) -> str:
    if from_locations_dir:
        return f"/locations/thank-you-{slug}"
    return f"/locations/thank-you-{slug}"


def local_hubspot_form_html(
    source: str,
    redirect: str = "/thank-you",
) -> str:
    return local_lead_form_html(source, redirect)


def hubspot_script_tags(prefix: str) -> str:
    return lead_form_script_tags(prefix)

