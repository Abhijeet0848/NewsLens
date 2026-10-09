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
  Search,
  BrainCircuit,
  Home,
  FileText,
  Layers,
  BarChart3,
  ArrowUpRight,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useClassifierStore } from "@/lib/store";
import { Logo } from "@/components/Logo";

const NAV_LINKS = [
  { href: "/", label: "Home", icon: Home },
  { href: "/classify", label: "Classifier", icon: FileText },
  { href: "/batch", label: "Batch", icon: Layers },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
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
          className="flex items-center cursor-pointer focus-visible:ring-2 focus-visible:ring-indigo-500/30 ring-offset-2 ring-offset-[#f7f6f3] rounded-lg outline-none"
        >
          <Logo size={32} />
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

        {/* 3. Search Bar (Right) — Clean search input control */}
        <div className="hidden md:flex items-center">
          <motion.button
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.98 }}
            type="button"
            onClick={() => setCommandPaletteOpen(true)}
            aria-label="Search articles and commands"
            className="group flex items-center gap-2 h-9 w-48 lg:w-52 pl-3 pr-3 rounded-lg bg-[#fdfcfb] border border-[#e7e3dd] hover:bg-[#f1efeb] hover:border-[#d6d1c9] shadow-xs shadow-[rgba(28,27,26,0.03)] transition-colors duration-150 focus-visible:ring-2 focus-visible:ring-indigo-500/30 ring-offset-2 ring-offset-[#f7f6f3] outline-none select-none cursor-pointer text-left"
          >
            <Search
              className="size-4 text-[#6b6660] shrink-0 group-hover:text-[#3f3d3a] transition-colors"
              strokeWidth={2}
            />
            <span className="flex-1 text-[13px] text-[#a8a29e] truncate font-normal">
              Search...
            </span>
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
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              onClick={() => setMobileMenuOpen(false)}
              className="fixed inset-0 bg-[#0f0f0e]/40 backdrop-blur-sm z-40 md:hidden"
            />

            {/* Drawer Container */}
            <motion.div
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", stiffness: 260, damping: 28 }}
              drag="x"
              dragConstraints={{ left: 0, right: 0 }}
              dragElastic={{ right: 0.3 }}
              onDragEnd={(_, info) => {
                if (info.offset.x > 80 || info.velocity.x > 300) {
                  setMobileMenuOpen(false);
                }
              }}
              className="fixed top-0 right-0 z-50 h-screen h-dvh w-80 bg-[#fdfcfb] border-l border-[#e7e3dd] shadow-[-8px_0_24px_rgba(28,27,26,0.08)] md:hidden flex flex-col"
            >
              {/* Header Row */}
              <div className="flex items-center justify-between h-16 px-5 border-b border-[#e7e3dd] shrink-0">
                <div className="flex items-center gap-2">
                  <div className="flex size-8 items-center justify-center rounded-lg bg-gradient-to-br from-indigo-500 to-violet-500 text-white shadow-sm shadow-indigo-500/20">
                    <BrainCircuit className="size-4" />
                  </div>
                  <span className="text-[15px] font-semibold text-[#0f0f0e] tracking-tight">
                    NewsScope
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => setMobileMenuOpen(false)}
                  aria-label="Close navigation"
                  className="flex size-8 items-center justify-center rounded-lg bg-transparent hover:bg-[#f1efeb] text-[#57534e] transition-colors"
                >
                  <X className="size-4" />
                </button>
              </div>

              {/* Nav Items & Search */}
              <div className="flex-1 overflow-y-auto px-3 py-4 flex flex-col gap-1">
                {NAV_LINKS.map((item, index) => {
                  const isActive = pathname === item.href;
                  const Icon = item.icon;
                  return (
                    <motion.div
                      key={item.href}
                      initial={shouldReduceMotion ? undefined : { opacity: 0, x: 12 }}
                      animate={shouldReduceMotion ? undefined : { opacity: 1, x: 0 }}
                      transition={{ duration: 0.2, delay: index * 0.04 }}
                    >
                      <Link
                        href={item.href}
                        onClick={() => setMobileMenuOpen(false)}
                        aria-current={isActive ? "page" : undefined}
                        className={cn(
                          "relative flex items-center gap-3 h-11 px-3 rounded-lg text-[15px] transition-colors duration-150 select-none",
                          isActive
                            ? "bg-[#f1efeb] text-[#0f0f0e] font-semibold"
                            : "bg-transparent text-[#3f3d3a] font-medium hover:bg-[#f1efeb] hover:text-[#0f0f0e]"
                        )}
                      >
                        {isActive && (
                          <span className="absolute left-0 top-2 bottom-2 w-[3px] bg-[#0f0f0e] rounded-r-full" />
                        )}
                        <Icon
                          className={cn(
                            "size-4 shrink-0 transition-colors",
                            isActive ? "text-[#0f0f0e]" : "text-[#6b6660]"
                          )}
                        />
                        <span>{item.label}</span>
                      </Link>
                    </motion.div>
                  );
                })}

                {/* Compact Search Trigger */}
                <motion.div
                  initial={shouldReduceMotion ? undefined : { opacity: 0, x: 12 }}
                  animate={shouldReduceMotion ? undefined : { opacity: 1, x: 0 }}
                  transition={{ duration: 0.2, delay: NAV_LINKS.length * 0.04 }}
                  className="mt-2"
                >
                  <button
                    type="button"
                    onClick={() => {
                      setMobileMenuOpen(false);
                      setCommandPaletteOpen(true);
                    }}
                    className="w-full flex items-center gap-2.5 h-11 px-3 rounded-lg bg-[#f1efeb] border border-[#e7e3dd] hover:bg-[#ebe8e3] transition-colors duration-150 text-left cursor-pointer"
                  >
                    <Search className="size-4 text-[#6b6660] shrink-0" />
                    <span className="text-[14px] text-[#6b6660]">Search...</span>
                  </button>
                </motion.div>
              </div>

              {/* Footer Row (Pinned to bottom) */}
              <div className="mt-auto px-5 py-4 border-t border-[#e7e3dd] flex items-center justify-between shrink-0">
                <a
                  href="https://github.com/Abhijeet0848/NewsLens"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1 text-[13px] text-[#57534e] hover:text-[#0f0f0e] transition-colors"
                >
                  <span>GitHub</span>
                  <ArrowUpRight className="size-3.5" />
                </a>
                <span className="text-[11px] font-medium uppercase tracking-wider bg-[#eef2ff] text-[#4f46e5] border border-[#c7d2fe] rounded-full px-2.5 py-1">
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
