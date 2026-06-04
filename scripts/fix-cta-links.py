#!/usr/bin/env python3
"""Point Get Started / CTA buttons to contact.html; fix Learn More service links."""

import re
from pathlib import Path
from typing import List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

CTA_MODAL_ONCLICK = "document.getElementById('ctaModal').classList.add('open')"
OPEN_MODAL_ONCLICK = "openModal()"


def button_to_link(html: str, contact_href: str) -> str:
    """Convert <button ... onclick=ctaModal/openModal> to <a href=contact>."""

    def repl(match: re.Match) -> str:
        tag = match.group(1)
        attrs = match.group(2) or ""
        content = match.group(3)
        classes = ""
        m_cls = re.search(r'class="([^"]*)"', tag + attrs)
        if m_cls:
            classes = m_cls.group(1)
        extra = ""
        m_style = re.search(r'style="([^"]*)"', attrs)
        if m_style:
            extra = f' style="{m_style.group(1)}"'
        return f'<a href="{contact_href}" class="{classes}"{extra}>{content}</a>'

    pattern = (
        r"<button\s+([^>]*?)"
        r"(?:onclick=\"(?:"
        + re.escape(CTA_MODAL_ONCLICK)
        + r"|"
        + re.escape(OPEN_MODAL_ONCLICK)
        + r"(?:;closeMobile\(\))?)\")"
        r"([^>]*)>(.*?)</button>"
    )
    return re.sub(pattern, repl, html, flags=re.DOTALL | re.IGNORECASE)


def fix_file(path: Path, contact_href: str, extra: Optional[List[Tuple[str, str]]] = None) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    text = button_to_link(text, contact_href)
    for old, new in extra or []:
        text = text.replace(old, new)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    changed = []

    index_extra = [
        ('<a class="logo" href="#">', '<a class="logo" href="index.html">'),
        ('<a href="#">Home</a>', '<a href="index.html" class="nav-a">Home</a>'),
        (
            '<a href="contact.html" class="svc-link" style="color:var(--yb-violet)">Learn More',
            '<a href="services/web-design.html" class="svc-link" style="color:var(--yb-violet)">Learn More',
        ),
        ('<a href="#contact" class="btn btn-grad">Work With Us', '<a href="contact.html" class="btn btn-grad">Work With Us'),
    ]
    if fix_file(ROOT / "index.html", "contact.html", index_extra):
        changed.append("index.html")

    if fix_file(ROOT / "about.html", "contact.html"):
        changed.append("about.html")

    for path in (ROOT / "services").glob("*.html"):
        if fix_file(path, "../contact.html"):
            changed.append(path.name)

    for path in changed:
        print(f"  · {path}")
    if not changed:
        print("No files changed.")


if __name__ == "__main__":
    main()
