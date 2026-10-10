import type { Metadata, Viewport } from "next";

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
};
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import "katex/dist/katex.min.css";
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { SmoothScroll } from "@/components/SmoothScroll";
import { ScrollProgress } from "@/components/ScrollProgress";
import { PageTransition } from "@/components/PageTransition";
import { MobileBottomNav } from "@/components/MobileBottomNav";
import { RoutePrefetcher } from "@/components/RoutePrefetcher";
import { CommandPalette } from "@/components/CommandPalette";
import { Toaster } from "sonner";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
  preload: true,
  weight: ["400", "500", "600"],
});

const mono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
  preload: true,
  weight: ["400", "500"],
});

export const metadata: Metadata = {
  title: "NewsScope — News Article Classifier",
  description: "AI-powered news classification across 5 domains.",
  metadataBase: new URL("https://newsscope.vercel.app"),
  openGraph: {
    title: "NewsScope — News Article Classifier",
    description: "AI-powered news classification across 5 domains.",
    images: ["/opengraph-image"],
    type: "website",
    siteName: "NewsScope",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "NewsScope — News Article Classifier",
    description: "AI-powered news classification across 5 domains.",
    images: ["/opengraph-image"],
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${mono.variable} scroll-smooth antialiased`}>
      <body
        className="font-sans min-h-screen bg-[#f7f6f3] text-[#0f0f0e] selection:bg-indigo-500 selection:text-[#fdfcfb] flex flex-col antialiased"
      >
        <SmoothScroll>
          <ScrollProgress />
          <Navbar />
          <PageTransition>{children}</PageTransition>
          <Footer />
        </SmoothScroll>
        <MobileBottomNav />
        <RoutePrefetcher />
        <CommandPalette />
        <Toaster
          position="bottom-right"
          theme="light"
          toastOptions={{
            style: {
              background: "#fdfcfb",
              border: "1px solid #e7e3dd",
              color: "#0f0f0e",
              boxShadow: "0 4px 12px rgba(28, 27, 26, 0.06)",
            },
          }}
        />
      </body>
    </html>
  );
}
