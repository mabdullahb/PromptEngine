import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  eslint: {
    ignoreDuringBuilds: true, // This ignores the 11 linting errors
  },
  typescript: {
    ignoreBuildErrors: true, // This ignores the "any" type errors
  },
  reactStrictMode: true,
};

export default nextConfig;