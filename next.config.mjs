/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  experimental: {
    serverComponentsExternalPackages: ["scikit-learn"],
    outputFileTracingIncludes: {
      "/api/classify": ["./models/**/*"],
    },
  },
};

export default nextConfig;
