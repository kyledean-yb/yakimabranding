import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: "export",
  // Match the static site's folder-based clean URLs (e.g. /landing-page/).
  trailingSlash: true,
  // Prevent Next from treating the static-site repo root as the app root.
  outputFileTracingRoot: path.join(__dirname),
  // Static export has no image optimizer.
  images: { unoptimized: true },
};

export default nextConfig;
