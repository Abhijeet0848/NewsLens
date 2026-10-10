"use client";

import * as React from "react";
import Link from "next/link";
import { ArrowLeft, Home, FileText, BarChart3, Search } from "lucide-react";
import { motion } from "framer-motion";

export default function NotFound() {
  return (
    <div className="relative flex min-h-[75vh] flex-col items-center justify-center px-6 py-16 text-center overflow-hidden">
      {/* Background Subtle Gradient Aura */}
      <div className="pointer-events-none absolute inset-0 -z-10 flex items-center justify-center">
        <div className="h-[480px] w-[640px] rounded-full bg-[radial-gradient(ellipse_at_center,_rgba(79,70,229,0.08),transparent_65%)] blur-3xl" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 12, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
        className="max-w-lg space-y-6"
      >
        {/* Eyebrow & Status */}
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#f1efeb] border border-[#e7e3dd] text-[11px] font-mono font-medium text-[#57534e]">
          <span className="size-2 rounded-full bg-[#ef4444]" />
          <span>ERROR 404 &bull; ROUTE NOT FOUND</span>
        </div>

        {/* Hero 404 Display */}
        <div className="space-y-2">
          <h1 className="text-7xl sm:text-8xl font-extrabold tracking-tight text-[#0f0f0e] font-mono tabular-nums leading-none">
            404
          </h1>
          <h2 className="font-heading text-2xl sm:text-3xl font-bold tracking-tight text-[#0f0f0e]">
            Page Out of Range
          </h2>
          <p className="text-[14px] text-[#57534e] max-w-md mx-auto leading-relaxed">
            The article, route, or analysis view you requested does not exist or has been shifted in the taxonomy.
          </p>
        </div>

        {/* Primary Action Buttons */}
        <div className="pt-2 flex flex-wrap items-center justify-center gap-3">
          <Link
            href="/"
            className="inline-flex items-center gap-2 h-11 px-5 rounded-xl bg-[#0f0f0e] text-white text-[13px] font-medium shadow-[0_2px_8px_rgba(15,15,14,0.15)] hover:bg-[#2a2a28] hover:shadow-[0_4px_12px_rgba(15,15,14,0.20)] hover:-translate-y-px active:scale-[0.99] transition-all duration-200 focus-visible:ring-2 focus-visible:ring-[#4f46e5]/40 focus:outline-none"
          >
            <Home aria-hidden="true" className="size-4 text-white" />
            <span>Return to Home</span>
          </Link>
          <Link
            href="/classify"
            className="inline-flex items-center gap-2 h-11 px-5 rounded-xl bg-[#fdfcfb] border border-[#e7e3dd] text-[13px] font-medium text-[#0f0f0e] hover:bg-[#f1efeb] hover:border-[#d6d1c9] shadow-xs hover:-translate-y-px active:scale-[0.99] transition-all duration-200 focus-visible:ring-2 focus-visible:ring-[#4f46e5]/40 focus:outline-none"
          >
            <FileText aria-hidden="true" className="size-4 text-[#57534e]" />
            <span>Open Classifier</span>
          </Link>
        </div>

        {/* Quick Route Suggestions */}
        <div className="pt-6 border-t border-[#e7e3dd] max-w-sm mx-auto">
          <p className="text-[11px] font-mono uppercase tracking-wider text-[#57534e] block mb-3 font-semibold">
            Suggested Destinations
          </p>
          <div className="grid grid-cols-2 gap-2 text-left">
            <Link
              href="/analytics"
              className="flex items-center gap-2 p-2.5 rounded-lg bg-[#fdfcfb] border border-[#e7e3dd] hover:bg-[#f1efeb] transition-colors text-xs font-medium text-[#3f3d3a] hover:text-[#0f0f0e] focus-visible:ring-2 focus-visible:ring-[#4f46e5]/40 focus:outline-none"
            >
              <BarChart3 aria-hidden="true" className="size-3.5 text-indigo-600" />
              <span>Model Analytics</span>
            </Link>
            <Link
              href="/architecture"
              className="flex items-center gap-2 p-2.5 rounded-lg bg-[#fdfcfb] border border-[#e7e3dd] hover:bg-[#f1efeb] transition-colors text-xs font-medium text-[#3f3d3a] hover:text-[#0f0f0e] focus-visible:ring-2 focus-visible:ring-[#4f46e5]/40 focus:outline-none"
            >
              <Search aria-hidden="true" className="size-3.5 text-[#0e7490]" />
              <span>ML Architecture</span>
            </Link>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
