#!/usr/bin/env python3
"""Generate location hub pages (master + 10 city hubs)."""

import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTIALS = ROOT / "partials" / "local-service"

sys.path.insert(0, str(ROOT / "scripts"))
from reviews_section_snippet import reviews_section_html
from schema_markup import seo_head_html
from site_accessibe_snippet import ACCESSIBE_BODY_SCRIPT
from site_staging_seo_snippet import STAGING_ROBOTS_META
from site_footer_snippet import site_footer_html
from site_nav_snippet import site_header_html

LOC_PIN = (
    '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'
    "</svg>"
)

SERVICE_THEMES = [
    {
        "folder": "seo",
        "accent": "var(--yb-cyan)",
        "wash": "var(--wash-cyan)",
        "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    },
    {
        "folder": "google-ads",
        "accent": "var(--yb-coral)",
        "wash": "var(--wash-coral)",
        "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/></svg>',
    },
    {
        "folder": "web-design",
        "accent": "#159468",
        "wash": "var(--wash-mint)",
        "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg>',
    },
    {
        "folder": "social-media",
        "accent": "#c77f12",
        "wash": "var(--wash-amber)",
        "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>',
    },
    {
        "folder": "branding",
        "accent": "var(--yb-violet)",
        "wash": "var(--wash-violet)",
        "icon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r="0.5" fill="currentColor"/><circle cx="17.5" cy="10.5" r="0.5" fill="currentColor"/><circle cx="8.5" cy="7.5" r="0.5" fill="currentColor"/><circle cx="6.5" cy="12.5" r="0.5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>',
    },
]

WHY_ICONS = [
    ('var(--yb-cyan)', "rgba(43,196,240,.18)", '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="var(--yb-cyan)" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/><polyline points="7 10 10 7 13 10 17 6"/></svg>'),
    ('var(--yb-violet)', "rgba(123,91,230,.2)", '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="var(--yb-violet)" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/><line x1="12" y1="2" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="22"/><line x1="2" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="22" y2="12"/></svg>'),
    ('var(--yb-mint)', "rgba(37,194,138,.18)", '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="var(--yb-mint)" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 1 18"/><polyline points="16 7 22 7 22 13"/></svg>'),
]

PAGE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--font-body);background:var(--bg);color:var(--fg1);-webkit-font-smoothing:antialiased;overflow-x:hidden}
::selection{background:var(--yb-blue);color:#fff}
img{display:block;max-width:100%}
a{color:inherit;text-decoration:none}
.container{width:100%;max-width:var(--container);margin:0 auto;padding:0 28px}
section{padding:88px 0}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-body);font-weight:700;font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--yb-blue)}
.eyebrow::before{content:'';display:block;width:7px;height:7px;border-radius:50%;background:currentColor;flex:none}
.btn{display:inline-flex;align-items:center;gap:8px;border:none;cursor:pointer;font-family:var(--font-body);font-weight:700;font-size:15px;border-radius:var(--r-md);padding:13px 22px;transition:all 240ms;white-space:nowrap;line-height:1}
.btn-grad{background:var(--grad-brand);color:#fff;box-shadow:0 14px 30px -10px rgba(63,111,214,.45)}
.btn-grad:hover{transform:translateY(-2px);filter:brightness(1.06)}
.btn-lg{padding:16px 28px;font-size:16px}
.btn-ghost-white{background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.35)}
.btn-ghost-white:hover{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.6)}
.hub-hero{position:relative;overflow:hidden;background:var(--grad-navy);padding:80px 0 100px}
.hub-hero-mesh{position:absolute;inset:0;background-image:var(--grad-mesh);pointer-events:none}
.hub-hero-inner{position:relative;display:grid;grid-template-columns:1.1fr .9fr;gap:56px;align-items:center}
.hub-hero h1{margin:16px 0 18px;font-family:var(--font-display);font-weight:800;font-size:clamp(2rem,3.6vw,3.2rem);color:#fff;line-height:1.08}
.hub-hero-accent{display:block;color:var(--yb-cyan);margin-top:6px}
.hero-lead{margin:0 0 32px;color:var(--fg2-on-dark);max-width:540px;font-size:clamp(1rem,1.3vw,1.15rem);line-height:1.7}
.hub-hero-actions{display:flex;gap:14px;flex-wrap:wrap}
.hub-hero-visual{position:relative;display:flex;align-items:center;justify-content:center}
.hub-hero-visual img{width:min(100%,420px);border-radius:var(--r-xl);box-shadow:0 24px 64px rgba(0,0,0,.35)}
.services{background:var(--bg-soft)}
.sec-header{text-align:center;max-width:680px;margin:0 auto 48px}
.sec-header h2{margin:14px 0 12px}
.hub-svc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.hub-svc-grid--5{grid-template-columns:repeat(6,1fr)}
.hub-svc-grid--5 .hub-svc-card:nth-child(-n+3){grid-column:span 2}
.hub-svc-grid--5 .hub-svc-card:nth-child(n+4){grid-column:span 3}
.hub-svc-card{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:26px;box-shadow:var(--sh-sm);transition:all 240ms;display:flex;flex-direction:column;border-top:4px solid var(--ac);height:100%}
.hub-svc-card:hover{transform:translateY(-6px);box-shadow:var(--sh-md)}
.hub-svc-chip{width:52px;height:52px;border-radius:var(--r-md);display:flex;align-items:center;justify-content:center;flex:none;margin-bottom:16px}
.hub-svc-chip svg{width:26px;height:26px}
.hub-svc-card h3{font-family:var(--font-display);font-size:19px;margin:0 0 9px;color:var(--ink)}
.hub-svc-card p{font-size:14.5px;margin:0 0 16px;flex:1;color:var(--fg2);line-height:1.65}
.hub-svc-link{display:inline-flex;align-items:center;gap:6px;font-weight:700;font-size:14px;margin-top:auto;color:var(--ac)}
.hub-svc-link svg{width:15px;height:15px;transition:transform 240ms}
.hub-svc-card:hover .hub-svc-link svg{transform:translateX(4px)}
.meet-team{background:var(--bg-soft)}
.meet-grid{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}
.meet-photo{border-radius:var(--r-xl);overflow:hidden;box-shadow:0 16px 48px rgba(22,32,58,.12)}
.meet-photo img{width:100%;height:auto}
.stats-band{background:var(--grad-navy);padding:56px 0;position:relative;overflow:hidden}
.stats-mesh{position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.7;pointer-events:none}
.stats-grid{position:relative;display:grid;grid-template-columns:repeat(4,1fr);gap:24px;text-align:center}
.stat-num{font-family:var(--font-display);font-weight:800;font-size:clamp(2.2rem,4vw,3.2rem);line-height:1;background:var(--grad-brand);-webkit-background-clip:text;background-clip:text;color:transparent}
.stat-label{font-size:13px;font-weight:600;color:var(--fg2-on-dark);margin-top:10px;letter-spacing:.03em}
.wave-div{position:relative;overflow:hidden;line-height:0;font-size:0}
.wave-div svg{display:block;width:100%;height:70px}
.locations-track{display:flex;width:max-content;animation:loc-scroll 35s linear infinite;gap:0}
.locations-track:hover{animation-play-state:paused}
.locations-set{display:flex;gap:12px;padding-right:12px}
.loc-chip{display:inline-flex;align-items:center;gap:7px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);color:rgba(255,255,255,.85);font-size:13px;font-weight:600;letter-spacing:.03em;padding:7px 16px;border-radius:var(--r-pill);white-space:nowrap;font-family:var(--font-display)}
.loc-chip svg{opacity:.6;flex:none}
@keyframes loc-scroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}
.loc-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:22px}
.loc-card{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:28px;box-shadow:var(--sh-sm);transition:all 240ms;display:flex;flex-direction:column;border-left:4px solid var(--yb-blue)}
.loc-card:hover{transform:translateY(-4px);box-shadow:var(--sh-md)}
.loc-card h3{font-family:var(--font-display);font-size:20px;margin:0 0 10px;color:var(--ink)}
.loc-card p{font-size:14.5px;color:var(--fg2);line-height:1.65;margin:0 0 16px;flex:1}
.loc-card-link{display:inline-flex;align-items:center;gap:6px;font-weight:700;font-size:14px;color:var(--yb-blue);margin-top:auto}
.overview-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:16px}
.overview-item{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:22px;text-align:center;box-shadow:var(--sh-sm);transition:all 240ms}
.overview-item:hover{transform:translateY(-4px);box-shadow:var(--sh-md)}
.overview-ic{width:48px;height:48px;border-radius:var(--r-md);display:flex;align-items:center;justify-content:center;margin:0 auto 12px}
.overview-item span{font-weight:700;font-size:14px;color:var(--ink);line-height:1.35;display:block}
.yb-lead{color:var(--fg2);font-size:16px;line-height:1.75}
.reviews-bg{background:var(--bg-soft)}
.reviews-scroll-track{display:flex;width:max-content;animation:rv-scroll 50s linear infinite;gap:22px}
.reviews-scroll-track:hover{animation-play-state:paused}
.reviews-scroll-set{display:flex;gap:22px}
.rv-scroll-card{width:320px;background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:22px;box-shadow:var(--sh-sm);flex:none;display:flex;flex-direction:column}
@keyframes rv-scroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}
.blog-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.blog-card{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden;box-shadow:var(--sh-sm);transition:all 240ms;cursor:pointer;display:flex;flex-direction:column;height:100%}
.blog-card:hover{transform:translateY(-5px);box-shadow:var(--sh-md)}
.blog-thumb{position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center;aspect-ratio:16/9}
.blog-cat{position:absolute;top:14px;left:14px;background:#fff;font-size:11px;font-weight:800;padding:5px 11px;border-radius:var(--r-pill);box-shadow:var(--sh-xs)}
.blog-body{padding:20px;display:flex;flex-direction:column;flex:1}
.blog-card h3{margin:0 0 9px;line-height:1.25;font-family:var(--font-display);font-size:17px;color:var(--ink)}
.blog-card p{font-size:14px;color:var(--fg2);margin:0 0 16px;flex:1}
.blog-meta{display:flex;align-items:center;justify-content:space-between;margin-top:auto}
.blog-read{font-size:12.5px;color:var(--fg3);font-weight:600}
.footer{background:var(--grad-navy);color:#fff;position:relative;overflow:hidden;padding:64px 0 28px}
.footer-mesh{position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.5;pointer-events:none}
.footer-grid{position:relative;display:grid;grid-template-columns:1.7fr 1fr 1fr 1.4fr;gap:40px;margin-bottom:42px}
.footer-brand p{color:var(--fg2-on-dark);font-size:14px;max-width:280px;margin:14px 0 18px}
.footer-col h4{font-family:var(--font-display);font-size:14px;font-weight:700;margin-bottom:14px;letter-spacing:.04em;color:#fff}
.footer-col ul{list-style:none;display:grid;gap:10px}
.footer-col a{color:var(--fg2-on-dark);font-size:14px;transition:color 240ms}
.footer-col a:hover{color:#fff}
.footer-bottom{position:relative;border-top:1px solid rgba(255,255,255,.12);padding-top:22px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;color:var(--fg2-on-dark);font-size:13px}
@media(max-width:1100px){.hub-svc-grid--5{grid-template-columns:1fr 1fr}.hub-svc-grid--5 .hub-svc-card{grid-column:auto !important}.overview-grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:900px){.hub-hero-inner{grid-template-columns:1fr}.hub-hero-visual{display:none}.hub-svc-grid{grid-template-columns:1fr 1fr}.meet-grid{grid-template-columns:1fr}.why-main-grid{grid-template-columns:1fr !important}.why-tiles-grid{grid-template-columns:1fr 1fr !important}.stats-grid{grid-template-columns:1fr 1fr}.loc-grid{grid-template-columns:1fr}}
@media(max-width:640px){.hub-svc-grid{grid-template-columns:1fr}.overview-grid{grid-template-columns:1fr 1fr}.why-tiles-grid{grid-template-columns:1fr !important}.footer-grid{grid-template-columns:1fr}section{padding:60px 0}.blog-grid{grid-template-columns:1fr}}
"""

STAT_JS = """
const nums = document.querySelectorAll('.stat-num[data-target]');
const statIO = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    statIO.unobserve(e.target);
    const end = +e.target.dataset.target, sfx = e.target.dataset.suffix || '';
    const dur = 1400, t0 = performance.now();
    (function tick(t) {
      const p = Math.min(1, (t - t0) / dur);
      e.target.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))) + (p >= 1 ? sfx : '');
      if (p < 1) requestAnimationFrame(tick);
    })(t0);
  });
}, { threshold: 0.5 });
nums.forEach(n => statIO.observe(n));
"""


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def load_data() -> list[dict]:
    script = (
        "import { locationHubs } from './locationHubs.js';"
        "process.stdout.write(JSON.stringify(locationHubs));"
    )
    result = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=ROOT / "data",
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def load_partial(name: str, prefix: str) -> str:
    text = (PARTIALS / name).read_text(encoding="utf-8")
    return text.replace("../", prefix)


def render_local_signals(signals: list[str], label: str = "Serving Your Market") -> str:
    chips = "".join(f'<span class="loc-chip">{LOC_PIN}{esc(s)}</span>' for s in signals)
    return f"""        <div style="grid-column:1/-1;margin-top:8px;overflow:hidden;border-radius:var(--r-lg)">
          <p style="color:rgba(255,255,255,.45);font-size:11px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;margin:0 0 12px;text-align:center">{esc(label)}</p>
          <div class="locations-track">
            <div class="locations-set">{chips}</div>
            <div class="locations-set" aria-hidden="true">{chips}</div>
          </div>
        </div>"""


def render_why_steps(steps: list[dict]) -> str:
    tiles = []
    for i, step in enumerate(steps[:2]):
        _, bg, icon = WHY_ICONS[i]
        tiles.append(
            f"""        <div style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:var(--r-lg);padding:26px">
          <div style="width:56px;height:56px;border-radius:var(--r-md);background:{bg};display:flex;align-items:center;justify-content:center;margin-bottom:16px">{icon}</div>
          <h3 style="font-family:var(--font-display);font-weight:800;font-size:17px;color:#fff;margin:0 0 10px;letter-spacing:.01em;text-transform:uppercase">{esc(step["label"])}</h3>
          <p style="color:var(--fg2-on-dark);font-size:14px;line-height:1.6;margin:0">{esc(step["body"])}</p>
        </div>"""
        )
    step3 = steps[2]
    _, bg3, icon3 = WHY_ICONS[2]
    tiles.append(
        f"""        <div style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:var(--r-lg);padding:26px;grid-column:1/-1;display:flex;gap:22px;align-items:center">
          <div style="width:64px;height:64px;border-radius:var(--r-md);background:{bg3};display:flex;align-items:center;justify-content:center;flex:none">{icon3}</div>
          <div>
            <h3 style="font-family:var(--font-display);font-weight:800;font-size:18px;color:#fff;margin:0 0 8px;letter-spacing:.01em;text-transform:uppercase">{esc(step3["label"])}</h3>
            <p style="color:var(--fg2-on-dark);font-size:14px;line-height:1.6;margin:0">{esc(step3["body"])}</p>
          </div>
        </div>"""
    )
    return "\n".join(tiles)


def render_why_section(why: dict, signals: list[str], prefix: str, signals_label: str) -> str:
    steps_html = render_why_steps(why["steps"])
    signals_html = render_local_signals(signals, signals_label)
    return f"""
