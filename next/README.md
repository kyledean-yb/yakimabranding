# YB Marketing — Next.js app

Wireframe landing pages and future Next.js marketing site work live here, separate from the static HTML site at the repo root.

**Important:** Deploy from the **repo root**, not from `next/`. Deploying this folder as a standalone Vercel project replaces the entire site with only the landing page routes.

## Run locally

```bash
cd next
npm install
npm run dev
```

Open [http://localhost:3010/landing-page](http://localhost:3010/landing-page)

## Build for the static site

From the repo root:

```bash
bash scripts/build-landing-page.sh
```

This exports `/landing-page` as static HTML into `landing-page/` at the repo root, plus `/_next` assets. The existing static pages (`/`, `/about`, `/contact`, etc.) are untouched.

## Vercel deployment

1. Link the Vercel project to the **repository root** (Root Directory: empty or `.`), not `next/`.
2. The root `vercel.json` runs `scripts/build-landing-page.sh` on deploy, then serves the static site.
3. Landing page URL: `https://<your-domain>/landing-page`

## Landing page

- Route: `/landing-page`
- Component: `components/landing/MarketingLandingPage.tsx`
- Config: `lib/landing-config.ts` (`phoenixConfig`, `triCitiesConfig`, etc.)

Swap the config object passed in `app/landing-page/page.tsx` to localize for Phoenix, Tri-Cities, Chicago, or other markets.

Design tokens mirror the static site (`colors_and_type.css`): YB blue, Sora + Plus Jakarta Sans, radii, shadows.
