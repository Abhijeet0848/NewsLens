"use client";

import * as React from "react";
import { motion, AnimatePresence, useMotionValue, useTransform, animate } from "framer-motion";
import {
  Download,
  Copy,
  Check,
  Activity,
  ChevronDown,
  Info,
  Tag,
  Flame,
  Award,
  Sparkles,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import type { ClassificationResponse } from "@/lib/types";
import { getCategoryConfig, CATEGORIES_CONFIG } from "@/lib/utils";
import { ease, fadeUp, scaleIn } from "@/lib/motion";
import confetti from "canvas-confetti";
import { toast } from "sonner";

function AnimatedConfidence({ value, duration = 0.8 }: { value: number; duration?: number }) {
  const count = useMotionValue(0);
  const rounded = useTransform(count, (latest) => `${latest.toFixed(1)}%`);

  React.useEffect(() => {
    const controls = animate(count, value, {
      duration,
      ease: ease.smooth,
    });
    return controls.stop;
  }, [value, count, duration]);

  return <motion.span className="tabular-nums">{rounded}</motion.span>;
}

interface ResultsPanelProps {
  result: ClassificationResponse;
  originalText: string;
}

export function ResultsPanel({ result, originalText }: ResultsPanelProps) {
  const [copied, setCopied] = React.useState(false);
  const [showExplanation, setShowExplanation] = React.useState(true);
  const [showHeatmap, setShowHeatmap] = React.useState(false);

  const catConfig = getCategoryConfig(result.category);

  React.useEffect(() => {
    if (result.confidence >= 0.85) {
      try {
        confetti({
          particleCount: 30,
          spread: 50,
          origin: { y: 0.7 },
          colors: ["#6366f1", "#8b5cf6", "#0891b2", "#059669"],
        });
      } catch {}
    }
  }, [result]);

  const handleCopyResult = () => {
    const textToCopy = `NewsScope Classification Result:
Category: ${result.category}
Confidence: ${result.confidence_percentage}%
Top Keywords: ${result.keywords.map((k) => k.word).join(", ")}
Latency: ${result.latency_ms}ms`;

    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    toast.success("Result copied to clipboard");
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadJSON = () => {
    const dataStr =
      "data:text/json;charset=utf-8," +
      encodeURIComponent(
        JSON.stringify(
          {
            ...result,
            article_snippet: originalText.slice(0, 300),
          },
          null,
          2
        )
      );
    const downloadAnchor = document.createElement("a");
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute(
      "download",
      `newsscope-${result.category.toLowerCase()}-${Date.now()}.json`
    );
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
    toast.success("JSON telemetry exported");
  };

  // Only the 5 authentic BBC categories
  const sortedCategories = Object.entries(CATEGORIES_CONFIG)
    .map(([catName]) => {
      const prob = result.all_scores[catName] || result.all_scores[catName.toLowerCase()] || 0;
      return [catName, prob] as [string, number];
    })
    .sort(([, a], [, b]) => b - a);

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      transition={{ duration: 0.4, ease: ease.smooth }}
      className="space-y-6"
    >
      {/* 1. Primary Result Card */}
      <motion.div
        variants={scaleIn}
        initial="hidden"
        animate="show"
        className={`relative overflow-hidden rounded-2xl border p-5 md:p-8 bg-[#fdfcfb] shadow-[0_8px_24px_rgba(15,15,14,0.06),0_2px_6px_rgba(15,15,14,0.04)] transition-all duration-300 ${catConfig.borderClass}`}
      >
        <div
          className={`absolute -right-20 -top-20 h-56 w-56 rounded-full bg-gradient-to-br ${catConfig.gradient} blur-2xl -z-10`}
        />

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#e7e3dd] pb-5 md:pb-6">
          <div className="flex items-center gap-3 md:gap-4">
            <motion.div
              initial={{ scale: 0.8, rotate: -6 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ type: "spring", stiffness: 350, damping: 22 }}
              className={`flex h-12 w-12 md:h-14 md:w-14 items-center justify-center rounded-xl border shadow-sm flex-shrink-0 ${catConfig.badgeClass}`}
            >
              <Award className="size-6 md:size-7" style={{ color: catConfig.colorHex }} />
            </motion.div>
            <div>
              <span className="text-[10px] md:text-[11px] font-semibold uppercase tracking-[0.14em] text-[#6b6660] font-mono">
                Predicted BBC Domain
              </span>
              <div className="flex items-center gap-2 mt-0.5">
                <h3 className="font-heading text-xl sm:text-2xl md:text-3xl font-semibold text-[#0f0f0e] tracking-tight">
                  {result.category}
                </h3>
                <span
                  className={`rounded-md px-2 py-0.5 text-[11px] md:text-xs font-semibold border ${catConfig.badgeClass}`}
                >
                  Verified
                </span>
              </div>
            </div>
          </div>

          <div className="text-left sm:text-right">
            <span className="text-[11px] md:text-xs font-mono font-medium text-[#6b6660]">Confidence</span>
            <div className="font-heading text-2xl md:text-3xl font-bold text-[#0f0f0e] font-mono">
              <AnimatedConfidence value={result.confidence_percentage} />
            </div>
            <div className="text-[11px] md:text-xs text-[#3f3d3a] font-mono font-medium flex items-center sm:justify-end gap-1 mt-0.5 tabular-nums">
              <Activity className="size-3 text-[#0891b2]" />
              <span>{result.latency_ms} ms</span>
            </div>
          </div>
        </div>

        {/* 2. Confidence Fill Bar */}
        <div className="mt-5 md:mt-6 space-y-2">
          <div className="flex justify-between text-[11px] md:text-xs font-mono font-medium text-[#3f3d3a]">
            <span>Probability Distribution</span>
            <span className="text-[#0f0f0e] font-semibold tabular-nums">{result.confidence_percentage}%</span>
          </div>
          <div className="h-2.5 w-full overflow-hidden rounded-full bg-[#f1efeb] border border-[#e7e3dd]">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${result.confidence_percentage}%` }}
              transition={{ duration: 0.8, ease: ease.smooth }}
              className="h-full rounded-full"
              style={{ backgroundColor: catConfig.colorHex }}
            />
          </div>
        </div>

        {/* Action Toolbar */}
        <div className="mt-5 md:mt-6 flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-[#e7e3dd] text-xs">
          <div className="flex items-center gap-2">
            <motion.div whileHover={{ y: -1 }} whileTap={{ scale: 0.97 }}>
              <Button
                variant="outline"
                size="sm"
                onClick={handleCopyResult}
                className="gap-1.5 text-xs h-8 rounded-lg font-medium text-[#3f3d3a] hover:text-[#0f0f0e]"
              >
                {copied ? <Check className="size-3.5 text-[#059669]" /> : <Copy className="size-3.5 text-[#6b6660]" />}
                <span>{copied ? "Copied" : "Copy"}</span>
              </Button>
            </motion.div>

            <motion.div whileHover={{ y: -1 }} whileTap={{ scale: 0.97 }}>
              <Button
                variant="outline"
                size="sm"
                onClick={handleDownloadJSON}
                className="gap-1.5 text-xs h-8 rounded-lg font-medium text-[#3f3d3a] hover:text-[#0f0f0e]"
              >
                <Download className="size-3.5 text-[#6b6660]" />
                <span>Export JSON</span>
              </Button>
            </motion.div>
          </div>

          <span className="text-[#6b6660] font-mono text-[11px] md:text-xs tabular-nums">
            {result.tokens_count} tokens &bull; {result.explanation.model_version}
          </span>
        </div>
      </motion.div>

      {/* 3. 5-Domain Probability Distribution Card */}
      <motion.div
        variants={fadeUp}
        initial="hidden"
        animate="show"
        transition={{ delay: 0.1 }}
        className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-8 shadow-[0_8px_24px_rgba(15,15,14,0.06),0_2px_6px_rgba(15,15,14,0.04)] space-y-4"
      >
        <div className="flex items-center justify-between">
          <h4 className="text-[14px] md:text-base font-semibold text-[#0f0f0e] flex items-center gap-2 font-heading">
            <Activity className="size-4 text-[#0891b2]" />
            Category Probability Distribution
          </h4>
          <span className="text-[11px] text-[#6b6660] font-mono font-medium">5 Domains</span>
        </div>

        <div className="space-y-3 md:space-y-3.5">
          {sortedCategories.map(([category, prob], index) => {
            const cfg = getCategoryConfig(category);
            const pct = Math.round(prob * 1000) / 10;
            const isTop = index === 0;

            return (
              <motion.div
                key={category}
                initial={{ opacity: 0, x: -6 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.35, delay: 0.15 + index * 0.05, ease: ease.smooth }}
                className="space-y-1.5"
              >
                <div className="flex items-center justify-between text-[12px] md:text-[13px]">
                  <span className="flex items-center gap-2 text-[#0f0f0e] font-medium">
                    <span
                      className="size-2 rounded-full"
                      style={{ backgroundColor: cfg.colorHex }}
                    />
                    <span>{category}</span>
                  </span>
                  <span className="font-mono text-[#3f3d3a] font-semibold text-[11px] md:text-xs tabular-nums">{pct}%</span>
                </div>
                <div className="h-1.5 w-full overflow-hidden rounded-full bg-[#f1efeb]">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${pct}%` }}
                    transition={{ duration: 0.7, delay: 0.2 + index * 0.05, ease: ease.smooth }}
                    className="h-full rounded-full relative"
                    style={{
                      backgroundColor: isTop ? cfg.colorHex : "#b8b2a8",
                    }}
                  />
                </div>
              </motion.div>
            );
          })}
        </div>
      </motion.div>

      {/* 4. Saliency Keywords Card */}
      <motion.div
        variants={fadeUp}
        initial="hidden"
        animate="show"
        transition={{ delay: 0.2 }}
        className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-8 shadow-[0_8px_24px_rgba(15,15,14,0.06),0_2px_6px_rgba(15,15,14,0.04)] space-y-3"
      >
        <div className="flex items-center justify-between">
          <h4 className="text-[14px] md:text-base font-semibold text-[#0f0f0e] flex items-center gap-2 font-heading">
            <Tag className="size-4 text-indigo-600" />
            Top Saliency Keywords
          </h4>
          <span className="text-[11px] text-[#6b6660] font-mono font-medium">TF-IDF Weights</span>
        </div>

        <div className="flex flex-wrap gap-2 pt-1">
          {result.keywords.map((kw, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3, delay: 0.25 + i * 0.04 }}
              whileHover={{ scale: 1.05, y: -1 }}
              className="flex items-center gap-1.5 rounded-lg border border-[#e7e3dd] bg-[#f1efeb] px-2.5 py-1 text-xs text-[#0f0f0e] shadow-sm cursor-default"
            >
              <Flame className="size-3 text-[#d97706]" />
              <span className="font-semibold">{kw.word}</span>
              <span className="font-mono font-medium text-[11px] text-[#0891b2] rounded bg-[#ecfeff] px-1 py-0.2 border border-[#a5f3fc] tabular-nums">
                {Math.round(kw.weight * 100)}%
              </span>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* 5. Accordion: Why This Prediction? */}
      <motion.div
        variants={fadeUp}
        initial="hidden"
        animate="show"
        transition={{ delay: 0.3 }}
        className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] shadow-[0_8px_24px_rgba(15,15,14,0.06),0_2px_6px_rgba(15,15,14,0.04)] overflow-hidden"
      >
        <button
          type="button"
          onClick={() => setShowExplanation(!showExplanation)}
          className="flex w-full items-center justify-between p-5 md:p-6 text-left text-sm font-semibold text-[#0f0f0e] hover:bg-[#f1efeb] transition-colors"
        >
          <div className="flex items-center gap-2">
            <Info className="size-4 text-[#0891b2]" />
            <span className="text-[13px] md:text-sm">Why this prediction? (Neural Explainability)</span>
          </div>
          <ChevronDown
            className={`size-4 text-[#6b6660] transition-transform duration-200 ${
              showExplanation ? "rotate-180" : ""
            }`}
          />
        </button>

        <AnimatePresence>
          {showExplanation && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.25, ease: ease.smooth }}
              className="px-5 md:px-6 pb-5 md:pb-6 space-y-3 border-t border-[#e7e3dd] pt-4 text-[13px] text-[#3f3d3a] overflow-hidden"
            >
              <p className="leading-relaxed">{result.explanation.summary}</p>
              <div className="space-y-1.5">
                <span className="font-mono text-[#6b6660] uppercase tracking-[0.14em] text-[10px] md:text-[11px] font-semibold">
                  Decision Factors:
                </span>
                <ul className="list-disc list-inside space-y-1 text-[#0f0f0e] font-medium pl-1">
                  {result.explanation.top_factors.map((factor, i) => (
                    <li key={i}>{factor}</li>
                  ))}
                </ul>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* 6. Attention Heatmap Visualizer */}
      <motion.div
        variants={fadeUp}
        initial="hidden"
        animate="show"
        transition={{ delay: 0.35 }}
        className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-8 shadow-[0_8px_24px_rgba(15,15,14,0.06),0_2px_6px_rgba(15,15,14,0.04)] space-y-3"
      >
        <div className="flex items-center justify-between">
          <h4 className="text-[14px] md:text-base font-semibold text-[#0f0f0e] font-heading flex items-center gap-2">
            <Sparkles className="size-4 text-[#0891b2]" />
            Token Attention Heatmap
          </h4>
          <Button
            size="sm"
            variant="outline"
            className="text-xs h-7 rounded-md font-medium text-[#3f3d3a]"
            onClick={() => setShowHeatmap(!showHeatmap)}
          >
            {showHeatmap ? "Collapse" : "Expand"}
          </Button>
        </div>

        <AnimatePresence>
          {showHeatmap && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.25 }}
              className="pt-2 overflow-hidden"
            >
              <div className="p-4 rounded-xl bg-[#f1efeb] border border-[#e7e3dd] text-xs leading-loose text-[#0f0f0e] font-mono max-h-56 overflow-y-auto">
                {result.attention_tokens.map((t, idx) => {
                  const bg = t.isKeyword ? "#c7d2fe" : "#ecfeff";
                  return (
                    <motion.span
                      key={idx}
                      whileHover={{ scale: 1.05 }}
                      className="inline-block rounded px-1.5 py-0.5 mx-0.5 border border-[#e7e3dd] shadow-sm transition-all"
                      style={{ backgroundColor: bg }}
                      title={`Token: "${t.token}" | Saliency: ${(t.weight * 100).toFixed(0)}%`}
                    >
                      {t.token}
                    </motion.span>
                  );
                })}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </motion.div>
  );
}

