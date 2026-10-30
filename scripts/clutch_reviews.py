"""Clutch reviews (many from encite, acquired by YB Marketing in January 2025)."""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLUTCH_URL = "https://clutch.co/profile/yb-marketing#reviews"
REVIEWS: list[dict] = json.loads((ROOT / "data" / "clutch-reviews.json").read_text(encoding="utf-8"))

STATE_ABBR = {"Colorado": "CO", "Illinois": "IL", "Washington": "WA", "Arizona": "AZ", "California": "CA", "Idaho": "ID"}
STAR = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'

T = {
    "en": {"via": "via encite, now YB Marketing", "verified": "Verified review", "read": "Read on Clutch"},
    "es": {"via": "vía encite, ahora YB Marketing", "verified": "Reseña verificada", "read": "Ver en Clutch"},
}

CSS = """
.cl-card{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:24px;box-shadow:var(--sh-md);display:flex;flex-direction:column}
.cl-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
.cl-verified{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--fg3)}
.cl-mark{font-family:var(--font-display);font-weight:800;font-size:13px;color:#17313B;letter-spacing:-.01em;text-decoration:none}
.cl-mark::before{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;background:#E62415;margin-right:5px;vertical-align:1px}
.cl-card blockquote{font-size:16px;line-height:1.55;color:var(--ink);margin:0 0 18px;flex:1;font-weight:600}
.cl-name{font-weight:700;font-size:14px;color:var(--ink)}
.cl-role{font-size:13px;color:var(--fg2);margin-top:2px}
.cl-loc{display:inline-flex;align-items:center;gap:5px;margin-top:10px;font-size:13px;font-weight:700;color:var(--yb-blue)}
.cl-loc svg{width:14px;height:14px}
.cl-via{display:block;font-size:11.5px;color:var(--fg3);margin-top:6px}
"""


def card(r: dict, lang: str = "en") -> str:
    t = T[lang]
    role = r["company"] if r["name"].startswith("Anonymous") else f'{r["title"]}, {r["company"]}'
    via = f'<span class="cl-via">{t["via"]}</span>' if r.get("via_encite") else ""
    return (
        f'<article class="cl-card"><div class="cl-top"><span class="cl-verified">{t["verified"]}</span>'
        f'<a class="cl-mark" href="{CLUTCH_URL}" target="_blank" rel="noopener" title="{t["read"]}">Clutch</a></div>'
        f'<blockquote>"{escape(r["quote"], quote=False)}"</blockquote>'
        f'<div><div class="cl-name">{escape(r["name"])}</div><div class="cl-role">{escape(role)}</div>'
        f'<span class="cl-loc">{PIN}{escape(r["city"])}, {escape(r["state"])}</span>{via}</div></article>'
    )


COORDS = {
    "Denver": (39.74, -104.99), "Aurora": (39.73, -104.83), "Delta": (38.74, -108.07), "Loveland": (40.40, -105.07),
    "Fort Collins": (40.59, -105.08), "Thornton": (39.87, -104.97), "Parker": (39.52, -104.76), "Lakewood": (39.70, -105.08),
    "Boulder": (40.01, -105.27), "Littleton": (39.61, -105.02), "Arvada": (39.80, -105.09), "Centennial": (39.58, -104.88),
    "Englewood": (39.65, -104.99),
}


PINNED = {"denver-co": ["Jade Cutler", "Greg Phelan", "James Iacino"]}


def for_location(city: str, state: str, seed: str = "", n: int = 3) -> list[dict]:
    """Closest reviews in the same state, named reviewers first; ties rotate by seed so nearby pages differ."""
    if seed in PINNED:
        return [next(r for r in REVIEWS if r["name"] == name) for name in PINNED[seed]][:n]
    abbr = STATE_ABBR.get(state, state)
    here = COORDS.get(city)
    pool = [r for r in REVIEWS if r["state"] == abbr]
    k = sum((i + 1) * ord(ch) for i, ch in enumerate(seed))

    def dist(r: dict) -> float:
        there = COORDS.get(r["city"])
        if r["city"] == city:
            return 0
        if not here or not there:
            return 999
        return round(((here[0] - there[0]) ** 2 + (here[1] - there[1]) ** 2) ** 0.5 * 69 / 10)

    return sorted(pool, key=lambda r: (dist(r), r["name"].startswith("Anonymous"), (REVIEWS.index(r) + k) % len(REVIEWS)))[:n]
