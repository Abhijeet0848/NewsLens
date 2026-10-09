"use client";

import * as React from "react";
import {
  Award,
  Target,
  BarChart3,
  Terminal,
  Copy,
  Check,
  X,
  HelpCircle,
} from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { ConfusionMatrix } from "@/components/confusion-matrix";
import {
  getMetrics,
  getBestModel,
  hasMetrics,
  MODEL_PARADIGMS,
} from "@/lib/metrics";
import { Button } from "@/components/ui/button";
import { motion, AnimatePresence } from "framer-motion";

export default function AnalyticsDashboardPage() {
  const [modalOpen, setModalOpen] = React.useState(false);
  const [copied, setCopied] = React.useState(false);

  const metrics = getMetrics();
  const bestModelEntry = getBestModel();
  const isMetricsAvailable = hasMetrics() && bestModelEntry !== null;

  const handleCopyCommand = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!isMetricsAvailable) {
    return (
      <div className="relative mx-auto max-w-4xl px-5 md:px-8 pt-16 md:pt-24 pb-24 text-center">
        {/* Faint Dot Grid Pattern */}
        <div className="absolute inset-x-0 top-0 h-64 -z-10 pointer-events-none opacity-20 [background-image:radial-gradient(#d6d1c9_1px,transparent_1px)] [background-size:24px_24px] [mask-image:radial-gradient(ellipse_at_center_top,black_30%,transparent_70%)]" />

        <div className="mx-auto max-w-md space-y-6">
          <div className="mx-auto flex size-14 items-center justify-center rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] shadow-xs text-indigo-600">
            <Terminal className="size-7" />
          </div>

          <div className="space-y-2">
            <h1 className="font-heading text-2xl sm:text-3xl font-bold tracking-tight text-[#0f0f0e]">
              No Training Metrics Yet
            </h1>
            <p className="text-sm text-[#57534e] leading-relaxed">
              No training metrics found. Run the training pipeline to generate{" "}
              <code className="rounded bg-[#f1efeb] px-1.5 py-0.5 text-xs font-mono text-[#0f0f0e]">
                data/metrics.json
              </code>
              .
            </p>
          </div>

          <div className="pt-2 flex justify-center">
            <Button
              type="button"
              onClick={() => setModalOpen(true)}
              className="gap-2 h-11 px-6 rounded-lg bg-[#4f46e5] text-white text-sm font-medium shadow-[0_2px_8px_rgba(79,70,229,0.20)] hover:bg-[#4338ca] hover:shadow-[0_4px_12px_rgba(79,70,229,0.28)] hover:-translate-y-px active:translate-y-0 active:scale-[0.98] transition-all duration-200"
            >
              <HelpCircle className="size-4" />
              <span>How to Train the Model</span>
            </Button>
          </div>
        </div>

        {/* Modal: How to Train */}
        <AnimatePresence>
          {modalOpen && (
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setModalOpen(false)}
                className="fixed inset-0 bg-[#0f0f0e]/40 backdrop-blur-xs"
              />
              <motion.div
                initial={{ opacity: 0, scale: 0.95, y: 10 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95, y: 10 }}
                transition={{ duration: 0.2 }}
                className="relative w-full max-w-lg rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-6 shadow-2xl text-left space-y-5 z-10"
              >
                <div className="flex items-center justify-between pb-2 border-b border-[#e7e3dd]">
                  <div className="flex items-center gap-2">
                    <Terminal className="size-5 text-indigo-600" />
                    <h3 className="font-heading text-base font-semibold text-[#0f0f0e]">
                      Model Training Pipeline
                    </h3>
                  </div>
                  <button
                    type="button"
                    onClick={() => setModalOpen(false)}
                    className="p-1 rounded-lg hover:bg-[#f1efeb] text-[#6b6660] transition-colors"
                  >
                    <X className="size-4.5" />
                  </button>
                </div>

                <div className="space-y-3 text-xs text-[#3f3d3a] leading-relaxed">
                  <p>
                    Run the Python training script from the root of your project
                    to train all supervised baseline classifiers and export test metrics:
                  </p>

                  <div className="relative rounded-xl border border-[#e7e3dd] bg-[#0f0f0e] p-4 text-[#fdfcfb] font-mono text-xs">
                    <pre className="overflow-x-auto text-[#34d399]">
                      python src/train.py
                    </pre>
                    <button
                      type="button"
                      onClick={() => handleCopyCommand("python src/train.py")}
                      aria-label="Copy training command"
                      className="absolute right-3 top-3 flex size-7 items-center justify-center rounded-md bg-white/10 text-white/80 hover:bg-white/20 hover:text-white transition-colors"
                    >
                      {copied ? <Check className="size-3.5" /> : <Copy className="size-3.5" />}
                    </button>
                  </div>

                  <p className="text-[#6b6660]">
                    This will split the corpus (80/20 train/test), fit TF-IDF feature representations, train Naive Bayes, Linear SVM, Decision Tree, and MLP, and automatically generate <code className="font-mono text-[#0f0f0e]">data/metrics.json</code>.
                  </p>
                </div>

                <div className="pt-2 flex justify-end">
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => setModalOpen(false)}
                    className="h-9 px-4 rounded-lg text-xs"
                  >
                    Close
                  </Button>
                </div>
              </motion.div>
            </div>
          )}
        </AnimatePresence>
      </div>
    );
  }

  const [bestModelKey, bestModelData] = bestModelEntry;
  const bestMeta = MODEL_PARADIGMS[bestModelKey] || {
    name: bestModelKey,
    paradigm: bestModelData.paradigm || "Machine Learning",
    badge: "Champion",
  };

  // Compute per-class breakdown from confusion matrix
  const perClassData = (bestModelData.classes || []).map((className, idx) => {
    const row = bestModelData.confusion_matrix?.[idx] || [];
    const correct = row[idx] || 0;
    const total = row.reduce((a, b) => a + b, 0);
    const accuracyPct = total > 0 ? Math.round((correct / total) * 100) : 0;
    return {
      category: className,
      accuracy: accuracyPct,
      correct,
      total,
    };
  });

  const formatPct = (num: number) => {
    if (num === undefined || num === null) return "0.0%";
    const val = num > 1 ? num : num * 100;
    return `${val.toFixed(1)}%`;
  };

  return (
    <div className="relative mx-auto max-w-7xl px-5 md:px-8 pt-8 md:pt-12 pb-16 md:pb-20 space-y-6 md:space-y-10">
      {/* Faint Dot Grid Pattern */}
      <div className="absolute inset-x-0 top-0 h-52 -z-10 pointer-events-none opacity-20 [background-image:radial-gradient(#d6d1c9_1px,transparent_1px)] [background-size:24px_24px] [mask-image:linear-gradient(to_bottom,black_20%,transparent_100%)]" />

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div className="space-y-1">
          <span className="text-[10px] md:text-[11px] uppercase tracking-[0.14em] text-[#0891b2] font-mono font-semibold block">
            TRAINING & EVALUATION BENCHMARK
          </span>
          <h1 className="font-heading text-2xl sm:text-3xl font-semibold tracking-tight text-[#0f0f0e]">
            Performance & Evaluation Analytics
          </h1>
          <p className="text-[13px] md:text-sm text-[#3f3d3a] max-w-2xl leading-relaxed">
            Real metrics loaded from held-out test split evaluation (Champion:{" "}
            <strong className="text-[#0f0f0e]">{bestMeta.name}</strong>).
          </p>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs text-[#3f3d3a]">
          <span className="size-2 rounded-full bg-[#059669]" />
          <span>Champion: {bestMeta.name}</span>
        </div>
      </div>

      <div className="border-t border-[#e7e3dd]" />

      {/* 4 Metric Cards (Champion Model) */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-xs space-y-1">
          <span className="text-xs font-mono font-medium text-[#6b6660]">Test Accuracy</span>
          <div className="font-heading text-2xl md:text-3xl font-bold text-[#0f0f0e] font-mono tabular-nums">
            {formatPct(bestModelData.accuracy)}
          </div>
          <p className="text-xs text-[#6b6660] font-mono">Overall test classification</p>
        </div>

        <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-xs space-y-1">
          <span className="text-xs font-mono font-medium text-[#6b6660]">Macro F1 Score</span>
          <div className="font-heading text-2xl md:text-3xl font-bold text-[#0f0f0e] font-mono tabular-nums">
            {formatPct(bestModelData.f1_macro)}
          </div>
          <p className="text-xs text-[#6b6660] font-mono">Unweighted harmonic mean</p>
        </div>

        <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-xs space-y-1">
          <span className="text-xs font-mono font-medium text-[#6b6660]">Macro Precision</span>
          <div className="font-heading text-2xl md:text-3xl font-bold text-[#0f0f0e] font-mono tabular-nums">
            {formatPct(bestModelData.precision)}
          </div>
          <p className="text-xs text-[#6b6660] font-mono">Exactness ratio</p>
        </div>

        <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-xs space-y-1">
          <span className="text-xs font-mono font-medium text-[#6b6660]">Macro Recall</span>
          <div className="font-heading text-2xl md:text-3xl font-bold text-[#0f0f0e] font-mono tabular-nums">
            {formatPct(bestModelData.recall)}
          </div>
          <p className="text-xs text-[#6b6660] font-mono">Completeness ratio</p>
        </div>
      </div>

      {/* Per-Class Accuracy Breakdown */}
      {perClassData.length > 0 && (
        <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-xs space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm md:text-base font-semibold text-[#0f0f0e] font-heading flex items-center gap-2">
              <BarChart3 className="size-4 text-indigo-600" />
              Per-Domain Accuracy Breakdown ({bestMeta.name})
            </h3>
            <span className="text-xs font-mono font-medium text-[#6b6660]">
              {bestModelData.classes?.length || perClassData.length} Classes
            </span>
          </div>

          <div className="h-64 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={perClassData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e7e3dd" />
                <XAxis dataKey="category" stroke="#6b6660" tick={{ fontSize: 11 }} />
                <YAxis domain={[0, 100]} stroke="#6b6660" tick={{ fontSize: 11 }} unit="%" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#fdfcfb",
                    borderColor: "#e7e3dd",
                    borderRadius: "0.75rem",
                    fontSize: "12px",
                    color: "#0f0f0e",
                    boxShadow: "0 4px 12px rgba(15, 15, 14, 0.06)",
                  }}
                  formatter={(val: any) => [`${val}%`, "Accuracy"]}
                />
                <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "8px" }} />
                <Bar
                  dataKey="accuracy"
                  name="Class Accuracy (%)"
                  fill="#4f46e5"
                  radius={[6, 6, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Confusion Matrix Heatmap */}
      {bestModelData.confusion_matrix && (
        <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-xs">
          <ConfusionMatrix
            categories={bestModelData.classes}
            matrix={bestModelData.confusion_matrix}
            title={`${bestMeta.name} Confusion Matrix`}
            description={`Contingency distribution across ${bestModelData.classes?.length || 5} categories on the test set.`}
          />
        </div>
      )}

      {/* Model Comparison Leaderboard */}
      <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-xs space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm md:text-base font-semibold text-[#0f0f0e] font-heading flex items-center gap-2">
            <Award className="size-5 text-[#d97706]" />
            Architecture Comparison Leaderboard
          </h3>
          <span className="text-xs font-mono font-medium text-[#6b6660]">
            {Object.keys(metrics).length} Models Evaluated
          </span>
        </div>

        <div className="overflow-x-auto rounded-xl border border-[#e7e3dd]">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#f1efeb] text-[#3f3d3a] font-mono uppercase tracking-wider font-semibold">
              <tr>
                <th className="p-3">Model Architecture</th>
                <th className="p-3">Paradigm</th>
                <th className="p-3">Accuracy</th>
                <th className="p-3">F1 Macro</th>
                <th className="p-3">Latency</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#e7e3dd] font-sans">
              {Object.entries(metrics)
                .sort((a, b) => b[1].accuracy - a[1].accuracy)
                .map(([key, model]) => {
                  const meta = MODEL_PARADIGMS[key] || {
                    name: key,
                    paradigm: model.paradigm || "Machine Learning",
                    badge: "",
                  };
                  return (
                    <tr key={key} className="hover:bg-[#f1efeb] transition-colors">
                      <td className="p-3">
                        <div className="font-semibold text-[#0f0f0e]">{meta.name}</div>
                        {meta.badge && (
                          <span className="text-[10px] text-indigo-600 font-mono font-medium">
                            {meta.badge}
                          </span>
                        )}
                      </td>
                      <td className="p-3 text-[#3f3d3a]">{meta.paradigm}</td>
                      <td className="p-3 font-mono font-bold text-[#059669] tabular-nums">
                        {formatPct(model.accuracy)}
                      </td>
                      <td className="p-3 font-mono font-semibold text-[#0f0f0e] tabular-nums">
                        {formatPct(model.f1_macro)}
                      </td>
                      <td className="p-3 font-mono text-[#0891b2] tabular-nums font-medium">
                        {model.latency_ms !== undefined ? `${model.latency_ms} ms` : "—"}
                      </td>
                    </tr>
                  );
                })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
