"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  motion,
  AnimatePresence,
  useScroll,
  useMotionValueEvent,
  useReducedMotion,
} from "framer-motion";
import {
  Menu,
  X,
  BrainCircuit,
  Search,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useClassifierStore } from "@/lib/store";

const NAV_LINKS = [
  { href: "/", label: "Home" },
  { href: "/classify", label: "Classifier" },
  { href: "/batch", label: "Batch" },
  { href: "/analytics", label: "Analytics" },
];

export function Navbar() {
  const pathname = usePathname();
  const shouldReduceMotion = useReducedMotion();
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);
  const [scrolled, setScrolled] = React.useState(false);
  const { scrollY } = useScroll();
  const { setCommandPaletteOpen } = useClassifierStore();

  useMotionValueEvent(scrollY, "change", (latest) => {
    setScrolled(latest >= 20);
  });

  return (
    <header
      className={cn(
        "sticky top-0 z-50 w-full h-14 transition-all duration-250 ease-out",
        scrolled
          ? "border-b border-[#e7e3dd] bg-[#f7f6f3]/85 backdrop-blur-xl shadow-[0_1px_2px_rgba(28,27,26,0.03)]"
          : "border-b border-transparent bg-transparent"
      )}
    >
        <div className="relative mx-auto flex h-14 max-w-6xl items-center justify-between px-5 md:px-6">
        {/* 1. Logo (Left) — 28px/32px icon, 14px/15px wordmark */}
        <Link
          href="/"
          className="flex items-center gap-2 cursor-pointer focus-visible:ring-2 focus-visible:ring-indigo-500/30 ring-offset-2 ring-offset-[#f7f6f3] rounded-lg outline-none"
        >
          <div className="flex size-7 md:size-8 items-center justify-center rounded-lg bg-gradient-to-br from-indigo-500 to-violet-500 shadow-sm shadow-indigo-500/20 text-[#fdfcfb] flex-shrink-0">
            <BrainCircuit className="size-3.5 md:size-4" />
          </div>
          <span className="font-heading text-sm md:text-[15px] font-semibold tracking-tight text-[#0f0f0e] leading-none">
            NewsScope
          </span>
        </Link>

        {/* 2. Nav Pill (Center) — Hidden on mobile, absolute true center */}
        <nav
          aria-label="Main Navigation"
          className="hidden md:inline-flex items-center gap-0.5 h-10 rounded-full border border-[#e7e3dd] bg-[#f1efeb] px-1 py-1 absolute left-1/2 -translate-x-1/2 top-1/2 -translate-y-1/2"
        >
          {NAV_LINKS.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                aria-current={isActive ? "page" : undefined}
                className={cn(
                  "relative h-8 px-3 lg:px-3.5 rounded-full text-[13px] font-medium leading-none flex items-center justify-center transition-colors duration-150 z-10 focus-visible:ring-2 focus-visible:ring-indigo-500/30 ring-offset-2 ring-offset-[#f7f6f3] outline-none select-none",
                  isActive
                    ? "text-[#0f0f0e] font-semibold"
                    : "text-[#57534e] hover:text-[#0f0f0e] hover:bg-[#e7e3dd]/50"
                )}
              >
                {isActive && (
                  <motion.div
                    layoutId={shouldReduceMotion ? undefined : "nav-active"}
                    className="absolute inset-0 bg-[#fdfcfb] rounded-full shadow-[0_1px_3px_rgba(28,27,26,0.08)] -z-10"
                    transition={{ type: "spring", stiffness: 400, damping: 30 }}
                  />
                )}
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* 3. ⌘K Button (Right) — Hidden on mobile, matches h-10 nav height */}
        <div className="hidden md:flex items-center">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.97 }}
            type="button"
            onClick={() => setCommandPaletteOpen(true)}
            aria-label="Open Command Palette (⌘K)"
            className="flex items-center gap-2.5 h-10 px-4 rounded-full bg-[#fdfcfb] border border-[#e7e3dd] text-[#3f3d3a] shadow-sm shadow-[rgba(28,27,26,0.04)] hover:bg-[#f1efeb] hover:text-[#0f0f0e] hover:border-[#d6d1c9] hover:shadow-md hover:shadow-[rgba(28,27,26,0.06)] transition-all duration-150 focus-visible:ring-2 focus-visible:ring-indigo-500/30 ring-offset-2 ring-offset-[#f7f6f3] outline-none select-none cursor-pointer"
          >
            <Search className="size-4 text-[#6b6660]" strokeWidth={2} />
            <kbd className="flex items-center gap-0.5 text-[13px] font-sans font-medium tracking-normal leading-none">
              <span className="text-[15px] leading-none">⌘</span>
              <span>K</span>
            </kbd>
          </motion.button>
        </div>

        {/* Mobile Hamburger Menu Toggle */}
        <div className="flex md:hidden items-center">
          <motion.button
            whileTap={{ scale: 0.92 }}
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
            className="flex size-9 items-center justify-center rounded-lg border border-[#e7e3dd] bg-[#f1efeb] text-[#0f0f0e] hover:bg-[#ebe8e3] transition-colors"
          >
            {mobileMenuOpen ? <X className="size-5" /> : <Menu className="size-5" />}
          </motion.button>
        </div>
      </div>

      {/* Mobile Drawer */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              onClick={() => setMobileMenuOpen(false)}
              className="fixed inset-0 bg-[#0f0f0e]/30 backdrop-blur-sm z-40 md:hidden"
            />
            <motion.div
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", stiffness: 260, damping: 28 }}
              className="fixed inset-y-0 right-0 w-72 border-l border-[#e7e3dd] bg-[#fdfcfb] p-6 shadow-2xl z-50 md:hidden flex flex-col justify-between"
            >
              <div className="space-y-6">
                {/* Drawer Header with Close Button */}
                <div className="flex items-center justify-between pb-4 border-b border-[#e7e3dd]">
                  <div className="flex items-center gap-2">
                    <div className="flex size-7 items-center justify-center rounded-lg bg-gradient-to-br from-indigo-500 to-violet-500 text-[#fdfcfb]">
                      <BrainCircuit className="size-3.5" />
                    </div>
                    <span className="font-heading text-sm font-semibold tracking-tight text-[#0f0f0e]">
                      NewsScope
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={() => setMobileMenuOpen(false)}
                    aria-label="Close navigation"
                    className="flex size-8 items-center justify-center rounded-lg border border-[#e7e3dd] bg-[#f1efeb] text-[#0f0f0e] hover:bg-[#ebe8e3]"
                  >
                    <X className="size-4" />
                  </button>
                </div>

                {/* Nav items stacked */}
                <div className="flex flex-col divide-y divide-[#f1efeb]">
                  {NAV_LINKS.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                      <Link
                        key={item.href}
                        href={item.href}
                        onClick={() => setMobileMenuOpen(false)}
                        aria-current={isActive ? "page" : undefined}
                        className={cn(
                          "relative flex items-center py-3 px-4 text-base transition-colors",
                          isActive
                            ? "text-[#0f0f0e] font-semibold bg-[#f1efeb]/60 rounded-lg"
                            : "text-[#3f3d3a] font-medium hover:text-[#0f0f0e] hover:bg-[#f1efeb]/40 rounded-lg"
                        )}
                      >
                        {isActive && (
                          <div className="w-1 bg-indigo-500 rounded-full h-5 absolute left-1.5" />
                        )}
                        <span>{item.label}</span>
                      </Link>
                    );
                  })}
                </div>

                {/* Gap below: ⌘K Search trigger */}
                <div className="pt-2">
                  <button
                    type="button"
                    onClick={() => {
                      setMobileMenuOpen(false);
                      setCommandPaletteOpen(true);
                    }}
                    className="w-full flex items-center justify-center gap-2 rounded-xl border border-[#e7e3dd] bg-[#f1efeb] px-4 py-3 text-sm font-medium text-[#3f3d3a] hover:bg-[#ebe8e3] hover:text-[#0f0f0e] shadow-xs transition-colors"
                  >
                    <Search className="size-4 text-[#6b6660]" />
                    <span>⌘K Search</span>
                  </button>
                </div>
              </div>

              {/* Bottom: GitHub & Status info */}
              <div className="pt-6 border-t border-[#e7e3dd] flex items-center justify-between text-xs text-[#6b6660]">
                <a
                  href="https://github.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="font-mono hover:text-[#0f0f0e] transition-colors py-1"
                >
                  GitHub Repository &rarr;
                </a>
                <span className="font-mono text-[11px] text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
                  BBC Corpus
                </span>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </header>
  );
}
