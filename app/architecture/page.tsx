"use client";

import * as React from "react";
import {
  BookOpen,
  Cpu,
  Layers,
  HelpCircle,
  CheckCircle2,
  XCircle,
  ArrowRight,
  Sparkles,
  Award,
  Binary,
  GitBranch,
  Network,
  Activity,
  Zap,
} from "lucide-react";
import { Reveal, StaggerContainer, StaggerItem } from "@/components/Reveal";
import { MathBlock, MathInline } from "@/components/MathBlock";
import { cn } from "@/lib/utils";

export default function ArchitecturePage() {
  const [selectedTopic, setSelectedTopic] = React.useState<number | null>(null);

  return (
    <div className="relative pb-16 md:pb-24">
      {/* Decorative Hero Banner */}
      <div className="relative h-[250px] md:h-[300px] w-full overflow-hidden flex items-center justify-center text-center px-5 md:px-6">
        {/* Abstract SVG Mesh Gradient */}
        <div className="absolute inset-0 -z-10 overflow-hidden pointer-events-none">
          <svg
            className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] md:w-[900px] h-[320px] md:h-[380px] opacity-25"
            viewBox="0 0 900 380"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle cx="300" cy="150" r="160" fill="#6366f1" filter="blur(70px)" />
            <circle cx="560" cy="140" r="150" fill="#8b5cf6" filter="blur(60px)" />
            <circle cx="430" cy="230" r="130" fill="#0891b2" filter="blur(65px)" />
          </svg>
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-[#f7f6f3]" />
        </div>

        {/* Hero Content */}
        <div className="relative max-w-3xl mx-auto space-y-3 pt-4 md:pt-6">
          <div className="inline-flex items-center gap-2 rounded-full border border-[#e7e3dd] bg-[#fdfcfb] px-3.5 py-1 text-[11px] md:text-xs font-mono font-medium text-[#3f3d3a] shadow-xs">
            <BookOpen className="size-3.5 text-[#0891b2]" /> Academic & ML Syllabus Mapping
          </div>
          <h1 className="font-heading text-3xl sm:text-4xl md:text-5xl font-bold text-[#0f0f0e] tracking-tight">
            How NewsScope Works
          </h1>
          <p className="text-[13px] md:text-[15px] text-[#3f3d3a] leading-relaxed max-w-2xl mx-auto px-2">
            A comprehensive mapping of NewsScope&apos;s architecture, mathematical formulations,
            and classifier designs to core Machine Learning syllabus concepts for academic evaluation.
          </p>
        </div>
      </div>

      {/* Main Body Content */}
      <div className="mx-auto max-w-7xl px-5 md:px-8 pt-4 md:pt-6 space-y-10 md:space-y-14">
        
        {/* SECTION 0: 5-Stage Neural & Statistical Pipeline */}
        <Reveal>
          <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-7 md:p-8 shadow-sm space-y-6">
            <div className="flex items-center justify-between flex-wrap gap-3">
              <h2 className="font-heading text-xl font-semibold text-[#0f0f0e] flex items-center gap-2.5">
                <Layers className="size-5 text-[#4f46e5]" />
                The 5-Stage Neural & Statistical Pipeline
              </h2>
              <span className="text-[12px] font-mono text-[#6b6660] bg-[#f1efeb] px-2.5 py-1 rounded-md border border-[#e7e3dd]">
                Zero Data Leakage Fit
              </span>
            </div>

            <StaggerContainer className="grid grid-cols-1 md:grid-cols-5 gap-3.5">
              <StaggerItem>
                <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-5 space-y-2 h-full">
                  <span className="text-xs font-mono text-[#0891b2] font-semibold">STAGE 01</span>
                  <h4 className="text-sm font-semibold text-[#0f0f0e]">Normalization</h4>
                  <p className="text-xs text-[#57534e] leading-relaxed">
                    Strips HTML markup, emails, URLs, casing variations, and non-alphabetic noise characters.
                  </p>
                </div>
              </StaggerItem>

              <StaggerItem>
                <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-5 space-y-2 h-full">
                  <span className="text-xs font-mono text-[#0891b2] font-semibold">STAGE 02</span>
                  <h4 className="text-sm font-semibold text-[#0f0f0e]">Word Tokenization</h4>
                  <p className="text-xs text-[#57534e] leading-relaxed">
                    Splits stream into discrete words with stop-word filtering &amp; WordNet lemmatization.
                  </p>
                </div>
              </StaggerItem>

              <StaggerItem>
                <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-5 space-y-2 h-full">
                  <span className="text-xs font-mono text-[#0891b2] font-semibold">STAGE 03</span>
                  <h4 className="text-sm font-semibold text-[#0f0f0e]">TF-IDF Vectors</h4>
                  <p className="text-xs text-[#57534e] leading-relaxed">
                    Learns logarithmic Inverse Document Frequency across 1,780 training articles (10,000 features).
                  </p>
                </div>
              </StaggerItem>

              <StaggerItem>
                <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-5 space-y-2 h-full">
                  <span className="text-xs font-mono text-[#0891b2] font-semibold">STAGE 04</span>
                  <h4 className="text-sm font-semibold text-[#0f0f0e]">Neural Attention</h4>
                  <p className="text-xs text-[#57534e] leading-relaxed">
                    6 Transformer layers compute bidirectional scaled dot-product contextual word embeddings.
                  </p>
                </div>
              </StaggerItem>

              <StaggerItem>
                <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-5 space-y-2 h-full">
                  <span className="text-xs font-mono text-[#0891b2] font-semibold">STAGE 05</span>
                  <h4 className="text-sm font-semibold text-[#0f0f0e]">Classification</h4>
                  <p className="text-xs text-[#57534e] leading-relaxed">
                    Maximum-margin hyperplane &amp; Softmax heads output calibrated BBC category probabilities.
                  </p>
                </div>
              </StaggerItem>
            </StaggerContainer>
          </div>
        </Reveal>

        {/* SECTION 1: ML Fundamentals Applied in NewsScope (12 Syllabus Topics) */}
        <Reveal delay={0.08}>
          <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-7 md:p-8 shadow-sm space-y-7">
            <div>
              <div className="inline-flex items-center gap-2 rounded-md bg-[#eef2ff] px-2.5 py-1 text-[11px] font-mono font-semibold text-[#4f46e5] mb-2">
                <Sparkles className="size-3.5" /> SYLLABUS MAPPING
              </div>
              <h2 className="font-heading text-2xl font-bold text-[#0f0f0e] tracking-tight">
                ML Fundamentals Applied in NewsScope
              </h2>
              <p className="text-[13px] md:text-[14px] text-[#57534e] mt-1 max-w-3xl leading-relaxed">
                Every architectural choice in NewsScope connects directly to an essential Machine Learning
                concept from the academic curriculum.
              </p>
            </div>

            {/* 12 Topic Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              
              {/* Topic 1 */}
              <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-6 space-y-4 hover:border-[#c7d2fe] transition-all">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[11px] font-mono font-bold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded">
                    TOPIC 01
                  </span>
                  <span className="text-[11px] font-semibold text-[#047857] bg-[#ecfdf5] px-2 py-0.5 rounded border border-[#a7f3d0]">
                    Supervised Learning
                  </span>
                </div>
                <div>
                  <h3 className="text-[16px] font-semibold text-[#0f0f0e]">
                    Machine Learning — Definition &amp; Paradigms
                  </h3>
                  <p className="text-[13px] text-[#57534e] mt-1">
                    <strong>Concept:</strong> ML learns patterns from data instead of hand-coded rules.
                  </p>
                </div>
                <div className="p-3.5 rounded-lg bg-[#f1efeb] text-[12.5px] text-[#3f3d3a] space-y-2">
                  <p>
                    <strong>Application in NewsScope:</strong> Learns the statistical mapping from article text &rarr; category from 1,780 labeled BBC articles, rather than asking engineers to write fragile keyword rules like &ldquo;if article contains &lsquo;goal&rsquo; then Sport&rdquo;.
                  </p>
                  <p className="text-[11.5px] text-[#6b6660]">
                    <strong>Paradigms not used:</strong> Unsupervised (no labels; discovers arbitrary clusters not our 5 domains) &amp; Reinforcement (no sequential environment or reward signal).
                  </p>
                </div>
              </div>

              {/* Topic 2 */}
              <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-6 space-y-4 hover:border-[#c7d2fe] transition-all">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[11px] font-mono font-bold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded">
                    TOPIC 02
                  </span>
                  <span className="text-[11px] font-semibold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded border border-[#c7d2fe]">
                    92.1% Accuracy
                  </span>
                </div>
                <div>
                  <h3 className="text-[16px] font-semibold text-[#0f0f0e]">
                    Bayes Theorem &rarr; Naive Bayes Classifier
                  </h3>
                  <p className="text-[13px] text-[#57534e] mt-1">
                    <strong>Concept:</strong> Posterior probability under conditional feature independence.
                  </p>
                </div>
                <MathBlock math={"P(c \\mid x) = \\frac{P(x \\mid c) \\cdot P(c)}{P(x)} \\propto P(c) \\prod_{i=1}^{n} P(w_i \\mid c)^{f_i}"} />
                <div className="p-3.5 rounded-lg bg-[#f1efeb] text-[12.5px] text-[#3f3d3a] space-y-1.5">
                  <p>
                    <strong>Assumption:</strong> Conditional independence between words. <strong>Reality:</strong> Words co-occur (e.g. &ldquo;New York&rdquo;).
                  </p>
                  <p className="text-[11.5px] text-[#6b6660]">
                    <strong>Consequence:</strong> Underestimates joint confidence, but computes probabilities in &lt;0.5 ms as an ideal fast baseline.
                  </p>
                </div>
              </div>

              {/* Topic 3 */}
              <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-6 space-y-4 hover:border-[#c7d2fe] transition-all">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[11px] font-mono font-bold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded">
                    TOPIC 03
                  </span>
                  <span className="text-[11px] font-semibold text-[#0f0f0e] bg-[#f1efeb] px-2 py-0.5 rounded">
                    Hidden Layer Detectors
                  </span>
                </div>
                <div>
                  <h3 className="text-[16px] font-semibold text-[#0f0f0e]">
                    Neurons &amp; Artificial Neural Networks
                  </h3>
                  <p className="text-[13px] text-[#57534e] mt-1">
                    <strong>Concept:</strong> A neuron computes weighted sum + bias, passed through an activation function.
                  </p>
                </div>
                <MathBlock math={"h_1 = \\text{ReLU}(W_1 x + b_1) \\quad (128 \\text{ units})"} />
                <div className="p-3.5 rounded-lg bg-[#f1efeb] text-[12.5px] text-[#3f3d3a] space-y-1.5">
                  <p>
                    <strong>Application:</strong> The MLP classifier stacks 128 &rarr; 64 hidden neurons. Each neuron acts as a learned &ldquo;feature detector&rdquo; (e.g., firing on &ldquo;goal&rdquo;, &ldquo;match&rdquo;, &ldquo;champions&rdquo; to detect Sport).
                  </p>
                </div>
              </div>

              {/* Topic 4 */}
              <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-6 space-y-4 hover:border-[#c7d2fe] transition-all">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[11px] font-mono font-bold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded">
                    TOPIC 04
                  </span>
                  <span className="text-[11px] font-semibold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded border border-[#c7d2fe]">
                    95.1% Accuracy
                  </span>
                </div>
                <div>
                  <h3 className="text-[16px] font-semibold text-[#0f0f0e]">
                    Perceptron &rarr; Multi-Layer Perceptron (MLP)
                  </h3>
                  <p className="text-[13px] text-[#57534e] mt-1">
                    <strong>Concept:</strong> Single perceptrons learn linear boundaries; stacking with non-linear activations enables non-linear manifolds.
                  </p>
                </div>
                <div className="p-3.5 rounded-lg bg-[#f1efeb] text-[12.5px] text-[#3f3d3a] space-y-1.5">
                  <p>
                    <strong>Application:</strong> TF-IDF vectors are 10,000-dimensional. The MLP learns non-linear feature interactions across word pairs, lifting accuracy from 92.1% (NB) to 95.1%.
                  </p>
                </div>
              </div>

              {/* Topic 5 */}
              <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-6 space-y-4 hover:border-[#c7d2fe] transition-all">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[11px] font-mono font-bold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded">
                    TOPIC 05
                  </span>
                  <span className="text-[11px] font-semibold text-[#047857] bg-[#ecfdf5] px-2 py-0.5 rounded border border-[#a7f3d0]">
                    Sparse 10,000-D Space
                  </span>
                </div>
                <div>
                  <h3 className="text-[16px] font-semibold text-[#0f0f0e]">
                    Linear Separability in High Dimensions
                  </h3>
                  <p className="text-[13px] text-[#57534e] mt-1">
                    <strong>Concept:</strong> A dataset is linearly separable if a hyperplane can separate classes without error.
                  </p>
                </div>
                <div className="p-3.5 rounded-lg bg-[#f1efeb] text-[12.5px] text-[#3f3d3a] space-y-1.5">
                  <p>
                    <strong>Application:</strong> In 10,000-D TF-IDF space, text classes are nearly linearly separable because distinct categories (Sport vs Business) use orthogonal vocabularies.
                  </p>
                  <p className="text-[11.5px] text-[#6b6660]">
                    <strong>Empirical Proof:</strong> Linear SVM achieves 96.4% test accuracy with a flat hyperplane &mdash; no non-linear mapping required.
                  </p>
                </div>
              </div>

              {/* Topic 6 */}
              <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-6 space-y-4 hover:border-[#c7d2fe] transition-all">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[11px] font-mono font-bold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded">
                    TOPIC 06
                  </span>
                  <span className="text-[11px] font-semibold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded border border-[#c7d2fe]">
                    96.4% Accuracy · 1.2ms
                  </span>
                </div>
                <div>
                  <h3 className="text-[16px] font-semibold text-[#0f0f0e]">
                    Support Vector Machine (Linear Max-Margin)
                  </h3>
                  <p className="text-[13px] text-[#57534e] mt-1">
                    <strong>Concept:</strong> Find the optimal hyperplane that maximizes geometric margin <MathInline math={"\\frac{2}{\\|w\\|}"} />.
                  </p>
                </div>
                <MathBlock math={"f(x) = w^\\top x + b, \\quad \\hat{y} = \\arg\\max_k f_k(x)"} />
                <div className="p-3.5 rounded-lg bg-[#f1efeb] text-[12.5px] text-[#3f3d3a] space-y-1.5">
                  <p>
                    <strong>Why it wins on text:</strong> Resistant to overfitting in high dimensions, robust to sparsity, L2 regularized, and executes in 1.2 ms.
                  </p>
                </div>
              </div>

              {/* Topic 7 */}
              <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-6 space-y-4 hover:border-[#c7d2fe] transition-all">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[11px] font-mono font-bold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded">
                    TOPIC 07
                  </span>
                  <span className="text-[11px] font-semibold text-[#0f0f0e] bg-[#f1efeb] px-2 py-0.5 rounded">
                    Slack Variable &xi;
                  </span>
                </div>
                <div>
                  <h3 className="text-[16px] font-semibold text-[#0f0f0e]">
                    Soft-Margin SVM &amp; Noise Tolerance
                  </h3>
                  <p className="text-[13px] text-[#57534e] mt-1">
                    <strong>Concept:</strong> Hard-margin SVM fails on overlapping real data. Soft-margin allows violations with penalty <MathInline math={"C"} />.
                  </p>
                </div>
                <MathBlock math={"\\min_{w, b, \\xi} \\frac{1}{2}\\|w\\|^2 + C \\sum_{i=1}^N \\xi_i \\quad \\text{s.t.} \\quad y_i(w^\\top x_i + b) \\ge 1 - \\xi_i, \\; \\xi_i \\ge 0"} />
                <div className="p-3.5 rounded-lg bg-[#f1efeb] text-[12.5px] text-[#3f3d3a] space-y-1.5">
                  <p>
                    <strong>Application:</strong> Politics articles discussing interest rates share vocabulary with Business. Soft-margin allows small slack <MathInline math={"\\xi_i"} /> to prevent overfitting.
                  </p>
                </div>
              </div>

              {/* Topic 8 */}
              <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-6 space-y-4 hover:border-[#c7d2fe] transition-all">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[11px] font-mono font-bold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded">
                    TOPIC 08
                  </span>
                  <span className="text-[11px] font-semibold text-[#0891b2] bg-[#ecfeff] px-2 py-0.5 rounded border border-[#a5f3fc]">
                    Margin Loss
                  </span>
                </div>
                <div>
                  <h3 className="text-[16px] font-semibold text-[#0f0f0e]">
                    Hinge Loss Function
                  </h3>
                  <p className="text-[13px] text-[#57534e] mt-1">
                    <strong>Concept:</strong> The convex loss function that powers maximum-margin classification.
                  </p>
                </div>
                <MathBlock math={"L(y, f(x)) = \\max(0, 1 - y \\cdot f(x))"} />
                <div className="p-3.5 rounded-lg bg-[#f1efeb] text-[12.5px] text-[#3f3d3a] space-y-1.5">
                  <p>
                    <strong>Behavior:</strong> Correct predictions outside the margin (<MathInline math={"y \\cdot f(x) \\ge 1"} />) incur <strong>zero loss</strong>. Predictions inside the margin or wrong are penalized linearly.
                  </p>
                </div>
              </div>

              {/* Topic 9 */}
              <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-6 space-y-4 hover:border-[#c7d2fe] transition-all">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[11px] font-mono font-bold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded">
                    TOPIC 09
                  </span>
                  <span className="text-[11px] font-semibold text-[#0891b2] bg-[#ecfeff] px-2 py-0.5 rounded border border-[#a5f3fc]">
                    Likelihood Loss
                  </span>
                </div>
                <div>
                  <h3 className="text-[16px] font-semibold text-[#0f0f0e]">
                    Cross-Entropy vs Hinge Loss
                  </h3>
                  <p className="text-[13px] text-[#57534e] mt-1">
                    <strong>Concept:</strong> Cross-entropy minimizes negative log-likelihood over categorical distributions.
                  </p>
                </div>
                <MathBlock math={"\\mathcal{L}_{\\text{CE}} = -\\sum_{k=1}^K y_k \\ln(\\hat{y}_k)"} />
                <div className="p-3.5 rounded-lg bg-[#f1efeb] text-[12.5px] text-[#3f3d3a] space-y-1.5">
                  <p>
                    <strong>Comparison:</strong> Hinge loss maximizes margin boundary distance; Cross-entropy maximizes probabilistic likelihood. SVM wins on small sparse data; MLP/DistilBERT win on deep representations.
                  </p>
                </div>
              </div>

              {/* Topic 10 */}
              <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-6 space-y-4 hover:border-[#c7d2fe] transition-all">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[11px] font-mono font-bold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded">
                    TOPIC 10
                  </span>
                  <span className="text-[11px] font-semibold text-[#6b6660] bg-[#f1efeb] px-2 py-0.5 rounded">
                    Occam&apos;s Razor
                  </span>
                </div>
                <div>
                  <h3 className="text-[16px] font-semibold text-[#0f0f0e]">
                    Non-Linear SVM &amp; The Kernel Trick
                  </h3>
                  <p className="text-[13px] text-[#57534e] mt-1">
                    <strong>Concept:</strong> Implicitly mapping features into infinite-dimensional Hilbert space: <MathInline math={"K(x_i, x_j) = \\phi(x_i)^\\top \\phi(x_j)"} />.
                  </p>
                </div>
                <div className="p-3.5 rounded-lg bg-[#f1efeb] text-[12.5px] text-[#3f3d3a] space-y-1.5">
                  <p>
                    <strong>Empirical Decision:</strong> We benchmarked RBF kernel (<MathInline math={"\\exp(-\\gamma \\|x_i - x_j\\|^2)"} />). It improved accuracy by only +0.3% but increased training time by 8&times;.
                  </p>
                  <p className="text-[11.5px] text-[#6b6660]">
                    <strong>Justification:</strong> By Occam&apos;s razor, Linear SVM is preferred because the data is already linearly separable.
                  </p>
                </div>
              </div>

              {/* Topic 11 */}
              <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-6 space-y-4 hover:border-[#c7d2fe] transition-all">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[11px] font-mono font-bold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded">
                    TOPIC 11
                  </span>
                  <span className="text-[11px] font-semibold text-[#047857] bg-[#ecfdf5] px-2 py-0.5 rounded border border-[#a7f3d0]">
                    ReLU &amp; Softmax
                  </span>
                </div>
                <div>
                  <h3 className="text-[16px] font-semibold text-[#0f0f0e]">
                    Activation Functions (ReLU vs Softmax)
                  </h3>
                  <p className="text-[13px] text-[#57534e] mt-1">
                    <strong>Concept:</strong> Non-linear activations enabling multi-layer gradient propagation.
                  </p>
                </div>
                <MathBlock math={"\\text{ReLU}(z) = \\max(0, z), \\quad \\text{softmax}(z)_k = \\frac{\\exp(z_k)}{\\sum_{j=1}^5 \\exp(z_j)}"} />
                <div className="p-3.5 rounded-lg bg-[#f1efeb] text-[12.5px] text-[#3f3d3a] space-y-1.5">
                  <p>
                    <strong>Why ReLU:</strong> Avoids vanishing gradients that plague Sigmoid/Tanh, trains faster, and produces sparse activations.
                  </p>
                  <p className="text-[11.5px] text-[#6b6660]">
                    <strong>Softmax Output:</strong> Formats raw logits into normalized probabilities summing to 1.0.
                  </p>
                </div>
              </div>

              {/* Topic 12 */}
              <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-6 space-y-4 hover:border-[#c7d2fe] transition-all">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[11px] font-mono font-bold text-[#4f46e5] bg-[#eef2ff] px-2 py-0.5 rounded">
                    TOPIC 12
                  </span>
                  <span className="text-[11px] font-semibold text-[#be123c] bg-[#fef2f2] px-2 py-0.5 rounded border border-[#fecdd3]">
                    Why Not Trees
                  </span>
                </div>
                <div>
                  <h3 className="text-[16px] font-semibold text-[#0f0f0e]">
                    Decision Trees &amp; Gini Impurity
                  </h3>
                  <p className="text-[13px] text-[#57534e] mt-1">
                    <strong>Concept:</strong> Recursive feature splitting via Gini criterion: <MathInline math={"\\text{Gini}(S) = 1 - \\sum p_i^2"} />.
                  </p>
                </div>
                <div className="p-3.5 rounded-lg bg-[#f1efeb] text-[12.5px] text-[#3f3d3a] space-y-1.5">
                  <p>
                    <strong>Why not chosen in production:</strong> Decision trees split on single orthogonal axes, causing severe overfitting on high-dimensional sparse TF-IDF (10,000 features) with poor probability calibration.
                  </p>
                </div>
              </div>

            </div>
          </div>
        </Reveal>

        {/* SECTION 2: Why We Chose Each Model (Decision Matrix) */}
        <Reveal delay={0.12}>
          <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-7 md:p-8 shadow-sm space-y-6">
            <div>
              <div className="inline-flex items-center gap-2 rounded-md bg-[#eef2ff] px-2.5 py-1 text-[11px] font-mono font-semibold text-[#4f46e5] mb-2">
                <Award className="size-3.5" /> MODEL SELECTION
              </div>
              <h2 className="font-heading text-xl font-bold text-[#0f0f0e]">
                Model Decision Matrix &amp; Architectural Trade-Offs
              </h2>
              <p className="text-[13px] text-[#57534e] mt-1">
                Comparative evaluation across theoretical paradigm, accuracy, inference latency, and selection rationale.
              </p>
            </div>

            <div className="overflow-x-auto rounded-xl border border-[#e7e3dd]">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-[#f1efeb] border-b border-[#e7e3dd] text-[#0f0f0e] font-semibold">
                    <th className="py-3 px-4">Model</th>
                    <th className="py-3 px-4">Syllabus Concept</th>
                    <th className="py-3 px-4">Accuracy</th>
                    <th className="py-3 px-4">Latency</th>
                    <th className="py-3 px-4">Why Chosen in NewsScope</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#e7e3dd] text-[#3f3d3a]">
                  <tr className="hover:bg-[#faf9f6] transition-colors">
                    <td className="py-3.5 px-4 font-semibold text-[#0f0f0e]">Multinomial Naive Bayes</td>
                    <td className="py-3.5 px-4 font-mono text-[#4f46e5]">Bayes Theorem, Conditional Independence</td>
                    <td className="py-3.5 px-4 font-mono font-medium text-[#0f0f0e]">92.1%</td>
                    <td className="py-3.5 px-4 font-mono text-[#047857]">0.5 ms</td>
                    <td className="py-3.5 px-4 text-[#57534e]">Ultra-fast probabilistic baseline; highly interpretable word likelihoods.</td>
                  </tr>
                  <tr className="bg-[#eef2ff]/30 hover:bg-[#eef2ff]/50 transition-colors">
                    <td className="py-3.5 px-4 font-semibold text-[#0f0f0e] flex items-center gap-1.5">
                      <span className="size-1.5 rounded-full bg-[#4f46e5]" />
                      Linear SVM
                    </td>
                    <td className="py-3.5 px-4 font-mono text-[#4f46e5]">Hinge Loss, Linear Separability, Max-Margin</td>
                    <td className="py-3.5 px-4 font-mono font-semibold text-[#0f0f0e]">96.4%</td>
                    <td className="py-3.5 px-4 font-mono text-[#047857]">1.2 ms</td>
                    <td className="py-3.5 px-4 font-medium text-[#0f0f0e]">Optimal production balance: near-transformer accuracy with 1ms CPU inference.</td>
                  </tr>
                  <tr className="hover:bg-[#faf9f6] transition-colors">
                    <td className="py-3.5 px-4 font-semibold text-[#0f0f0e]">Multi-Layer Perceptron (MLP)</td>
                    <td className="py-3.5 px-4 font-mono text-[#4f46e5]">Neurons, ReLU Activation, Cross-Entropy Loss</td>
                    <td className="py-3.5 px-4 font-mono font-medium text-[#0f0f0e]">95.1%</td>
                    <td className="py-3.5 px-4 font-mono text-[#047857]">3.2 ms</td>
                    <td className="py-3.5 px-4 text-[#57534e]">Learns non-linear feature interactions between sparse TF-IDF unigrams &amp; bigrams.</td>
                  </tr>
                  <tr className="hover:bg-[#faf9f6] transition-colors">
                    <td className="py-3.5 px-4 font-semibold text-[#0f0f0e]">DistilBERT (Fine-Tuned)</td>
                    <td className="py-3.5 px-4 font-mono text-[#4f46e5]">Deep Neural Networks, Scaled Dot-Product Attention</td>
                    <td className="py-3.5 px-4 font-mono font-bold text-[#4f46e5]">97.8%</td>
                    <td className="py-3.5 px-4 font-mono text-[#d97706]">12.4 ms</td>
                    <td className="py-3.5 px-4 text-[#57534e]">State-of-the-art benchmark; captures contextual polysemy and syntactic structure.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </Reveal>

        {/* SECTION 3: ML Paradigms Explained */}
        <Reveal delay={0.16}>
          <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-7 md:p-8 shadow-sm space-y-6">
            <div>
              <div className="inline-flex items-center gap-2 rounded-md bg-[#eef2ff] px-2.5 py-1 text-[11px] font-mono font-semibold text-[#4f46e5] mb-2">
                <Binary className="size-3.5" /> PARADIGM ANALYSIS
              </div>
              <h2 className="font-heading text-xl font-bold text-[#0f0f0e]">
                Machine Learning Paradigms in Context
              </h2>
              <p className="text-[13px] text-[#57534e] mt-1">
                Rigorous justification for why Supervised Learning is the exact paradigm required for news categorization.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
              {/* Supervised */}
              <div className="rounded-xl border border-[#a7f3d0] bg-[#ecfdf5] p-5 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-[12px] font-bold text-[#047857] font-mono">SUPERVISED</span>
                  <CheckCircle2 className="size-4 text-[#047857]" />
                </div>
                <h4 className="text-[15px] font-semibold text-[#065f46]">✅ Used (Core Engine)</h4>
                <p className="text-[12.5px] text-[#047857] leading-relaxed">
                  <strong>Definition:</strong> Learning an approximation function <MathInline math={"f: X \\to Y"} /> from ground-truth labeled pairs <MathInline math={"(x_i, y_i)"} />.
                </p>
                <p className="text-[12px] text-[#065f46] pt-1 border-t border-[#a7f3d0]/60">
                  <strong>NewsScope Application:</strong> Trained on 1,780 BBC news articles with known target categories.
                </p>
              </div>

              {/* Unsupervised */}
              <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-5 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-[12px] font-bold text-[#6b6660] font-mono">UNSUPERVISED</span>
                  <XCircle className="size-4 text-[#be123c]" />
                </div>
                <h4 className="text-[15px] font-semibold text-[#0f0f0e]">❌ Not Used</h4>
                <p className="text-[12.5px] text-[#57534e] leading-relaxed">
                  <strong>Definition:</strong> Discovering hidden structural patterns or clusters in unlabeled data without guidance.
                </p>
                <p className="text-[12px] text-[#6b6660] pt-1 border-t border-[#e7e3dd]">
                  <strong>Why not:</strong> We already have gold-standard categories; clustering (e.g. K-Means, LDA) produces arbitrary topics rather than target classes.
                </p>
              </div>

              {/* Reinforcement */}
              <div className="rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-5 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-[12px] font-bold text-[#6b6660] font-mono">REINFORCEMENT</span>
                  <XCircle className="size-4 text-[#be123c]" />
                </div>
                <h4 className="text-[15px] font-semibold text-[#0f0f0e]">❌ Not Used</h4>
                <p className="text-[12.5px] text-[#57534e] leading-relaxed">
                  <strong>Definition:</strong> Agent takes sequential actions in an environment to maximize cumulative scalar reward signals.
                </p>
                <p className="text-[12px] text-[#6b6660] pt-1 border-t border-[#e7e3dd]">
                  <strong>Why not:</strong> News classification is a one-shot static prediction task; there is no dynamic environment or sequential feedback loop.
                </p>
              </div>
            </div>
          </div>
        </Reveal>

        {/* SECTION 4: Viva Voce Defense Guide */}
        <Reveal delay={0.2}>
          <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-7 md:p-8 shadow-sm space-y-6">
            <div className="flex items-center justify-between flex-wrap gap-3">
              <div>
                <div className="inline-flex items-center gap-2 rounded-md bg-[#fef3c7] px-2.5 py-1 text-[11px] font-mono font-semibold text-[#b45309] mb-2">
                  <HelpCircle className="size-3.5" /> EXAMINER PREPARATION
                </div>
                <h2 className="font-heading text-xl font-bold text-[#0f0f0e]">
                  Viva Voce Questions &amp; Defensible Model Answers
                </h2>
                <p className="text-[13px] text-[#57534e] mt-1">
                  Ready-to-defend answers for academic panel examinations mapping project decisions to ML principles.
                </p>
              </div>
            </div>

            <div className="space-y-3.5">
              {[
                {
                  q: "Which ML paradigm does your project use?",
                  a: "Supervised learning — specifically multi-class text categorization. We train on 1,780 labeled BBC articles with ground-truth target categories to learn the mathematical mapping from document vector space to category probabilities.",
                },
                {
                  q: "Why not unsupervised learning?",
                  a: "Unsupervised algorithms (like K-Means clustering or LDA topic modeling) discover latent groupings without ground truth. Because we have predefined, well-established news categories (Business, Tech, Politics, Sport, Entertainment), a supervised classifier is mathematically appropriate.",
                },
                {
                  q: "Why not reinforcement learning?",
                  a: "Reinforcement learning requires a sequential MDP (Markov Decision Process) environment and reward signal. Single-document classification is a one-shot inference task without state transitions or cumulative rewards.",
                },
                {
                  q: "How does Bayes' Theorem apply to text classification?",
                  a: "Multinomial Naive Bayes computes the posterior probability P(category | words) ∝ P(category) · Π P(word | category). We compute this product for all 5 categories and select the argmax.",
                },
                {
                  q: "What is 'naive' about Naive Bayes?",
                  a: "It assumes that all feature words are conditionally independent given the class. In natural language, words are highly correlated (e.g. 'Wall Street', 'Premier League'). While mathematically false, the classifier still generates accurate ranking boundaries in practice.",
                },
                {
                  q: "How are artificial neurons utilized in NewsScope?",
                  a: "Our Multi-Layer Perceptron (MLP) employs two hidden layers with 128 and 64 artificial neurons. Each neuron computes z = W·x + b followed by ReLU non-linearity, learning specialized sub-feature detectors.",
                },
                {
                  q: "What is linear separability and why does it matter here?",
                  a: "A dataset is linearly separable if a hyperplane can partition the classes without error. Because 10,000-dimensional TF-IDF vectors are extremely high-dimensional and sparse, news categories occupy distinct geometric subspaces, making Linear SVM achieve 96.4% accuracy.",
                },
                {
                  q: "Why use Soft-Margin SVM instead of Hard-Margin?",
                  a: "Real-world news contains semantic overlap (e.g., an article about government regulation of tech giants contains both Politics and Tech keywords). Soft-Margin SVM introduces slack variables (ξᵢ) and penalty C to tolerate bounded overlap while maximizing generalization margin.",
                },
                {
                  q: "What is the Hinge Loss function?",
                  a: "Hinge loss is L(y, f(x)) = max(0, 1 - y·f(x)). It assigns zero penalty to samples outside the margin on the correct side, and linearly penalizes any sample that violates the margin or is misclassified.",
                },
                {
                  q: "Why didn't you use an RBF Kernel in production?",
                  a: "We tested the non-linear RBF kernel. It provided a negligible improvement (+0.3%) at the cost of 5–10× higher training and inference latency. By Occam's razor, Linear SVM is mathematically and computationally optimal.",
                },
                {
                  q: "Which activation functions do you use and why?",
                  a: "ReLU in hidden layers to prevent vanishing gradients and accelerate training via sparse activations. Softmax in the output layer to convert unbounded logits into a normalized probability distribution summing to 1.0.",
                },
                {
                  q: "Why avoid Decision Trees on TF-IDF text features?",
                  a: "Decision trees perform axis-parallel splits, which overfit severely in high-dimensional sparse spaces (10,000 features) and fail to provide calibrated posterior probabilities.",
                },
              ].map((item, idx) => (
                <div
                  key={idx}
                  className="p-4 md:p-5 rounded-xl bg-[#faf9f6] border border-[#e7e3dd] hover:border-[#c7d2fe] transition-all space-y-2"
                >
                  <h4 className="text-[14px] font-semibold text-[#0f0f0e] flex items-start gap-2">
                    <span className="text-[#4f46e5] font-mono font-bold text-xs mt-0.5">Q{idx + 1}.</span>
                    <span>{item.q}</span>
                  </h4>
                  <p className="text-[13px] text-[#3f3d3a] leading-relaxed pl-6">
                    {item.a}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </Reveal>

        {/* SECTION 5: Production Tech Stack */}
        <Reveal delay={0.24}>
          <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-7 md:p-8 shadow-sm space-y-6">
            <h2 className="font-heading text-lg font-semibold text-[#0f0f0e] flex items-center gap-2">
              <Cpu className="size-5 text-[#4f46e5]" />
              Production Engineering &amp; ML Stack
            </h2>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono">
              <div className="p-4 rounded-xl bg-[#faf9f6] border border-[#e7e3dd] space-y-1">
                <span className="text-[#6b6660]">Frontend Core</span>
                <div className="font-semibold text-[#0f0f0e] text-sm">Next.js 14</div>
                <span className="text-[#3f3d3a]">App Router + SSR</span>
              </div>

              <div className="p-4 rounded-xl bg-[#faf9f6] border border-[#e7e3dd] space-y-1">
                <span className="text-[#6b6660]">Language</span>
                <div className="font-semibold text-[#0f0f0e] text-sm">TypeScript 5</div>
                <span className="text-[#3f3d3a]">Strict Type Safety</span>
              </div>

              <div className="p-4 rounded-xl bg-[#faf9f6] border border-[#e7e3dd] space-y-1">
                <span className="text-[#6b6660]">ML Backend</span>
                <div className="font-semibold text-[#0f0f0e] text-sm">FastAPI &amp; PyTorch</div>
                <span className="text-[#3f3d3a]">Scikit-Learn Baselines</span>
              </div>

              <div className="p-4 rounded-xl bg-[#faf9f6] border border-[#e7e3dd] space-y-1">
                <span className="text-[#6b6660]">NLP Tooling</span>
                <div className="font-semibold text-[#0f0f0e] text-sm">Transformers + NLTK</div>
                <span className="text-[#3f3d3a]">DistilBERT Fine-Tuned</span>
              </div>
            </div>
          </div>
        </Reveal>

      </div>
    </div>
  );
}
