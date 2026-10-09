"use client";

import * as React from "react";
import { motion, useReducedMotion } from "framer-motion";
import { cn } from "@/lib/utils";

export interface LogoProps {
  size?: number;
  showWordmark?: boolean;
  variant?: "primary" | "filled" | "dark" | "light";
  className?: string;
  animate?: boolean;
}

export function Logo({
  size = 32,
  showWordmark = true,
  variant = "primary",
  className,
  animate = true,
}: LogoProps) {
  const shouldReduceMotion = useReducedMotion();

  // Color & background styling per variant
  const getContainerStyles = () => {
    switch (variant) {
      case "dark":
        return {
          background: "#0f0f0e",
          border: "none",
          shadow: "shadow-sm shadow-black/10",
        };
      case "light":
        return {
          background: "#ffffff",
          border: "1px solid #e7e3dd",
          shadow: "shadow-xs",
        };
      case "primary":
      case "filled":
      default:
        return {
          background: "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
          border: "none",
          shadow: "shadow-sm shadow-indigo-500/20",
        };
    }
  };

  const styles = getContainerStyles();
  const glyphStrokeColor = variant === "light" ? "#0f0f0e" : "white";
  const iconSize = size * 0.56;

  return (
    <div className={cn("inline-flex items-center gap-2 select-none", className)}>
      <motion.div
        whileHover={animate && !shouldReduceMotion ? { scale: 1.05 } : undefined}
        transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
        className={cn(
          "rounded-lg flex items-center justify-center shrink-0 transition-transform",
          styles.shadow
        )}
        style={{
          width: size,
          height: size,
          background: styles.background,
          border: styles.border,
        }}
      >
        {variant === "filled" ? (
          /* Filled 3-Facet Fold Glyph (for Hero/Feature usage) */
          <svg
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            style={{ width: iconSize, height: iconSize }}
          >
            {/* Back facet (top-right triangle, lighter) */}
            <path d="M14 4 L20 4 L20 10 Z" fill="white" fillOpacity="0.35" />

            {/* Middle facet (right side) */}
            <path d="M14 4 L20 10 L14 10 Z" fill="white" fillOpacity="0.55" />

            {/* Front facet (main face, solid) */}
            <path d="M4 4 L14 4 L14 10 L14 20 L4 20 Z" fill="white" fillOpacity="1" />

            {/* Fold line highlight */}
            <path d="M14 4 L14 20" stroke="white" strokeWidth="0.5" strokeOpacity="0.4" />

            {/* Corner accent on folded tip */}
            <path
              d="M17 4 L20 4 L20 7"
              stroke="white"
              strokeWidth="1"
              strokeLinecap="round"
              strokeOpacity="0.9"
              fill="none"
            />
          </svg>
        ) : (
          /* Minimal Line Art Fold Glyph (Primary: Folded Newspaper Page + Crease Lines) */
          <svg
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            style={{ width: iconSize, height: iconSize }}
          >
            {/* Main document outline */}
            <path
              d="M5 4 H15 L20 9 V20 H5 Z"
              stroke={glyphStrokeColor}
              strokeWidth="1.8"
              strokeLinejoin="round"
              strokeLinecap="round"
              fill="none"
            />

            {/* Fold line (diagonal corner) */}
            <path
              d="M15 4 V9 H20"
              stroke={glyphStrokeColor}
              strokeWidth="1.8"
              strokeLinejoin="round"
              strokeLinecap="round"
              fill="none"
            />

            {/* Fold crease & headline lines */}
            <path
              d="M10 12 H15"
              stroke={glyphStrokeColor}
              strokeWidth="1.5"
              strokeLinecap="round"
              opacity={variant === "light" ? "0.6" : "0.7"}
            />
            <path
              d="M10 15 H15"
              stroke={glyphStrokeColor}
              strokeWidth="1.5"
              strokeLinecap="round"
              opacity={variant === "light" ? "0.45" : "0.5"}
            />
            <path
              d="M10 18 H13"
              stroke={glyphStrokeColor}
              strokeWidth="1.5"
              strokeLinecap="round"
              opacity={variant === "light" ? "0.3" : "0.3"}
            />
          </svg>
        )}
      </motion.div>

      {showWordmark && (
        <span
          className="font-heading font-semibold tracking-tight text-[#0f0f0e] leading-none"
          style={{ fontSize: Math.max(13, Math.round(size * 0.47)) }}
        >
          NewsScope
        </span>
      )}
    </div>
  );
}
