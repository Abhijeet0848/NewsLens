"use client";

import * as React from "react";
import Link from "next/link";
import {
  History,
  Trash2,
  Cpu,
  GitCompare,
  X,
  Award,
  ExternalLink,
  Loader2,
  Play,
  Sparkles,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { ClassifierInput } from "@/components/classifier-input";
import { ResultsPanel } from "@/components/results-panel";
import { useClassifierStore } from "@/lib/store";
import { classifyArticle } from "@/lib/api";
import { getCategoryConfig } from "@/lib/utils";
import { ModelId, MODELS } from "@/lib/models";
import { validateInput, sanitizeForApi } from "@/lib/validateInput";
import { toast } from "sonner";
import { ease, fadeUp } from "@/lib/motion";

function mapFriendlyError(err: any): string {
  const message = err?.message || "";
  const status = err?.status;

  if (
    status === 422 ||
    message.includes("422") ||
    message.includes("too short") ||
    message.includes("Text is too short")
  ) {
    return (
      message.replace(/^Backend error:\s*422\s*-\s*/i, "") ||
      "Text is too short for reliable classification. Please provide a full article or paragraph."
    );
  }

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
  const [isModalOpen, setIsModalOpen] = React.useState(false);

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
    } catch (err: any) {
      console.error("Classify error:", err);
      const is422 =
        err?.status === 422 ||
        err?.message?.includes("too short") ||
        err?.message?.includes("422");
      const friendlyMsg = mapFriendlyError(err);
      if (is422) {
        toast.error(friendlyMsg, {
          duration: 6000,
        });
      } else {
        toast.error(friendlyMsg);
      }
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
        resultsMap[m] = r;
      }

      setMultiResults(resultsMap);
      if (resultsMap[selectedModel]) {
        setResult(resultsMap[selectedModel]);
      } else if (resultsMap["linear-svm"]) {
        setResult(resultsMap["linear-svm"]);
      }
    } catch (err: any) {
      console.error("Compare error:", err);
      const is422 =
        err?.status === 422 ||
        err?.message?.includes("too short") ||
        err?.message?.includes("422");
      const friendlyMsg = mapFriendlyError(err);
      if (is422) {
        toast.error(friendlyMsg, {
          duration: 6000,
        });
      } else {
        toast.error(friendlyMsg);
      }
    } finally {
      setIsComparing(false);
    }
  };

  return (
    <main className="px-4 md:px-6 lg:px-8 py-8 max-w-7xl mx-auto w-full overflow-hidden">
      {/* Header Row */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 max-w-6xl mx-auto w-full">
        <div>
          <h1 className="font-heading text-3xl md:text-4xl font-semibold tracking-[-0.02em] text-[#0f0f0e]">
            News Article Classifier
          </h1>
          <p className="text-[14px] md:text-[15px] text-[#6b6660] max-w-2xl mt-2 leading-relaxed">
            Paste an article to see its predicted BBC domain.
          </p>
        </div>

        {/* Right-aligned Toolbar button */}
        <div className="flex items-center gap-3 w-full sm:w-auto">
          <motion.div whileHover={{ y: -1 }} whileTap={{ scale: 0.98 }} className="w-full sm:w-auto">
            <button
              type="button"
              onClick={() => {
                setIsModalOpen(true);
                if (currentText.trim().length >= 10 && !multiResults && !isComparing) {
                  handleCompareAll();
                }
              }}
              className="bg-[#fdfcfb] border border-[#e7e3dd] rounded-lg h-9 px-4 text-[13px] font-medium text-[#0f0f0e] hover:bg-[#f1efeb] hover:border-[#d6d1c9] transition-colors duration-150 flex items-center justify-center gap-2 w-full sm:w-auto shadow-sm cursor-pointer"
            >
              <GitCompare className="size-4 text-[#57534e]" />
              <span>{isComparing ? "Benchmarking..." : "Compare 4 Models"}</span>
            </button>
          </motion.div>
        </div>
      </div>

      {/* Main Grid: 1 col on mobile, 2 equal cols on desktop */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 max-w-6xl mx-auto w-full mt-8 items-start">
        {/* Left Column */}
        <motion.div
          variants={fadeUp}
          initial="hidden"
          animate="show"
          transition={{ duration: 0.4, delay: 0, ease: ease.smooth }}
          className="flex flex-col space-y-5 min-w-0"
        >
          <div className="flex-1 min-w-0">
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
          className="flex flex-col space-y-5 min-w-0"
        >
          <div className="flex-1 min-w-0">
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
                className="rounded-2xl border border-indigo-200 bg-[#f5f3ff] p-6 shadow-[0_1px_2px_rgba(28,27,26,0.04),0_8px_24px_-8px_rgba(28,27,26,0.06)] space-y-4 min-w-0 overflow-hidden"
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
                        className="rounded-xl border border-[#e7e3dd] bg-[#fdfcfb] p-3 space-y-1 shadow-sm min-w-0 overflow-hidden"
                      >
                        <span className="text-[11px] font-mono font-semibold uppercase tracking-[0.14em] text-[#57534e] block truncate">
                          {mKey.replace("_", " ")}
                        </span>
                        <div className="flex items-center justify-between font-bold text-[#0f0f0e] text-[13px] gap-1">
                          <span className="truncate">{data.category}</span>
                          <span className="text-[#0e7490] font-mono tabular-nums font-semibold shrink-0">{data.confidence_percentage}%</span>
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

      {/* 4-Model Comparison & Benchmarking Modal */}
      <AnimatePresence>
        {isModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 overflow-y-auto">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsModalOpen(false)}
              className="fixed inset-0 bg-[#0f0f0e]/50 backdrop-blur-sm"
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 12 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 12 }}
              transition={{ duration: 0.2 }}
              className="relative w-full max-w-2xl rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] shadow-2xl text-left z-10 max-h-[85vh] md:max-h-[90vh] flex flex-col overflow-hidden"
            >
              {/* Modal Header */}
              <div className="sticky top-0 bg-[#fdfcfb] z-10 flex items-center justify-between px-6 py-4 border-b border-[#e7e3dd]">
                <div className="flex items-center gap-2.5">
                  <div className="flex size-9 items-center justify-center rounded-xl bg-indigo-50 border border-indigo-100 text-[#4f46e5]">
                    <GitCompare className="size-4.5" />
                  </div>
                  <div>
                    <h2 className="font-heading text-base font-semibold text-[#0f0f0e]">
                      4-Model Architecture Comparison
                    </h2>
                    <p className="text-xs text-[#57534e]">
                      Held-out test evaluation benchmarks &amp; live simultaneous inference
                    </p>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  aria-label="Close comparison modal"
                  className="p-1.5 rounded-lg hover:bg-[#f1efeb] text-[#57534e] transition-colors focus-visible:ring-2 focus-visible:ring-[#4f46e5]/40 focus:outline-none cursor-pointer"
                >
                  <X aria-hidden="true" className="size-4.5" />
                </button>
              </div>

              {/* Scrollable Content Wrapper */}
              <div className="flex-1 overflow-y-auto px-6 py-5 space-y-6">
                {/* Leaderboard Table */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] font-mono uppercase tracking-[0.12em] font-semibold text-[#57534e] flex items-center gap-1.5">
                      <Award className="size-3.5 text-[#d97706]" />
                      Architecture Leaderboard
                    </span>
                    <span className="text-[11px] font-mono text-[#059669] font-medium">
                      Evaluated on 445 Held-Out Articles
                    </span>
                  </div>

                  <div className="overflow-x-auto rounded-xl border border-[#e7e3dd]">
                    <table className="w-full text-left text-xs">
                      <thead className="bg-[#f1efeb] text-[#3f3d3a] font-mono uppercase tracking-wider font-semibold">
                        <tr>
                          <th className="p-2.5">Model</th>
                          <th className="p-2.5">Paradigm</th>
                          <th className="p-2.5">Accuracy</th>
                          <th className="p-2.5">Latency</th>
                          <th className="p-2.5">Status</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-[#e7e3dd]">
                        {[
                          {
                            name: "DistilBERT",
                            paradigm: "Transformer Attention",
                            acc: "97.8%",
                            lat: "12.4 ms",
                            role: "High Capacity",
                            roleColor: "text-purple-700 bg-purple-50 border-purple-200",
                          },
                          {
                            name: "Linear SVM",
                            paradigm: "Maximum-Margin (Platt)",
                            acc: "96.4%",
                            lat: "1.2 ms",
                            role: "Champion",
                            roleColor: "text-emerald-700 bg-emerald-50 border-emerald-200 font-semibold",
                          },
                          {
                            name: "Neural MLP",
                            paradigm: "Multi-Layer Perceptron",
                            acc: "95.1%",
                            lat: "3.2 ms",
                            role: "Neural Baseline",
                            roleColor: "text-indigo-700 bg-indigo-50 border-indigo-200",
                          },
                          {
                            name: "Naive Bayes",
                            paradigm: "Multinomial Generative",
                            acc: "92.1%",
                            lat: "0.5 ms",
                            role: "Fast Baseline",
                            roleColor: "text-slate-700 bg-slate-100 border-slate-200",
                          },
                        ].map((item) => (
                          <tr key={item.name} className="hover:bg-[#f8f7f5] transition-colors">
                            <td className="p-2.5 font-semibold text-[#0f0f0e]">
                              {item.name}
                            </td>
                            <td className="p-2.5 text-[#57534e]">
                              {item.paradigm}
                            </td>
                            <td className="p-2.5 font-mono font-bold text-[#059669] tabular-nums">
                              {item.acc}
                            </td>
                            <td className="p-2.5 font-mono text-[#0891b2] tabular-nums font-medium">
                              {item.lat}
                            </td>
                            <td className="p-2.5">
                              <span className={`inline-block px-1.5 py-0.5 rounded text-[10px] font-mono border ${item.roleColor}`}>
                                {item.role}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* Live Inference Benchmark Section */}
                <div className="space-y-3 pt-1">
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] font-mono uppercase tracking-[0.12em] font-semibold text-[#57534e] flex items-center gap-1.5">
                      <Sparkles className="size-3.5 text-[#4f46e5]" />
                      Live Simultaneous Inference
                    </span>
                    {currentText.trim().length >= 10 && (
                      <button
                        type="button"
                        onClick={handleCompareAll}
                        disabled={isComparing}
                        className="text-xs text-[#4f46e5] font-medium hover:underline flex items-center gap-1 disabled:opacity-50 cursor-pointer"
                      >
                        {isComparing ? (
                          <>
                            <Loader2 className="size-3 animate-spin" />
                            <span>Benchmarking...</span>
                          </>
                        ) : (
                          <>
                            <Play className="size-3" />
                            <span>Re-run Benchmark</span>
                          </>
                        )}
                      </button>
                    )}
                  </div>

                  {isComparing ? (
                    <div className="flex items-center justify-center p-8 rounded-xl border border-indigo-100 bg-[#f5f3ff] text-indigo-700 text-xs font-medium gap-2">
                      <Loader2 className="size-4 animate-spin" />
                      <span>Running simultaneous inference across Linear SVM, DistilBERT, Neural MLP, and Naive Bayes...</span>
                    </div>
                  ) : multiResults ? (
                    <div className="grid grid-cols-2 gap-2.5">
                      {Object.entries(multiResults).map(([mKey, data]) => {
                        const modelConfig = MODELS[mKey as ModelId];
                        const cfg = getCategoryConfig(data.category);
                        return (
                          <div
                            key={mKey}
                            className="rounded-xl border border-[#e7e3dd] bg-[#fbfaf9] p-3 space-y-1.5 shadow-2xs"
                          >
                            <div className="flex items-center justify-between">
                              <span className="text-[11px] font-mono font-semibold uppercase tracking-[0.12em] text-[#57534e] truncate">
                                {modelConfig?.name || mKey}
                              </span>
                              <span className="text-[10px] font-mono text-[#0891b2] tabular-nums font-medium">
                                {data.latency_ms ? `${data.latency_ms.toFixed(1)}ms` : `${modelConfig?.latency || 1.2}ms`}
                              </span>
                            </div>
                            <div className="flex items-center justify-between">
                              <span className={`inline-block px-2 py-0.5 rounded text-xs font-semibold ${cfg.badgeClass}`}>
                                {data.category}
                              </span>
                              <span className="font-mono text-xs font-bold text-[#0f0f0e] tabular-nums">
                                {data.confidence_percentage}%
                              </span>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  ) : currentText.trim().length >= 10 ? (
                    <div className="flex items-center justify-between p-4 rounded-xl border border-[#e7e3dd] bg-[#fbfaf9]">
                      <div className="space-y-0.5">
                        <p className="text-xs font-medium text-[#0f0f0e]">Article text is ready in the classifier</p>
                        <p className="text-[11px] text-[#57534e]">Click below to run real-time inference across all 4 architectures.</p>
                      </div>
                      <button
                        type="button"
                        onClick={handleCompareAll}
                        className="px-3 py-1.5 rounded-lg bg-[#4f46e5] text-white text-xs font-medium hover:bg-[#4338ca] transition-colors flex items-center gap-1.5 shadow-xs shrink-0 cursor-pointer"
                      >
                        <Play className="size-3" />
                        <span>Benchmark Now</span>
                      </button>
                    </div>
                  ) : (
                    <div className="p-4 rounded-xl border border-dashed border-[#e7e3dd] bg-[#fbfaf9] text-center space-y-1">
                      <p className="text-xs text-[#57534e]">
                        Paste an article into the classifier input to benchmark predictions across all 4 models live.
                      </p>
                    </div>
                  )}
                </div>
              </div>

              {/* Modal Footer */}
              <div className="sticky bottom-0 bg-[#fdfcfb] z-10 px-6 py-3.5 border-t border-[#e7e3dd] flex items-center justify-between">
                <Link
                  href="/analytics#model-comparison"
                  onClick={() => setIsModalOpen(false)}
                  className="text-xs text-[#4f46e5] hover:text-[#4338ca] font-medium flex items-center gap-1 hover:underline transition-colors"
                >
                  <span>View Full Evaluation Analytics &amp; Confusion Matrix</span>
                  <ExternalLink className="size-3" />
                </Link>

                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="h-8 px-4 rounded-lg border border-[#e7e3dd] bg-[#fdfcfb] text-xs font-medium text-[#0f0f0e] hover:bg-[#f1efeb] transition-colors cursor-pointer"
                >
                  Close
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </main>
  );
}
