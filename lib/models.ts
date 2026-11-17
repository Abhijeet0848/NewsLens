import rawMetrics from "@/data/metrics.json";

export type ModelId =
  | "linear-svm"
  | "naive-bayes"
  | "decision-tree";

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
const nbAcc = m.naive_bayes?.accuracy ?? 0.921;
const dtAcc = m.decision_tree?.accuracy ?? 0.838;

export const MODELS: Record<ModelId, ModelInfo> = {
  "linear-svm": {
    id: "linear-svm",
    name: "Linear SVM",
    subtitle: "Maximum-Margin Boundary",
    metric: `${(svmAcc * 100).toFixed(1)}%`,
    accuracy: Number((svmAcc * 100).toFixed(1)),
    latency: m.svm?.latency_ms ?? 1.2,
    role: "champion",
    description: "Best balance of speed and accuracy (Our Winner ⭐)",
  },
  "naive-bayes": {
    id: "naive-bayes",
    name: "Naive Bayes",
    subtitle: "Probabilistic Generative",
    metric: `${(nbAcc * 100).toFixed(1)}%`,
    accuracy: Number((nbAcc * 100).toFixed(1)),
    latency: m.naive_bayes?.latency_ms ?? 0.5,
    role: "baseline",
    description: "Fast probabilistic word-frequency baseline",
  },
  "decision-tree": {
    id: "decision-tree",
    name: "Decision Tree",
    subtitle: "Rule-Based Flowchart",
    metric: `${(dtAcc * 100).toFixed(1)}%`,
    accuracy: Number((dtAcc * 100).toFixed(1)),
    latency: m.decision_tree?.latency_ms ?? 0.8,
    role: "baseline",
    description: "Hierarchical Yes/No decision split baseline",
  },
};

export const DEFAULT_MODEL: ModelId = "linear-svm";
