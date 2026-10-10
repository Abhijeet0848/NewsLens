"use client";

import * as React from "react";
import {
  HelpCircle,
  BookOpen,
  Search,
  CheckCircle,
  Copy,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { toast } from "sonner";
import { MathBlock, MathInline } from "@/components/MathBlock";

interface VivaQA {
  q: string;
  a: string;
  topic: string;
  math?: string;
}

const VIVA_QUESTIONS: VivaQA[] = [
  {
    topic: "ML Paradigms",
    q: "Which paradigm does your project use?",
    a: "Supervised learning — specifically multi-class classification. We have labeled training data (1,780 BBC articles with known categories) and learn the mapping from text → category.",
  },
  {
    topic: "ML Paradigms",
    q: "Why not unsupervised learning?",
    a: "Unsupervised learning discovers groups without labels. We already know our 5 categories — we need a classifier, not a clustering algorithm.",
  },
  {
    topic: "ML Paradigms",
    q: "Why not reinforcement learning?",
    a: "Reinforcement learning requires an environment and reward signal. Classification is a one-shot prediction — no sequential decision making, no reward to maximize.",
  },
  {
    topic: "Bayes Theorem",
    q: "How does Bayes Theorem apply to text classification?",
    a: "Multinomial Naive Bayes applies Bayes' rule: P(category | words) ∝ P(category) · Π P(word | category). We compute this for each of the 5 categories and pick the highest.",
    math: "P(c \\mid x) = \\frac{P(x \\mid c) \\cdot P(c)}{P(x)} \\propto P(c) \\prod_{i=1}^n P(w_i \\mid c)^{f_i}",
  },
  {
    topic: "Bayes Theorem",
    q: "Why Naive Bayes — what's 'naive' about it?",
    a: "It assumes every word is independent given the category. In reality words are correlated (e.g., 'New York'). This assumption is false, but the classifier still works well in practice — a well-known result in NLP.",
  },
  {
    topic: "Neural Networks",
    q: "How are neurons used in the project?",
    a: "The MLP has two hidden layers of 128 and 64 neurons. Each neuron computes a weighted sum of inputs plus bias, then applies ReLU activation.",
    math: "h_1 = \\text{ReLU}(W_1 x + b_1), \\quad h_2 = \\text{ReLU}(W_2 h_1 + b_2)",
  },
  {
    topic: "Support Vector Machines",
    q: "What is linear separability?",
    a: "A dataset is linearly separable if a hyperplane can separate classes. TF-IDF vectors are high-dimensional and sparse, so text classes often ARE linearly separable. That's why Linear SVM achieves 96.4% on this data.",
  },
  {
    topic: "Support Vector Machines",
    q: "Why soft-margin SVM, not hard-margin?",
    a: "Real data has noise. Hard-margin SVM fails when classes overlap. Soft-margin allows some misclassifications via slack variables ξᵢ, trading margin violations for better generalization.",
    math: "\\min_{w, b, \\xi} \\frac{1}{2}\\|w\\|^2 + C \\sum_{i=1}^N \\xi_i",
  },
  {
    topic: "Loss Functions",
    q: "What loss function does SVM use?",
    a: "Hinge loss: L = max(0, 1 − y·f(x)). It penalizes predictions inside the margin and zero-penalizes correct predictions outside it.",
    math: "L(y, f(x)) = \\max(0, 1 - y \\cdot f(x))",
  },
  {
    topic: "Loss Functions",
    q: "What loss function does MLP use and how does it compare?",
    a: "Cross-entropy loss: L = -Σ yₖ ln(ŷₖ). Hinge loss maximizes margin boundary distance, while cross-entropy maximizes probabilistic likelihood.",
    math: "\\mathcal{L}_{\\text{CE}} = -\\sum_{k=1}^5 y_k \\ln(\\hat{y}_k)",
  },
  {
    topic: "Kernels & Non-Linearity",
    q: "Why not use RBF kernel for SVM?",
    a: "We tested it. RBF gave marginal improvement (~0.3%) but at 5–10× the training cost. Since the data is already linearly separable, the linear kernel is the right choice — Occam's razor.",
  },
  {
    topic: "Activation Functions",
    q: "What activation functions do you use?",
    a: "ReLU in hidden layers — it prevents vanishing gradients and is fast to compute. Softmax in the output layer — it converts raw scores into a probability distribution summing to 1.",
    math: "\\text{ReLU}(z) = \\max(0, z), \\quad \\text{softmax}(z)_k = \\frac{\\exp(z_k)}{\\sum_{j=1}^5 \\exp(z_j)}",
  },
  {
    topic: "Decision Trees",
    q: "Why not a Decision Tree?",
    a: "Decision trees overfit on high-dimensional TF-IDF features (10,000 features) and don't naturally output probabilities. They're interpretable but underperform linear models on sparse text.",
  },
];

export default function VivaPreparationPage() {
  const [search, setSearch] = React.useState("");
  const [selectedTopic, setSelectedTopic] = React.useState<string>("All");

  const topics = ["All", ...Array.from(new Set(VIVA_QUESTIONS.map((q) => q.topic)))];

  const filtered = VIVA_QUESTIONS.filter((item) => {
    const matchesTopic = selectedTopic === "All" || item.topic === selectedTopic;
    const matchesSearch =
      item.q.toLowerCase().includes(search.toLowerCase()) ||
      item.a.toLowerCase().includes(search.toLowerCase());
    return matchesTopic && matchesSearch;
  });

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success("Answer copied to clipboard");
  };

  return (
    <div className="relative min-h-screen py-10 md:py-16 px-5 md:px-8 max-w-5xl mx-auto space-y-8">
      {/* Header */}
      <div className="space-y-3">
        <div className="inline-flex items-center gap-2 rounded-full border border-[#e7e3dd] bg-[#fdfcfb] px-3.5 py-1 text-xs font-mono font-medium text-[#3f3d3a]">
          <BookOpen className="size-3.5 text-[#4f46e5]" /> Academic Oral Defense
        </div>
        <h1 className="font-heading text-3xl sm:text-4xl font-bold text-[#0f0f0e] tracking-tight">
          NewsScope Viva Voce Defense Guide
        </h1>
        <p className="text-[14px] text-[#57534e] max-w-2xl leading-relaxed">
          Curated questions and defensible model answers covering every ML syllabus topic for the project examination.
        </p>
      </div>

      {/* Filter Bar */}
      <div className="flex flex-col sm:flex-row gap-3 items-stretch sm:items-center justify-between">
        <div className="relative flex-1">
          <Search aria-hidden="true" className="absolute left-3.5 top-1/2 -translate-y-1/2 size-4 text-[#57534e]" />
          <input
            type="text"
            placeholder="Search questions or keywords..."
            aria-label="Search questions or keywords"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full h-10 pl-10 pr-4 rounded-xl border border-[#e7e3dd] bg-[#faf9f6] text-[13.5px] text-[#0f0f0e] placeholder:text-[#8a847d] focus:bg-[#fdfcfb] focus:border-[#4f46e5]/40 focus:outline-none focus-visible:ring-2 focus-visible:ring-[#4f46e5]/40 transition-all"
          />
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
          {topics.map((t) => (
            <button
              key={t}
              onClick={() => setSelectedTopic(t)}
              className={`h-8 px-3 rounded-lg text-xs font-medium whitespace-nowrap transition-colors focus-visible:ring-2 focus-visible:ring-[#4f46e5]/40 focus:outline-none ${
                selectedTopic === t
                  ? "bg-[#0f0f0e] text-white"
                  : "bg-[#faf9f6] border border-[#e7e3dd] text-[#57534e] hover:bg-[#f1efeb] hover:text-[#0f0f0e]"
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* QA List */}
      <div className="space-y-4">
        {filtered.map((item, idx) => (
          <div
            key={idx}
            className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-6 shadow-sm hover:border-[#c7d2fe] transition-all space-y-3"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-2">
                <span className="text-[11px] font-mono font-bold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded">
                  {item.topic}
                </span>
              </div>
              <button
                type="button"
                onClick={() => handleCopy(`Q: ${item.q}\nA: ${item.a}`)}
                aria-label={`Copy question ${idx + 1} and answer`}
                className="text-[#57534e] hover:text-[#0f0f0e] transition-colors p-1 rounded-md hover:bg-[#f1efeb] focus-visible:ring-2 focus-visible:ring-[#4f46e5]/40 focus:outline-none"
              >
                <Copy aria-hidden="true" className="size-3.5" />
              </button>
            </div>

            <h2 className="text-[15px] font-semibold text-[#0f0f0e] flex items-start gap-2">
              <span className="text-[#4f46e5] font-mono font-bold text-xs mt-0.5">Q.</span>
              <span>{item.q}</span>
            </h2>

            {item.math && (
              <div className="my-2">
                <MathBlock math={item.math} />
              </div>
            )}

            <div className="p-4 rounded-xl bg-[#faf9f6] border border-[#e7e3dd] text-[13.5px] text-[#3f3d3a] leading-relaxed">
              <span className="font-semibold text-[#0f0f0e] mr-1.5">Answer:</span>
              &ldquo;{item.a}&rdquo;
            </div>
          </div>
        ))}

        {filtered.length === 0 && (
          <div className="text-center py-12 text-[#57534e] text-sm">
            No questions found matching your search.
          </div>
        )}
      </div>
    </div>
  );
}
