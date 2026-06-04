#!/usr/bin/env python3
"""Replace <footer> blocks with the shared homepage footer (no WP fetch)."""

import re
from pathlib import Path

from site_footer_snippet import site_footer_html

ROOT = Path(__file__).resolve().parents[1]
FOOTER_RE = re.compile(r"<footer class=\"footer\">.*?</footer>", re.DOTALL)

TARGETS = [
    (ROOT / "insights.html", ""),
    *[(p, "../../") for p in (ROOT / "blog" / "posts").glob("*.html")],
]


def main():
    for path, prefix in TARGETS:
        text = path.read_text(encoding="utf-8")
        new_footer = site_footer_html(prefix).strip()
        updated, n = FOOTER_RE.subn(new_footer, text, count=1)
        if n != 1:
            print(f"skip {path.name}: footer not found ({n})")
            continue
        path.write_text(updated, encoding="utf-8")
        print(f"patched {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
