"""SVG chart helpers for case study detail pages."""

from __future__ import annotations

import html
import re


def _fmt_num(n: float | int) -> str:
    return f"{int(n):,}"


def _short_month(label: str) -> str:
    match = re.match(r"^([A-Za-z]{3})\s+(\d{4})$", label.strip())
    if match:
        return f"{match.group(1)} '{match.group(2)[2:]}"
    return label


def render_area_chart(
    data: list[dict],
    x_key: str,
    y_key: str,
    y_label: str,
    accent: str,
    chart_id: str,
    annotate_peak: bool = False,
) -> str:
    width, height, pad_l, pad_r, pad_t, pad_b = 900, 380, 88, 32, 36, 108
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    ys = [float(row[y_key]) for row in data]
    y_min, y_max = 0, max(ys) * 1.1
    n = len(data)
    points = []
    for i, row in enumerate(data):
        x = pad_l + (i / max(n - 1, 1)) * plot_w
        y = pad_t + plot_h - ((float(row[y_key]) - y_min) / max(y_max - y_min, 1)) * plot_h
        points.append((x, y, row))
    line_pts = " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in points)
    area_pts = f"{pad_l},{pad_t + plot_h} {line_pts} {pad_l + plot_w},{pad_t + plot_h}"
    grid = []
    labels_y = []
    for i in range(6):
        val = y_min + (y_max - y_min) * (i / 5)
        y = pad_t + plot_h - (i / 5) * plot_h
        grid.append(
            f'<line x1="{pad_l}" y1="{y:.1f}" x2="{pad_l + plot_w}" y2="{y:.1f}" class="cs-chart__grid"/>'
        )
        labels_y.append(
            f'<text x="{pad_l - 14}" y="{y + 4:.1f}" class="cs-chart__tick" text-anchor="end">'
            f"{_fmt_num(val)}</text>"
        )
    x_labels = []
    step = max(1, n // 6)
    for i in range(0, n, step):
        x, _, row = points[i]
        label = html.escape(_short_month(str(row[x_key])))
        x_labels.append(
            f'<text x="{x:.1f}" y="{height - 24}" class="cs-chart__tick cs-chart__tick--x" '
            f'text-anchor="middle">{label}</text>'
        )
    if (n - 1) % step != 0:
        x, _, row = points[-1]
        label = html.escape(_short_month(str(row[x_key])))
        x_labels.append(
            f'<text x="{x:.1f}" y="{height - 24}" class="cs-chart__tick cs-chart__tick--x" '
            f'text-anchor="middle">{label}</text>'
        )
    grad_id = f"cs-area-{chart_id}"
    caption = html.escape(y_label)
    peak_markup = ""
    if annotate_peak and points:
        peak_i = max(range(len(points)), key=lambda i: float(points[i][2][y_key]))
        px, py, prow = points[peak_i]
        peak_val = _fmt_num(prow[y_key])
        peak_markup = (
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{accent}" stroke="#fff" stroke-width="2"/>'
            f'<text x="{px:.1f}" y="{py - 14:.1f}" class="cs-chart__peak-label" text-anchor="middle">'
            f"Peak {peak_val}</text>"
        )
    return f"""<figure class="cs-chart cs-chart--area" role="group" aria-label="{caption} over time">
  <figcaption class="cs-chart__caption">{caption}</figcaption>
  <div class="cs-chart__canvas">
    <svg viewBox="0 0 {width} {height}" class="cs-chart__svg" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
      <defs>
        <linearGradient id="{grad_id}" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="{accent}" stop-opacity="0.32"/>
          <stop offset="100%" stop-color="{accent}" stop-opacity="0.02"/>
        </linearGradient>
      </defs>
      {''.join(grid)}
      <polygon points="{area_pts}" fill="url(#{grad_id})"/>
      <polyline points="{line_pts}" fill="none" stroke="{accent}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
      {peak_markup}
      {''.join(labels_y)}
      {''.join(x_labels)}
    </svg>
  </div>
</figure>"""


def render_dual_line_chart(
    data: list[dict],
    x_key: str,
    lines: list[dict],
    y_label: str,
    chart_id: str,
) -> str:
    width, height, pad_l, pad_r, pad_t, pad_b = 900, 380, 88, 32, 36, 118
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    values = []
    for row in data:
        for line in lines:
            val = row.get(line["key"])
            if val is not None:
                values.append(float(val))
    y_min = min(min(values), 0) - 50
    y_max = max(values) + 50
    n = len(data)
    grid = []
    for pct in (0, 0.25, 0.5, 0.75, 1):
        y = pad_t + plot_h * (1 - pct)
        val = y_min + (y_max - y_min) * pct
        grid.append(
            f'<line x1="{pad_l}" y1="{y:.1f}" x2="{pad_l + plot_w}" y2="{y:.1f}" class="cs-chart__grid"/>'
        )
        sign = "+" if val >= 0 else ""
        grid.append(
            f'<text x="{pad_l - 14}" y="{y + 4:.1f}" class="cs-chart__tick" text-anchor="end">'
            f"{sign}{val:.0f}%</text>"
        )
    zero_y = pad_t + plot_h - ((0 - y_min) / max(y_max - y_min, 1)) * plot_h
    baseline = (
        f'<line x1="{pad_l}" y1="{zero_y:.1f}" x2="{pad_l + plot_w}" y2="{zero_y:.1f}" '
        f'class="cs-chart__baseline" stroke-dasharray="6 5"/>'
    )
    polylines = []
    legend = []
    for line in lines:
        pts = []
        for i, row in enumerate(data):
            val = row.get(line["key"])
            if val is None:
                continue
            x = pad_l + (i / max(n - 1, 1)) * plot_w
            y = pad_t + plot_h - ((float(val) - y_min) / max(y_max - y_min, 1)) * plot_h
            pts.append(f"{x:.1f},{y:.1f}")
        if pts:
            polylines.append(
                f'<polyline points="{" ".join(pts)}" fill="none" stroke="{line["color"]}" '
                f'stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
            )
        legend.append(
            f'<span class="cs-chart__legend-item"><span class="cs-chart__legend-swatch" '
            f'style="background:{line["color"]}"></span>{html.escape(line["label"])}</span>'
        )
    x_labels = []
    for i, row in enumerate(data):
        x = pad_l + (i / max(n - 1, 1)) * plot_w
        x_labels.append(
            f'<text x="{x:.1f}" y="{height - 28}" class="cs-chart__tick cs-chart__tick--x" '
            f'text-anchor="middle">{html.escape(str(row[x_key]))}</text>'
        )
    caption = html.escape(y_label)
    return f"""<figure class="cs-chart cs-chart--lines" role="group" aria-label="{caption}">
  <figcaption class="cs-chart__caption">{caption}</figcaption>
  <div class="cs-chart__canvas">
    <svg viewBox="0 0 {width} {height}" class="cs-chart__svg" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
      {''.join(grid)}
      {baseline}
      {''.join(polylines)}
      {''.join(x_labels)}
    </svg>
  </div>
  <div class="cs-chart__legend">{''.join(legend)}</div>
</figure>"""


def render_bar_chart(
    data: list[dict],
    x_key: str,
    y_key: str,
    y_label: str,
    accent: str,
    chart_id: str,
    badge: str | None = None,
    muted_color: str = "#c5d0e3",
) -> str:
    width, height, pad_l, pad_r, pad_t, pad_b = 900, 340, 80, 80, 48, 72
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    ys = [float(row[y_key]) for row in data]
    y_max = max(ys) * 1.22
    n = len(data)
    bar_gap = plot_w / n * 0.35
    bar_w = (plot_w - bar_gap * (n + 1)) / n
    bars = []
    labels = []
    values = []
    for i, row in enumerate(data):
        val = float(row[y_key])
        x = pad_l + bar_gap + i * (bar_w + bar_gap)
        bar_h = (val / y_max) * plot_h if y_max else 0
        y = pad_t + plot_h - bar_h
        color = muted_color if i < n - 1 else accent
        rx = 10
        bars.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" '
            f'rx="{rx}" fill="{color}"/>'
        )
        values.append(
            f'<text x="{x + bar_w / 2:.1f}" y="{y - 12:.1f}" class="cs-chart__bar-value" '
            f'text-anchor="middle">{_fmt_num(val)}</text>'
        )
        labels.append(
            f'<text x="{x + bar_w / 2:.1f}" y="{height - 28}" class="cs-chart__tick cs-chart__tick--year" '
            f'text-anchor="middle">{html.escape(str(row[x_key]))}</text>'
        )
    badge_html = ""
    if badge and n >= 2:
        last_x = pad_l + bar_gap + (n - 1) * (bar_w + bar_gap) + bar_w / 2
        last_val = float(data[-1][y_key])
        last_h = (last_val / y_max) * plot_h if y_max else 0
        badge_y = pad_t + plot_h - last_h - 42
        badge_html = (
            f'<text x="{last_x:.1f}" y="{badge_y:.1f}" class="cs-chart__badge" '
            f'text-anchor="middle">{html.escape(badge)}</text>'
        )
    caption = html.escape(y_label)
    return f"""<figure class="cs-chart cs-chart--bar cs-chart--featured" role="group" aria-label="{caption}">
  <figcaption class="cs-chart__caption">{caption}</figcaption>
  <div class="cs-chart__canvas">
    <svg viewBox="0 0 {width} {height}" class="cs-chart__svg" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
      {''.join(bars)}
      {''.join(values)}
      {badge_html}
      {''.join(labels)}
    </svg>
  </div>
</figure>"""


