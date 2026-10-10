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
  AlertTriangle,
  HelpCircle,
  ArrowRight,
  Loader2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import type { ClassificationResponse } from "@/lib/types";
import { getCategoryConfig } from "@/lib/utils";
import { MODELS, ModelId } from "@/lib/models";
import { ease, fadeUp, scaleIn } from "@/lib/motion";
import confetti from "canvas-confetti";
import { toast } from "sonner";

function AnimatedConfidence({ value, duration = 0.8 }: { value: number; duration?: number }) {
  const count = useMotionValue(0);
  const rounded = useTransform(count, (latest) => `${latest.toFixed(1)}%`);

  React.useEffect(() => {
    const controls = (animate as any)(count, value, {
      duration,
      ease: ease.smooth,
    });
    return controls.stop;
  }, [value, count, duration]);

  return <motion.span className="tabular-nums">{rounded}</motion.span>;
}

// Multi-tier Confidence Badge Configuration
function getConfidenceBadge(confidence: number) {
  if (confidence < 0.4) {
    return {
      label: "Uncertain",
      style: "text-[#92400e] bg-[#fef3c7] border-[#fde68a]",
      icon: AlertTriangle,
    };
  }
  if (confidence < 0.6) {
    return {
      label: "Low confidence",
      style: "text-[#92400e] bg-[#fef3c7] border-[#fde68a]",
      icon: AlertTriangle,
    };
  }
  if (confidence < 0.8) {
    return {
      label: "Probable",
      style: "text-[#0e7490] bg-[#ecfeff] border-[#a5f3fc]",
      icon: Info,
    };
  }
  return {
    label: "Verified",
    style: "text-[#047857] bg-[#ecfdf5] border-[#a7f3d0]",
    icon: Check,
  };
}

export type ResultState = "empty" | "ready" | "loading" | "done";

export interface ResultsPanelProps {
  result: ClassificationResponse | null;
  isLoading?: boolean;
  text?: string;
  selectedModel?: string;
  originalText?: string;
}

