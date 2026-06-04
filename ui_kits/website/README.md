# YB Marketing — Website UI Kit

A high-fidelity, interactive recreation of the **YB Marketing** (yb.marketing) marketing website, restructured to be bright, colorful, and engaging while keeping the original content.

> This is the brand's single product surface — a marketing website (Next.js). There is no app/dashboard, so this is the only UI kit.

## Run it
Open `index.html`. It loads React + Babel from CDN, Lucide icons (pinned `0.460.0` for brand icons), and the shared tokens from `../../colors_and_type.css`.

## Interactions
- **Sticky header** with translucent blur, a Services mega-dropdown (hover), and a mobile hamburger menu.
- **Smooth-scroll nav** — Home / About / Services / Blog / Contact jump to sections.
- **Get Started / Start Your Project / Book Meeting** open a **contact modal** with a working (fake) submit → success state.
- **Animated stat counters** tick up from 0 on scroll into view.
- **Hover lifts** on service cards, review cards, and blog cards.

## Components (`*.jsx`)
| File | Exports | Notes |
|---|---|---|
| `ui.jsx` | `Button`, `Icon`, `IconChip`, `Eyebrow`, `Container` | Primitives. `Button` variants: primary, grad, coral, navy, ghost, ghostLight. |
| `Header.jsx` | `Header`, `Logo`, `YB_SERVICES` | Sticky nav + announcement bar + services dropdown. `YB_SERVICES` is the shared service data (label/icon/accent/blurb/feats). |
| `Hero.jsx` | `Hero` | Mesh-gradient hero, gradient headline, floating stat + review chips, image placeholder. |
| `Services.jsx` | `Services`, `ServiceCard` | 6 accent-coded service cards + navy CTA strip. |
| `Proof.jsx` | `WhyChoose`, `StatCounter`, `Reviews`, `ReviewCard` | About/why band, navy stats band, masonry review wall (Clutch/Google). |
| `Blog.jsx` | `Blog`, `BlogCard`, `POSTS` | Insights grid (featured + two). |
| `CTAFooter.jsx` | `Contact`, `Footer`, `ContactModal` | Contact methods, navy footer with offices, modal form. |

Components export to `window` (each Babel script has its own scope). Import order in `index.html`: `ui` → `Header` → `Hero` → `Services` → `Proof` → `Blog` → `CTAFooter` → App.

## Content sources
All copy (services, blurbs, reviews, blog titles, offices, contact details) is pulled from **yb.marketing** per the brief — kept the same, restructured visually.

## Known placeholders / caveats
- **Images** are placeholder tiles (hero, team photo, blog thumbnails) — swap in real photography. Consider `image-slot.js` for drag-and-drop fills.
- **Stat numbers** (12 yrs, 40+, 250+, 75+) are reasonable stand-ins; the live site renders these from a CMS. Confirm exact figures.
- **Social icons** require Lucide `0.460.0` (brand glyphs were removed in later versions).
