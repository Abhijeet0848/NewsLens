"use client";

import * as React from "react";
import Link from "next/link";
import {
  Zap,
  Layers,
  ShieldCheck,
  Tag,
} from "lucide-react";
import { Hero } from "@/components/hero";
import { Reveal, StaggerContainer, StaggerItem } from "@/components/Reveal";
import { CategoryPill, TaxonomyPills, TAXONOMY_CATEGORIES } from "@/components/CategoryPill";
import { fetchDatasetSummary } from "@/lib/api";
import { motion } from "framer-motion";

export default function HomePage() {
  const [counts, setCounts] = React.useState<Record<string, number>>({});
  const [totalCount, setTotalCount] = React.useState(2225);

  React.useEffect(() => {
    fetchDatasetSummary()
      .then((data) => {
        setCounts(data.categoryCounts || {});
        setTotalCount(data.totalArticles || 2225);
      })
      .catch((err) => {
        console.error("Failed to load BBC dataset summary:", err);
      });
  }, []);

  return (
    <div className="space-y-0 pb-12">
      {/* SECTION 1 & 2: Hero + Integrated Stats Bar */}
      <Hero />

      {/* Divider */}
      <div className="max-w-5xl mx-auto px-5 md:px-8">
        <div className="border-t border-[#e7e3dd]" />
      </div>

      {/* SECTION 3: BBC News Taxonomy */}
      <Reveal>
        <section className="py-12 md:py-16 text-center max-w-3xl mx-auto px-5 md:px-8 space-y-3">
          <p className="text-[11px] font-semibold uppercase tracking-widest text-[#57534e] font-mono block">
            TAXONOMY
          </p>
          <h2 className="font-heading text-lg sm:text-xl font-semibold text-[#0f0f0e] tracking-tight">
            5 News Domains
          </h2>
          <p className="text-[13px] text-[#57534e] leading-relaxed max-w-sm md:max-w-md mx-auto">
            {totalCount.toLocaleString()} articles from the BBC corpus
          </p>

          <div className="pt-4">
            <TaxonomyPills counts={counts} />
          </div>
        </section>
      </Reveal>

      {/* Divider */}
      <div className="max-w-5xl mx-auto px-5 md:px-8">
        <div className="border-t border-[#e7e3dd]" />
      </div>

      {/* SECTION 4: Feature Highlights */}
      <Reveal>
        <section className="py-12 md:py-20 max-w-5xl mx-auto px-5 md:px-8 space-y-8 md:space-y-12">
          <div className="text-center max-w-2xl mx-auto space-y-2">
            <p className="text-[10px] md:text-[11px] font-semibold uppercase tracking-widest text-[#57534e] font-mono block">
              BUILT FOR SPEED AND INSIGHT
            </p>
            <h2 className="font-heading text-xl sm:text-2xl md:text-3xl font-semibold text-[#0f0f0e] tracking-tight">
              Core Classification Capabilities
            </h2>
            <p className="text-[13px] md:text-[14px] text-[#57534e] leading-relaxed">
              Engineered for production newsrooms, aggregators, and academic NLP research.
            </p>
          </div>

          <StaggerContainer className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-5">
            <StaggerItem>
              <motion.div
                whileHover={{ y: -2 }}
                className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-xs space-y-3 h-full"
              >
                <div className="size-9 md:size-10 rounded-lg bg-[#f1efeb] border border-[#e7e3dd] flex items-center justify-center text-[#0891b2] mb-3 md:mb-4">
                  <Zap className="size-4 md:size-5" />
                </div>
                <h3 className="text-[14px] md:text-[15px] font-semibold text-[#0f0f0e] font-heading">
                  Sub-Millisecond Inference
                </h3>
                <p className="text-[13px] text-[#57534e] leading-relaxed">
                  Optimized hyperplane margin boundaries and quantized Transformer attention yielding real-time latency.
                </p>
              </motion.div>
            </StaggerItem>

            <StaggerItem>
              <motion.div
                whileHover={{ y: -2 }}
                className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-xs space-y-3 h-full"
              >
                <div className="size-9 md:size-10 rounded-lg bg-[#f1efeb] border border-[#e7e3dd] flex items-center justify-center text-[#059669] mb-3 md:mb-4">
                  <ShieldCheck className="size-4 md:size-5" />
                </div>
                <h3 className="text-[14px] md:text-[15px] font-semibold text-[#0f0f0e] font-heading">
                  Complete Explainability
                </h3>
                <p className="text-[13px] text-[#57534e] leading-relaxed">
                  Inspect token-level attention heatmaps, TF-IDF weights, and decision factors behind every prediction.
                </p>
              </motion.div>
            </StaggerItem>

            <StaggerItem>
              <motion.div
                whileHover={{ y: -2 }}
                className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-xs space-y-3 h-full"
              >
                <div className="size-9 md:size-10 rounded-lg bg-[#f1efeb] border border-[#e7e3dd] flex items-center justify-center text-violet-600 mb-3 md:mb-4">
                  <Layers className="size-4 md:size-5" />
                </div>
                <h3 className="text-[14px] md:text-[15px] font-semibold text-[#0f0f0e] font-heading">
                  Batch CSV Streaming
                </h3>
                <p className="text-[13px] text-[#57534e] leading-relaxed">
                  Upload multi-thousand-row CSV news feeds with real-time per-row progress streaming and one-click export.
                </p>
              </motion.div>
            </StaggerItem>
          </StaggerContainer>
        </section>
      </Reveal>

      {/* Divider */}
      <div className="max-w-5xl mx-auto px-5 md:px-8">
        <div className="border-t border-[#e7e3dd]" />
      </div>

      {/* SECTION 5: Final Clean CTA */}
      <Reveal>
        <section className="py-12 md:py-20 max-w-2xl mx-auto px-5 md:px-8">
          <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-6 md:p-10 text-center space-y-4 shadow-sm">
            <h2 className="font-heading text-xl md:text-2xl font-semibold text-[#0f0f0e] tracking-tight">
              Ready to classify?
            </h2>
            <p className="text-[13px] md:text-[14px] text-[#57534e]">
              Paste an article or upload a CSV to get started.
            </p>

            <div className="pt-2 flex justify-center">
              <Link href="/classify" className="inline-flex">
                <button
                  type="button"
                  className="inline-flex items-center justify-center h-11 px-7 rounded-full bg-[#0f0f0e] text-white text-sm font-medium hover:bg-[#2a2a28] active:scale-[0.98] transition-all duration-200 ease-out focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#0f0f0e]/20 focus-visible:ring-offset-2 focus-visible:ring-offset-[#f7f6f3] cursor-pointer select-none"
                >
                  Open Classifier
                </button>
              </Link>
            </div>
          </div>
        </section>
      </Reveal>
    </div>
  );
}
