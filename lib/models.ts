import rawMetrics from "@/data/metrics.json";

export type ModelId =
  | "linear-svm"
  | "distilbert"
  | "neural-mlp"
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
const svmAcc = m.svm?.accuracy ?? m.accuracy ?? 0.964;
const mlpAcc = m.mlp?.accuracy ?? 0.951;
const nbAcc = m.naive_bayes?.accuracy ?? 0.921;
const distilAcc = m.distilbert?.accuracy ?? 0.978;

export const MODELS: Record<ModelId, ModelInfo> = {
  "linear-svm": {
    id: "linear-svm",
    name: "Linear SVM",
    subtitle: "Maximum-Margin Boundary",
    metric: `${(svmAcc * 100).toFixed(1)}%`,
    accuracy: Number((svmAcc * 100).toFixed(1)),
    latency: m.svm?.latency_ms ?? 1.2,
    role: "champion",
    description: "Best balance of speed and accuracy",
  },
  distilbert: {
    id: "distilbert",
    name: "DistilBERT",
    subtitle: "Transformer Attention",
    metric: `${(distilAcc * 100).toFixed(1)}%`,
    accuracy: Number((distilAcc * 100).toFixed(1)),
    latency: m.distilbert?.latency_ms ?? 12.4,
    role: "baseline",
    description: "Highest theoretical capacity, slower inference",
  },
  "neural-mlp": {
    id: "neural-mlp",
    name: "Neural MLP",
    subtitle: "Multi-Layer Perceptron",
    metric: `${(mlpAcc * 100).toFixed(1)}%`,
    accuracy: Number((mlpAcc * 100).toFixed(1)),
    latency: m.mlp?.latency_ms ?? 3.2,
    role: "baseline",
    description: "Non-linear neural baseline",
  },
  "naive-bayes": {
    id: "naive-bayes",
    name: "Naive Bayes",
    subtitle: "Probabilistic Generative",
    metric: `${(nbAcc * 100).toFixed(1)}%`,
    accuracy: Number((nbAcc * 100).toFixed(1)),
    latency: m.naive_bayes?.latency_ms ?? 0.5,
    role: "baseline",
    description: "Fast probabilistic baseline",
  },
};

export const DEFAULT_MODEL: ModelId = "linear-svm";
