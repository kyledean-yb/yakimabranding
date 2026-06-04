# YB Marketing — Design System

A bright, colorful, engaging design system for **YB Marketing** (operated by **Yakima Branding**, yakimabranding.com / yb.marketing) — an award-winning, full-spectrum digital marketing agency.

This system anchors on YB's brand monogram (cornflower blue + navy) and extends it into a vivid, service-mapped accent spectrum so the brand can feel energetic and approachable without losing its professional, results-driven credibility.

---

## Company / product context

**What they do.** YB Marketing is a full-service marketing agency that helps businesses grow through **branding & brand identity, SEO (incl. AI search), Google Ads / PPC, social media marketing, website design & development, and content & email marketing**. The positioning is practical and outcomes-focused: *attract more leads, improve visibility, build a stronger online presence.*

**Footprint.** Offices in **Colorado (Denver), Arizona (Scottsdale), California (San Francisco), Illinois (Chicago), and Washington State (Yakima)**. The brand notes that *"encite International is now YB Marketing"* — there was an acquisition/rebrand.

**Proof points.** Heavy emphasis on social proof — verified reviews from **Clutch** and **Google**, client testimonials, and stat counters (Years in Business, Industries, Active Clients, Years of Cumulative Experience).

**One product surface:** the **marketing website** (yb.marketing) — a Next.js marketing site with Home, About, Services (+ 6 service detail pages), Blog, Reviews, and Contact. There is no app or dashboard. The UI kit in this system recreates the marketing-website surface.

### Sources reviewed
- **Logo files** (provided): `uploads/YB_Logo_White_300x300.png`, `uploads/YB_Logo_Transparent_300x300.png` → copied to `assets/`.
- **yb.marketing** — primary content source (services, reviews, blog, offices, stats, tone). *Content reused verbatim where possible per the brief.*
- **atomicsocial.com** — referenced for visual *energy* only (bright, friendly, conversion-driven marketing-agency look). We did **not** copy their layout; structure here is original.

> No codebase, Figma, or slide decks were attached. The visual foundations below are derived from the logo, the live sites' content, and the brief ("bright, colorful, engaging, easy to use").

---

## CONTENT FUNDAMENTALS

**Voice:** confident, warm, and plain-spoken. Expert without jargon-dumping. The brand sells *results and partnership*, not buzzwords.

**Point of view:** speaks as **"we"** ("We craft exceptional brand experiences…", "We turn smart plans into bold execution"). Addresses the reader as **"you / your business."** Inclusive, collaborative — clients are framed as partners ("We view them as an extension of our own team").

**Casing:** Headlines use **Title Case** or sentence case with a bold key phrase. Eyebrow/kicker labels above sections are short and Title Case ("What YB Offers", "Why Choose Us", "Get Started"). Section H2s often pair a calm phrase with a punchy promise — e.g. *"Solutions That Deliver"*, *"YB Marketing Drives Real Results"*.

**Sentence style:** short, active, benefit-first. Verbs lead ("Drive immediate traffic…", "Boost visibility…", "Grow your brand presence…"). Service descriptions are 1–2 tight sentences followed by a 3–4 item feature list.

**Numbers & proof:** lean on concrete outcomes and verified review counts. Stat counters animate up from 0. Testimonials always carry name + role + company + location and a verification badge (Clutch / Google).

**Emoji:** essentially none in the YB voice (the occasional client review contains one, but brand copy stays emoji-free). **Do not add emoji** to YB-authored UI.

**Example snippets (reuse these):**
- Hero: *"Full-Spectrum Branding & Digital Marketing — Move Your Business Forward."*
- Sub: *"We craft exceptional brand experiences that captivate audiences, drive engagement, and accelerate business growth through innovative digital marketing strategies."*
- Section kicker → headline: *"Why Choose Us"* → *"YB Marketing Drives Real Results."*
- CTA: *"Ready to elevate your brand?"* / button: *"Get Started"*, *"Start Your Project"*, *"Book Meeting"*.
- Value pills: *Dedicated Team · Proven Results · Custom Solutions.*

---

## VISUAL FOUNDATIONS

**Overall vibe:** bright, optimistic, modern-agency. Clean white canvas punctuated by saturated brand color and the occasional deep-navy section for contrast and gravity. Lots of air; generous spacing; rounded, friendly geometry.