<div class="wave-div" style="background:#F6F8FC"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,50 C480,70 960,10 1440,30 L1440,70 L0,70 Z" fill="#1B2A4A"/></svg></div>
<div style="background:var(--grad-navy)">
<div class="stats-band" style="background:transparent">
  <div class="stats-mesh"></div>
  <div class="container stats-grid">
    <div><div class="stat-num" data-target="22">0</div><div class="stat-label">Years in Business</div></div>
    <div><div class="stat-num" data-target="40" data-suffix="+">0</div><div class="stat-label">Industries</div></div>
    <div><div class="stat-num" data-target="250" data-suffix="+">0</div><div class="stat-label">Active Clients</div></div>
    <div><div class="stat-num" data-target="60" data-suffix="+">0</div><div class="stat-label">Years of Cumulative Experience</div></div>
  </div>
</div>
<section style="position:relative;overflow:hidden;padding:88px 0">
  <div style="position:absolute;inset:0;background-image:var(--grad-mesh);opacity:.6;pointer-events:none"></div>
  <div class="container" style="position:relative">
    <div style="display:grid;grid-template-columns:1fr 1.3fr;gap:48px;align-items:center" class="why-main-grid">
      <div style="background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);border-radius:var(--r-xl);padding:40px">
        <span class="eyebrow" style="color:var(--yb-cyan)">{esc(why["eyebrow"])}</span>
        <h2 style="margin:14px 0 18px;color:#fff;font-size:clamp(1.8rem,2.6vw,2.4rem);line-height:1.12">{esc(why["heading"])}</h2>
        <p style="color:var(--fg2-on-dark);font-size:15.5px;line-height:1.65;margin:0 0 32px">{esc(why["body"])}</p>
        <a href="{prefix}contact.html" class="btn btn-grad btn-lg">Let's Talk
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </a>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px" class="why-tiles-grid">
{steps_html}
{signals_html}
      </div>
    </div>
  </div>
