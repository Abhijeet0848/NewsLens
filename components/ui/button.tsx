import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-lg text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500/20 focus-visible:ring-offset-2 focus-visible:ring-offset-[#f7f6f3] disabled:pointer-events-none disabled:opacity-50 active:scale-[0.98]",
  {
    variants: {
      variant: {
        default:
          "bg-gradient-to-r from-indigo-500 via-indigo-600 to-violet-600 text-[#fdfcfb] shadow-[0_4px_12px_rgba(99,102,241,0.25)] hover:brightness-105",
        destructive:
          "bg-[#fff1f2] text-[#e11d48] border border-[#fecdd3] hover:bg-[#ffe4e6]",
        outline:
          "border border-[#e7e3dd] bg-[#fdfcfb] text-[#1c1b1a] hover:bg-[#f1efeb] shadow-sm",
        secondary:
          "bg-[#fdfcfb] text-[#1c1b1a] border border-[#e7e3dd] hover:bg-[#f1efeb] shadow-sm",
        ghost:
          "text-[#57534e] hover:text-[#1c1b1a] hover:bg-[#f1efeb]",
        link: "text-indigo-600 underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2 text-xs font-medium",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-12 rounded-lg px-8 text-sm font-semibold",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
