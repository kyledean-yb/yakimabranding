#!/usr/bin/env python3
"""Add YB hero logo overlay to all pages with hero sections."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def assets_prefix(path: Path) -> str:
    rel = path.parent.relative_to(ROOT)
    depth = len(rel.parts)
    return "../" * depth if depth else ""


def upgrade_existing(content: str) -> str:
    content = re.sub(
        r'<div class="hero-logo-overlay"(?!\s+hero-logo-overlay--)',
        '<div class="hero-logo-overlay hero-logo-overlay--left"',
        content,
    )
    content = content.replace(
        'hero-logo-overlay hero-logo-overlay--light"',
        'hero-logo-overlay hero-logo-overlay--light hero-logo-overlay--left"',
    )
    return content


def snippet(kind: str, assets: str) -> str:
    if kind == "light":
        return (
            f'  <div class="hero-logo-overlay hero-logo-overlay--light hero-logo-overlay--left" aria-hidden="true">\n'
            f'    <img src="{assets}assets/yb-logo-color.png" alt="">\n'
            f"  </div>\n"
        )
    if kind == "right":
        return (
            f'  <div class="hero-logo-overlay hero-logo-overlay--right" aria-hidden="true">\n'
            f'    <img src="{assets}assets/yb-logo-white.png" alt="">\n'
            f"  </div>\n"
        )
    if kind == "center":
        return (
            f'  <div class="hero-logo-overlay hero-logo-overlay--center" aria-hidden="true">\n'
            f'    <img src="{assets}assets/yb-logo-white.png" alt="">\n'
            f"  </div>\n"
        )
    return (
        f'  <div class="hero-logo-overlay hero-logo-overlay--left" aria-hidden="true">\n'
        f'    <img src="{assets}assets/yb-logo-white.png" alt="">\n'
        f"  </div>\n"
    )


MESH_RULES = [
    (r'<div class="hero-mesh"></div>', "light"),
    (r'<div class="team-hero-mesh"></div>', "right"),
    (r'<div class="svc-hero-mesh"></div>', "left"),
    (r'<div class="about-hero-mesh"></div>', "left"),
    (r'<div class="blog-hero-mesh"></div>', "center"),
    (r'<div class="news-hero-mesh"[^>]*></div>', "left"),
]


def insert_after_mesh(content: str, path: Path) -> tuple[str, bool]:
    assets = assets_prefix(path)
    changed = False
    for pattern, kind in MESH_RULES:
        if not re.search(pattern, content):
            continue

        def repl(match: re.Match[str]) -> str:
            nonlocal changed
            end = match.end()
            rest = content[end : end + 200]
            if "hero-logo-overlay" in rest:
                return match.group(0)
            changed = True
            return match.group(0) + "\n" + snippet(kind, assets)

        content = re.sub(pattern, repl, content, count=1)
    return content, changed


def main() -> None:
    touched = []
    for path in sorted(ROOT.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        if not any(
            s in text
            for s in (
                "svc-hero-mesh",
                "about-hero-mesh",
                "blog-hero-mesh",
                "news-hero-mesh",
                "team-hero-mesh",
                'class="hero"',
            )
        ):
            continue
        original = text
        text = upgrade_existing(text)
        text, inserted = insert_after_mesh(text, path)
        if text != original:
            path.write_text(text, encoding="utf-8")
            touched.append(path.relative_to(ROOT))

    print(f"Updated {len(touched)} files:")
    for p in touched:
        print(f"  · {p}")


if __name__ == "__main__":
    main()