</section>
</div>
<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path d="M0,0 C360,70 1080,70 1440,0 L1440,70 L0,70 Z" fill="#F6F8FC"/></svg></div>"""


def render_service_cards(cards: list[dict], slug: str, prefix: str) -> str:
    items = []
    for card, theme in zip(cards, SERVICE_THEMES):
        href = f"{prefix}{theme['folder']}/{slug}.html"
        items.append(
            f"""      <a href="{href}" class="hub-svc-card" style="--ac:{theme['accent']}">
        <div class="hub-svc-chip" style="background:{theme['wash']};color:{theme['accent']}">{theme['icon']}</div>
        <h3>{esc(card["title"])}</h3>
        <p>{esc(card["body"])}</p>
        <span class="hub-svc-link" style="color:{theme['accent']}">Learn More <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span>
      </a>"""
        )
    return "\n".join(items)


def render_hero(hero: dict, prefix: str) -> str:
    return f"""
<section class="hub-hero">
  <div class="hub-hero-mesh"></div>
  <div class="hero-logo-overlay hero-logo-overlay--left" aria-hidden="true">
    <img src="{prefix}assets/yb-logo-white.png" alt="">
  </div>
  <div class="container hub-hero-inner">
    <div>
      <span class="eyebrow" style="color:var(--yb-cyan)">{esc(hero["eyebrow"])}</span>
      <h1>{esc(hero["headline"])} <span class="hub-hero-accent">{esc(hero["accentHeadline"])}</span></h1>
      <p class="hero-lead">{esc(hero["body"])}</p>
      <div class="hub-hero-actions">
        <a href="{prefix}contact.html" class="btn btn-grad btn-lg">Get Started Today
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </a>
        <a href="tel:5099019735" class="btn btn-hdr-phone btn-lg">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.96a16 16 0 0 0 6.07 6.07l1.08-.9a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          509-901-9735
        </a>
      </div>
    </div>
    <div class="hub-hero-visual">
      <img src="{prefix}assets/team-photo.webp" alt="YB Marketing team">
    </div>
  </div>
