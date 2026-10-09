"use client";

import * as React from "react";
import Link from "next/link";

export default function ButtonTestPage() {
  const variations = [
    {
      id: "var-1",
      number: 1,
      title: "VARIATION 1 — Linear Ghost",
      techDesc: "Linear ghost · h-10 · rounded-lg · outline",
      button: (
        <Link href="/classify" className="inline-flex">
          <button
            type="button"
            className="inline-flex items-center justify-center h-10 px-5 rounded-lg bg-transparent border border-[#d6d1c9] text-[#0f0f0e] text-sm font-medium hover:bg-[#f1efeb] hover:border-[#a8a29e] transition-colors duration-200 cursor-pointer select-none"
          >
            Open Classifier
          </button>
        </Link>
      ),
    },
    {
      id: "var-2",
      number: 2,
      title: "VARIATION 2 — Vercel Solid Pill",
      techDesc: "Vercel solid pill · h-11 · rounded-full · solid black",
      button: (
        <Link href="/classify" className="inline-flex">
          <button
            type="button"
            className="inline-flex items-center justify-center h-11 px-7 rounded-full bg-[#0f0f0e] text-white text-sm font-medium hover:bg-[#2a2a28] transition-colors duration-200 cursor-pointer select-none"
          >
            Open Classifier
          </button>
        </Link>
      ),
    },
    {
      id: "var-3",
      number: 3,
      title: "VARIATION 3 — Stripe Solid Indigo",
      techDesc: "Stripe solid indigo · h-10 · rounded-md · shadow-sm",
      button: (
        <Link href="/classify" className="inline-flex">
          <button
            type="button"
            className="inline-flex items-center justify-center h-10 px-4 rounded-md bg-[#635bff] text-white text-[14px] font-medium shadow-sm hover:bg-[#5851e6] transition-colors duration-200 cursor-pointer select-none"
          >
            Open Classifier
          </button>
        </Link>
      ),
    },
    {
      id: "var-4",
      number: 4,
      title: "VARIATION 4 — Apple Pill",
      techDesc: "Apple pill · h-11 · rounded-full · solid blue",
      button: (
        <Link href="/classify" className="inline-flex">
          <button
            type="button"
            className="inline-flex items-center justify-center h-11 px-7 rounded-full bg-[#0071e3] text-white text-[15px] font-normal hover:bg-[#0077ed] transition-colors duration-200 cursor-pointer select-none"
          >
            Open Classifier
          </button>
        </Link>
      ),
    },
    {
      id: "var-5",
      number: 5,
      title: "VARIATION 5 — Notion Soft",
      techDesc: "Notion soft · h-9 · rounded-md · light card outline",
      button: (
        <Link href="/classify" className="inline-flex">
          <button
            type="button"
            className="inline-flex items-center justify-center h-9 px-4 rounded-md bg-[#ffffff] border border-[#e7e3dd] text-[#0f0f0e] text-sm font-medium hover:bg-[#f7f6f3] shadow-xs transition-colors duration-200 cursor-pointer select-none"
          >
            Open Classifier
          </button>
        </Link>
      ),
    },
  ];

  return (
    <div className="min-h-screen bg-[#f7f6f3] text-[#0f0f0e] py-20 px-5 md:px-8">
      <div className="mx-auto max-w-3xl">
        {/* Page Title & Intro */}
        <div className="mb-16 text-center space-y-2">
          <span className="text-[11px] font-mono font-semibold uppercase tracking-widest text-[#0891b2] block">
            LAB & EXPERIMENTS
          </span>
          <h1 className="font-heading text-3xl font-bold tracking-tight text-[#0f0f0e]">
            Hero CTA Button Showcase
          </h1>
          <p className="text-sm text-[#6b6660]">
            Review all 5 button variations in authentic hero context to pick your favorite.
          </p>
        </div>

        {/* Variations List */}
        <div className="space-y-0">
          {variations.map((v, index) => (
            <div key={v.id}>
              <div className="text-center py-6">
                {/* Variation Label */}
                <span className="text-[11px] font-mono font-semibold uppercase tracking-wider text-[#a8a29e] block mb-4">
                  {v.title}
                </span>

                {/* Hero Preview Block */}
                <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-8 md:p-12 shadow-xs">
                  <h2 className="font-heading text-2xl sm:text-3xl md:text-4xl font-semibold text-[#0f0f0e] tracking-tight mb-3">
                    Classify News Articles in Milliseconds
                  </h2>
                  <p className="text-[14px] md:text-[15px] text-[#57534e] mb-6 max-w-md mx-auto">
                    Instant categorization across 5 domains.
                  </p>

                  <div className="flex flex-col items-center justify-center">
                    {v.button}
                    <p className="text-[11px] text-[#a8a29e] mt-4 font-mono">
                      {v.techDesc}
                    </p>
                  </div>
                </div>
              </div>

              {/* Divider between variations */}
              {index < variations.length - 1 && (
                <div className="border-t border-[#e7e3dd] my-10" />
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
