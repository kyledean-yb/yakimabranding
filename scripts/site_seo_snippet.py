"""SeoHead-equivalent helpers for JSON-LD structured data."""

from schema_markup import inject_schema_into_html, render_schema_head, schemas_for_rel_path, seo_head_html

__all__ = [
    "inject_schema_into_html",
    "render_schema_head",
    "schemas_for_rel_path",
    "seo_head_html",
]
