"use client";

import * as React from "react";
import { motion, useReducedMotion } from "framer-motion";

export const TAXONOMY_CATEGORIES = {
  business: { label: "Business", bg: "#fffbeb", border: "#fde68a", text: "#a16207" },
  entertainment: { label: "Entertainment", bg: "#fdf2f8", border: "#fbcfe8", text: "#be185d" },
  politics: { label: "Politics", bg: "#fff1f2", border: "#fecdd3", text: "#be123c" },
  sport: { label: "Sport", bg: "#ecfdf5", border: "#a7f3d0", text: "#047857" },
  tech: { label: "Tech", bg: "#ecfeff", border: "#a5f3fc", text: "#0e7490" },
} as const;

export interface CategoryPillProps {
  name: string;
  count: number | string;
  colors: {
    bg: string;
    border: string;
    text: string;
  };
}

export function CategoryPill({ name, count, colors }: CategoryPillProps) {
  const shouldReduce = useReducedMotion();

  return (
    <motion.div
      whileHover={shouldReduce ? undefined : { scale: 1.02, filter: "brightness(0.98)" }}
      transition={{ duration: 0.15 }}
      className="flex items-center gap-2 h-8 px-3 rounded-full border shrink-0 snap-start transition-colors duration-150 cursor-pointer select-none"
      style={{
        backgroundColor: colors.bg,
        borderColor: colors.border,
      }}
    >
      <span
        className="size-1.5 rounded-full shrink-0"
        style={{ backgroundColor: colors.text }}
      />
      <span
        className="text-[13px] font-medium leading-none"
        style={{ color: colors.text }}
      >
        {name}
      </span>
      {count !== undefined && count !== null && count !== 0 && (
        <span className="text-[11px] font-mono text-[#a8a29e] leading-none tabular-nums">
          {count}
        </span>
      )}
    </motion.div>
  );
}
