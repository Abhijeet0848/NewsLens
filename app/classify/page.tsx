"use client";

import * as React from "react";
import {
  History,
  Trash2,
  Cpu,
  GitCompare,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { ClassifierInput } from "@/components/classifier-input";
import { ResultsPanel } from "@/components/results-panel";
import { useClassifierStore } from "@/lib/store";
import { classifyArticle } from "@/lib/api";
import { getCategoryConfig } from "@/lib/utils";
import { ModelId } from "@/lib/models";
import { validateInput, sanitizeForApi } from "@/lib/validateInput";
import { toast } from "sonner";
import { ease, fadeUp } from "@/lib/motion";

function mapFriendlyError(err: any): string {
  const message = err?.message || "";
  if (typeof navigator !== "undefined" && !navigator.onLine) {
    return "Connection issue. Check your internet.";
  }
  if (message.includes("Failed to fetch") || message.includes("NetworkError")) {
    return "Connection issue. Check your internet or API server.";
  }
  if (message.includes("429") || message.includes("Too many requests")) {
    return "Too many requests. Please wait a moment.";
  }
  if (message.includes("500") || message.includes("Server error")) {
    return "Server error. Please try again.";
  }
  if (message.includes("timeout") || message.includes("Timed out") || message.includes("timed out")) {
    return "Request timed out. Please try again.";
  }
  return message || "Classification failed. Please try again.";
}

export default function ClassifyPage() {
  const {
    currentText,
    setCurrentText,
    selectedModel,
    setSelectedModel,
    result,
    setResult,
    isLoading,
    setIsLoading,
    history,
    addToHistory,
    clearHistory,
    incrementCount,
  } = useClassifierStore();

  const [multiResults, setMultiResults] = React.useState<Record<string, any> | null>(null);
  const [isComparing, setIsComparing] = React.useState(false);

  const handleTextChange = (val: string) => {
    setCurrentText(val);
    if (result) {
      setResult(null);
    }
  };

  const handleClassify = async () => {
    const v = validateInput(currentText);

    if (!v.ok) {
      toast.error(v.reason || "Please enter an article to classify.");
      return;
    }

    if (v.warning) {
      toast.warning(v.warning);
    }

    const clean = v.sanitized || sanitizeForApi(currentText);
    setIsLoading(true);

    try {
      const res = await classifyArticle(clean, selectedModel);

      // Apply confidence penalty on suspicious inputs if flagged
      if (v.confidence_penalty) {
        const factor = 1 - v.confidence_penalty;
        res.confidence = Math.max(0.18, Math.round(res.confidence * factor * 1000) / 1000);
        res.confidence_percentage = Math.round(res.confidence * 1000) / 10;
        if (res.all_scores) {
          const remaining = (1 - res.confidence) / 4;
          for (const key of Object.keys(res.all_scores)) {
            res.all_scores[key] = key === res.category ? res.confidence : Math.round(remaining * 1000) / 1000;
          }
        }
      }

      // Low confidence alert
      if (res.confidence < 0.4) {
        toast.warning(
          `Low confidence (${Math.round(res.confidence * 100)}%). The article may be outside the model's training distribution.`
        );
      }

      setResult(res);
      addToHistory({
        id: `hist-${Date.now()}`,
        textSnippet: clean.slice(0, 85) + "...",
        category: res.category,
        confidence: res.confidence_percentage,
        timestamp: "Just now",
      });
      incrementCount();
      toast.success(`Predicted: ${res.category} (${res.confidence_percentage}%)`);
    } catch (err: any) {
      console.error("Classify error:", err);
      toast.error(mapFriendlyError(err));
    } finally {
      // CRITICAL: Always clear loading state
      setIsLoading(false);
    }
  };

  const handleCompareAll = async () => {
    const v = validateInput(currentText);

    if (!v.ok) {
      toast.error(v.reason || "Please enter an article to benchmark.");
      return;
    }

    if (v.warning) {
      toast.warning(v.warning);
    }

    const clean = v.sanitized || sanitizeForApi(currentText);
    setIsComparing(true);

    try {
      const models: ModelId[] = ["linear-svm", "distilbert", "neural-mlp", "naive-bayes"];
      const resultsMap: Record<string, any> = {};

      for (const m of models) {
        const r = await classifyArticle(clean, m);
        if (v.confidence_penalty) {
          const factor = 1 - v.confidence_penalty;
          r.confidence = Math.max(0.18, Math.round(r.confidence * factor * 1000) / 1000);
          r.confidence_percentage = Math.round(r.confidence * 1000) / 10;
        }
        resultsMap[m] = r;
      }

      setMultiResults(resultsMap);
      if (resultsMap[selectedModel]) {
        setResult(resultsMap[selectedModel]);
      } else if (resultsMap["linear-svm"]) {
        setResult(resultsMap["linear-svm"]);
      }
      toast.success("Benchmark completed across 4 model architectures");
    } catch (err: any) {
      console.error("Compare error:", err);
      toast.error(mapFriendlyError(err));
    } finally {
      setIsComparing(false);
    }
  };

  return (
    <div className="mx-auto max-w-6xl px-5 md:px-8 pt-10 pb-16">
      {/* Header Row */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <span className="text-[11px] uppercase tracking-[0.14em] text-[#0891b2] font-mono font-semibold block mb-2">
            INTERACTIVE CLASSIFICATION WORKSPACE
          </span>
          <h1 className="font-heading text-3xl md:text-4xl font-semibold tracking-[-0.02em] text-[#0f0f0e]">
            News Article Classifier
          </h1>
          <p className="text-[14px] md:text-[15px] text-[#3f3d3a] max-w-2xl mt-2 leading-relaxed">
            Input news copy to obtain calibrated domain predictions, statistical distributions, and token saliency.
          </p>
        </div>

        {/* Right-aligned Toolbar button */}
        <div className="flex items-center gap-3 w-full sm:w-auto">
          <motion.div whileHover={{ y: -1 }} whileTap={{ scale: 0.98 }} className="w-full sm:w-auto">
            <button
              type="button"
              onClick={handleCompareAll}
              disabled={isComparing || isLoading}
              className="bg-[#fdfcfb] border border-[#e7e3dd] rounded-lg h-9 px-4 text-[13px] font-medium text-[#0f0f0e] hover:bg-[#f1efeb] hover:border-[#d6d1c9] transition-colors duration-150 flex items-center justify-center gap-2 w-full sm:w-auto shadow-sm disabled:opacity-50 disabled:pointer-events-none"
            >
              <GitCompare className="size-4 text-[#57534e]" />
              <span>{isComparing ? "Benchmarking..." : "Compare 4 Models"}</span>
            </button>
          </motion.div>
        </div>
      </div>

      {/* Main Grid: 1.1fr / 1fr Split on lg+, stacked on mobile */}
      <div className="grid grid-cols-1 lg:grid-cols-[1.1fr_1fr] gap-5 md:gap-6 items-stretch mt-8">
        {/* Left Column */}
        <motion.div
          variants={fadeUp}
          initial="hidden"
          animate="show"
          transition={{ duration: 0.4, delay: 0, ease: ease.smooth }}
          className="flex flex-col space-y-5"
        >
          <div className="flex-1">
            <ClassifierInput
              text={currentText}
              onChangeText={handleTextChange}
              selectedModel={selectedModel}
              onChangeModel={setSelectedModel}
              onClassify={handleClassify}
              isLoading={isLoading}
            />
          </div>

          {/* Recent History Card */}
          {history.length > 0 && (
            <motion.div
              variants={fadeUp}
              initial="hidden"
              animate="show"
              className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-6 shadow-[0_1px_2px_rgba(28,27,26,0.04),0_8px_24px_-8px_rgba(28,27,26,0.06)] hover:shadow-[0_1px_2px_rgba(28,27,26,0.06),0_12px_32px_-8px_rgba(28,27,26,0.10)] transition-shadow duration-200 space-y-3"
            >
              <div className="flex items-center justify-between border-b border-[#e7e3dd] pb-3">
                <h2 className="text-[11px] uppercase tracking-[0.14em] text-[#57534e] font-mono flex items-center gap-1.5 font-semibold">
                  <History aria-hidden="true" className="size-3.5 text-[#4f46e5]" />
                  Recent Classifications ({history.length})
                </h2>
                <button
                  type="button"
                  onClick={clearHistory}
                  aria-label="Clear classification history"
                  className="text-[12px] text-[#57534e] hover:text-[#dc2626] transition-colors flex items-center gap-1 font-medium focus-visible:ring-2 focus-visible:ring-[#4f46e5]/40 focus:outline-none"
                >
                  <Trash2 aria-hidden="true" className="size-3.5" /> Clear History
                </button>
              </div>

              <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
                {history.map((item) => {
                  const cfg = getCategoryConfig(item.category);
                  return (
                    <motion.div
                      key={item.id}
                      whileHover={{ y: -1 }}
                      whileTap={{ scale: 0.99 }}
                      onClick={() => {
                        setCurrentText(item.textSnippet);
                        if (result) setResult(null);
                      }}
                      className="group flex items-center justify-between rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-3 text-[13px] text-[#3f3d3a] hover:bg-[#f1efeb] hover:text-[#0f0f0e] cursor-pointer shadow-sm transition-all"
                    >
                      <div className="flex items-center gap-3 truncate pr-2">
                        <span
                          className="size-2 rounded-full flex-shrink-0"
                          style={{ backgroundColor: cfg.colorHex }}
                        />
                        <span className="truncate font-sans text-[#3f3d3a] font-medium group-hover:text-[#0f0f0e]">
                          {item.textSnippet}
                        </span>
                      </div>
                      <div className="flex items-center gap-2 flex-shrink-0 font-mono text-[12px] tabular-nums">
                        <span className={`px-2 py-0.5 rounded border text-[11px] font-semibold ${cfg.badgeClass}`}>
                          {item.category}
                        </span>
                        <span className="text-[#0f0f0e] font-semibold">{item.confidence}%</span>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </motion.div>
          )}
        </motion.div>

        {/* Right Column */}
        <motion.div
          variants={fadeUp}
          initial="hidden"
          animate="show"
          transition={{ duration: 0.4, delay: 0.08, ease: ease.smooth }}
          className="flex flex-col space-y-5"
        >
          <div className="flex-1">
            <ResultsPanel
              result={result}
              isLoading={isLoading}
              text={currentText}
              selectedModel={selectedModel}
            />
          </div>

          {/* 4-Model Consensus Grid */}
          <AnimatePresence>
            {multiResults && (
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -12 }}
                className="rounded-2xl border border-indigo-200 bg-[#f5f3ff] p-6 shadow-[0_1px_2px_rgba(28,27,26,0.04),0_8px_24px_-8px_rgba(28,27,26,0.06)] space-y-4"
              >
                <div className="flex items-center justify-between">
                  <h2 className="text-[14px] font-semibold text-[#0f0f0e] flex items-center gap-2 font-heading">
                    <Cpu aria-hidden="true" className="size-4 text-[#4f46e5]" />
                    Consensus Across 4 Architectures
                  </h2>
                  <span className="text-[11px] font-mono font-semibold text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded border border-indigo-200">
                    Simultaneous
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-2.5 text-xs">
                  {Object.entries(multiResults).map(([mKey, data]) => {
                    return (
                      <div
                        key={mKey}
                        className="rounded-xl border border-[#e7e3dd] bg-[#fdfcfb] p-3 space-y-1 shadow-sm"
                      >
                        <span className="text-[11px] font-mono font-semibold uppercase tracking-[0.14em] text-[#57534e] block">
                          {mKey.replace("_", " ")}
                        </span>
                        <div className="flex items-center justify-between font-bold text-[#0f0f0e] text-[13px]">
                          <span>{data.category}</span>
                          <span className="text-[#0e7490] font-mono tabular-nums font-semibold">{data.confidence_percentage}%</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </div>
  );
}
