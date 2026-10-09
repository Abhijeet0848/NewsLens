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
import { Home, FileText, Layers, BarChart3 } from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { href: "/", label: "Home", icon: Home },
  { href: "/classify", label: "Classifier", icon: FileText },
  { href: "/batch", label: "Batch", icon: Layers },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
];

export function MobileBottomNav() {
  const pathname = usePathname();
  const shouldReduceMotion = useReducedMotion();
  const { scrollY } = useScroll();
  const [hidden, setHidden] = React.useState(false);
  const hiddenRef = React.useRef(false);
  const lastScrollY = React.useRef(0);

  useMotionValueEvent(scrollY, "change", (latest) => {
    const diff = latest - lastScrollY.current;
    if (latest > 50 && diff > 8) {
      if (!hiddenRef.current) {
        hiddenRef.current = true;
        setHidden(true); // scrolling down
      }
    } else if (diff < -8 || latest <= 20) {
      if (hiddenRef.current) {
        hiddenRef.current = false;
        setHidden(false); // scrolling up or near top
      }
    }
    lastScrollY.current = latest;
  });

  return (
    <motion.nav
      role="navigation"
      aria-label="Mobile Navigation"
      initial={shouldReduceMotion ? false : { y: 100, opacity: 0 }}
      animate={{
        y: hidden ? 90 : 0,
        opacity: hidden ? 0 : 1,
      }}
      transition={{ duration: 0.25, ease: [0.22, 1, 0.36, 1] }}
      className="fixed bottom-4 left-4 right-4 z-50 h-16 rounded-2xl bg-[#fdfcfb]/95 backdrop-blur-md border border-[#e7e3dd] shadow-[0_8px_24px_rgba(28,27,26,0.10),0_2px_6px_rgba(28,27,26,0.06)] pb-[env(safe-area-inset-bottom)] md:hidden flex items-center justify-around px-2 pointer-events-auto select-none"
    >
      {NAV_ITEMS.map((item) => {
        const isActive = pathname === item.href;
        const Icon = item.icon;

        return (
          <Link
            key={item.href}
            href={item.href}
            prefetch={true}
            aria-current={isActive ? "page" : undefined}
            aria-label={item.label}
            className="relative flex-1 h-full py-2 flex flex-col items-center justify-center gap-1 rounded-xl active:scale-95 transition-transform duration-150 focus-visible:ring-2 focus-visible:ring-[#0f0f0e]/20 ring-offset-2 ring-offset-[#f7f6f3] outline-none"
          >
            {isActive && (
              <motion.div
                layoutId={shouldReduceMotion ? undefined : "mobile-nav-active-pill"}
                className="absolute inset-1 rounded-xl bg-[#f1efeb] -z-10 shadow-xs"
                transition={{ type: "spring", stiffness: 400, damping: 32 }}
              />
            )}
            <Icon
              className={cn(
                "size-5 transition-colors duration-150",
                isActive ? "text-[#0f0f0e]" : "text-[#6b6660]"
              )}
            />
            <span
              className={cn(
                "text-[10px] tracking-tight transition-colors duration-150 leading-none",
                isActive
                  ? "text-[#0f0f0e] font-semibold"
                  : "text-[#6b6660] font-medium"
              )}
            >
              {item.label}
            </span>
          </Link>
        );
      })}
    </motion.nav>
  );
}
