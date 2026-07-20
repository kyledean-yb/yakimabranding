#!/usr/bin/env bash
# Build the Next.js HVAC landing page as static HTML and merge it into the root
# static site. Safe to run locally or as the Vercel build command.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLUG="phx-hvac"

echo "==> Installing Next.js dependencies"
cd "$ROOT/next"
if [ -f package-lock.json ]; then
  npm ci
else
  npm install
fi

echo "==> Building static export"
npm run build:export

if [ ! -d out ]; then
  echo "error: Next export directory 'next/out' was not created" >&2
  exit 1
fi

echo "==> Copying landing page into static site"
LANDING_SRC=""
if [ -f "out/${SLUG}/index.html" ]; then
  LANDING_SRC="out/${SLUG}"
elif [ -f "out/${SLUG}.html" ]; then
  mkdir -p "out/${SLUG}"
  cp "out/${SLUG}.html" "out/${SLUG}/index.html"
  LANDING_SRC="out/${SLUG}"
else
  echo "error: landing page export not found in next/out/${SLUG}" >&2
  exit 1
fi

rm -rf "$ROOT/${SLUG}" "$ROOT/landing-page"
mkdir -p "$ROOT/${SLUG}"
cp -R "$LANDING_SRC/." "$ROOT/${SLUG}/"

echo "==> Copying Next.js assets"
rm -rf "$ROOT/_next"
cp -R out/_next "$ROOT/_next"

echo "==> Copying landing page public assets"
for asset in yb-logo-color.png yb-logo-white.png; do
  if [ -f "public/$asset" ]; then
    cp "public/$asset" "$ROOT/$asset"
  fi
done

mkdir -p "$ROOT/js"
for asset in hero-orbit.js hubspot-form.js; do
  if [ -f "public/js/$asset" ]; then
    cp "public/js/$asset" "$ROOT/js/$asset"
  fi
done

echo "==> Landing page ready at /${SLUG}/"
