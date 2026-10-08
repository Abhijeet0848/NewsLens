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
import { ResultsPanel, EmptyResultsSkeleton } from "@/components/results-panel";
import { Button } from "@/components/ui/button";
import { useClassifierStore } from "@/lib/store";
import { classifyArticle } from "@/lib/api";
import { getCategoryConfig } from "@/lib/utils";
import { toast } from "sonner";
import { ease, fadeUp } from "@/lib/motion";

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

  const handleClassify = async () => {
    if (!currentText.trim() || currentText.length < 50) {
      toast.error("Please provide at least 50 characters for neural classification");
      return;
    }
    setIsLoading(true);
    try {
      const res = await classifyArticle(currentText, selectedModel);
      setResult(res);
      addToHistory({
        id: `hist-${Date.now()}`,
        textSnippet: currentText.slice(0, 85) + "...",
        category: res.category,
        confidence: res.confidence_percentage,
        timestamp: "Just now",
      });
      incrementCount();
      toast.success(`Predicted: ${res.category} (${res.confidence_percentage}%)`);
    } catch (err: any) {
      toast.error(err.message || "Classification failed");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCompareAll = async () => {
    if (!currentText.trim() || currentText.length < 50) {
      toast.error("Please provide at least 50 characters to benchmark models");
      return;
    }
    setIsComparing(true);
    try {
      const models = ["distilbert", "linear_svm", "mlp", "naive_bayes"];
      const resultsMap: Record<string, any> = {};

      for (const m of models) {
        const r = await classifyArticle(currentText, m);
        resultsMap[m] = r;
      }

      setMultiResults(resultsMap);
      if (resultsMap["distilbert"]) {
        setResult(resultsMap["distilbert"]);
      }
      toast.success("Benchmark completed across 4 model architectures");
    } catch {
      toast.error("Multi-model comparison failed");
    } finally {
      setIsComparing(false);
    }
  };

  return (
    <div className="mx-auto max-w-7xl px-5 md:px-8 pt-8 md:pt-10 pb-16 md:pb-20 space-y-6 md:space-y-8">
      {/* Header Row */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div className="space-y-1">
          <span className="text-[10px] md:text-[11px] uppercase tracking-[0.14em] text-[#0891b2] font-mono font-semibold block">
            INTERACTIVE CLASSIFICATION WORKSPACE
          </span>
          <h1 className="font-heading text-2xl sm:text-3xl font-semibold tracking-[-0.02em] text-[#0f0f0e]">
            News Article Classifier
          </h1>
          <p className="text-[13px] md:text-sm text-[#3f3d3a] max-w-2xl leading-relaxed">
            Input news copy to obtain calibrated domain predictions, statistical distributions, and token saliency.
          </p>
        </div>

        {/* Right-aligned Toolbar button */}
        <div className="flex items-center gap-3 w-full sm:w-auto">
          <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }} className="w-full sm:w-auto">
            <Button
              variant="secondary"
              size="sm"
              onClick={handleCompareAll}
              disabled={isComparing || isLoading}
              className="gap-2 h-11 sm:h-10 px-4 rounded-xl text-xs font-medium border border-[#e7e3dd] shadow-sm text-[#3f3d3a] w-full sm:w-auto"
            >
              <GitCompare className="size-4 text-indigo-600" />
              <span>{isComparing ? "Benchmarking..." : "Compare 4 Models"}</span>
            </Button>
          </motion.div>
        </div>
      </div>

      {/* Divider */}
      <div className="border-t border-[#e7e3dd]" />

      {/* Main Grid: 55 / 45 Split on lg+, stacked on mobile */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 md:gap-8 items-stretch">
        {/* Left Column (55% -> 7 cols) */}
        <motion.div
          variants={fadeUp}
          initial="hidden"
          animate="show"
          transition={{ duration: 0.4, ease: ease.smooth }}
          className="lg:col-span-7 flex flex-col space-y-6"
        >
          <div className="flex-1">
            <ClassifierInput
              text={currentText}
              onChangeText={setCurrentText}
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
              className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-6 shadow-[0_8px_24px_rgba(15,15,14,0.06),0_2px_6px_rgba(15,15,14,0.04)] space-y-3"
            >
              <div className="flex items-center justify-between border-b border-[#e7e3dd] pb-3">
                <span className="text-[11px] uppercase tracking-[0.14em] text-[#6b6660] font-mono flex items-center gap-1.5 font-semibold">
                  <History className="size-3.5 text-indigo-600" />
                  Recent Classifications ({history.length})
                </span>
                <button
                  type="button"
                  onClick={clearHistory}
                  className="text-xs text-[#6b6660] hover:text-[#dc2626] transition-colors flex items-center gap-1 font-medium"
                >
                  <Trash2 className="size-3" /> Clear History
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
                      onClick={() => setCurrentText(item.textSnippet)}
                      className="group flex items-center justify-between rounded-xl border border-[#e7e3dd] bg-[#fdfcfb] p-3 text-xs text-[#3f3d3a] hover:bg-[#f1efeb] hover:text-[#0f0f0e] cursor-pointer shadow-sm transition-all"
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
                      <div className="flex items-center gap-2 flex-shrink-0 font-mono text-xs tabular-nums">
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

        {/* Right Column (45% -> 5 cols) */}
        <motion.div
          variants={fadeUp}
          initial="hidden"
          animate="show"
          transition={{ duration: 0.4, delay: 0.1, ease: ease.smooth }}
          className="lg:col-span-5 flex flex-col space-y-6"
        >
          <div className="flex-1">
            <AnimatePresence mode="wait">
              {result ? (
                <ResultsPanel key="results" result={result} originalText={currentText} />
              ) : (
                <EmptyResultsSkeleton key="empty" />
              )}
            </AnimatePresence>
          </div>

          {/* 4-Model Consensus Grid */}
          <AnimatePresence>
            {multiResults && (
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -12 }}
                className="rounded-2xl border border-indigo-200 bg-[#f5f3ff] p-6 shadow-[0_8px_24px_rgba(15,15,14,0.06),0_2px_6px_rgba(15,15,14,0.04)] space-y-4"
              >
                <div className="flex items-center justify-between">
                  <h4 className="text-base font-semibold text-[#0f0f0e] flex items-center gap-2 font-heading">
                    <Cpu className="size-4 text-indigo-600" />
                    Consensus Across 4 Architectures
                  </h4>
                  <span className="text-xs font-mono font-medium text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded border border-indigo-200">
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
                        <span className="text-[11px] font-mono font-semibold uppercase tracking-[0.14em] text-[#6b6660] block">
                          {mKey.replace("_", " ")}
                        </span>
                        <div className="flex items-center justify-between font-bold text-[#0f0f0e]">
                          <span>{data.category}</span>
                          <span className="text-[#0891b2] font-mono tabular-nums font-semibold">{data.confidence_percentage}%</span>
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
