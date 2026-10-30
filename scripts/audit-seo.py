#!/usr/bin/env python3
"""Check every public page for structured data and head tag problems. Exits non-zero on problems."""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from seo_graph import SITE, is_public  # noqa: E402

BANNED = ["Pacific Northwest", "PLACEHOLDER", "instagram.com/yakimabranding", "linkedin.com/company/yakima-branding", '"noIndex"']
SINGLE_TAGS = ["og:title", "og:description", "og:image", "og:url", "og:type", "og:locale", "twitter:card", "twitter:image"]
SHARED_IDS = ("/#organization", "/#website", "/#logo", "#blog", "#person", "#service")


def main() -> int:
    problems: dict[str, list[str]] = defaultdict(list)
    pages = 0
    for path in sorted(ROOT.rglob("*.html")):
        if not is_public(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in text[:4000]:
            continue
        pages += 1
        head = text.split("</head>")[0]
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)
        if len(blocks) != 1:
            problems[f"JSON-LD blocks = {len(blocks)}"].append(rel)
            continue
        try:
            graph = json.loads(blocks[0].replace("<\\/", "</"))["@graph"]
        except (ValueError, KeyError) as exc:
            problems["invalid JSON-LD"].append(f"{rel}: {exc}")
            continue
        ids = {n.get("@id") for n in graph}

        def walk(obj):
            if isinstance(obj, dict):
                if set(obj) == {"@id"} and obj["@id"] not in ids and not obj["@id"].endswith(SHARED_IDS):
                    problems["unresolved @id"].append(f"{rel}: {obj['@id']}")
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for v in obj:
                    walk(v)

        walk(graph)
        site_level = json.dumps(graph[:2])
        for bad in BANNED:
            if bad in site_level or (bad != "Pacific Northwest" and bad in blocks[0]):
                problems[f"schema contains {bad}"].append(rel)
        for tag in SINGLE_TAGS:
            n = len(re.findall(rf'(?:property|name)="{re.escape(tag)}"', head))
            if n != 1:
                problems[f"{tag} count {n}"].append(rel)
        if len(re.findall(r'rel="canonical"', head)) != 1:
            problems["canonical count != 1"].append(rel)
        hreflangs = re.findall(r'hreflang="([^"]+)"', head)
        if len(hreflangs) != len(set(hreflangs)):
            problems["duplicate hreflang"].append(rel)
        if len(re.findall(r"<h1\b", text)) != 1:
            problems["h1 count != 1"].append(rel)
        for node in graph:
            types = node["@type"] if isinstance(node["@type"], list) else [node["@type"]]
            if "FAQPage" in types:
                for q in node["mainEntity"]:
                    if not q["name"] or not q["acceptedAnswer"]["text"]:
                        problems["empty FAQ entry"].append(rel)
            if node["@type"] in ("BlogPosting", "Article") and "headline" in node and "author" in node:
                if node["@type"] == "BlogPosting" and "datePublished" not in node:
                    problems["post without datePublished"].append(rel)
            if node["@type"] == "ImageObject":
                local = ROOT / node["url"].replace(f"{SITE}/", "")
                if node["url"].startswith(SITE) and not local.exists():
                    problems["image file missing"].append(f"{rel}: {node['url']}")

    print(f"audited {pages} pages")
    for name, items in sorted(problems.items()):
        print(f"\n{name}: {len(items)}")
        for item in items[:8]:
            print(f"  {item}")
    if not problems:
        print("no problems found")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
