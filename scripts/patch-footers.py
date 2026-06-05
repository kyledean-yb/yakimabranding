#!/usr/bin/env python3
"""Replace <footer> blocks with the shared site footer snippet."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from site_footer_snippet import site_footer_html

FOOTER_RE = re.compile(r'<footer class="footer">.*?</footer>', re.DOTALL)
EXCLUDE_DIRS = {"preview", "partials", "ui_kits", "posts", "scripts", "assets", "js", "node_modules"}


def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth


def is_public_page(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part.startswith(".") for part in rel.parts):
        return False
    if rel.parts[0] in EXCLUDE_DIRS:
        return False
    return True


def main() -> None:
    patched = 0
    skipped = 0
    for path in sorted(ROOT.rglob("*.html")):
        if not is_public_page(path):
            continue
        text = path.read_text(encoding="utf-8")
        if not FOOTER_RE.search(text):
            continue
        prefix = prefix_for(path)
        new_footer = site_footer_html(prefix).strip()
        updated, n = FOOTER_RE.subn(new_footer, text, count=1)
        if n != 1:
            skipped += 1
            print(f"skip {path.relative_to(ROOT)}: footer not replaced ({n})")
            continue
        path.write_text(updated, encoding="utf-8")
        patched += 1
        print(f"patched {path.relative_to(ROOT)}")

    print(f"patched {patched} footers ({skipped} skipped)")


if __name__ == "__main__":
    main()