</section>
<div class="wave-div" style="background:#1B2A4A"><svg viewBox="0 0 1440 80" preserveAspectRatio="none" style="height:80px"><path d="M0,0 C360,80 1080,80 1440,0 L1440,80 L0,80 Z" fill="#F6F8FC"/></svg></div>"""


def schema_json_city(loc: dict) -> tuple[str, str]:
    city = loc["city"]
    local_business = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "YB Marketing",
        "url": "https://yakimabranding.com",
        "telephone": "+15099019735",
        "email": "info@yakimabranding.com",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": loc["schema"]["addressLocality"],
            "addressRegion": loc["schema"]["addressRegion"],
            "addressCountry": loc["schema"].get("addressCountry", "US"),
        },
        "areaServed": city,
        "description": loc["metaDescription"],
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://yakimabranding.com"},
            {"@type": "ListItem", "position": 2, "name": "Locations", "item": "https://yakimabranding.com/locations"},
            {
                "@type": "ListItem",
                "position": 3,
                "name": f"{city} Digital Marketing",
                "item": loc["canonicalUrl"],
            },
        ],
    }
    return json.dumps(local_business, ensure_ascii=False), json.dumps(
        breadcrumb, ensure_ascii=False
    )


def render_insights(prefix: str) -> str:
    return f"""
