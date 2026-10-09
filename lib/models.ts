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

export const MODELS: Record<ModelId, ModelInfo> = {
  "linear-svm": {
    id: "linear-svm",
    name: "Linear SVM",
    subtitle: "Maximum-Margin Boundary",
    metric: "96.4%",
    accuracy: 96.4,
    latency: 1.2,
    role: "default",
    description: "Best balance of speed and accuracy",
  },
  distilbert: {
    id: "distilbert",
    name: "DistilBERT",
    subtitle: "Transformer Attention",
    metric: "97.8%",
    accuracy: 97.8,
    latency: 12.4,
    role: "champion",
    description: "Highest accuracy, slower inference",
  },
  "neural-mlp": {
    id: "neural-mlp",
    name: "Neural MLP",
    subtitle: "Multi-Layer Perceptron",
    metric: "95.1%",
    accuracy: 95.1,
    latency: 3.2,
    role: "baseline",
    description: "Non-linear neural baseline",
  },
  "naive-bayes": {
    id: "naive-bayes",
    name: "Naive Bayes",
    subtitle: "Probabilistic Generative",
    metric: "92.1%",
    accuracy: 92.1,
    latency: 0.5,
    role: "baseline",
    description: "Fast probabilistic baseline",
  },
};

export const DEFAULT_MODEL: ModelId = "linear-svm";