**Color.** Primary is a brightened cornflower **YB Blue `#3F6FD6`** (derived from the logo's blue, pushed more vivid for energy). **Navy `#1B2A4A`** is the ink and the "dark mode" section color. A **bright accent spectrum** — cyan, violet, coral, amber, mint, pink — maps one color per service so the site reads colorful and the services are instantly distinguishable. Accents appear as: icon chips, tinted card washes (10–14%), underlines, and gradient CTAs. Rule of thumb: **white/soft-grey base, blue as the lead, one accent per element — never a rainbow in a single component.** Max 1–2 background treatments per page.

**Type.** Display = **Sora** (geometric, confident, slightly techy) for all headings, weights 600–800, tight tracking (-0.02em). Body = **Plus Jakarta Sans** (friendly humanist sans), 400–600, line-height 1.65. Eyebrows are uppercase Plus Jakarta 700 at 0.14em tracking, colored with the section's accent. Strict heading hierarchy: one H1 per page (hero), H2 per section, H3 per card/sub-block, H4 for small labels.

**Backgrounds.** Mostly flat white (`#FFFFFF`) and soft blue-grey (`#F6F8FC`). Hero and CTA bands use subtle **mesh-gradient glows** (`--grad-mesh`) or the **navy gradient** (`--grad-navy`). Gradients are used deliberately on heroes/CTAs/icon chips — *not* slathered everywhere. No photographic textures or grain by default; imagery is full-color, warm, and people/work-focused (placeholders provided where real photos are needed).

**Imagery.** Bright, natural-light photography of teams, screens, and client work — warm-neutral, high-key, never desaturated or moody. Rounded corners on all media (`--r-lg`). Use `<image-slot>`-style placeholders in mocks until real assets arrive.

**Animation.** Smooth and purposeful: fades + short upward slides on scroll (16–24px, `--ease-out`), stat counters that tick up from 0, gentle hover lifts. Easing favors `cubic-bezier(.16,1,.3,1)`. A touch of `--ease-bounce` on playful elements (icon chips, badges). No infinite/distracting loops on content. Respect `prefers-reduced-motion`.

**Hover states.** Buttons darken (`--yb-blue` → `--yb-blue-600`) and lift 1–2px with a colored shadow. Cards lift (translateY -4px) and gain `--sh-md`, often revealing an accent top-border or arrow. Links shift to `--yb-blue` and reveal an underline.

**Press states.** Scale down slightly (`transform: scale(.97)`), shadow softens — tactile, quick (`--dur-fast`).

**Borders.** Hairlines `#E3E9F2` (1px). Cards favor border + soft shadow rather than heavy strokes. Accent cards use a 3–4px colored top-edge or left-edge as a service signal.

**Shadows / elevation.** Soft, blue-tinted, diffuse (never harsh black). Scale: `--sh-xs` (controls) → `--sh-sm` (resting cards) → `--sh-md` (hover) → `--sh-lg` (modals/floating). Colored CTA shadows (`--sh-blue`, `--sh-coral`) reinforce brand on primary actions.

**Corner radii.** Friendly and generous: inputs/buttons `--r-sm/--r-md` (10–16px), cards `--r-lg` (22px), hero panels/images `--r-xl` (32px), pills/chips `--r-pill`. Nothing sharp-cornered.

**Transparency & blur.** Sticky header uses a translucent white with `backdrop-filter: blur(12px)`. Glass effect reserved for overlays/nav. Tinted accent washes are solid (not alpha) for crisp print/export.

**Layout rules.** Max content width `1200px`, centered, with comfortable gutters. 12-col mental grid; service cards in 2–3 col grids. Sticky top header. Sections separated by generous vertical rhythm (`--s-8`/`--s-9`). Fixed elements: header (sticky), occasional floating "Schedule a Call" CTA.

---

## ICONOGRAPHY

**Approach:** clean, modern **line icons** with rounded caps/joins, ~1.75–2px stroke — friendly but crisp, matching Sora's geometry. Icons are almost always presented inside a **rounded "chip"** (squircle, `--r-md`) filled with the relevant service accent at full or tint strength.

**System used:** **[Lucide](https://lucide.dev)** (loaded from CDN) is the canonical icon set for this design system. *Substitution note:* the live yb.marketing site uses a mix of its own inline SVGs and stock service icons; since those source SVGs were not provided, we standardize on **Lucide** as the closest-matching open line-icon set (rounded, consistent 2px stroke). **Flagged for the user** — if you have the original icon SVGs, drop them into `assets/icons/` and we'll swap them in.

**Service → icon → accent mapping:**
| Service | Lucide icon | Accent |
|---|---|---|
| Branding / Identity | `palette` / `sparkles` | violet `#7B5BE6` |
| SEO / AI Search | `search` / `trending-up` | cyan `#2BC4F0` |
| Google Ads / PPC | `target` / `mouse-pointer-click` | coral `#FF6B57` |
| Social Media | `share-2` / `heart` | amber `#FFB23E` |
| Web Design & Dev | `layout` / `code` | mint `#25C28A` |
| Content & Email | `pen-line` / `mail` | pink `#FF5C9D` |

**Emoji:** not used in brand UI. **Unicode glyphs:** only functional arrows (→, ↗) for links/CTAs. **Logos:** the YB monogram (`assets/yb-logo-color.png`) pairs with a "YB Marketing" wordmark set in Sora. The white monogram (`assets/yb-logo-white.png`) is white-on-transparent for use on navy/photo backgrounds.

---

## Font substitution note ⚠️

No brand font files were provided. This system uses **Sora** (display) + **Plus Jakarta Sans** (body) from **Google Fonts CDN** — chosen to match the modern, friendly, geometric marketing-agency feel. **If YB has specified brand typefaces, send the files and we'll swap the `--font-display` / `--font-body` tokens.**

---

## Index / manifest

**Root**
- `README.md` — this file (context, content & visual foundations, iconography, manifest).
- `colors_and_type.css` — all design tokens: color, type scale, semantic element styles, radii, shadows, spacing, motion. **Import this in every file.**
- `SKILL.md` — Agent-Skills-compatible entry point.

**`assets/`** — `yb-logo-color.png`, `yb-logo-white.png` (more: drop brand photos / original icon SVGs here).

**`preview/`** — Design-System-tab cards (type, color, spacing, components, brand). Each is a small standalone HTML specimen.

**`ui_kits/website/`** — high-fidelity recreation of the YB Marketing website.
- `index.html` — interactive click-through (home + service-aware nav).
- `*.jsx` — modular components: `Header`, `Hero`, `ServiceCard`, `StatCounter`, `ReviewCard`, `BlogCard`, `CTABand`, `Footer`, `Button`, etc.
- `README.md` — kit-specific notes.

---

*Maintained for YB Marketing / Yakima Branding. Keep the system bright, keep it colorful, keep it easy to use.*
