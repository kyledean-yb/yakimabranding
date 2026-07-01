#!/usr/bin/env python3
"""Inject sitewide tracking snippets into all public HTML pages."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from site_tracking_snippet import (
    ATTRIBUTER_END,
    ATTRIBUTER_FOOTER_BLOCK,
    ATTRIBUTER_START,
    GTM_BODY_END,
    GTM_BODY_NOSCRIPT_BLOCK,
    GTM_BODY_START,
    TRACKING_HEAD_BLOCK,
    TRACKING_HEAD_END,
    TRACKING_HEAD_START,
)

SKIP_DIRS = {"preview", "partials", "ui_kits", "posts"}

MARKER_BLOCK_RE = re.compile(
    r"<!-- yb-(?:tracking-head|gtm-body|attributer)-start -->.*?<!-- yb-(?:tracking-head|gtm-body|attributer)-end -->\s*",
    re.DOTALL,
)
HEAD_CLOSE_RE = re.compile(r"</head>", re.IGNORECASE)
BODY_OPEN_RE = re.compile(r"(<body[^>]*>)", re.IGNORECASE)
BODY_CLOSE_RE = re.compile(r"</body>", re.IGNORECASE)


def strip_markers(text: str) -> str:
    return MARKER_BLOCK_RE.sub("", text)


def inject_head(text: str) -> str:
    if TRACKING_HEAD_START in text:
        text = re.sub(
            re.escape(TRACKING_HEAD_START) + r".*?" + re.escape(TRACKING_HEAD_END) + r"\s*",
            TRACKING_HEAD_BLOCK + "\n",
            text,
            count=1,
            flags=re.DOTALL,
        )
        return text
    return HEAD_CLOSE_RE.sub(TRACKING_HEAD_BLOCK + "\n</head>", text, count=1)


def inject_gtm_body(text: str) -> str:
    if GTM_BODY_START in text:
        text = re.sub(
            re.escape(GTM_BODY_START) + r".*?" + re.escape(GTM_BODY_END) + r"\s*",
            GTM_BODY_NOSCRIPT_BLOCK + "\n",
            text,
            count=1,
            flags=re.DOTALL,
        )
        return text

    match = BODY_OPEN_RE.search(text)
    if not match:
        return text
    insert_at = match.end()
    return text[:insert_at] + f"\n{GTM_BODY_NOSCRIPT_BLOCK}\n" + text[insert_at:]


def inject_attributer(text: str) -> str:
    if ATTRIBUTER_START in text:
        text = re.sub(
            re.escape(ATTRIBUTER_START) + r".*?" + re.escape(ATTRIBUTER_END) + r"\s*",
            ATTRIBUTER_FOOTER_BLOCK + "\n",
            text,
            count=1,
            flags=re.DOTALL,
        )
        return text
    return BODY_CLOSE_RE.sub(ATTRIBUTER_FOOTER_BLOCK + "\n</body>", text, count=1)


def patch(text: str) -> str:
    text = strip_markers(text)
    text = inject_head(text)
    text = inject_gtm_body(text)
    text = inject_attributer(text)
    return text


def main() -> None:
    patched = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP_DIRS:
            continue
        original = path.read_text(encoding="utf-8")
        updated = patch(original)
        if updated == original:
            continue
        path.write_text(updated, encoding="utf-8")
        patched += 1
        print(f"patched {rel}")
    print(f"patched {patched} files")


if __name__ == "__main__":
    main()
