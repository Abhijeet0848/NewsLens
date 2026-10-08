"use client";

import * as React from "react";
import {
  TrendingUp,
  Award,
  Target,
  ArrowUpRight,
} from "lucide-react";
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { ConfusionMatrix } from "@/components/confusion-matrix";

const BBC_PERFORMANCE_METRICS = {
  overall: {
    accuracy: 0.978,
    accuracy_delta: "+2.1%",
    f1_macro: 0.976,
    f1_delta: "+1.9%",
    precision: 0.979,
    precision_delta: "+1.8%",
    recall: 0.975,
    recall_delta: "+2.0%",
    total_samples: 2225,
    test_samples: 445,
  },
  radarData: [
    { subject: "Accuracy", DistilBERT: 97.8, SVM: 96.4, NaiveBayes: 92.1, fullMark: 100 },
    { subject: "Precision", DistilBERT: 97.9, SVM: 96.2, NaiveBayes: 91.8, fullMark: 100 },
    { subject: "Recall", DistilBERT: 97.5, SVM: 96.5, NaiveBayes: 92.3, fullMark: 100 },
    { subject: "F1 Score", DistilBERT: 97.6, SVM: 96.3, NaiveBayes: 92.0, fullMark: 100 },
    { subject: "Robustness", DistilBERT: 98.2, SVM: 94.1, NaiveBayes: 86.4, fullMark: 100 },
  ],
  trainingHistory: [
    { epoch: 1, trainLoss: 0.72, valLoss: 0.54, trainAcc: 78.4, valAcc: 82.1 },
    { epoch: 2, trainLoss: 0.38, valLoss: 0.31, trainAcc: 89.2, valAcc: 90.5 },
    { epoch: 3, trainLoss: 0.21, valLoss: 0.18, trainAcc: 94.6, valAcc: 94.2 },
    { epoch: 4, trainLoss: 0.11, valLoss: 0.12, trainAcc: 97.5, valAcc: 96.8 },
    { epoch: 5, trainLoss: 0.06, valLoss: 0.09, trainAcc: 98.8, valAcc: 97.8 },
  ],
  modelComparison: [
    {
      name: "DistilBERT (Fine-Tuned)",
      type: "Transformer / Deep Learning",
      accuracy: 97.8,
      f1: 97.6,
      latency: "12.4 ms",
      modelSize: "268 MB",
      badge: "⭐ Champion",
      pros: "Deep semantic context, handles negation and idioms across BBC domains",
    },
    {
      name: "Support Vector Machine (Linear SVM)",
      type: "Maximum-Margin Hyperplane",
      accuracy: 96.4,
      f1: 96.3,
      latency: "1.2 ms",
      modelSize: "3.8 MB",
      badge: "Fast & Accurate",
      pros: "Extremely fast inference, optimal on sparse TF-IDF vocabulary",
    },
    {
      name: "Multi-Layer Perceptron (MLP)",
      type: "Feedforward Neural Network",
      accuracy: 95.1,
      f1: 94.8,
      latency: "3.2 ms",
      modelSize: "16.4 MB",
      badge: "Neural Baseline",
      pros: "Learns non-linear feature combinations",
    },
    {
      name: "Multinomial Naive Bayes",
      type: "Generative Probabilistic",
      accuracy: 92.1,
      f1: 92.0,
      latency: "0.5 ms",
      modelSize: "1.6 MB",
      badge: "Lightweight",
      pros: "Fast baseline with probabilistic class priors",
    },
  ],
};

