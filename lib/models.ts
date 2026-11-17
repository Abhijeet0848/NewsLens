import rawMetrics from "@/data/metrics.json";

export type ModelId =
  | "linear-svm"
  | "naive-bayes";

export type ModelInfo = {
  id: ModelId;
  name: string;
  subtitle: string;
  metric: string;
  accuracy: number;
  latency: number;
  role: "champion" | "default" | "baseline";
  description: string;
};

const m: any = rawMetrics || {};
const svmAcc = m.svm?.accuracy ?? m.accuracy ?? 0.986;
const nbAcc = m.naive_bayes?.accuracy ?? 0.976;

export const MODELS: Record<ModelId, ModelInfo> = {
  "linear-svm": {
    id: "linear-svm",
    name: "Linear SVM",
    subtitle: "Maximum-Margin Boundary",
    metric: `${(svmAcc * 100).toFixed(1)}%`,
    accuracy: Number((svmAcc * 100).toFixed(1)),
    latency: m.svm?.latency_ms ?? 0.02,
    role: "champion",
    description: "Best balance of speed and accuracy (Our Winner ⭐)",
  },
  "naive-bayes": {
    id: "naive-bayes",
    name: "Naive Bayes",
    subtitle: "Probabilistic Generative",
    metric: `${(nbAcc * 100).toFixed(1)}%`,
    accuracy: Number((nbAcc * 100).toFixed(1)),
    latency: m.naive_bayes?.latency_ms ?? 0.02,
    role: "baseline",
    description: "Fast probabilistic word-frequency baseline",
  },
};

export const DEFAULT_MODEL: ModelId = "linear-svm";
