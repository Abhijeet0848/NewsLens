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
      "/api/**/*": ["./models/**/*"],
    },
  },
  async rewrites() {
    return [
      {
        source: "/api/classify",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8000/api/classify"
            : "/api/classify.py",
      },
      {
        source: "/api/health",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8000/api/health"
            : "/api/health.py",
      },
    ];
  },
};

export default nextConfig;
