#!/usr/bin/env bash
# Build the Next.js landing page as static HTML and merge it into the root
# static site. Safe to run locally or as the Vercel build command.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

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
if [ -f out/landing-page/index.html ]; then
  LANDING_SRC="out/landing-page"
elif [ -f out/landing-page.html ]; then
  mkdir -p out/landing-page
  cp out/landing-page.html out/landing-page/index.html
  LANDING_SRC="out/landing-page"
else
  echo "error: landing page export not found in next/out" >&2
  exit 1
fi

rm -rf "$ROOT/landing-page"
mkdir -p "$ROOT/landing-page"
cp -R "$LANDING_SRC/." "$ROOT/landing-page/"

echo "==> Copying Next.js assets"
rm -rf "$ROOT/_next"
cp -R out/_next "$ROOT/_next"

echo "==> Copying landing page public assets"
for asset in yb-logo-color.png yb-logo-white.png; do
  if [ -f "public/$asset" ]; then
    cp "public/$asset" "$ROOT/$asset"
  fi
done

if [ -f public/js/hero-orbit.js ]; then
  mkdir -p "$ROOT/js"
  cp public/js/hero-orbit.js "$ROOT/js/hero-orbit.js"
fi

echo "==> Landing page ready at /landing-page/"
