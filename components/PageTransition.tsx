"use client";

import * as React from "react";
import { motion, useReducedMotion } from "framer-motion";
import { usePathname } from "next/navigation";
import { ease } from "@/lib/motion";

export function PageTransition({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const shouldReduce = useReducedMotion();

  if (shouldReduce) {
    return <main className="flex-1 pb-24 md:pb-0">{children}</main>;
  }

  return (
    <motion.main
      key={pathname}
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: ease.smooth }}
      className="flex-1 pb-24 md:pb-0"
    >
      {children}
    </motion.main>
  );
}
