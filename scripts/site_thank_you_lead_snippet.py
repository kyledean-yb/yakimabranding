"""Consent-gated lead conversion events for thank-you pages."""


def thank_you_lead_script_html(prefix: str) -> str:
    return f'<script src="{prefix}js/thank-you-lead.js" defer></script>'
