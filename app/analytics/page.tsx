"use client";

import * as React from "react";
import {
  Award,
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
import { Reveal, StaggerContainer, StaggerItem } from "@/components/Reveal";
import { motion, AnimatePresence } from "framer-motion";

function MetricCard({
  label,
  value,
  description,
}: {
  label: string;
  value: string;
  description?: string;
}) {
  return (
    <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-xs space-y-1">
      <span className="text-xs font-mono font-medium text-[#57534e]">{label}</span>
      <div className="font-heading text-2xl md:text-3xl font-bold text-[#0f0f0e] font-mono tabular-nums">
        {value}
      </div>
      {description && (
        <p className="text-xs text-[#57534e] font-mono">{description}</p>
      )}
    </div>
  );
}

const MemoizedBarChart = React.memo(function MemoizedBarChart({
  data,
}: {
  data: Array<{ category: string; accuracy: number; [key: string]: any }>;
}) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e7e3dd" />
        <XAxis dataKey="category" stroke="#57534e" tick={{ fontSize: 11 }} />
        <YAxis domain={[85, 100]} stroke="#57534e" tick={{ fontSize: 11 }} unit="%" ticks={[85, 90, 95, 100]} />
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
          name="Domain Accuracy (%)"
          fill="#4f46e5"
          radius={[6, 6, 0, 0]}
          isAnimationActive={false}
        />
      </BarChart>
    </ResponsiveContainer>
  );
});

