#!/usr/bin/env python3
"""Inject AccessiBe inline script at the top of <body> on all public pages."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SKIP_DIRS = {"preview", "partials", "ui_kits", "posts"}

from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT

ACCESSIBE_JS_RE = re.compile(
    r'\s*<script src="(?:\.\./)*js/accessibe\.js"></script>\s*',
    re.IGNORECASE,
)
EXISTING_INLINE_RE = re.compile(
    r'\s*<script>\s*\(function\(\)\{ var s = document\.createElement\(\'script\'\);.*?acsbJS\.init\(\{.*?\}\); \}; h\.appendChild\(s\); \}\)\(\);\s*</script>\s*',
    re.DOTALL,
)
BODY_OPEN_RE = re.compile(r"(<body[^>]*>)", re.IGNORECASE)


def inject_accessibe(text: str) -> str:
    text = ACCESSIBE_JS_RE.sub("\n", text)
    text = EXISTING_INLINE_RE.sub("\n", text)

    match = BODY_OPEN_RE.search(text)
    if not match:
        return text.replace("</body>", f"\n{ACCESSIBE_BODY_SCRIPT}\n</body>", 1)

    insert_at = match.end()
    following = text[insert_at : insert_at + 200]
    if "acsbapp.com/apps/app/dist/js/app.js" in following and "acsbJS.init" in following:
        return text

    return text[:insert_at] + f"\n{ACCESSIBE_BODY_SCRIPT}\n" + text[insert_at:]


def main() -> None:
    patched = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP_DIRS:
            continue
        original = path.read_text(encoding="utf-8")
        updated = inject_accessibe(original)
        if updated == original:
            continue
        path.write_text(updated, encoding="utf-8")
        patched += 1
        print(f"patched {rel}")
    print(f"patched {patched} files")


if __name__ == "__main__":
    main()