def _fmt_pct(val: float) -> str:
    sign = "+" if val >= 0 else "−"
    magnitude = abs(val)
    if magnitude >= 1000:
        return f"{sign}{_fmt_num(magnitude)}%"
    return f"{sign}{magnitude:.0f}%"


def indexed_growth_data(data: list[dict], y_key: str, out_key: str = "growth") -> list[dict]:
    baseline = float(data[0][y_key])
    if baseline == 0:
        baseline = 1.0
    return [
        {**row, out_key: round(((float(row[y_key]) - baseline) / baseline) * 100)}
        for row in data
    ]


def render_growth_area_chart(
    data: list[dict],
    x_key: str,
    y_key: str,
    y_label: str,
    accent: str,
    chart_id: str,
    featured: bool = False,
    annotate_peak: bool = False,
) -> str:
    height = 400 if featured else 380
    pad_b = 118 if featured else 108
    width, pad_l, pad_r, pad_t = 900, 88, 32, 36
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    ys = [float(row[y_key]) for row in data]
    y_min = min(min(ys), 0) - 25
    y_max = max(ys) + 25
    n = len(data)
    points = []
    for i, row in enumerate(data):
        x = pad_l + (i / max(n - 1, 1)) * plot_w
        y = pad_t + plot_h - ((float(row[y_key]) - y_min) / max(y_max - y_min, 1)) * plot_h
        points.append((x, y, row))
    line_pts = " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in points)
    area_pts = f"{pad_l},{pad_t + plot_h} {line_pts} {pad_l + plot_w},{pad_t + plot_h}"
    zero_y = pad_t + plot_h - ((0 - y_min) / max(y_max - y_min, 1)) * plot_h
    grid = []
    for pct in (0, 0.25, 0.5, 0.75, 1):
        y = pad_t + plot_h * (1 - pct)
        val = y_min + (y_max - y_min) * pct
        grid.append(
            f'<line x1="{pad_l}" y1="{y:.1f}" x2="{pad_l + plot_w}" y2="{y:.1f}" class="cs-chart__grid"/>'
        )
        grid.append(
            f'<text x="{pad_l - 14}" y="{y + 4:.1f}" class="cs-chart__tick" text-anchor="end">'
            f"{_fmt_pct(val)}</text>"
        )
    baseline = (
        f'<line x1="{pad_l}" y1="{zero_y:.1f}" x2="{pad_l + plot_w}" y2="{zero_y:.1f}" '
        f'class="cs-chart__baseline" stroke-dasharray="6 5"/>'
    )
    x_labels = []
    step = max(1, n // 8) if n > 20 else max(1, n // 6)
    for i in range(0, n, step):
        x, _, row = points[i]
        x_labels.append(
            f'<text x="{x:.1f}" y="{height - 24}" class="cs-chart__tick cs-chart__tick--x" '
            f'text-anchor="middle">{html.escape(_short_month(str(row[x_key])))}</text>'
        )
    if (n - 1) % step != 0:
        x, _, row = points[-1]
        x_labels.append(
            f'<text x="{x:.1f}" y="{height - 24}" class="cs-chart__tick cs-chart__tick--x" '
            f'text-anchor="middle">{html.escape(_short_month(str(row[x_key])))}</text>'
        )
    grad_id = f"cs-growth-{chart_id}"
    caption = html.escape(y_label)
    featured_class = " cs-chart--featured" if featured else ""
    peak_markup = ""
    if annotate_peak and points:
        peak_i = max(range(len(points)), key=lambda i: float(points[i][2][y_key]))
        px, py, prow = points[peak_i]
        peak_val = _fmt_pct(float(prow[y_key]))
        peak_markup = (
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{accent}" stroke="#fff" stroke-width="2"/>'
            f'<text x="{px:.1f}" y="{py - 14:.1f}" class="cs-chart__peak-label" text-anchor="middle">'
            f"Peak {peak_val}</text>"
        )
    return f"""<figure class="cs-chart cs-chart--growth-area{featured_class}" role="group" aria-label="{caption}">
  <figcaption class="cs-chart__caption">{caption}</figcaption>
  <div class="cs-chart__canvas">
    <svg viewBox="0 0 {width} {height}" class="cs-chart__svg" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
      <defs>
        <linearGradient id="{grad_id}" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="{accent}" stop-opacity="0.24"/>
          <stop offset="100%" stop-color="{accent}" stop-opacity="0.02"/>
        </linearGradient>
      </defs>
      {''.join(grid)}
      {baseline}
      <polygon points="{area_pts}" fill="url(#{grad_id})"/>
      <polyline points="{line_pts}" fill="none" stroke="{accent}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
      {peak_markup}
      {''.join(x_labels)}
    </svg>
  </div>
</figure>"""
