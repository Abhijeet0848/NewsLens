"use client";

import * as React from "react";
import Link from "next/link";
import { ArrowLeft, Home } from "lucide-react";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";

export default function NotFound() {
  return (
    <div className="relative flex min-h-[70vh] flex-col items-center justify-center px-6 text-center overflow-hidden">
      {/* Centered Aurora Blob (Clean, no dot grid) */}
      <div className="pointer-events-none absolute inset-0 -z-10 flex items-center justify-center">
        <div className="h-[450px] w-[600px] rounded-full bg-[radial-gradient(ellipse_at_center,_rgba(139,92,246,0.15),transparent_65%)] blur-3xl" />
      </div>

      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
        className="max-w-md space-y-4"
      >
        <span className="text-7xl font-bold tracking-tight text-[#0f0f0e] font-mono tabular-nums block">
          404
        </span>
        <h1 className="text-2xl font-semibold text-[#0f0f0e] tracking-tight">
          Page Not Found
        </h1>
        <p className="text-[14px] text-[#57534e] leading-relaxed">
          The classification route or resource you are looking for does not exist or has been relocated.
        </p>

        <div className="pt-4 flex justify-center gap-3">
          <Link href="/">
            <Button className="h-10 px-5 gap-2 rounded-xl text-xs font-semibold shadow-sm">
              <Home className="size-4" />
              <span>Back to Home</span>
            </Button>
          </Link>
          <Link href="/classify">
            <Button variant="secondary" className="h-10 px-5 gap-2 rounded-xl text-xs font-medium border border-[#e7e3dd] text-[#3f3d3a]">
              <ArrowLeft className="size-4 text-[#6b6660]" />
              <span>Classifier</span>
            </Button>
          </Link>
        </div>
      </motion.div>
    </div>
  );
}
