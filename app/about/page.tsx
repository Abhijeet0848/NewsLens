"use client";

import {
  BookOpen,
  Cpu,
  Layers,
  HelpCircle,
  Code,
} from "lucide-react";
import { Reveal, StaggerContainer, StaggerItem } from "@/components/Reveal";

export default function AboutPage() {
  return (
    <div className="relative pb-16 md:pb-24">
      {/* Decorative Hero Banner */}
      <div className="relative h-[240px] md:h-[280px] w-full overflow-hidden flex items-center justify-center text-center px-5 md:px-6">
        {/* Abstract SVG Geometry / Mesh Gradient Overlay */}
        <div className="absolute inset-0 -z-10 overflow-hidden pointer-events-none">
          <svg
            className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] md:w-[800px] h-[300px] md:h-[340px] opacity-20"
            viewBox="0 0 800 340"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle cx="280" cy="140" r="140" fill="#6366f1" filter="blur(60px)" />
            <circle cx="480" cy="120" r="130" fill="#8b5cf6" filter="blur(50px)" />
            <circle cx="390" cy="200" r="110" fill="#0891b2" filter="blur(55px)" />
          </svg>
          {/* Bottom fade to page bg #f7f6f3 */}
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-[#f7f6f3]" />
        </div>

        {/* Hero Content */}
        <div className="relative max-w-3xl mx-auto space-y-3 pt-4 md:pt-6">
          <div className="inline-flex items-center gap-2 rounded-full border border-[#e7e3dd] bg-[#fdfcfb] px-3 md:px-3.5 py-1 text-[11px] md:text-xs font-mono font-medium text-[#3f3d3a] shadow-xs">
            <BookOpen className="size-3.5 text-[#0891b2]" /> Architecture & Theory Reference
          </div>
          <h1 className="font-heading text-3xl sm:text-4xl md:text-5xl font-bold text-[#0f0f0e] tracking-tight">
            How NewsScope Works
          </h1>
          <p className="text-[13px] md:text-[15px] text-[#3f3d3a] leading-relaxed max-w-2xl mx-auto px-2">
            Industrial NLP architecture combining Transformer multi-head self-attention with
            classical maximum-margin hyperplane baselines for robust text categorization.
          </p>
        </div>
      </div>

      {/* Main Body Content */}
      <div className="mx-auto max-w-7xl px-5 md:px-8 pt-6 md:pt-8 space-y-8 md:space-y-12">
        {/* 1. 5-Stage Pipeline */}
        <Reveal>
          <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-8 shadow-lg space-y-6">
            <h2 className="font-heading text-xl font-semibold text-[#0f0f0e] flex items-center gap-2.5">
              <Layers className="size-5 text-indigo-600" />
              The 5-Stage Neural & Statistical Pipeline
            </h2>

            <StaggerContainer className="grid grid-cols-1 md:grid-cols-5 gap-4">
              <StaggerItem>
                <div className="rounded-xl border border-[#e7e3dd] bg-[#f1efeb] p-5 space-y-2 h-full">
                  <span className="text-xs font-mono text-[#0891b2] font-semibold">STAGE 01</span>
                  <h4 className="text-sm font-semibold text-[#0f0f0e]">Normalization</h4>
                  <p className="text-xs text-[#3f3d3a] leading-relaxed">
                    Strips formatting artifacts, HTML markup, casing variations, and non-alphabetic noise.
                  </p>
                </div>
              </StaggerItem>

              <StaggerItem>
                <div className="rounded-xl border border-[#e7e3dd] bg-[#f1efeb] p-5 space-y-2 h-full">
                  <span className="text-xs font-mono text-[#0891b2] font-semibold">STAGE 02</span>
                  <h4 className="text-sm font-semibold text-[#0f0f0e]">WordPiece Tokens</h4>
                  <p className="text-xs text-[#3f3d3a] leading-relaxed">
                    Splits text into sub-word tokens with position embeddings and attention masks.
                  </p>
                </div>
              </StaggerItem>

              <StaggerItem>
                <div className="rounded-xl border border-[#e7e3dd] bg-[#f1efeb] p-5 space-y-2 h-full">
                  <span className="text-xs font-mono text-[#0891b2] font-semibold">STAGE 03</span>
                  <h4 className="text-sm font-semibold text-[#0f0f0e]">TF-IDF Vectors</h4>
                  <p className="text-xs text-[#3f3d3a] leading-relaxed">
                    Calculates logarithmic Inverse Document Frequency across 2,225 BBC News corpus documents.
                  </p>
                </div>
              </StaggerItem>

              <StaggerItem>
                <div className="rounded-xl border border-[#e7e3dd] bg-[#f1efeb] p-5 space-y-2 h-full">
                  <span className="text-xs font-mono text-[#0891b2] font-semibold">STAGE 04</span>
                  <h4 className="text-sm font-semibold text-[#0f0f0e]">Self-Attention</h4>
                  <p className="text-xs text-[#3f3d3a] leading-relaxed">
                    6 Transformer layers compute contextual word embeddings using bidirectional dot-product attention.
                  </p>
                </div>
              </StaggerItem>

              <StaggerItem>
                <div className="rounded-xl border border-[#e7e3dd] bg-[#f1efeb] p-5 space-y-2 h-full">
                  <span className="text-xs font-mono text-[#0891b2] font-semibold">STAGE 05</span>
                  <h4 className="text-sm font-semibold text-[#0f0f0e]">Classification</h4>
                  <p className="text-xs text-[#3f3d3a] leading-relaxed">
                    Linear classification head maps 768-dim pooled vectors to 5 calibrated BBC category probabilities.
                  </p>
                </div>
              </StaggerItem>
            </StaggerContainer>
          </div>
        </Reveal>

        {/* 2. Mathematical Formulations */}
        <Reveal delay={0.1}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-6 shadow-md space-y-3">
              <div className="flex items-center gap-2 text-indigo-600 font-mono text-xs uppercase font-semibold">
                <Code className="size-4" /> 1. Scaled Dot-Product Attention (DistilBERT)
              </div>
              <h3 className="text-base font-semibold text-[#0f0f0e]">Transformer Attention Formula</h3>
              <div className="rounded-xl bg-[#f1efeb] p-4 font-mono text-xs text-[#0891b2] border border-[#e7e3dd] font-semibold">
                Attention(Q, K, V) = softmax( (Q &bull; K^T) / √d_k ) &bull; V
              </div>
              <p className="text-xs text-[#3f3d3a] leading-relaxed">
                Allows the model to dynamically weight token relevance across long contexts, capturing
                nuanced journalistic domain markers regardless of sentence position.
              </p>
            </div>

            <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-6 shadow-md space-y-3">
              <div className="flex items-center gap-2 text-[#059669] font-mono text-xs uppercase font-semibold">
                <Code className="size-4" /> 2. Support Vector Machine (Linear SVM)
              </div>
              <h3 className="text-base font-semibold text-[#0f0f0e]">Hyperplane Decision Function</h3>
              <div className="rounded-xl bg-[#f1efeb] p-4 font-mono text-xs text-[#059669] border border-[#e7e3dd] font-semibold">
                f(x) = sign( w^T &bull; Φ(x) + b ) &bull; TF-IDF(t, d)
              </div>
              <p className="text-xs text-[#3f3d3a] leading-relaxed">
                Constructs optimal separating hyperplanes maximizing geometric margins between
                text vector clusters in sparse 5,000-dimensional vocabulary space.
              </p>
            </div>
          </div>
        </Reveal>

        {/* 3. Tech Stack Matrix */}
        <Reveal delay={0.15}>
          <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-8 shadow-md space-y-6">
            <h2 className="font-heading text-lg font-semibold text-[#0f0f0e] flex items-center gap-2">
              <Cpu className="size-5 text-indigo-600" />
              Production Technology Stack
            </h2>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono">
              <div className="p-4 rounded-xl bg-[#f1efeb] border border-[#e7e3dd] space-y-1">
                <span className="text-[#6b6660]">Frontend Core</span>
                <div className="font-semibold text-[#0f0f0e] text-sm">Next.js 14</div>
                <span className="text-[#3f3d3a]">App Router</span>
              </div>

              <div className="p-4 rounded-xl bg-[#f1efeb] border border-[#e7e3dd] space-y-1">
                <span className="text-[#6b6660]">Language</span>
                <div className="font-semibold text-[#0f0f0e] text-sm">TypeScript 5</div>
                <span className="text-[#3f3d3a]">Type-Safe</span>
              </div>

              <div className="p-4 rounded-xl bg-[#f1efeb] border border-[#e7e3dd] space-y-1">
                <span className="text-[#6b6660]">Styling</span>
                <div className="font-semibold text-[#0f0f0e] text-sm">Tailwind CSS</div>
                <span className="text-[#3f3d3a]">Warm Light Theme</span>
              </div>

              <div className="p-4 rounded-xl bg-[#f1efeb] border border-[#e7e3dd] space-y-1">
                <span className="text-[#6b6660]">ML Backend</span>
                <div className="font-semibold text-[#0f0f0e] text-sm">FastAPI</div>
                <span className="text-[#3f3d3a]">Scikit-Learn</span>
              </div>
            </div>
          </div>
        </Reveal>

        {/* 4. Viva Defense FAQ */}
        <Reveal delay={0.2}>
          <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-8 shadow-lg space-y-6">
            <h2 className="font-heading text-lg font-semibold text-[#0f0f0e] flex items-center gap-2">
              <HelpCircle className="size-5 text-[#d97706]" />
              Academic & Technical FAQ (Viva Defense)
            </h2>

            <div className="space-y-4 text-xs">
              <div className="p-5 rounded-xl bg-[#f1efeb] border border-[#e7e3dd] space-y-2">
                <h4 className="font-semibold text-[#0f0f0e] text-sm">
                  Q: Why does Linear SVM outperform Naive Bayes on news text?
                </h4>
                <p className="text-[#3f3d3a] leading-relaxed">
                  Linear SVM does not assume conditional independence among words. Because news articles
                  frequently exhibit strong term co-occurrences (e.g. &quot;interest&quot; + &quot;rates&quot; + &quot;inflation&quot;),
                  maximum-margin hyperplanes discover superior discriminative boundaries.
                </p>
              </div>

              <div className="p-5 rounded-xl bg-[#f1efeb] border border-[#e7e3dd] space-y-2">
                <h4 className="font-semibold text-[#0f0f0e] text-sm">
                  Q: How is data leakage prevented during TF-IDF extraction?
                </h4>
                <p className="text-[#3f3d3a] leading-relaxed">
                  The TF-IDF vectorizer vocabulary and IDF weights are strictly fitted exclusively on the 80%
                  training split. The 20% test partition is only transformed using the pre-fitted parameters.
                </p>
              </div>
            </div>
          </div>
        </Reveal>
      </div>
    </div>
  );
}
