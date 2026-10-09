"use client";

import * as React from "react";
import { motion, useReducedMotion, type HTMLMotionProps } from "framer-motion";
import { spring } from "@/lib/motion";
import { cn } from "@/lib/utils";

export interface MotionButtonProps extends HTMLMotionProps<"button"> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "destructive";
  size?: "sm" | "default" | "lg" | "icon";
}

const variants = {
  primary:
    "bg-gradient-to-r from-indigo-500 via-indigo-600 to-violet-600 text-[#fdfcfb] shadow-sm shadow-indigo-500/20 hover:shadow-md hover:shadow-indigo-500/25",
  secondary:
    "bg-[#fdfcfb] text-[#1c1b1a] border border-[#e7e3dd] hover:bg-[#f1efeb] shadow-xs",
  outline:
    "border border-[#e7e3dd] bg-transparent text-[#1c1b1a] hover:bg-[#f1efeb]",
  ghost:
    "text-[#57534e] hover:text-[#1c1b1a] hover:bg-[#f1efeb] bg-transparent",
  destructive:
    "bg-[#fff1f2] text-[#e11d48] border border-[#fecdd3] hover:bg-[#ffe4e6]",
};

const sizes = {
  sm: "h-8 px-3 text-xs rounded-lg gap-1.5",
  default: "h-10 px-4 py-2 text-sm rounded-lg gap-2",
  lg: "h-12 px-6 text-base rounded-xl gap-2.5 font-medium",
  icon: "h-9 w-9 rounded-lg flex items-center justify-center p-0",
};

export const Button = React.forwardRef<HTMLButtonElement, MotionButtonProps>(
  (
    {
      className,
      variant = "primary",
      size = "default",
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    const shouldReduce = useReducedMotion();

    return (
      <motion.button
        ref={ref}
        whileHover={disabled || shouldReduce ? undefined : { y: -1 }}
        whileTap={disabled || shouldReduce ? undefined : { scale: 0.97 }}
        transition={spring.snappy}
        disabled={disabled}
        className={cn(
          "inline-flex items-center justify-center whitespace-nowrap font-medium transition-colors select-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500/30 ring-offset-2 ring-offset-[#f7f6f3] disabled:pointer-events-none disabled:opacity-50 cursor-pointer",
          variants[variant],
          sizes[size],
          className
        )}
        {...props}
      >
        {children}
      </motion.button>
    );
  }
);

Button.displayName = "Button";
