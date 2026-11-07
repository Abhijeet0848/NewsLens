/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  devIndicators: {
    buildActivity: false,
  },
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
  async redirects() {
    return [
      {
        source: "/classifier",
        destination: "/classify",
        permanent: false,
      },
    ];
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
