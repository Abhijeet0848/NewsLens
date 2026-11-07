import metrics from "@/data/metrics.json";

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
    badge: "Champion",
  },
  svm: {
    name: "Linear SVM",
    paradigm: "Maximum-Margin Hyperplane (Calibrated)",
    badge: "Production Default",
  },
  linear_svm: {
    name: "Linear SVM",
    paradigm: "Maximum-Margin Hyperplane",
    badge: "Production Default",
  },
  mlp: {
    name: "Neural MLP",
    paradigm: "Feedforward Neural Network",
    badge: "Neural Baseline",
  },
  naive_bayes: {
    name: "Multinomial Naive Bayes",
    paradigm: "Generative Probabilistic",
    badge: "Fast Baseline",
  },
  decision_tree: {
    name: "Decision Tree",
    paradigm: "Recursive Feature Splitting",
    badge: "Interpretable Tree",
  },
};

export const getMetrics = () => metrics;

export const hasMetrics = (): boolean => {
  const m = metrics || {};
  return Object.keys(m).length > 0;
};

export const getBestModel = (): [string, ModelMetrics] | null => {
  const m: any = metrics || {};
  const entries = Object.entries(m).filter(
    ([k, v]) => typeof v === "object" && v !== null && "accuracy" in (v as any)
  ) as [string, ModelMetrics][];
  if (entries.length === 0) return null;
  return entries.reduce(
    (best, [name, data]) =>
      data.accuracy > best[1].accuracy ? [name, data] : best,
    entries[0]
  );
};
