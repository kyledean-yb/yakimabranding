---
name: yb-marketing-design
description: Use this skill to generate well-branded interfaces and assets for YB Marketing (Yakima Branding), either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the `README.md` file within this skill, and explore the other available files.

Key files:
- `README.md` — brand context, content fundamentals, visual foundations, iconography, manifest.
- `colors_and_type.css` — all design tokens (color, type, spacing, radii, shadows, motion) + semantic element styles. Import this in every artifact.
- `assets/` — YB logo (color + white).
- `preview/` — small specimen cards for every token group.
- `ui_kits/website/` — high-fidelity, interactive recreation of the YB Marketing website with modular React components.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some clarifying questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

Brand quick-reference: cornflower-blue primary (`#3F6FD6`) + navy ink (`#1B2A4A`), extended with a bright service-accent spectrum (cyan/violet/coral/amber/mint/pink). Display type = Sora, body = Plus Jakarta Sans. Friendly rounded geometry, soft blue-tinted shadows, generous whitespace, no emoji in brand voice. Lucide line icons in accent chips.
