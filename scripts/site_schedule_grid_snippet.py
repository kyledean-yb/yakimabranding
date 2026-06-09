#!/usr/bin/env python3
"""Reusable team schedule grid HTML for contact, home, and service pages."""

from __future__ import annotations

import html

TEAM_SCHEDULE = [
    {
        "name": "Jacob Ross",
        "short": "Jacob",
        "slug": "jacob",
        "calendly": "https://calendly.com/jacobybmarketing",
        "photo": "jacob-headshot.webp",
    },
    {
        "name": "Kristin Sparling",
        "short": "Kristin",
        "slug": "kristin",
        "calendly": "https://calendly.com/kristin-sparling/connect",
        "photo": "kristin-headshot.webp",
    },
    {
        "name": "Kevin Dean",
        "short": "Kevin",
        "slug": "kevin",
        "calendly": "https://calendly.com/kdean-wsi",
        "photo": "kevin-headshot.webp",
    },
    {
        "name": "Sophie Mann",
        "short": "Sophie",
        "slug": "sophie",
        "calendly": "https://calendly.com/sophie-yakimabranding/30min",
        "photo": "sophie-headshot.webp",
    },
]


def schedule_card_html(member: dict, prefix: str, indent: str = "          ") -> str:
    asset = f"{prefix}assets/{member['photo']}"
    about = f"{prefix}about/{member['slug']}.html"
    name = html.escape(member["name"])
    meet = html.escape(f"Meet {member['short']}")
    calendly = html.escape(member["calendly"])
    return f"""{indent}<div class="yb-schedule-card yb-schedule-card--split">
{indent}  <img src="{asset}" alt="{name}" class="yb-schedule-card__photo" width="64" height="64" loading="lazy">
{indent}  <span class="yb-schedule-card__info">
{indent}    <span class="yb-schedule-card__name">{name}</span>
{indent}    <a href="{calendly}" target="_blank" rel="noopener noreferrer" class="yb-schedule-card__cta">Schedule Call</a>
{indent}    <a href="{about}" class="yb-schedule-card__meet">{meet}</a>
{indent}  </span>
{indent}</div>"""


def schedule_grid_html(prefix: str, indent: str = "        ") -> str:
    cards = "\n".join(schedule_card_html(m, prefix, indent + "  ") for m in TEAM_SCHEDULE)
    return f"""{indent}<p class="yb-schedule-intro">Choose who you'd like to meet with</p>
{indent}<div class="yb-schedule-grid">
{cards}
{indent}</div>"""


def schedule_intro_header_html(compact: bool = False) -> str:
    if compact:
        return """          <div style="text-align:center;padding-bottom:22px;border-bottom:1px solid var(--line);margin-bottom:22px">
            <div style="width:52px;height:52px;background:var(--grad-brand);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 10px;font-family:var(--font-display);font-weight:800;font-size:20px;color:#fff">YB</div>
            <div style="font-size:12px;font-weight:600;color:var(--fg3);margin-bottom:4px">YB Marketing Team</div>
            <div style="font-weight:700;font-size:17px;color:var(--ink);margin-bottom:6px">Introduction Meeting</div>
            <div style="display:inline-flex;align-items:center;gap:6px;font-size:13px;color:var(--fg3);background:#fff;border-radius:var(--r-pill);padding:5px 12px;border:1px solid var(--line)">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              30 min · Free
            </div>
            <p style="font-size:13px;color:var(--fg2);margin-top:14px;line-height:1.6">An introduction meeting to learn more about your business, your goals, and how we can help you grow. No commitment required.</p>
          </div>"""
    return """        <div style="text-align:center;padding-bottom:22px;border-bottom:1px solid var(--line);margin-bottom:22px">
          <div style="width:56px;height:56px;background:var(--grad-brand);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 12px;font-family:var(--font-display);font-weight:800;font-size:22px;color:#fff">YB</div>
          <div style="font-size:12px;font-weight:600;color:var(--fg3);margin-bottom:4px">YB Marketing Team</div>
          <div style="font-weight:700;font-size:18px;color:var(--ink);margin-bottom:6px">Introduction Meeting</div>
          <div style="display:inline-flex;align-items:center;gap:6px;font-size:13px;color:var(--fg3);background:#fff;border-radius:var(--r-pill);padding:5px 12px;border:1px solid var(--line)">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            30 min · Free
          </div>
          <p style="font-size:13.5px;color:var(--fg2);margin-top:14px;line-height:1.6">An introduction meeting to learn more about your business, your goals, and how we can help you grow. No commitment required.</p>
        </div>"""


def service_schedule_panel_html(prefix: str = "../") -> str:
    header = schedule_intro_header_html(compact=True)
    grid = schedule_grid_html(prefix, indent="          ")
    return f"""{header}
{grid}"""


def thank_you_calendly_section_html(prefix: str = "") -> str:
    """Calendly booking section for thank-you pages (team schedule grid)."""
    header = schedule_intro_header_html(compact=False).replace("\n        ", "\n      ")
    grid = schedule_grid_html(prefix, indent="      ")
    return f"""<section class="ty-calendly" id="book">
  <div class="container" style="text-align:center">
    <h2 style="font-size:clamp(1.6rem,2.4vw,2rem);margin:0 0 12px">Don't Want to Wait? Book a Meeting Now.</h2>
    <p class="yb-lead" style="max-width:560px;margin:0 auto 36px">Schedule your free 30-minute introduction call directly — no forms, no back and forth.</p>
    <div class="ty-calendly-card ty-calendly-card--schedule">
{header}
{grid}
    </div>
  </div>
</section>"""