export function ResultsPanel({
  result,
  isLoading = false,
  text = "",
  selectedModel = "linear-svm",
  originalText = "",
}: ResultsPanelProps) {
  const [copied, setCopied] = React.useState(false);
  const [showExplanation, setShowExplanation] = React.useState(false);
  const [showHeatmap, setShowHeatmap] = React.useState(false);

  const rawText = text || originalText;
  const trimmed = rawText.trim();
  const wordCount = (rawText.match(/[a-zA-Z]+/g) || []).length;
  const charCount = rawText.length;

  const resultState: ResultState = isLoading
    ? "loading"
    : result
    ? "done"
    : trimmed.length > 0
    ? "ready"
    : "empty";

  const activeModel =
    MODELS[((result?.model_id || selectedModel) as ModelId)] || MODELS["linear-svm"];

  React.useEffect(() => {
    if (result && result.confidence >= 0.8) {
      try {
        confetti({
          particleCount: 25,
          spread: 50,
          origin: { y: 0.65 },
          colors: ["#4f46e5", "#059669", "#d97706"],
          disableForReducedMotion: true,
        });
      } catch {}
    }
  }, [result]);

  const bbcCategories = [
    { label: "Business", cfg: getCategoryConfig("Business") },
    { label: "Entertainment", cfg: getCategoryConfig("Entertainment") },
    { label: "Politics", cfg: getCategoryConfig("Politics") },
    { label: "Sport", cfg: getCategoryConfig("Sport") },
    { label: "Tech", cfg: getCategoryConfig("Tech") },
  ];

  // 1. STATE: EMPTY
  if (resultState === "empty") {
    return (
      <motion.div
        key="empty"
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -6 }}
        transition={{ duration: 0.25 }}
        className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-6 md:p-7 shadow-[0_1px_2px_rgba(28,27,26,0.04),0_8px_24px_-8px_rgba(28,27,26,0.06)] space-y-6"
      >
        <div className="flex items-center justify-between border-b border-[#e7e3dd] pb-5">
          <div className="flex items-center gap-3.5">
            <div className="flex size-12 items-center justify-center rounded-xl bg-[#f1efeb] border border-[#e7e3dd] text-[#8a847d]">
              <HelpCircle className="size-6 text-[#a8a29e]" />
            </div>
            <div className="space-y-0.5">
              <span className="text-[10px] font-mono uppercase tracking-widest text-[#8a847d] font-semibold">
                Waiting for input
              </span>
              <h3 className="text-[20px] font-semibold text-[#6b6660] tracking-tight">
                No Article Analyzed
              </h3>
            </div>
          </div>
          <div className="text-right">
            <span className="text-[10px] font-mono uppercase tracking-widest text-[#8a847d] font-semibold">
              Status
            </span>
            <div className="text-xs font-mono font-semibold text-[#8a847d] bg-[#f1efeb] px-2 py-0.5 rounded border border-[#e7e3dd] mt-0.5">
              STANDBY
            </div>
          </div>
        </div>

        <p className="text-[13px] text-[#8a847d] leading-relaxed">
          Paste news article text, upload a document, or fetch from a URL to inspect predicted categories and statistical distributions.
        </p>

        {/* 5-Class Standby Distribution */}
        <div className="space-y-3">
          <div className="flex justify-between items-center text-[10px] font-mono font-semibold uppercase tracking-widest text-[#8a847d]">
            <span>5-Class BBC Distribution</span>
            <span>0.0% Standby</span>
          </div>

          <div className="space-y-2.5 pt-1">
            {bbcCategories.map((c) => (
              <div key={c.label} className="space-y-1">
                <div className="flex justify-between items-center text-xs">
                  <span className="flex items-center text-[#6b6660] font-medium">
                    <span
                      className="size-1.5 rounded-full mr-2"
                      style={{ backgroundColor: c.cfg.colorHex }}
                    />
                    <span>{c.label}</span>
                  </span>
                  <span className="font-mono text-[#a8a29e] text-[11px]">0.0%</span>
                </div>
                <div className="h-1.5 w-full bg-[#f1efeb] rounded-full overflow-hidden">
                  <div className="h-full w-0 bg-transparent" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </motion.div>
    );
  }

  // 2. STATE: READY
  if (resultState === "ready") {
    return (
      <motion.div
        key="ready"
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -6 }}
        transition={{ duration: 0.25 }}
        className="rounded-2xl border border-indigo-200 bg-[#fdfcfb] p-6 md:p-7 shadow-[0_1px_2px_rgba(28,27,26,0.04),0_8px_24px_-8px_rgba(28,27,26,0.06)] space-y-5"
      >
        <div className="flex items-center justify-between border-b border-[#e7e3dd] pb-5">
          <div className="flex items-center gap-3.5">
            <div className="flex size-12 items-center justify-center rounded-xl bg-[#eef2ff] border border-indigo-100 text-[#4f46e5]">
              <Sparkles className="size-6 text-[#4f46e5]" />
            </div>
            <div className="space-y-0.5">
              <span className="text-[10px] font-mono uppercase tracking-widest text-[#4f46e5] font-semibold">
                Input Registered
              </span>
              <h3 className="text-[20px] font-semibold text-[#0f0f0e] tracking-tight">
                Ready to Classify
              </h3>
            </div>
          </div>
          <div className="text-right">
            <span className="text-[10px] font-mono uppercase tracking-widest text-[#4f46e5] font-semibold">
              Status
            </span>
            <div className="text-xs font-mono font-semibold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded border border-indigo-200 mt-0.5">
              READY
            </div>
          </div>
        </div>

        {/* Live Counter Card */}
        <div className="p-4 rounded-xl bg-[#faf9f6] border border-[#e7e3dd] space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="text-[12px] font-mono text-[#0f0f0e] font-semibold">
              {wordCount} words &bull; {charCount} chars
            </span>
            <span className="text-[11px] font-mono font-semibold text-[#047857] bg-[#ecfdf5] border border-[#a7f3d0] px-2 py-0.5 rounded">
              Ready for inference
            </span>
          </div>
          <p className="text-[12px] text-[#6b6660]">
            Using <span className="font-semibold text-[#0f0f0e]">{activeModel.name}</span> &bull; {activeModel.metric} benchmark accuracy
          </p>
        </div>

        <p className="text-[13px] text-[#57534e]">
          Click <span className="font-semibold text-[#0f0f0e]">&ldquo;Classify Article Now&rdquo;</span> or press <kbd className="bg-[#f1efeb] border border-[#e7e3dd] rounded px-1.5 py-0.5 text-[11px] font-mono font-medium text-[#3f3d3a]">⌘+Enter</kbd> to run NLP vectorization and probability estimation.
        </p>

        {/* Standby 5-Class BBC Distribution */}
        <div className="space-y-3 pt-1">
          <div className="flex justify-between items-center text-[10px] font-mono font-semibold uppercase tracking-widest text-[#8a847d]">
            <span>5-Class BBC Distribution</span>
            <span>Awaiting inference</span>
          </div>

          <div className="space-y-2.5 pt-1">
            {bbcCategories.map((c) => (
              <div key={c.label} className="space-y-1">
                <div className="flex justify-between items-center text-xs">
                  <span className="flex items-center text-[#6b6660] font-medium">
                    <span
                      className="size-1.5 rounded-full mr-2"
                      style={{ backgroundColor: c.cfg.colorHex }}
                    />
                    <span>{c.label}</span>
                  </span>
                  <span className="font-mono text-[#a8a29e] text-[11px]">Ready</span>
                </div>
                <div className="h-1.5 w-full bg-[#f1efeb] rounded-full overflow-hidden">
                  <div className="h-full w-0 bg-transparent" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </motion.div>
    );
  }

  // 3. STATE: LOADING
  if (resultState === "loading") {
    return (
      <motion.div
        key="loading"
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -6 }}
        transition={{ duration: 0.25 }}
        className="rounded-2xl border border-indigo-200 bg-[#fdfcfb] p-6 md:p-7 shadow-[0_1px_2px_rgba(28,27,26,0.04),0_8px_24px_-8px_rgba(28,27,26,0.06)] space-y-6"
      >
        <div className="flex items-center justify-between border-b border-[#e7e3dd] pb-5">
          <div className="flex items-center gap-3.5">
            <div className="flex size-12 items-center justify-center rounded-xl bg-[#eef2ff] border border-indigo-100 text-[#4f46e5]">
              <Loader2 className="size-6 animate-spin text-[#4f46e5]" />
            </div>
            <div className="space-y-0.5">
              <span className="text-[10px] font-mono uppercase tracking-widest text-[#4f46e5] font-semibold">
                Inference in progress
              </span>
              <h3 className="text-[20px] font-semibold text-[#0f0f0e] tracking-tight">
                Analyzing Article...
              </h3>
            </div>
          </div>
          <div className="text-right">
            <span className="text-[10px] font-mono uppercase tracking-widest text-[#4f46e5] font-semibold">
              Status
            </span>
            <div className="text-xs font-mono font-semibold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded border border-indigo-200 mt-0.5">
              PROCESSING
            </div>
          </div>
        </div>

        <p className="text-[13px] text-[#57534e]">
          Running TF-IDF tokenization, stopword extraction, and calibrated {activeModel.name} inference...
        </p>

        {/* Pulse Skeleton Bars for the 5 categories */}
        <div className="space-y-3">
          <div className="flex justify-between items-center text-[10px] font-mono font-semibold uppercase tracking-widest text-[#8a847d]">
            <span>Estimating Category Probabilities</span>
            <span className="animate-pulse text-[#4f46e5]">Computing...</span>
          </div>

          <div className="space-y-3 pt-1">
            {["Business", "Entertainment", "Politics", "Sport", "Tech"].map((cat) => (
              <div key={cat} className="space-y-1.5">
                <div className="flex justify-between items-center">
                  <div className="h-3 w-24 bg-[#e7e3dd] rounded animate-pulse" />
                  <div className="h-3 w-8 bg-[#e7e3dd] rounded animate-pulse" />
                </div>
                <div className="h-2 w-full bg-[#f1efeb] rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-indigo-200 via-indigo-300 to-indigo-200 rounded-full animate-pulse w-3/4" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </motion.div>
    );
  }

  // 4. STATE: DONE (Full Results Display)
  if (!result) return null;

  const catConfig = getCategoryConfig(result.category);
  const badgeInfo = getConfidenceBadge(result.confidence);
  const BadgeIcon = badgeInfo.icon;

  const allCategories = ["Business", "Entertainment", "Politics", "Sport", "Tech"];
  const sortedCategories = allCategories
    .map((cat) => [cat, result.all_scores?.[cat] ?? 0.05] as [string, number])
    .sort((a, b) => b[1] - a[1]);

  const handleCopyResult = () => {
    const summary = `NewsScope Prediction: ${result.category} (${result.confidence_percentage}% confidence)\nModel: ${result.explanation.model_version}\nTop Saliency Keywords: ${result.keywords.map((k) => k.word).join(", ")}`;
    navigator.clipboard.writeText(summary);
    setCopied(true);
    toast.success("Classification summary copied to clipboard");
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadJSON = () => {
    const dataStr =
      "data:text/json;charset=utf-8," +
      encodeURIComponent(JSON.stringify(result, null, 2));
    const downloadAnchor = document.createElement("a");
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute(
      "download",
      `classification-${result.category.toLowerCase()}-${Date.now()}.json`
    );
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
    toast.success("JSON telemetry downloaded");
  };

  return (
    <motion.div
      key="done"
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -8 }}
      transition={{ duration: 0.4, ease: ease.smooth }}
      className="space-y-5"
    >
      {/* Primary Result & Probability Distribution Card */}
      <motion.div
        variants={scaleIn}
        initial="hidden"
        animate="show"
        className={`relative overflow-hidden rounded-2xl border p-6 md:p-7 bg-[#fdfcfb] shadow-[0_1px_2px_rgba(28,27,26,0.04),0_8px_24px_-8px_rgba(28,27,26,0.06)] hover:shadow-[0_1px_2px_rgba(28,27,26,0.06),0_12px_32px_-8px_rgba(28,27,26,0.10)] transition-all duration-200 ${catConfig.borderClass}`}
      >
        <div
          className={`absolute -right-20 -top-20 h-56 w-56 rounded-full bg-gradient-to-br ${catConfig.gradient} blur-2xl -z-10`}
        />

        {/* Prediction Header */}
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
              <span className="text-[11px] font-semibold uppercase tracking-[0.12em] text-[#6b6660] font-mono">
                Predicted BBC Domain
              </span>
              <div className="flex items-center gap-2 mt-0.5">
                <h3 className="font-heading text-xl sm:text-2xl md:text-3xl font-semibold text-[#0f0f0e] tracking-tight">
                  {result.category}
                </h3>
                <span
                  className={`inline-flex items-center gap-1 text-[10px] font-medium uppercase tracking-wide border rounded-full px-2 py-0.5 ${badgeInfo.style}`}
                >
                  <BadgeIcon className="size-3" />
                  {badgeInfo.label}
                </span>
              </div>
            </div>
          </div>

          <div className="text-left sm:text-right">
            <span className="text-[12px] font-mono font-medium text-[#6b6660]">Confidence</span>
            <div className="font-heading text-2xl md:text-3xl font-bold text-[#0f0f0e] font-mono">
              <AnimatedConfidence value={result.confidence_percentage} />
            </div>
            <div className="text-[12px] text-[#3f3d3a] font-mono font-medium flex items-center sm:justify-end gap-1 mt-0.5 tabular-nums">
              <Activity className="size-3 text-[#0891b2]" />
              <span>{result.latency_ms} ms</span>
            </div>
          </div>
        </div>

        {/* Model Attribution Strip */}
        <div className="flex flex-wrap items-center gap-2 text-[11px] text-[#57534e] bg-[#faf9f6] border border-[#e7e3dd] rounded-lg px-3 py-1.5 mt-5">
          <span className="size-1.5 rounded-full bg-[#4f46e5] shrink-0" />
          <span>Predicted by</span>
          <span className="font-medium text-[#0f0f0e]">{activeModel.name}</span>
          <span className="text-[#57534e]">&bull;</span>
          <span className="font-mono text-[#0f0f0e]">{activeModel.metric}</span>
          <span className="text-[#57534e]">&bull;</span>
          <span className="font-mono text-[#57534e]">{result.latency_ms}ms latency</span>
        </div>

        {/* 5-Domain Probability Distribution */}
        <div className="mt-5 space-y-3">
          <div className="flex justify-between items-center text-[11px] font-semibold uppercase tracking-[0.12em] text-[#57534e]">
            <span>Probability Distribution</span>
            <span>5 BBC Domains</span>
          </div>

          <div className="space-y-2.5 pt-1">
            {sortedCategories.map(([category, prob], index) => {
              const cfg = getCategoryConfig(category);
              const pct = Math.round(prob * 1000) / 10;

              return (
                <div key={category} className="space-y-1">
                  <div className="flex justify-between items-center text-xs">
                    <span className="flex items-center text-[13px] text-[#3f3d3a] font-medium">
                      <span
                        className="size-1.5 rounded-full mr-2 flex-shrink-0"
                        style={{ backgroundColor: cfg.colorHex }}
                      />
                      <span>{category}</span>
                    </span>
                    <span className="font-mono text-[#0f0f0e] tabular-nums font-semibold text-[12px]">
                      {pct}%
                    </span>
                  </div>
                  <div className="h-1.5 bg-[#f1efeb] rounded-full w-full overflow-hidden">
                    <motion.div
                      initial={{ width: "0.5%" }}
                      animate={{ width: `${pct}%` }}
                      transition={{ duration: 0.8, delay: 0.05 + index * 0.04, ease: ease.smooth }}
                      className="h-full rounded-full"
                      style={{
                        backgroundColor: cfg.colorHex,
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>

          {/* Model Uncertain Warning Banner when confidence < 40% */}
          {result.confidence < 0.4 && (
            <div className="rounded-xl border border-[#fde68a] bg-[#fef3c7]/50 p-3.5 mt-4">
              <div className="flex items-start gap-2.5">
                <AlertTriangle aria-hidden="true" className="size-4 text-[#92400e] mt-0.5 shrink-0" />
                <div>
                  <p className="text-[13px] font-medium text-[#92400e]">
                    Low prediction confidence
                  </p>
                  <p className="text-[12px] text-[#854d0e] mt-1 leading-relaxed">
                    The article may be short or outside the BBC training taxonomy. Provide additional descriptive context for higher confidence.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Action Toolbar */}
        <div className="mt-5 flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-[#e7e3dd] text-xs">
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleCopyResult}
              aria-label="Copy classification result to clipboard"
              className="h-8 px-3 rounded-md bg-[#fdfcfb] border border-[#e7e3dd] text-[12px] font-medium text-[#0f0f0e] hover:bg-[#f1efeb] hover:border-[#d6d1c9] transition-colors duration-150 flex items-center gap-1.5 shadow-sm active:scale-[0.98] focus-visible:ring-2 focus-visible:ring-[#4f46e5]/40 focus:outline-none"
            >
              {copied ? <Check aria-hidden="true" className="size-3.5 text-[#047857]" /> : <Copy aria-hidden="true" className="size-3.5 text-[#57534e]" />}
              <span>{copied ? "Copied" : "Copy"}</span>
            </button>

            <button
              type="button"
              onClick={handleDownloadJSON}
              aria-label="Export result as JSON file"
              className="h-8 px-3 rounded-md bg-[#fdfcfb] border border-[#e7e3dd] text-[12px] font-medium text-[#0f0f0e] hover:bg-[#f1efeb] hover:border-[#d6d1c9] transition-colors duration-150 flex items-center gap-1.5 shadow-sm active:scale-[0.98] focus-visible:ring-2 focus-visible:ring-[#4f46e5]/40 focus:outline-none"
            >
              <Download aria-hidden="true" className="size-3.5 text-[#57534e]" />
              <span>Export JSON</span>
            </button>
          </div>

          <span className="text-[#57534e] font-mono text-[12px] tabular-nums font-medium">
            {result.tokens_count > 5 ? (
              `${result.tokens_count} tokens • ${result.explanation.model_version}`
            ) : (
              "Short input — prediction may be approximate"
            )}
          </span>
        </div>
      </motion.div>

      {/* Saliency Keywords Card */}
      <motion.div
        variants={fadeUp}
        initial="hidden"
        animate="show"
        transition={{ delay: 0.15 }}
        className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-6 md:p-7 shadow-[0_1px_2px_rgba(28,27,26,0.04),0_8px_24px_-8px_rgba(28,27,26,0.06)] hover:shadow-[0_1px_2px_rgba(28,27,26,0.06),0_12px_32px_-8px_rgba(28,27,26,0.10)] transition-shadow duration-200 space-y-3"
      >
        <div className="flex items-center justify-between">
          <h3 className="text-[15px] font-semibold text-[#0f0f0e] flex items-center gap-2 font-heading">
            <Tag aria-hidden="true" className="size-4 text-[#4f46e5]" />
            Top Saliency Keywords
          </h3>
          <span className="text-[11px] text-[#57534e] font-mono uppercase tracking-[0.12em] font-semibold">TF-IDF Weights</span>
        </div>

        {result.keywords.length > 0 ? (
          <div className="flex flex-wrap gap-2 pt-1">
            {result.keywords.map((kw, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3, delay: 0.18 + i * 0.04 }}
                whileHover={{ scale: 1.03, y: -1 }}
                className="flex items-center gap-1.5 rounded-lg border border-[#e7e3dd] bg-[#faf9f6] px-2.5 py-1 text-xs text-[#0f0f0e] shadow-sm cursor-default"
              >
                <Flame aria-hidden="true" className="size-3 text-[#d97706]" />
                <span className="font-semibold text-[#0f0f0e]">{kw.word}</span>
                <span className="font-mono font-semibold text-[11px] text-[#0e7490] rounded bg-[#ecfeff] px-1 py-0.2 border border-[#a5f3fc] tabular-nums">
                  {Math.round(kw.weight * 100)}%
                </span>
              </motion.div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-[#57534e] italic">No strong discriminative keywords identified in this text.</p>
        )}
      </motion.div>

      {/* Accordion: Neural Explainability */}
      <motion.div
        variants={fadeUp}
        initial="hidden"
        animate="show"
        transition={{ delay: 0.2 }}
        className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] shadow-[0_1px_2px_rgba(28,27,26,0.04),0_8px_24px_-8px_rgba(28,27,26,0.06)] hover:shadow-[0_1px_2px_rgba(28,27,26,0.06),0_12px_32px_-8px_rgba(28,27,26,0.10)] transition-shadow duration-200 overflow-hidden"
      >
        <button
          type="button"
          onClick={() => setShowExplanation(!showExplanation)}
          aria-expanded={showExplanation}
          className="flex w-full items-center justify-between p-5 md:p-6 text-left text-[14px] font-semibold text-[#0f0f0e] hover:bg-[#f1efeb] transition-colors focus-visible:ring-2 focus-visible:ring-[#4f46e5]/40 focus:outline-none"
        >
          <div className="flex items-center gap-2">
            <Info aria-hidden="true" className="size-4 text-[#0891b2]" />
            <span className="text-[14px]">Why this prediction? (Neural Explainability)</span>
          </div>
          <ChevronDown
            aria-hidden="true"
            className={`size-4 text-[#57534e] transition-transform duration-200 ${
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
                <span className="font-mono text-[#57534e] uppercase tracking-[0.12em] text-[11px] font-semibold">
                  Decision Factors:
                </span>
                <ul className="list-disc list-inside space-y-1 text-[#0f0f0e] font-medium pl-1 text-[13px]">
                  {result.explanation.top_factors.map((factor, i) => (
                    <li key={i}>{factor}</li>
                  ))}
                </ul>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Attention Heatmap Visualizer */}
      <motion.div
        variants={fadeUp}
        initial="hidden"
        animate="show"
        transition={{ delay: 0.25 }}
        className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-6 md:p-7 shadow-[0_1px_2px_rgba(28,27,26,0.04),0_8px_24px_-8px_rgba(28,27,26,0.06)] hover:shadow-[0_1px_2px_rgba(28,27,26,0.06),0_12px_32px_-8px_rgba(28,27,26,0.10)] transition-shadow duration-200 space-y-3"
      >
        <div className="flex items-center justify-between">
          <h3 className="text-[15px] font-semibold text-[#0f0f0e] font-heading flex items-center gap-2">
            <Sparkles aria-hidden="true" className="size-4 text-[#0891b2]" />
            Token Attention Heatmap
          </h3>
          <Button
            size="sm"
            variant="outline"
            className="text-xs h-7 rounded-md font-medium text-[#0f0f0e] hover:bg-[#f1efeb]"
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
              <div className="p-4 rounded-xl bg-[#faf9f6] border border-[#e7e3dd] text-[13px] leading-loose text-[#0f0f0e] font-mono max-h-56 overflow-y-auto">
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

export function EmptyResultsSkeleton() {
  return <ResultsPanel result={null} />;
}