export default function AnalyticsDashboardPage() {
  const { overall, radarData, trainingHistory, modelComparison } =
    BBC_PERFORMANCE_METRICS;

  return (
    <div className="relative mx-auto max-w-7xl px-5 md:px-8 pt-8 md:pt-12 pb-16 md:pb-20 space-y-6 md:space-y-10">
      {/* Faint Dot Grid Pattern */}
      <div className="absolute inset-x-0 top-0 h-52 -z-10 pointer-events-none opacity-25 [background-image:radial-gradient(#d6d1c9_1px,transparent_1px)] [background-size:24px_24px] [mask-image:linear-gradient(to_bottom,black_20%,transparent_100%)]" />

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div className="space-y-1">
          <span className="text-[10px] md:text-[11px] uppercase tracking-[0.14em] text-[#0891b2] font-mono font-semibold block">
            BBC NEWS DATASET EVALUATION
          </span>
          <h1 className="font-heading text-2xl sm:text-3xl font-semibold tracking-[-0.02em] text-[#0f0f0e]">
            Performance & Saliency Analytics
          </h1>
          <p className="text-[13px] md:text-sm text-[#3f3d3a] max-w-2xl leading-relaxed">
            Evaluated on held-out 20% test split (445 verified BBC articles from 2,225 corpus).
          </p>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs text-[#3f3d3a]">
          <span className="size-2 rounded-full bg-[#059669]" />
          <span>BBC Split: 80 / 20 (445 test)</span>
        </div>
      </div>

      <div className="border-t border-[#e7e3dd]" />

      {/* 4 Metric Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-md space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono font-medium text-[#6b6660]">Test Accuracy</span>
            <span className="flex items-center text-[11px] font-mono font-semibold text-[#059669] tabular-nums">
              <ArrowUpRight className="size-3" />
              {overall.accuracy_delta}
            </span>
          </div>
          <div className="font-heading text-2xl md:text-3xl font-bold text-[#0f0f0e] font-mono tabular-nums">
            {(overall.accuracy * 100).toFixed(1)}%
          </div>
          <p className="text-xs text-[#6b6660] font-mono tabular-nums">435 / 445 correct</p>
        </div>

        <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-md space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono font-medium text-[#6b6660]">Macro F1 Score</span>
            <span className="flex items-center text-[11px] font-mono font-semibold text-[#059669] tabular-nums">
              <ArrowUpRight className="size-3" />
              {overall.f1_delta}
            </span>
          </div>
          <div className="font-heading text-2xl md:text-3xl font-bold text-[#0f0f0e] font-mono tabular-nums">
            {(overall.f1_macro * 100).toFixed(1)}%
          </div>
          <p className="text-xs text-[#6b6660] font-mono">Harmonic precision-recall</p>
        </div>

        <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-md space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono font-medium text-[#6b6660]">Macro Precision</span>
            <span className="flex items-center text-[11px] font-mono font-semibold text-[#059669] tabular-nums">
              <ArrowUpRight className="size-3" />
              {overall.precision_delta}
            </span>
          </div>
          <div className="font-heading text-2xl md:text-3xl font-bold text-[#0f0f0e] font-mono tabular-nums">
            {(overall.precision * 100).toFixed(1)}%
          </div>
          <p className="text-xs text-[#6b6660] font-mono">Minimal false positives</p>
        </div>

        <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-md space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono font-medium text-[#6b6660]">Macro Recall</span>
            <span className="flex items-center text-[11px] font-mono font-semibold text-[#059669] tabular-nums">
              <ArrowUpRight className="size-3" />
              {overall.recall_delta}
            </span>
          </div>
          <div className="font-heading text-2xl md:text-3xl font-bold text-[#0f0f0e] font-mono tabular-nums">
            {(overall.recall * 100).toFixed(1)}%
          </div>
          <p className="text-xs text-[#6b6660] font-mono">Minimal false negatives</p>
        </div>
      </div>

      {/* 2 Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-8">
        {/* Convergence Chart */}
        <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-md space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm md:text-base font-semibold text-[#0f0f0e] font-heading flex items-center gap-2">
              <TrendingUp className="size-4 text-[#0891b2]" />
              Loss & Accuracy Convergence (BBC Corpus)
            </h3>
            <span className="text-xs font-mono font-medium text-[#6b6660]">AdamW</span>
          </div>

          <div className="h-64 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trainingHistory}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e7e3dd" />
                <XAxis dataKey="epoch" stroke="#6b6660" tick={{ fontSize: 11 }} />
                <YAxis stroke="#6b6660" tick={{ fontSize: 11 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#fdfcfb",
                    borderColor: "#e7e3dd",
                    borderRadius: "0.75rem",
                    fontSize: "12px",
                    color: "#0f0f0e",
                    boxShadow: "0 4px 12px rgba(15, 15, 14, 0.06)",
                  }}
                />
                <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "8px" }} />
                <Line
                  type="monotone"
                  dataKey="trainAcc"
                  name="Train Acc (%)"
                  stroke="#6366f1"
                  strokeWidth={2}
                  dot={{ r: 3 }}
                />
                <Line
                  type="monotone"
                  dataKey="valAcc"
                  name="Val Acc (%)"
                  stroke="#059669"
                  strokeWidth={2}
                  dot={{ r: 3 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Radar Chart */}
        <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-md space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm md:text-base font-semibold text-[#0f0f0e] font-heading flex items-center gap-2">
              <Target className="size-4 text-indigo-600" />
              Architectural Profile on BBC Domains
            </h3>
            <span className="text-xs font-mono font-medium text-[#6b6660]">5 Classes</span>
          </div>

          <div className="h-64 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#e7e3dd" />
                <PolarAngleAxis dataKey="subject" stroke="#3f3d3a" tick={{ fontSize: 11, fontWeight: 500 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#8a847d" />
                <Radar
                  name="DistilBERT"
                  dataKey="DistilBERT"
                  stroke="#0891b2"
                  fill="#0891b2"
                  fillOpacity={0.2}
                />
                <Radar
                  name="Linear SVM"
                  dataKey="SVM"
                  stroke="#059669"
                  fill="#059669"
                  fillOpacity={0.15}
                />
                <Radar
                  name="Naive Bayes"
                  dataKey="NaiveBayes"
                  stroke="#8b5cf6"
                  fill="#8b5cf6"
                  fillOpacity={0.15}
                />
                <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "8px" }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Confusion Matrix Section */}
      <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-lg">
        <ConfusionMatrix />
      </div>

      {/* Comparison Leaderboard */}
      <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-6 shadow-lg space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm md:text-base font-semibold text-[#0f0f0e] font-heading flex items-center gap-2">
            <Award className="size-5 text-[#d97706]" />
            Architecture Comparison Leaderboard
          </h3>
          <span className="text-xs font-mono font-medium text-[#6b6660]">2,225 BBC Articles Benchmark</span>
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
                <th className="p-3">Key Strengths</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#e7e3dd] font-sans">
              {modelComparison.map((m) => (
                <tr key={m.name} className="hover:bg-[#f1efeb] transition-colors">
                  <td className="p-3">
                    <div className="font-semibold text-[#0f0f0e]">{m.name}</div>
                    <span className="text-[10px] text-[#0891b2] font-mono font-medium">{m.badge}</span>
                  </td>
                  <td className="p-3 text-[#3f3d3a]">{m.type}</td>
                  <td className="p-3 font-mono font-bold text-[#059669] tabular-nums">{m.accuracy}%</td>
                  <td className="p-3 font-mono font-semibold text-[#0f0f0e] tabular-nums">{m.f1}%</td>
                  <td className="p-3 font-mono text-[#0891b2] tabular-nums font-medium">{m.latency}</td>
                  <td className="p-3 text-[#3f3d3a] max-w-xs">{m.pros}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
