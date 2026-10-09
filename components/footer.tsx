"use client";

import * as React from "react";
import Link from "next/link";
import { motion, AnimatePresence, useReducedMotion } from "framer-motion";
import {
  BrainCircuit,
  ArrowUpRight,
  FileText,
  BarChart3,
  Github,
  ArrowUp,
} from "lucide-react";
import { ease } from "@/lib/motion";

export function Footer() {
  const shouldReduceMotion = useReducedMotion();
  const [showBackToTop, setShowBackToTop] = React.useState(false);

  React.useEffect(() => {
    const handleScroll = () => {
      setShowBackToTop(window.scrollY > 400);
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToTop = () => {
    if (typeof window !== "undefined") {
      const lenis = (window as any).__lenis;
      if (lenis) {
        lenis.scrollTo(0, { duration: 1.2 });
      } else {
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
    }
  };

  return (
    <>
      <motion.footer
        initial={shouldReduceMotion ? false : { opacity: 0, y: 20 }}
        whileInView={shouldReduceMotion ? false : { opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-60px" }}
        transition={{ duration: 0.6, ease: ease.smooth }}
        className="border-t border-[#e7e3dd] bg-[#edeae4] text-[#3f3d3a] pt-16 pb-8 transition-colors"
      >
        <div className="mx-auto max-w-6xl px-5 md:px-8">
          {/* Main 4-Column Grid */}
          <div className="grid grid-cols-12 gap-8 md:gap-10 lg:gap-12">
            {/* Zone 1: Brand Column (Col 5) */}
            <motion.div
              initial={shouldReduceMotion ? false : { opacity: 0, y: 12 }}
              whileInView={shouldReduceMotion ? false : { opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0, ease: ease.smooth }}
              className="col-span-12 md:col-span-5 space-y-4"
            >
              <div className="flex items-center gap-2.5">
                <div className="flex size-9 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-violet-500 text-[#fdfcfb] shadow-xs flex-shrink-0">
                  <BrainCircuit className="size-4.5" />
                </div>
                <span className="text-[15px] font-semibold tracking-tight text-[#0f0f0e] font-heading leading-none">
                  NewsScope
                </span>
              </div>

              <p className="text-[13px] text-[#57534e] leading-relaxed max-w-sm mt-4">
                Industrial ML for sub-millisecond news classification with explainable neural attention.
              </p>

              <p className="text-[12px] text-[#6b6660] font-mono mt-4">
                Fine-tuned on the BBC News corpus
              </p>
            </motion.div>

            {/* Zone 2: Product Links (Col 3 on desktop, Col 6 on mobile) */}
            <motion.div
              initial={shouldReduceMotion ? false : { opacity: 0, y: 12 }}
              whileInView={shouldReduceMotion ? false : { opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.08, ease: ease.smooth }}
              className="col-span-6 md:col-span-3"
            >
              <h4 className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[#8a847d] font-mono mb-4">
                Product & Routes
              </h4>
              <ul className="space-y-2.5 text-[13px]">
                <li>
                  <Link
                    href="/classify"
                    className="group flex items-center gap-1 text-[#3f3d3a] font-medium hover:text-[#0f0f0e] transition-colors py-0.5"
                  >
                    <span>Live Classifier</span>
                    <ArrowUpRight className="size-3 opacity-70 md:opacity-0 -translate-x-0.5 md:-translate-x-1 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-200 text-indigo-600" />
                  </Link>
                </li>
                <li>
                  <Link
                    href="/batch"
                    className="group flex items-center gap-1 text-[#3f3d3a] font-medium hover:text-[#0f0f0e] transition-colors py-0.5"
                  >
                    <span>Bulk CSV</span>
                    <ArrowUpRight className="size-3 opacity-70 md:opacity-0 -translate-x-0.5 md:-translate-x-1 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-200 text-indigo-600" />
                  </Link>
                </li>
                <li>
                  <Link
                    href="/analytics"
                    className="group flex items-center gap-1 text-[#3f3d3a] font-medium hover:text-[#0f0f0e] transition-colors py-0.5"
                  >
                    <span>Model Metrics</span>
                    <ArrowUpRight className="size-3 opacity-70 md:opacity-0 -translate-x-0.5 md:-translate-x-1 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-200 text-indigo-600" />
                  </Link>
                </li>
                <li>
                  <Link
                    href="/about"
                    className="group flex items-center gap-1 text-[#3f3d3a] font-medium hover:text-[#0f0f0e] transition-colors py-0.5"
                  >
                    <span>Architecture</span>
                    <ArrowUpRight className="size-3 opacity-70 md:opacity-0 -translate-x-0.5 md:-translate-x-1 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-200 text-indigo-600" />
                  </Link>
                </li>
              </ul>
            </motion.div>

            {/* Zone 3: Tech Stack (Col 2 on desktop, Col 6 on mobile) */}
            <motion.div
              initial={shouldReduceMotion ? false : { opacity: 0, y: 12 }}
              whileInView={shouldReduceMotion ? false : { opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.16, ease: ease.smooth }}
              className="col-span-6 md:col-span-2"
            >
              <h4 className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[#8a847d] font-mono mb-4">
                Tech Stack
              </h4>
              <ul className="space-y-2.5 text-[13px] text-[#3f3d3a] font-medium">
                <li className="py-0.5 hover:text-[#0f0f0e] transition-colors">Next.js 14</li>
                <li className="py-0.5 hover:text-[#0f0f0e] transition-colors">TypeScript</li>
                <li className="py-0.5 hover:text-[#0f0f0e] transition-colors">PyTorch</li>
                <li className="py-0.5 hover:text-[#0f0f0e] transition-colors">FastAPI</li>
              </ul>
            </motion.div>

            {/* Zone 4: Meta / Status Column (Col 2 on desktop, Col 12 on mobile) */}
            <motion.div
              initial={shouldReduceMotion ? false : { opacity: 0, y: 12 }}
              whileInView={shouldReduceMotion ? false : { opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.24, ease: ease.smooth }}
              className="col-span-12 md:col-span-2 flex flex-col justify-start md:items-end text-left md:text-right pt-2 md:pt-0"
            >
              <h4 className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[#8a847d] font-mono mb-4">
                System
              </h4>
              <div className="space-y-2">
                <div className="inline-flex items-center gap-1.5 text-[11px] font-medium text-[#3f3d3a]">
                  <span className="size-1.5 rounded-full bg-emerald-500 animate-pulse flex-shrink-0" />
                  <span>All systems operational</span>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Divider & Row 3: Bottom Bar */}
          <div className="mt-12 border-t border-[#e7e3dd] pt-6 flex flex-col md:flex-row md:justify-between md:items-center gap-4 text-[12px] text-[#6b6660]">
            {/* Left: Copyright */}
            <p className="text-center md:text-left">
              &copy; 2025 NewsScope Engine &bull; MIT License
            </p>

            {/* Right: Legal & Resource Links with icons */}
            <div className="flex flex-wrap items-center justify-center md:justify-end gap-5 md:gap-6">
              <Link
                href="/about"
                className="flex items-center gap-1.5 text-[12px] text-[#6b6660] hover:text-[#0f0f0e] transition-colors py-1"
              >
                <FileText className="size-3.5 text-[#6b6660]" />
                <span>Documentation</span>
              </Link>
              <Link
                href="/analytics"
                className="flex items-center gap-1.5 text-[12px] text-[#6b6660] hover:text-[#0f0f0e] transition-colors py-1"
              >
                <BarChart3 className="size-3.5 text-[#6b6660]" />
                <span>API Benchmarks</span>
              </Link>
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Source code on GitHub"
                className="flex items-center gap-1.5 text-[12px] text-[#6b6660] hover:text-[#0f0f0e] transition-colors py-1"
              >
                <Github className="size-3.5 text-[#6b6660]" />
                <span>Source Code</span>
              </a>
            </div>
          </div>
        </div>
      </motion.footer>

      {/* Floating Back to Top Button: bottom-5 right-5 on mobile, bottom-8 right-8 on desktop */}
      <AnimatePresence>
        {showBackToTop && (
          <motion.button
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.9 }}
            whileHover={{ scale: 1.08 }}
            whileTap={{ scale: 0.92 }}
            onClick={scrollToTop}
            aria-label="Scroll back to top"
            className="fixed bottom-5 right-5 md:bottom-8 md:right-8 z-30 flex size-9 md:size-10 items-center justify-center rounded-full bg-[#fdfcfb] border border-[#e7e3dd] text-[#3f3d3a] hover:text-[#0f0f0e] hover:bg-[#f1efeb] shadow-[0_4px_16px_rgba(15,15,14,0.12)] transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
          >
            <ArrowUp className="size-4" />
          </motion.button>
        )}
      </AnimatePresence>
    </>
  );
}
