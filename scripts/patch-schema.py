#!/usr/bin/env python3
"""Inject JSON-LD schema markup into all public HTML pages."""

import csv
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from schema_markup import inject_schema_into_html, schemas_for_rel_path

SKIP_DIRS = {"preview", "partials", "ui_kits", "posts", "scripts", "assets", "js", "node_modules", "data", "uploads"}
SKIP_FILES = {"blog.html"}


def is_public_page(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if rel.name in SKIP_FILES:
        return False
    if any(part.startswith(".") for part in rel.parts):
        return False
    if rel.parts and rel.parts[0] in SKIP_DIRS:
        return False
    return True


def page_url(rel: str) -> str:
    if rel == "index.html":
        return "/"
    return "/" + rel.replace(".html", "")


def main() -> None:
    report: list[tuple[str, str, str]] = []
    patched = 0
    skipped = 0
    total_blocks = 0

    for path in sorted(ROOT.rglob("*.html")):
        if not is_public_page(path):
            continue
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        original = path.read_text(encoding="utf-8")
        schemas, types, notes = schemas_for_rel_path(rel)
        updated = inject_schema_into_html(original, schemas)
        if updated == original:
            skipped += 1
            continue
        path.write_text(updated, encoding="utf-8")
        patched += 1
        total_blocks += len(schemas)
        report.append((page_url(rel), types, notes))

    print(f"patched {patched} pages ({skipped} unchanged)")
    print(f"total schema blocks added: {total_blocks}")

    manual = [row for row in report if row[2]]
    print(f"pages requiring manual review: {len(manual)}")

    out = ROOT / "schema-implementation-report.csv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["Page URL", "Schema Types Added", "Notes"])
        writer.writerows(report)
    print(f"report written to {out.name}")


if __name__ == "__main__":
    main()
