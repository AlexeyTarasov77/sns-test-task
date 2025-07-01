import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  images: { remotePatterns: [{ hostname: "e7.pngegg.com" }, { hostname: "localhost" }, { hostname: "0.0.0.0" }] },
};

export default nextConfig;