/**
 * Empty State Skeleton Component for the 5 BBC Categories with 0% state
 */
export function EmptyResultsSkeleton() {
  const bbcCategories = [
    { name: "Business", color: "#d97706" },
    { name: "Entertainment", color: "#db2777" },
    { name: "Politics", color: "#e11d48" },
    { name: "Sport", color: "#059669" },
    { name: "Tech", color: "#0891b2" },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.4, delay: 0.1, ease: ease.smooth }}
      className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-8 shadow-[0_8px_24px_rgba(15,15,14,0.06),0_2px_6px_rgba(15,15,14,0.04)] space-y-6 select-none flex flex-col justify-between h-full min-h-[440px] md:min-h-[480px]"
    >
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex size-9 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600 border border-indigo-100 flex-shrink-0">
              <Activity className="size-4" />
            </div>
            <div>
              <h3 className="text-base font-semibold text-[#0f0f0e] font-heading">
                Prediction Telemetry
              </h3>
              <p className="text-[13px] text-[#6b6660] mt-0.5">Real-time inference probabilities</p>
            </div>
          </div>
          <span className="bg-[#f1efeb] text-[#6b6660] text-[10px] md:text-[11px] font-semibold uppercase tracking-wider rounded-full px-2.5 py-0.5 border border-[#e7e3dd]">
            idle
          </span>
        </div>

        {/* Section label "PROBABILITY DISTRIBUTION" + "5 Domains" */}
        <div className="pt-2 space-y-3">
          <div className="flex justify-between text-[10px] md:text-[11px] font-semibold uppercase tracking-[0.14em] text-[#6b6660] font-mono mb-3">
            <span>Probability Distribution</span>
            <span>5 Domains</span>
          </div>

          {/* 5 Real BBC Domains in Idle 0% state */}
          <div className="space-y-3 md:space-y-3.5">
            {bbcCategories.map((c, i) => (
              <div key={c.name} className="space-y-1.5">
                <div className="flex justify-between text-[12px] md:text-[13px] font-medium text-[#3f3d3a]">
                  <span className="flex items-center gap-2">
                    <span className="size-2 rounded-full" style={{ backgroundColor: c.color }} />
                    <span>{c.name}</span>
                  </span>
                  <span className="font-mono text-[11px] md:text-xs font-medium text-[#8a847d] tabular-nums">0.0%</span>
                </div>
                <div className="h-1.5 w-full rounded-full bg-[#f1efeb] overflow-hidden">
                  <div className="h-full rounded-full bg-[#e7e3dd]" style={{ width: "0%" }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Centered empty-state prompt */}
      <div className="flex-1 flex flex-col items-center justify-center pt-6 md:pt-8 pb-4 text-center">
        <Sparkles className="size-8 text-[#c8c4bd] mb-3 stroke-[1.5]" />
        <p className="text-sm font-medium text-[#3f3d3a]">Awaiting article input</p>
        <p className="text-[13px] text-[#6b6660] max-w-xs text-center mt-1">
          Paste an article or pick a BBC sample to see predictions
        </p>
      </div>
    </motion.div>
  );
}
