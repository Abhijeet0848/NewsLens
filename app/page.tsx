"use client";

import * as React from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Zap,
  Layers,
  ShieldCheck,
  Tag,
  ArrowRight,
  FileText,
} from "lucide-react";
import { Hero } from "@/components/hero";
import { Button } from "@/components/ui/button";
import { Reveal, StaggerContainer, StaggerItem } from "@/components/Reveal";
import { useClassifierStore } from "@/lib/store";
import { CATEGORIES_CONFIG } from "@/lib/utils";
import { fetchDatasetSummary } from "@/lib/api";
import type { BBCArticle } from "@/lib/types";
import { motion } from "framer-motion";
import { toast } from "sonner";

export default function HomePage() {
  const router = useRouter();
  const { setCurrentText } = useClassifierStore();
  const [samples, setSamples] = React.useState<BBCArticle[]>([]);
  const [counts, setCounts] = React.useState<Record<string, number>>({});
  const [totalCount, setTotalCount] = React.useState(2225);

  React.useEffect(() => {
    fetchDatasetSummary()
      .then((data) => {
        setSamples(data.samples || []);
        setCounts(data.categoryCounts || {});
        setTotalCount(data.totalArticles || 2225);
      })
      .catch((err) => {
        console.error("Failed to load BBC dataset:", err);
      });
  }, []);

  const handleSelectSample = (sample: BBCArticle) => {
    setCurrentText(sample.content || sample.title);
    router.push(`/classify?sample=${encodeURIComponent(sample.category)}`);
    toast.success(`Loaded BBC ${sample.category.toUpperCase()} article: "${sample.title.slice(0, 35)}..."`);
  };

  return (
    <div className="space-y-0 pb-12">
      {/* SECTION 1 & 2: Hero + Integrated Stats Bar */}
      <Hero />

      {/* Divider */}
      <div className="max-w-5xl mx-auto px-5 md:px-8">
        <div className="border-t border-[#e7e3dd]" />
      </div>

      {/* SECTION 3: Try A Real BBC Sample */}
      <Reveal>
        <section className="py-10 md:py-16 text-center max-w-3xl mx-auto px-5 md:px-8 space-y-4">
          <span className="text-[10px] md:text-[11px] font-semibold uppercase tracking-widest text-[#6b6660] font-mono block">
            REAL BBC NEWS SAMPLES
          </span>
          <h2 className="font-heading text-xl sm:text-2xl font-semibold text-[#0f0f0e] tracking-tight">
            Try a Benchmark Article
          </h2>
          <p className="text-[13px] md:text-[14px] text-[#6b6660] max-w-md mx-auto">
            Click any sample from the BBC corpus to test neural categorization.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-2.5 pt-3">
            {samples.length > 0 ? (
              samples.map((sample) => (
                <motion.button
                  key={sample.id}
                  whileHover={{ y: -1, scale: 1.02 }}
                  whileTap={{ scale: 0.97 }}
                  onClick={() => handleSelectSample(sample)}
                  className="rounded-full bg-[#fdfcfb] border border-[#e7e3dd] px-4 py-2 text-[12px] md:text-[13px] font-medium text-[#3f3d3a] hover:border-indigo-300 hover:text-[#0f0f0e] hover:bg-indigo-50/30 transition-colors duration-150 shadow-xs cursor-pointer active:scale-[0.97] flex items-center gap-1.5 max-w-xs truncate"
                >
                  <span className="size-1.5 rounded-full bg-indigo-500 flex-shrink-0" />
                  <span className="font-semibold capitalize text-[#0f0f0e]">{sample.category}:</span>
                  <span className="truncate">{sample.title}</span>
                </motion.button>
              ))
            ) : (
              <div className="text-xs text-[#6b6660] font-mono py-2">Loading BBC samples...</div>
            )}
          </div>
        </section>
      </Reveal>

      {/* Divider */}
      <div className="max-w-5xl mx-auto px-5 md:px-8">
        <div className="border-t border-[#e7e3dd]" />
      </div>

      {/* SECTION 4: Taxonomy Preview (5 Real BBC Domains) */}
      <Reveal>
        <section className="py-12 md:py-20 text-center max-w-3xl mx-auto px-5 md:px-8 space-y-4">
          <span className="text-[10px] md:text-[11px] font-semibold uppercase tracking-widest text-[#6b6660] font-mono block">
            BBC NEWS TAXONOMY
          </span>
          <h2 className="font-heading text-xl sm:text-2xl md:text-3xl font-semibold text-[#0f0f0e] tracking-tight">
            5 Distinct News Domains
          </h2>
          <p className="text-[13px] md:text-[14px] text-[#6b6660] leading-relaxed max-w-sm md:max-w-md mx-auto">
            {totalCount.toLocaleString()} verified articles across business, entertainment, politics, sport, and tech.
          </p>

          <div className="relative pt-4">
            <div className="flex gap-2.5 overflow-x-auto pb-2 -mx-5 px-5 md:mx-0 md:px-0 md:flex-wrap md:justify-center snap-x snap-mandatory [&::-webkit-scrollbar]:hidden [scrollbar-width:none]">
              {Object.entries(CATEGORIES_CONFIG).map(([name, cat]) => {
                const count = counts[name.toLowerCase()] || counts[name] || 0;
                return (
                  <span
                    key={name}
                    className="snap-start flex-shrink-0 flex items-center gap-2 px-4 py-2 rounded-full border text-[12px] md:text-[13px] font-medium shadow-xs"
                    style={{
                      backgroundColor: cat.bgLight,
                      borderColor: cat.borderColor,
                      color: cat.colorHex,
                    }}
                  >
                    <Tag className="size-3.5" style={{ color: cat.colorHex }} />
                    <span className="font-semibold">{name}</span>
                    {count > 0 && (
                      <span className="text-[11px] font-mono opacity-85 tabular-nums">
                        ({count} articles)
                      </span>
                    )}
                  </span>
                );
              })}
            </div>
          </div>
        </section>
      </Reveal>

      {/* Divider */}
      <div className="max-w-5xl mx-auto px-5 md:px-8">
        <div className="border-t border-[#e7e3dd]" />
      </div>

      {/* SECTION 5: Feature Highlights */}
      <Reveal>
        <section className="py-12 md:py-20 max-w-5xl mx-auto px-5 md:px-8 space-y-8 md:space-y-12">
          <div className="text-center max-w-2xl mx-auto space-y-2">
            <span className="text-[10px] md:text-[11px] font-semibold uppercase tracking-widest text-[#6b6660] font-mono block">
              BUILT FOR SPEED AND INSIGHT
            </span>
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

      {/* SECTION 6: Final Clean CTA */}
      <Reveal>
        <section className="py-12 md:py-20 max-w-2xl mx-auto px-5 md:px-8">
          <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-6 md:p-10 text-center space-y-4 shadow-sm">
            <h2 className="font-heading text-xl md:text-2xl font-semibold text-[#0f0f0e] tracking-tight">
              Ready to classify?
            </h2>
            <p className="text-[13px] md:text-[14px] text-[#6b6660]">
              Paste an article or upload a CSV to get started.
            </p>

            <div className="pt-2 flex justify-center">
              <motion.div whileHover={{ scale: 1.02, y: -1 }} whileTap={{ scale: 0.98 }} className="w-full sm:w-auto">
                <Link href="/classify" className="w-full block">
                  <Button size="lg" className="w-full sm:w-auto h-11 md:h-10 px-6 rounded-xl gap-2 text-sm font-semibold shadow-[0_4px_12px_rgba(99,102,241,0.25)]">
                    <Zap className="size-4 text-[#fdfcfb]" />
                    <span>Open Classifier</span>
                    <ArrowRight className="size-4" />
                  </Button>
                </Link>
              </motion.div>
            </div>
          </div>
        </section>
      </Reveal>
    </div>
  );
}