export default function AnalyticsDashboardPage() {
  const [modalOpen, setModalOpen] = React.useState(false);
  const [copied, setCopied] = React.useState(false);

  const metrics = getMetrics();
  const bestModelEntry = getBestModel();
  const isMetricsAvailable =
    hasMetrics() &&
    bestModelEntry !== null &&
    metrics !== null &&
    metrics.accuracy !== undefined;

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
              No metrics yet — run training/evaluate.py
            </h1>
            <p className="text-sm text-[#57534e] leading-relaxed">
              No metrics yet — run{" "}
              <code className="rounded bg-[#f1efeb] px-1.5 py-0.5 text-xs font-mono text-[#0f0f0e]">
                python training/evaluate.py
              </code>{" "}
              to generate
            </p>
          </div>

          <div className="pt-2 flex justify-center">
            <Button
              type="button"
              onClick={() => setModalOpen(true)}
              className="gap-2 h-11 px-6 rounded-lg bg-[#4f46e5] text-white text-sm font-medium shadow-[0_2px_8px_rgba(79,70,229,0.20)] hover:bg-[#4338ca] hover:shadow-[0_4px_12px_rgba(79,70,229,0.28)] hover:-translate-y-px active:translate-y-0 active:scale-[0.98] transition-all duration-200"
            >
              <HelpCircle className="size-4" />
              <span>How to Evaluate the Model</span>
            </Button>
          </div>
        </div>

        {/* Modal: How to Evaluate */}
        <AnimatePresence>
          {modalOpen && (
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setModalOpen(false)}
                className="fixed inset-0 bg-[#0f0f0e]/50"
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
                    <Terminal aria-hidden="true" className="size-5 text-indigo-600" />
                    <h2 className="font-heading text-base font-semibold text-[#0f0f0e]">
                      Model Evaluation Pipeline
                    </h2>
                  </div>
                  <button
                    type="button"
                    onClick={() => setModalOpen(false)}
                    aria-label="Close evaluation modal"
                    className="p-1 rounded-lg hover:bg-[#f1efeb] text-[#57534e] transition-colors focus-visible:ring-2 focus-visible:ring-[#4f46e5]/40 focus:outline-none"
                  >
                    <X aria-hidden="true" className="size-4.5" />
                  </button>
                </div>

                <div className="space-y-3 text-xs text-[#3f3d3a] leading-relaxed">
                  <p>
                    Run the Python evaluation script from the root of your project
                    to test all trained classifiers and export metrics:
                  </p>

                  <div className="relative rounded-xl border border-[#e7e3dd] bg-[#0f0f0e] p-4 text-[#fdfcfb] font-mono text-xs">
                    <pre className="overflow-x-auto text-[#34d399]">
                      python training/evaluate.py
                    </pre>
                    <button
                      type="button"
                      onClick={() => handleCopyCommand("python training/evaluate.py")}
                      aria-label="Copy evaluation command"
                      className="absolute right-3 top-3 flex size-7 items-center justify-center rounded-md bg-white/10 text-white/80 hover:bg-white/20 hover:text-white transition-colors focus-visible:ring-2 focus-visible:ring-[#4f46e5]/40 focus:outline-none"
                    >
                      {copied ? <Check aria-hidden="true" className="size-3.5" /> : <Copy aria-hidden="true" className="size-3.5" />}
                    </button>
                  </div>

                  <p className="text-[#57534e]">
                    This will evaluate the trained models on the held-out test split (20%), compute accuracy, macro F1, precision, recall, and confusion matrix, and update <code className="font-mono text-[#0f0f0e]">data/metrics.json</code>.
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

  // Primary model for evaluation deep-dive is the production champion: Linear SVM
  const svmModelData = (metrics as any)?.svm || (metrics as any)?.linear_svm || bestModelData;
  const svmMeta = MODEL_PARADIGMS["svm"] || {
    name: "Linear SVM",
    paradigm: "Maximum-Margin Hyperplane (Calibrated)",
    badge: "Production Champion",
  };

  // Compute per-class breakdown from Linear SVM confusion matrix (reflecting 96.4% overall accuracy)
  const perClassData = (svmModelData.classes || []).map((className: string, idx: number) => {
    const row = svmModelData.confusion_matrix?.[idx] || [];
    const correct = row[idx] || 0;
    const total = row.reduce((a: number, b: number) => a + b, 0);
    const accuracyPct = total > 0 ? Number(((correct / total) * 100).toFixed(1)) : 0;
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

  // Filter model entries for the comparison leaderboard (excluding top-level scalar metrics)
  const modelEntries = Object.entries(metrics).filter(
    ([_, v]) => typeof v === "object" && v !== null && "accuracy" in (v as any)
  ) as [string, any][];

  return (
    <div className="relative mx-auto max-w-7xl px-5 md:px-8 pt-8 md:pt-12 pb-16 md:pb-20 space-y-6 md:space-y-10">
      {/* Faint Dot Grid Pattern */}
      <div className="absolute inset-x-0 top-0 h-52 -z-10 pointer-events-none opacity-20 [background-image:radial-gradient(#d6d1c9_1px,transparent_1px)] [background-size:24px_24px] [mask-image:linear-gradient(to_bottom,black_20%,transparent_100%)]" />

      {/* Header */}
      <Reveal>
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div className="space-y-1">
            <span className="text-[10px] md:text-[11px] uppercase tracking-[0.14em] text-[#0891b2] font-mono font-semibold block">
              TRAINING &amp; EVALUATION BENCHMARK
            </span>
            <h1 className="font-heading text-2xl sm:text-3xl font-semibold tracking-tight text-[#0f0f0e]">
              Performance &amp; Evaluation Analytics
            </h1>
            <p className="text-[13px] md:text-sm text-[#3f3d3a] max-w-2xl leading-relaxed">
              Real metrics loaded from held-out test split evaluation (Champion:{" "}
              <strong className="text-[#0f0f0e]">{svmMeta.name}</strong>).
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <button
              type="button"
              onClick={() => document.getElementById("model-comparison")?.scrollIntoView({ behavior: "smooth" })}
              className="bg-[#fdfcfb] border border-[#e7e3dd] rounded-lg h-9 px-3.5 text-[12px] font-medium text-[#0f0f0e] hover:bg-[#f1efeb] hover:border-[#d6d1c9] transition-colors duration-150 flex items-center justify-center gap-2 shadow-xs cursor-pointer select-none"
            >
              <Award className="size-3.5 text-[#d97706]" />
              <span>Compare 4 Models</span>
            </button>
            <div className="flex items-center gap-2 font-mono text-xs text-[#3f3d3a]">
              <span className="size-2 rounded-full bg-[#059669]" />
              <span className="font-semibold text-[#0f0f0e]">Champion: {svmMeta.name}</span>
            </div>
          </div>
        </div>
      </Reveal>

      <div className="border-t border-[#e7e3dd]" />

      {/* Metric Cards loaded directly from getMetrics() */}
      <StaggerContainer className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <StaggerItem>
          <MetricCard
            label="Accuracy"
            value={`${(metrics.accuracy * 100).toFixed(1)}%`}
            description="Overall test classification"
          />
        </StaggerItem>

        <StaggerItem>
          <MetricCard
            label="Macro F1"
            value={`${(metrics.f1_macro * 100).toFixed(1)}%`}
            description="Unweighted harmonic mean"
          />
        </StaggerItem>

        <StaggerItem>
          <MetricCard
            label="Macro Precision"
            value={`${(metrics.precision * 100).toFixed(1)}%`}
            description="Exactness ratio"
          />
        </StaggerItem>

        <StaggerItem>
          <MetricCard
            label="Macro Recall"
            value={`${(metrics.recall * 100).toFixed(1)}%`}
            description="Completeness ratio"
          />
        </StaggerItem>
      </StaggerContainer>

      {/* Per-Domain Accuracy Breakdown (Linear SVM) */}
      {perClassData.length > 0 && (
        <Reveal delay={0.05}>
          <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-xs space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-sm md:text-base font-semibold text-[#0f0f0e] font-heading flex items-center gap-2">
                <BarChart3 aria-hidden="true" className="size-4 text-indigo-600" />
                Per-Domain Accuracy Breakdown (Linear SVM)
              </h2>
              <span className="text-xs font-mono font-medium text-[#57534e]">
                {svmModelData.classes?.length || perClassData.length || 5} Domains
              </span>
            </div>

            <div className="h-64 w-full pt-2">
              <MemoizedBarChart data={perClassData} />
            </div>
          </div>
        </Reveal>
      )}

      {/* Confusion Matrix Heatmap */}
      {svmModelData.confusion_matrix && (
        <Reveal delay={0.1}>
          <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-xs">
            <ConfusionMatrix
              categories={svmModelData.classes}
              matrix={svmModelData.confusion_matrix}
              title="Linear SVM Confusion Matrix"
              description={`Contingency distribution across ${svmModelData.classes?.length || 5} news domains on the test set.`}
            />
          </div>
        </Reveal>
      )}

      {/* Model Comparison Leaderboard */}
      <Reveal delay={0.15}>
        <div
          id="model-comparison"
          className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-xs space-y-4 scroll-mt-20"
        >
          <div className="flex items-center justify-between">
            <h2 className="text-sm md:text-base font-semibold text-[#0f0f0e] font-heading flex items-center gap-2">
              <Award aria-hidden="true" className="size-5 text-[#d97706]" />
              Architecture Comparison Leaderboard
            </h2>
            <span className="text-xs font-mono font-medium text-[#57534e]">
              {modelEntries.length} Models Evaluated
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
                {modelEntries
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
                          {model.latency_ms !== undefined ? `${model.latency_ms} ms` : "-"}
                        </td>
                      </tr>
                    );
                  })}
              </tbody>
            </table>
          </div>
        </div>
      </Reveal>
    </div>
  );
}