<section style="background:#fff" id="insights">
  <div class="container">
    <div style="text-align:center;max-width:640px;margin:0 auto 40px">
      <span class="eyebrow" style="color:var(--yb-blue)">Insights</span>
      <h2 style="margin:14px 0 12px">Latest from YB Marketing</h2>
      <p class="yb-lead">Practical digital marketing advice for Pacific Northwest businesses.</p>
    </div>
    <div class="blog-grid" data-blog-insights data-variant="related" data-base="{prefix}" data-count="3"></div>
  </div>
</section>
<script src="{prefix}js/blog-insights.js" defer></script>"""


def render_reviews(prefix: str) -> str:
    reviews = reviews_section_html().replace('src="../', f'src="{prefix}')
    # why-choose already ends with this wave; partial repeats it
    marker = "<!-- REVIEWS -->"
    if marker in reviews:
        reviews = reviews[reviews.index(marker) :]
    return reviews


def render_contact(prefix: str) -> str:
    return load_partial("contact-section.html", prefix)


def page_shell(
    title: str,
    description: str,
    canonical: str,
    prefix: str,
    schema_blocks: str,
    body: str,
    extra_scripts: str = "",
) -> str:
    header = site_header_html(prefix).strip()
    footer = site_footer_html(prefix).strip()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{STAGING_ROBOTS_META}
<link rel="icon" href="{prefix}favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{prefix}favicon.png">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">
<link rel="stylesheet" href="{prefix}colors_and_type.css">
<link rel="stylesheet" href="{prefix}site.css">
<link rel="stylesheet" href="{prefix}insights.css">
<style>{PAGE_CSS}</style>
{schema_blocks}
</head>
<body>
{ACCESSIBE_BODY_SCRIPT}

{header}
{body}
{footer}

<script src="{prefix}js/contact-forms.js" defer></script>
<script src="{prefix}js/newsletter-popup.js" defer></script>
<script src="{prefix}js/chat-widget.js" defer></script>
<script src="{prefix}js/site.js"></script>
<script>{STAT_JS}</script>
{extra_scripts}
</body>
</html>
"""


