"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  motion,
  useScroll,
  useMotionValueEvent,
  useReducedMotion,
} from "framer-motion";
import { Search } from "lucide-react";
import { cn } from "@/lib/utils";
import { useClassifierStore } from "@/lib/store";
import { Logo } from "@/components/Logo";

const NAV_LINKS = [
  { href: "/", label: "Home" },
  { href: "/classify", label: "Classifier" },
  { href: "/batch", label: "Batch" },
  { href: "/analytics", label: "Analytics" },
];

export function Navbar() {
  const pathname = usePathname();
  const shouldReduceMotion = useReducedMotion();
  const [scrolled, setScrolled] = React.useState(false);
  const scrolledRef = React.useRef(false);
  const { scrollY } = useScroll();
  const { setCommandPaletteOpen } = useClassifierStore();

  useMotionValueEvent(scrollY, "change", (latest) => {
    const next = latest >= 20;
    if (next !== scrolledRef.current) {
      scrolledRef.current = next;
      setScrolled(next);
    }
  });

  return (
    <header
      className={cn(
        "sticky top-0 z-40 w-full h-14 transition-colors duration-200",
        scrolled
          ? "border-b border-[#e7e3dd] bg-[#f7f6f3]/95 backdrop-blur-md shadow-[0_1px_2px_rgba(28,27,26,0.03)]"
          : "border-b border-transparent bg-transparent"
      )}
    >
      <div className="relative mx-auto flex h-14 max-w-6xl items-center justify-between px-5 md:px-6">
        {/* 1. Logo (Left) */}
        <Link
          href="/"
          prefetch={true}
          className="flex items-center cursor-pointer focus-visible:ring-2 focus-visible:ring-indigo-500/30 ring-offset-2 ring-offset-[#f7f6f3] rounded-lg outline-none"
        >
          <div className="hidden sm:block">
            <Logo size={32} />
          </div>
          <div className="block sm:hidden">
            <Logo size={28} />
          </div>
        </Link>

        {/* 2. Nav Pill (Center) — Hidden on mobile, absolute true center on desktop */}
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
                prefetch={true}
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
                    layoutId={shouldReduceMotion ? undefined : "desktop-nav-active-pill"}
                    className="absolute inset-0 bg-[#fdfcfb] rounded-full shadow-[0_1px_3px_rgba(28,27,26,0.08)] -z-10"
                    transition={{ type: "spring", stiffness: 400, damping: 32 }}
                  />
                )}
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* 3. Search Bar (Right) — Desktop full input trigger */}
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
              aria-hidden="true"
              className="size-4 text-[#57534e] shrink-0 group-hover:text-[#3f3d3a] transition-colors"
              strokeWidth={2}
            />
            <span className="flex-1 text-[13px] text-[#8a847d] truncate font-normal">
              Search...
            </span>
          </motion.button>
        </div>

        {/* Mobile Search Icon Button (Right) */}
        <div className="flex md:hidden items-center">
          <motion.button
            whileTap={{ scale: 0.92 }}
            type="button"
            onClick={() => setCommandPaletteOpen(true)}
            aria-label="Search articles and commands"
            className="flex size-9 items-center justify-center rounded-lg border border-[#e7e3dd] bg-[#f1efeb] text-[#0f0f0e] hover:bg-[#ebe8e3] transition-colors focus-visible:ring-2 focus-visible:ring-[#4f46e5]/40 focus:outline-none"
          >
            <Search aria-hidden="true" className="size-4 text-[#57534e]" strokeWidth={2} />
          </motion.button>
        </div>
      </div>
    </header>
  );
}
