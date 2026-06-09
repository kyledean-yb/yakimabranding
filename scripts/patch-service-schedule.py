#!/usr/bin/env python3
"""Replace legacy Calendly button blocks with the team schedule grid."""

import re
from pathlib import Path

from site_schedule_grid_snippet import schedule_grid_html, service_schedule_panel_html

ROOT = Path(__file__).resolve().parents[1]

LOCAL_DIRS = (
    "locations",
    "branding",
    "google-ads",
    "social-media",
    "web-design",
)

SERVICE_OLD = re.compile(
    r'<div style="text-align:center;padding-bottom:18px;border-bottom:1px solid var\(--line\);margin-bottom:18px">'
    r"[\s\S]*?"
    r'<div style="background:var\(--bg-soft\);border-radius:var\(--r-md\);padding:10px 14px;text-align:center;font-size:11\.5px;color:var\(--yb-blue\)">'
    r"Replace the button above with your Calendly inline embed when ready\.</div>",
    re.MULTILINE,
)

GRID_OLD = re.compile(
    r'<p class="yb-schedule-intro">Choose who you\'d like to meet with</p>\s*'
    r'<div class="yb-schedule-grid">[\s\S]*?</div>\s*'
    r'(?=<(?:<!-- FORM PANEL -->|<!-- Contact form -->|</div>\s*\n\s*<!-- ))',
    re.MULTILINE,
)


def patch_service_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "yb-schedule-grid" in text and "Meet Jacob" in text:
        return False
    new_panel = service_schedule_panel_html("../")
    updated, count = SERVICE_OLD.subn(new_panel, text, count=1)
    if count:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def patch_root_grid(path: Path, prefix: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if "Meet Sophie" in text and "yb-schedule-card--split" in text:
        # Already fully patched
        if not GRID_OLD.search(text):
            return False
    new_grid = schedule_grid_html(prefix)
    updated, count = GRID_OLD.subn(new_grid, text, count=1)
    if count:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def localized_html_files() -> list[Path]:
    files: list[Path] = []
    for folder in LOCAL_DIRS:
        dir_path = ROOT / folder
        if dir_path.is_dir():
            files.extend(sorted(dir_path.glob("*.html")))
    return files


def main():
    patched = []

    for path in sorted((ROOT / "services").glob("*.html")):
        if patch_service_file(path):
            patched.append(str(path.relative_to(ROOT)))

    for path in localized_html_files():
        if patch_service_file(path):
            patched.append(str(path.relative_to(ROOT)))

    for name, prefix in (("index.html", ""), ("contact.html", "")):
        path = ROOT / name
        if path.exists() and patch_root_grid(path, prefix):
            patched.append(name)

    print(f"Patched {len(patched)} files:")
    for p in patched:
        print(f"  {p}")


if __name__ == "__main__":
    main()