def render_city_page(loc: dict, prefix: str = "../") -> str:
    slug = loc["slug"]
    city = loc["city"]
    svc = loc["servicesSection"]
    cred = loc["credibility"]
    schema_head = seo_head_html(f"locations/{slug}.html")
    cred_paras = "".join(
        f'<p style="margin:0 0 16px;font-size:15px;color:var(--fg2);line-height:1.75">{esc(p)}</p>'
        for p in cred["paragraphs"]
    )
    body = f"""{render_hero(loc["hero"], prefix)}
<section class="services" id="services">
  <div class="container">
    <div class="sec-header">
      <span class="eyebrow">{esc(svc["eyebrow"])}</span>
      <h2>{esc(svc["heading"])}</h2>
      <p class="yb-lead">{esc(svc["subheading"])}</p>
    </div>
    <div class="hub-svc-grid hub-svc-grid--5">
{render_service_cards(svc["cards"], slug, prefix)}
    </div>
  </div>
</section>
<section class="meet-team">
  <div class="container meet-grid">
    <div>
      <span class="eyebrow" style="color:var(--yb-blue)">{esc(cred["eyebrow"])}</span>
      <h2 style="margin:14px 0 16px">{esc(cred["heading"])}</h2>
      {cred_paras}
      <a href="{prefix}contact.html" class="btn btn-grad">Work With Us
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
      </a>
    </div>
    <div class="meet-photo">
      <img src="{prefix}assets/team-photo.webp" alt="The YB Marketing team serving {esc(city)}">
    </div>
  </div>
</section>
{render_why_section(loc["whyYb"], loc["localSignals"], prefix, f"Serving {city} & Surrounding Areas")}
{render_reviews(prefix)}
{render_insights(prefix)}
{render_contact(prefix)}"""
    return page_shell(
        loc["titleTag"],
        loc["metaDescription"],
        loc["canonicalUrl"],
        prefix,
        schema_head,
        body,
    )


def main() -> None:
    hubs = load_data()
    out_dir = ROOT / "locations"
    out_dir.mkdir(exist_ok=True)

    for loc in hubs:
        path = out_dir / f"{loc['slug']}.html"
        path.write_text(render_city_page(loc), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")

    print(f"generated {len(hubs)} location hub pages")


if __name__ == "__main__":
    main()
