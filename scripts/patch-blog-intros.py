#!/usr/bin/env python3
"""Add Short Answer, Summary, and Key Takeaways blocks to blog post HTML files."""

from pathlib import Path

from blog_intro_snippet import load_posts_meta, patch_post_html

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "blog" / "posts"


def main():
    meta_by_slug = load_posts_meta()
    updated = 0
    skipped = 0

    for path in sorted(POSTS_DIR.glob("*.html")):
        slug = path.stem
        meta = meta_by_slug.get(slug, {"slug": slug, "title": slug, "excerpt": ""})
        if patch_post_html(path, meta):
            print(f"  patched {path.name}")
            updated += 1
        else:
            print(f"  skipped {path.name}")
            skipped += 1

    print(f"\nDone: {updated} updated, {skipped} skipped.")


if __name__ == "__main__":
    main()
