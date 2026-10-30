#!/usr/bin/env python3
"""Rebuild JSON-LD, Open Graph, Twitter, canonical, and hreflang tags on every public page.

Run after any page generator (alongside apply-mega-nav.py). Safe to re-run.
"""

import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from seo_graph import apply_to_html, build_page, is_public  # noqa: E402


def main() -> None:
    report = []
    types = Counter()
    patched = unchanged = skipped = 0
    for path in sorted(ROOT.rglob("*.html")):
        if not is_public(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        raw = path.read_text(encoding="utf-8")
        data = build_page(rel, raw)
        if data is None:
            skipped += 1
            continue
        node_types = []
        for node in data["graph"]:
            t = node["@type"]
            node_types.extend(t if isinstance(t, list) else [t])
        types.update(node_types)
        report.append((data["meta"]["url"], ", ".join(node_types)))
        updated = apply_to_html(raw, data)
        if updated == raw:
            unchanged += 1
            continue
        path.write_text(updated, encoding="utf-8")
        patched += 1

    out = ROOT / "schema-implementation-report.csv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["Page URL", "Schema Types"])
        writer.writerows(sorted(report))
    print(f"patched {patched} pages ({unchanged} unchanged, {skipped} redirects skipped)")
    print("types:", dict(types.most_common()))


if __name__ == "__main__":
    main()
