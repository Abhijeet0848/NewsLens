"use client";

import * as React from "react";
import Link from "next/link";
import { ArrowRight, Zap } from "lucide-react";
import { motion, useMotionValue, useTransform, animate } from "framer-motion";
import { Button } from "@/components/ui/button";
import { useClassifierStore } from "@/lib/store";
import { ease } from "@/lib/motion";

function AnimatedCount({ value, duration = 1.4 }: { value: number; duration?: number }) {
  const count = useMotionValue(0);
  const rounded = useTransform(count, (latest) => Math.round(latest).toLocaleString());

  React.useEffect(() => {
    const controls = animate(count, value, {
      duration,
      ease: ease.smooth,
    });
    return controls.stop;
  }, [value, count, duration]);

  return <motion.span className="tabular-nums">{rounded}</motion.span>;
}

export function Hero() {
  const { totalClassifiedCount } = useClassifierStore();

  return (
    <section className="relative overflow-hidden pt-12 md:pt-24 pb-12 md:pb-20 text-center">
      {/* 1. Aurora Gradient Blob & 2. Dot Grid Pattern (Hero top only) */}
      <div className="absolute inset-0 -z-10 overflow-hidden pointer-events-none select-none">
        {/* Aurora radial glow */}
        <div className="absolute left-1/2 top-0 -translate-x-1/2 h-[300px] md:h-[500px] w-[500px] md:w-[1000px] bg-[radial-gradient(ellipse_at_center,_rgba(139,92,246,0.08),transparent_60%)] blur-3xl" />
        <div className="absolute left-[20%] top-[20%] h-[200px] md:h-[350px] w-[200px] md:w-[350px] bg-[radial-gradient(circle,_rgba(6,182,212,0.05),transparent_70%)] blur-3xl" />

        {/* Fading Dot Grid pattern - masked to fade cleanly */}
        <div className="absolute inset-0 opacity-20 [background-image:radial-gradient(#d6d1c9_1px,transparent_1px)] [background-size:24px_24px] [mask-image:radial-gradient(ellipse_at_center_top,black_30%,transparent_70%)]" />

        {/* Fade to bottom page background */}
        <div className="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-[#f7f6f3] to-transparent" />
      </div>

      <div className="mx-auto max-w-4xl px-5 md:px-8 space-y-6">
        {/* Badge */}
        <motion.div
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1, ease: ease.smooth }}
          className="inline-flex items-center gap-2 rounded-full border border-[#e7e3dd] bg-[#fdfcfb] px-2.5 md:px-3.5 py-1 text-[11px] md:text-xs text-[#3f3d3a] shadow-xs font-medium max-w-[90vw] truncate"
        >
          <span className="size-1.5 rounded-full bg-indigo-500 inline-block animate-pulse flex-shrink-0" />
          <span className="font-mono text-[#3f3d3a] truncate">BBC News Dataset</span>
          <span className="text-[#6b6660]">&bull;</span>
          <span className="text-[#0f0f0e] font-semibold tabular-nums flex-shrink-0">5 Major Domains</span>
        </motion.div>

        {/* Headline */}
        <div className="space-y-1">
          <motion.h1
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.55, delay: 0.2, ease: ease.smooth }}
            className="font-heading text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight text-[#0f0f0e] leading-[1.1] md:leading-[1.05]"
          >
            Classify News Articles
          </motion.h1>

          <motion.h2
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.55, delay: 0.3, ease: ease.smooth }}
            className="font-heading text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight bg-gradient-to-r from-indigo-500 via-violet-500 to-cyan-600 bg-clip-text text-transparent leading-[1.1] md:leading-[1.05]"
          >
            in Milliseconds
          </motion.h2>
        </div>

        {/* Subheadline */}
        <motion.p
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.55, delay: 0.4, ease: ease.smooth }}
          className="mx-auto max-w-md md:max-w-2xl text-[14px] md:text-[15px] text-[#3f3d3a] leading-relaxed font-normal px-2"
        >
          Instant multi-class categorization across 5 major domains with explainable neural attention.
        </motion.p>

        {/* Single Focused CTA Button */}
        <motion.div
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.55, delay: 0.5, ease: ease.smooth }}
          className="pt-2 md:pt-4 flex items-center justify-center"
        >
          <Link href="/classify" className="inline-flex">
            <button
              type="button"
              className="group inline-flex items-center gap-2 h-11 px-6 rounded-xl bg-gradient-to-r from-indigo-500 to-violet-500 text-white text-sm font-medium tracking-normal shadow-[0_4px_14px_rgba(99,102,241,0.25)] ring-1 ring-inset ring-white/20 hover:shadow-[0_6px_20px_rgba(99,102,241,0.35)] hover:-translate-y-0.5 active:translate-y-0 active:scale-[0.98] transition-all duration-200 cursor-pointer select-none"
            >
              <Zap className="size-4 ml-0.5" strokeWidth={2.5} />
              <span>Open Classifier</span>
              <ArrowRight className="size-4 ml-1 transition-transform duration-200 group-hover:translate-x-0.5" />
            </button>
          </Link>
        </motion.div>

        {/* Real Stats Row from BBC Dataset */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.65, ease: ease.smooth }}
          className="pt-8 md:pt-10"
        >
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-10 text-center">
            {/* Stat 1 */}
            <div className="w-full sm:w-auto py-1 sm:py-0">
              <div className="font-heading text-lg md:text-xl font-bold text-[#0f0f0e] font-mono tabular-nums">
                <AnimatedCount value={totalClassifiedCount} />
              </div>
              <p className="text-[10px] md:text-[11px] font-mono font-semibold uppercase tracking-widest text-[#6b6660] mt-0.5">
                BBC News Articles
              </p>
            </div>

            {/* Mobile Horizontal Divider / Desktop Vertical Divider */}
            <div className="h-px w-12 mx-auto bg-[#e7e3dd] block sm:hidden" />
            <div className="h-6 w-px bg-[#e7e3dd] hidden sm:block" />

            {/* Stat 2 */}
            <div className="w-full sm:w-auto py-1 sm:py-0">
              <div className="font-heading text-lg md:text-xl font-bold text-[#0f0f0e] font-mono tabular-nums">
                BBC News
              </div>
              <p className="text-[10px] md:text-[11px] font-mono font-semibold uppercase tracking-widest text-[#6b6660] mt-0.5">
                Benchmark Corpus
              </p>
            </div>

            {/* Mobile Horizontal Divider / Desktop Vertical Divider */}
            <div className="h-px w-12 mx-auto bg-[#e7e3dd] block sm:hidden" />
            <div className="h-6 w-px bg-[#e7e3dd] hidden sm:block" />

            {/* Stat 3 */}
            <div className="w-full sm:w-auto py-1 sm:py-0">
              <div className="font-heading text-lg md:text-xl font-bold text-[#0f0f0e] font-mono tabular-nums">
                5
              </div>
              <p className="text-[10px] md:text-[11px] font-mono font-semibold uppercase tracking-widest text-[#6b6660] mt-0.5">
                Domains Supported
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
