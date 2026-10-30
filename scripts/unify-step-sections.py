#!/usr/bin/env python3
"""Convert older step by step sections to the shared numbered timeline (.timeline in site.css).

Safe to run repeatedly. Handles English and Spanish pages.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"preview", "ui_kits", "partials", "scraps", "node_modules", "next", "_next", "emails", ".git"}

TAG = r"<{t}\b[^>]*>"


ACRONYMS = {"SEO", "PPC", "AI", "CRM", "ROI", "GBP", "URL", "UX", "SMS", "Y", "LSA"}
SMALL = {"a", "an", "and", "the", "of", "to", "for", "in", "on", "at", "by", "with", "that", "y", "de", "del", "la", "el", "en", "para", "con", "que", "los", "las", "un", "una"}


def fix_caps(title: str) -> str:
    letters = [c for c in re.sub(r"&\w+;", "", title) if c.isalpha()]
    if not letters or any(c.islower() for c in letters):
        return title
    words = title.split(" ")
    out = []
    for i, w in enumerate(words):
        core = w.strip("&;,.:")
        if core in ACRONYMS and core != "Y":
            out.append(w)
        elif i and core.lower() in SMALL:
            out.append(w.lower())
        else:
            out.append(w[:1] + w[1:].lower() if not w.startswith("&") else w.lower())
    return " ".join(out)


def li(n: int, title: str, body: str, when: str = "") -> str:
    when_html = f'<span class="timeline-when">{when}</span>' if when else ""
    return f'      <li><span class="timeline-n">{n}</span>{when_html}<h3>{fix_caps(title.strip())}</h3>{body.strip()}</li>'


def fix_existing_caps(html: str) -> str:
    return re.sub(
        r'(<li><span class="timeline-n">\d+</span>(?:<span class="timeline-when">.*?</span>)?<h3>)(.*?)(</h3>)',
        lambda m: m.group(1) + fix_caps(m.group(2)) + m.group(3),
        html,
    )


def timeline(items: list[str], indent: str = "    ") -> str:
    return f'<ol class="timeline" style="--steps:{len(items)}">\n' + "\n".join(items) + f"\n{indent}</ol>"


CARD = re.compile(
    r'<div style="background:#fff;border-radius:var\(--r-lg\);padding:28px;border:1px solid var\(--line\);box-shadow:0 2px 8px rgba\(22,32,58,\.05\)">\s*'
    r"<h3[^>]*>(.*?)</h3>\s*(<p[^>]*>.*?</p>)\s*</div>",
    re.S,
)


def strip_attrs(p: str) -> str:
    return re.sub(r"<p\b[^>]*>", "<p>", p)


def convert_process_tiles(html: str) -> str:
    """City service pages: three plain cards under <!-- PROCESS -->."""
    start = html.find("<!-- PROCESS -->")
    if start < 0:
        return html
    end = html.find("<!--", start + 5)
    end = len(html) if end < 0 else end
    block = html[start:end]
    m = re.search(r'<div\b[^>]*class="why-tiles-grid"[^>]*>(.*?)</div>\s*</div>\s*</section>', block, re.S)
    if not m:
        return html
    cards = CARD.findall(m.group(1))
    if not cards:
        return html
    items = [li(i, t, strip_attrs(p)) for i, (t, p) in enumerate(cards, 1)]
    new_inner = timeline(items) + "\n  </div>\n</section>"
    block = block[: m.start()] + new_inner + block[m.end():]
    return html[:start] + block + html[end:]


def convert_seo_steps(html: str) -> str:
    m = re.search(r'<ol class="seo-steps"[^>]*>(.*?)</ol>', html, re.S)
    if not m:
        return html
    items = []
    for i, step in enumerate(re.findall(r'<li class="seo-step">(.*?)</li>', m.group(1), re.S), 1):
        when = re.search(r'<span class="seo-step-when">(.*?)</span>', step, re.S)
        title = re.search(r"<h3>(.*?)</h3>", step, re.S)
        paras = "".join(re.findall(r"<p>.*?</p>", step, re.S))
        items.append(li(i, title.group(1), paras, when.group(1) if when else ""))
    return html[: m.start()] + timeline(items) + html[m.end():]


def convert_simple(html: str, wrap_cls: str, item_cls: str, num_cls: str) -> str:
    m = re.search(rf'<div class="{wrap_cls}">(.*?</div>)\s*</div>(?=\s*(?:</div>|<h2))', html, re.S)
    if not m:
        return html
    steps = re.findall(
        rf'<div class="{item_cls}"><div class="{num_cls}">[^<]*</div><h3>(.*?)</h3>(<p>.*?</p>)</div>',
        m.group(1), re.S,
    )
    if not steps:
        return html
    items = [li(i, t, p) for i, (t, p) in enumerate(steps, 1)]
    return html[: m.start()] + timeline(items) + "\n" + html[m.end():]


def convert_thank_you(html: str) -> str:
    m = re.search(r'<div class="ty-steps-grid">(.*?)</div>\s*</div>\s*</section>', html, re.S)
    if not m:
        return html
    steps = re.findall(
        r'<div class="ty-step">\s*<div class="ty-step-ic"[^>]*>.*?</div>\s*<h3>(.*?)</h3>\s*(<p>.*?</p>)\s*</div>',
        m.group(1), re.S,
    )
    if not steps:
        return html
    items = [li(i, t, p.replace(" — ", ", ").replace(" —", ",")) for i, (t, p) in enumerate(steps, 1)]
    return html[: m.start()] + timeline(items) + "\n  </div>\n</section>" + html[m.end():]


def main() -> None:
    changed = 0
    for path in ROOT.rglob("*.html"):
        if SKIP & set(path.relative_to(ROOT).parts):
            continue
        html = path.read_text(encoding="utf-8")
        new = convert_process_tiles(html)
        new = convert_seo_steps(new)
        new = convert_simple(new, "steps", "step", "step-num")
        new = convert_simple(new, "team-steps", "team-step", "team-step-num")
        new = convert_thank_you(new)
        new = fix_existing_caps(new)
        new = new.replace("<h3>Campaign Estrategia y Configuración</h3>", "<h3>Estrategia y configuración de campañas</h3>")
        new = new.replace("<h3>SEO Auditoría del sitio</h3>", "<h3>Auditoría SEO del sitio</h3>")
        if new != html:
            path.write_text(new, encoding="utf-8")
            changed += 1
    print(f"unified step sections on {changed} pages")


if __name__ == "__main__":
    main()
