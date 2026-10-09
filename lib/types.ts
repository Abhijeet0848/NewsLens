export interface ClassificationResponse {
  category: string;
  confidence: number;
  confidence_percentage: number;
  all_scores: Record<string, number>;
  keywords: Array<{ word: string; weight: number }>;
  explanation: {
    top_factors: string[];
    summary: string;
    model_version: string;
    linguistic_cues: string[];
  };
  attention_tokens: Array<{ token: string; weight: number; isKeyword: boolean }>;
  latency_ms: number;
  tokens_count: number;
  timestamp: string;
  model_id?: string;
}

export interface BBCArticle {
  id: number;
  category: "business" | "entertainment" | "politics" | "sport" | "tech";
  title: string;
  content: string;
}
