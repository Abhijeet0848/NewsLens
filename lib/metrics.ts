import metricsData from "@/data/metrics.json";

export type ModelMetrics = {
  accuracy: number;
  f1_macro: number;
  precision: number;
  recall: number;
  latency_ms: number;
  confusion_matrix: number[][];
  classes: string[];
  paradigm?: string;
  per_class?: Array<{
    category: string;
    precision: number;
    recall: number;
    f1_score: number;
    support?: number;
  }>;
};

export const MODEL_PARADIGMS: Record<
  string,
  { name: string; paradigm: string; badge?: string; desc?: string }
> = {
  distilbert: {
    name: "DistilBERT (Fine-Tuned)",
    paradigm: "Transformer Attention / Deep Learning",
    badge: "⭐ Champion",
  },
  linear_svm: {
    name: "Linear Support Vector Machine (SVM)",
    paradigm: "Maximum-Margin Hyperplane",
    badge: "Fast & Optimal",
  },
  naive_bayes: {
    name: "Multinomial Naive Bayes",
    paradigm: "Generative Probabilistic",
    badge: "Lightweight Baseline",
  },
  mlp: {
    name: "Multi-Layer Perceptron (MLP)",
    paradigm: "Feedforward Neural Network",
    badge: "Nonlinear Neural",
  },
  decision_tree: {
    name: "Decision Tree",
    paradigm: "Recursive Feature Splitting",
    badge: "Interpretable Tree",
  },
};

export const getMetrics = (): Record<string, ModelMetrics> => {
  return (metricsData || {}) as Record<string, ModelMetrics>;
};

export const hasMetrics = (): boolean => {
  const m = getMetrics();
  return Object.keys(m).length > 0;
};

export const getBestModel = (): [string, ModelMetrics] | null => {
  const m = getMetrics();
  const entries = Object.entries(m);
  if (entries.length === 0) return null;
  return entries.reduce(
    (best, [name, data]) =>
      data.accuracy > best[1].accuracy ? [name, data] : best,
    entries[0]
  );
};
