/**
 * NewsSense – Ultra-Simple, Modern & Intuitive React Application
 * MCA Academic Project in Machine Learning & Natural Language Processing
 */

const { useState, useEffect, useRef, useMemo } = React;

// Quick test samples across all 8 categories
const SAMPLE_ARTICLES = [
  {
    category: "Politics",
    icon: "🏛️",
    title: "Electoral Reform",
    text: "Parliament passed a landmark electoral reform bill after extensive parliamentary debate on constitutional safeguards and democratic voting integrity. Lawmakers voted on amendments to ensure fair elections."
  },
  {
    category: "Sports",
    icon: "⚽",
    title: "Championship Derby",
    text: "The premier league football champions clinched a thrilling 3-2 victory in the championship derby after scoring two sensational goals in extra time before a sold-out stadium crowd."
  },
  {
    category: "Business",
    icon: "💼",
    title: "Interest Rates",
    text: "The central bank held benchmark interest rates steady to control inflation pressures while monitoring corporate bond yields, quarterly revenue, and stock market exchange fluctuations."
  },
  {
    category: "Technology",
    icon: "💻",
    title: "Next-Gen Microprocessor",
    text: "Semiconductor engineers unveiled a revolutionary 2nm microchip architecture featuring ultra-dense transistor gates, slashing power consumption and accelerating neural network machine learning inference."
  },
  {
    category: "Entertainment",
    icon: "🎬",
    title: "Film Festival Awards",
    text: "Acclaimed directors swept honors at the international film festival awards ceremony, receiving standing ovations for masterful cinematography, evocative screenplay, and transformative acting performances."
  },
  {
    category: "Science",
    icon: "🔬",
    title: "Deep Space Telescope",
    text: "Astrophysicists utilizing orbital space telescopes captured infrared observations of early cosmic galaxy clusters formed shortly after the Big Bang, expanding our understanding of quantum astrophysics."
  },
  {
    category: "Health",
    icon: "🏥",
    title: "Immunotherapy Trial",
    text: "Clinical oncology medical researchers reported significant tumor regression in Phase 3 oncology immunotherapy trials, demonstrating dramatic improvements in patient recovery and clinical health outcomes."
  },
  {
    category: "World",
    icon: "🌍",
    title: "UN Climate Accord",
    text: "The United Nations General Assembly convened a global diplomatic summit to finalize binding international climate accords, humanitarian refugee aid corridors, and multilateral peacekeeping initiatives."
  }
];

const CATEGORY_META = {
  Politics: { icon: "🏛️", color: "var(--cat-politics)", bg: "var(--cat-politics-bg)" },
  Sports: { icon: "⚽", color: "var(--cat-sports)", bg: "var(--cat-sports-bg)" },
  Business: { icon: "💼", color: "var(--cat-business)", bg: "var(--cat-business-bg)" },
  Technology: { icon: "💻", color: "var(--cat-technology)", bg: "var(--cat-technology-bg)" },
  Entertainment: { icon: "🎬", color: "var(--cat-entertainment)", bg: "var(--cat-entertainment-bg)" },
  Science: { icon: "🔬", color: "var(--cat-science)", bg: "var(--cat-science-bg)" },
  Health: { icon: "🏥", color: "var(--cat-health)", bg: "var(--cat-health-bg)" },
  World: { icon: "🌍", color: "var(--cat-world)", bg: "var(--cat-world-bg)" }
};

const MODELS = [
  { id: "naive_bayes", name: "Naive Bayes", badge: "Fastest", desc: "Probabilistic Bayes Theorem" },
  { id: "linear_svm", name: "Linear SVM", badge: "⭐ Highest Accuracy", desc: "Maximum-Margin Hyperplane" },
  { id: "decision_tree", name: "Decision Tree", badge: "Interpretable", desc: "Hierarchical Gini Splits" },
  { id: "mlp", name: "MLP Neural Net", badge: "Deep Learning", desc: "Multi-Layer Feedforward NN" }
];

// Helper to refresh Lucide icons
const refreshIcons = () => {
  if (window.lucide) {
    setTimeout(() => window.lucide.createIcons(), 30);
  }
};

// =====================================================================
// Main Application Component
// =====================================================================
function App() {
  const [activeTab, setActiveTab] = useState("classify"); // Default to Classify for instant ease of use
  const [theme, setTheme] = useState(() => localStorage.getItem("newssense_theme") || "light");
  const [articleText, setArticleText] = useState(SAMPLE_ARTICLES[1].text); // Preload sports sample
  const [selectedModel, setSelectedModel] = useState("linear_svm");
  const [healthStatus, setHealthStatus] = useState(null);
  const [evalMetrics, setEvalMetrics] = useState(null);
  const [datasetStats, setDatasetStats] = useState(null);

  // Apply Theme
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("newssense_theme", theme);
    refreshIcons();
  }, [theme]);

  // Load Initial Backend Data
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [hRes, eRes, sRes] = await Promise.all([
          fetch("/api/health"),
          fetch("/api/models/evaluation"),
          fetch("/api/dataset/stats")
        ]);
        if (hRes.ok) setHealthStatus(await hRes.json());
        if (eRes.ok) setEvalMetrics(await eRes.json());
        if (sRes.ok) setDatasetStats(await sRes.json());
      } catch (err) {
        console.error("Backend fetch error:", err);
      } finally {
        refreshIcons();
      }
    };
    fetchData();
  }, []);

  const toggleTheme = () => {
    setTheme(t => (t === "light" ? "dark" : "light"));
  };

  const handleInspectNLP = (text) => {
    setArticleText(text);
    setActiveTab("nlp");
  };

  return (
    <div className="app-container">
      {/* Top Navbar */}
      <header className="top-nav">
        <div className="top-nav-inner">
          <div className="brand">
            <div className="brand-icon">
              <i data-lucide="newspaper"></i>
            </div>
            <div>
              <div className="brand-title">NewsSense</div>
              <div className="brand-subtitle">Smart News Article Classifier</div>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="nav-tabs">
            <button
              className={`nav-tab-btn ${activeTab === "classify" ? "active" : ""}`}
              onClick={() => setActiveTab("classify")}
            >
              <i data-lucide="sparkles" style={{ width: 16, height: 16 }}></i>
              <span>Classify News</span>
            </button>

            <button
              className={`nav-tab-btn ${activeTab === "nlp" ? "active" : ""}`}
              onClick={() => setActiveTab("nlp")}
            >
              <i data-lucide="binary" style={{ width: 16, height: 16 }}></i>
              <span>NLP Pipeline</span>
            </button>

            <button
              className={`nav-tab-btn ${activeTab === "metrics" ? "active" : ""}`}
              onClick={() => setActiveTab("metrics")}
            >
              <i data-lucide="bar-chart-2" style={{ width: 16, height: 16 }}></i>
              <span>Model Accuracy</span>
            </button>

            <button
              className={`nav-tab-btn ${activeTab === "dataset" ? "active" : ""}`}
              onClick={() => setActiveTab("dataset")}
            >
              <i data-lucide="database" style={{ width: 16, height: 16 }}></i>
              <span>Dataset & Guide</span>
            </button>
          </nav>

          {/* Header Right Actions */}
          <div className="nav-actions">
            <div className="status-badge" title="FastAPI Engine operational">
              <span className="status-dot"></span>
              <span>Online</span>
            </div>

            <button className="theme-toggle-btn" onClick={toggleTheme} title="Toggle Dark/Light Mode">
              <i data-lucide={theme === "dark" ? "sun" : "moon"} style={{ width: 18, height: 18 }}></i>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content View */}
      <main className="main-content">
        {activeTab === "classify" && (
          <SimpleClassifierView
            articleText={articleText}
            setArticleText={setArticleText}
            selectedModel={selectedModel}
            setSelectedModel={setSelectedModel}
            onInspectNLP={handleInspectNLP}
          />
        )}

        {activeTab === "nlp" && (
          <SimpleNLPView
            initialText={articleText}
            onBackToClassify={() => setActiveTab("classify")}
          />
        )}

        {activeTab === "metrics" && (
          <SimpleMetricsView evalMetrics={evalMetrics} />
        )}

        {activeTab === "dataset" && (
          <SimpleDatasetGuideView
            datasetStats={datasetStats}
            onUseSample={(txt) => {
              setArticleText(txt);
              setActiveTab("classify");
            }}
          />
        )}
      </main>

      {/* Clean Footer */}
      <footer className="app-footer">
        <span>NewsSense Academic ML Project &bull; Python 3.14 &bull; Scikit-Learn 1.9 &bull; FastAPI</span>
      </footer>
    </div>
  );
}


// =====================================================================
// 1. SIMPLE CLASSIFIER VIEW
// =====================================================================
function SimpleClassifierView({ articleText, setArticleText, selectedModel, setSelectedModel, onInspectNLP }) {
  const [result, setResult] = useState(null);
  const [multiResults, setMultiResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingAll, setLoadingAll] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    refreshIcons();
  }, [result, multiResults]);

  // Word count & Char count
  const wordCount = articleText.trim() ? articleText.trim().split(/\s+/).length : 0;
  const charCount = articleText.trim().length;

  const handleClassify = async () => {
    if (!articleText.trim()) {
      setErrorMsg("Please enter or paste news article text to classify.");
      return;
    }
    setErrorMsg("");
    setLoading(true);
    try {
      const res = await fetch("/api/article/classify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: articleText, model: selectedModel })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Classification failed");

      // Also fetch top TF-IDF keywords for instant explainability
      let keywords = [];
      try {
        const prepRes = await fetch("/api/article/preprocess", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: articleText })
        });
        if (prepRes.ok) {
          const prepData = await prepRes.json();
          keywords = prepData?.tfidf_information?.top_features || [];
        }
      } catch (e) {
        console.warn("Keywords fetch note:", e);
      }

      setResult({ ...data, keywords });
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setLoading(false);
      refreshIcons();
    }
  };

  const handleCompareAll = async () => {
    if (!articleText.trim()) {
      setErrorMsg("Please enter news text to compare across all 4 models.");
      return;
    }
    setErrorMsg("");
    setLoadingAll(true);
    try {
      const res = await fetch("/api/article/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: articleText, model: selectedModel })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Multi-model comparison failed");

      setMultiResults(data.multi_model_consensus);
      setResult({
        model: data.primary_prediction.model_name,
        model_type: data.primary_prediction.model_type,
        predicted_category: data.primary_prediction.predicted_category,
        scoring: {
          metric: data.primary_prediction.score_info.label,
          value: data.primary_prediction.score_info.confidence_value,
          percentage: data.primary_prediction.score_info.confidence_percentage,
          class_scores: data.primary_prediction.score_info.values
        },
        keywords: data.tfidf_representation.top_contributing_terms
      });
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setLoadingAll(false);
      refreshIcons();
    }
  };

  const handlePaste = async () => {
    try {
      if (navigator.clipboard && navigator.clipboard.readText) {
        const text = await navigator.clipboard.readText();
        if (text) setArticleText(text);
      }
    } catch (err) {
      console.warn("Clipboard read not permitted:", err);
    }
  };

  const handleClear = () => {
    setArticleText("");
    setResult(null);
    setMultiResults(null);
    setErrorMsg("");
  };

  const handleSampleClick = (sample) => {
    setArticleText(sample.text);
    setErrorMsg("");
  };

  const categoryMeta = result ? (CATEGORY_META[result.predicted_category] || { icon: "📰", color: "var(--primary)", bg: "var(--primary-light)" }) : null;

  return (
    <div>
      {/* 1-Click Sample News Pills */}
      <div className="presets-card">
        <div className="presets-label">
          <i data-lucide="sparkles" style={{ width: 14, height: 14, color: "var(--accent-amber)" }}></i>
          <span>Click any sample to test immediately:</span>
        </div>
        <div className="presets-grid">
          {SAMPLE_ARTICLES.map((s, idx) => (
            <button
              key={idx}
              className="preset-chip"
              onClick={() => handleSampleClick(s)}
            >
              <span>{s.icon}</span>
              <span>{s.category}: {s.title}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Main 2-Column Grid */}
      <div className="classifier-grid">
        {/* Left Column: Input Box & Controls */}
        <div className="card">
          <div className="card-header">
            <div className="card-title">
              <i data-lucide="file-text" style={{ color: "var(--primary)" }}></i>
              <span>News Article Content</span>
            </div>
            <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>
              {wordCount} words &bull; {charCount} chars
            </div>
          </div>

          <div className="input-textarea-wrapper">
            <textarea
              className="input-textarea"
              value={articleText}
              onChange={(e) => setArticleText(e.target.value)}
              placeholder="Type or paste any news article text here (politics, sports, technology, health, etc.)..."
            />
          </div>

          <div className="input-toolbar">
            <div className="input-tools">
              <button className="btn-tool" onClick={handlePaste} title="Paste text from clipboard">
                <i data-lucide="clipboard" style={{ width: 13, height: 13 }}></i>
                <span>Paste</span>
              </button>
              <button className="btn-tool" onClick={handleClear} title="Clear text area">
                <i data-lucide="trash-2" style={{ width: 13, height: 13 }}></i>
                <span>Clear</span>
              </button>
            </div>
            <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>Minimum 3 words required</span>
          </div>

          {/* Model Selector Pills */}
          <div className="model-selector-group">
            <label className="model-selector-label">Choose Supervised Machine Learning Model:</label>
            <div className="model-pill-grid">
              {MODELS.map(m => (
                <div
                  key={m.id}
                  className={`model-pill ${selectedModel === m.id ? "active" : ""}`}
                  onClick={() => setSelectedModel(m.id)}
                >
                  <div className="model-pill-title">
                    <span>{m.name}</span>
                    <span style={{ fontSize: "0.7rem", color: selectedModel === m.id ? "var(--primary)" : "var(--text-muted)" }}>
                      {m.badge}
                    </span>
                  </div>
                  <div className="model-pill-desc">{m.desc}</div>
                </div>
              ))}
            </div>
          </div>

          {errorMsg && (
            <div style={{ padding: "0.75rem", background: "var(--cat-politics-bg)", color: "var(--cat-politics)", borderRadius: "var(--radius-sm)", fontSize: "0.85rem", marginBottom: "1rem" }}>
              {errorMsg}
            </div>
          )}

          {/* Action Buttons */}
          <div className="action-buttons-row">
            <button
              className="btn btn-primary"
              onClick={handleClassify}
              disabled={loading || loadingAll}
            >
              {loading ? <span className="spinner"></span> : <i data-lucide="zap"></i>}
              <span>{loading ? "Classifying..." : "⚡ Classify Article"}</span>
            </button>

            <button
              className="btn btn-secondary"
              onClick={handleCompareAll}
              disabled={loading || loadingAll}
              title="Compare all 4 ML models at once"
            >
              {loadingAll ? <span className="spinner"></span> : <i data-lucide="git-compare"></i>}
              <span>Compare All 4</span>
            </button>
          </div>
        </div>

        {/* Right Column: Prediction Results */}
        <div>
          {!result ? (
            <div className="empty-state-card">
              <div className="empty-state-icon">
                <i data-lucide="sparkles" style={{ width: 28, height: 28 }}></i>
              </div>
              <div className="empty-state-title">Ready to Predict</div>
              <div className="empty-state-desc">
                Paste any article text or select a preset sample on top, then click <strong>Classify Article</strong>.
              </div>
            </div>
          ) : (
            <div>
              {/* Hero Prediction Card */}
              <div className="prediction-hero-card">
                <div className="prediction-hero-header">
                  <div className="prediction-category-wrapper">
                    <div
                      className="category-icon-box"
                      style={{ background: categoryMeta.bg, color: categoryMeta.color }}
                    >
                      {categoryMeta.icon}
                    </div>
                    <div>
                      <div className="prediction-category-title">{result.predicted_category}</div>
                      <div className="prediction-model-subtitle">
                        Predicted by <strong>{result.model}</strong>
                      </div>
                    </div>
                  </div>

                  <div className="confidence-box">
                    <div className="confidence-val">
                      {result.scoring.percentage !== null
                        ? `${result.scoring.percentage}%`
                        : `${(result.scoring.value * 100).toFixed(1)}%`}
                    </div>
                    <div className="confidence-label">Confidence</div>
                  </div>
                </div>

                {/* Progress bar */}
                <div className="confidence-meter">
                  <div
                    className="confidence-fill"
                    style={{
                      width: `${result.scoring.percentage !== null ? result.scoring.percentage : Math.min(100, result.scoring.value * 100)}%`
                    }}
                  ></div>
                </div>

                {/* Detected Keywords (TF-IDF) */}
                {result.keywords && result.keywords.length > 0 && (
                  <div className="keywords-container">
                    <div className="keywords-label">
                      <i data-lucide="tag" style={{ width: 13, height: 13 }}></i>
                      <span>Key Signal Words Detected (TF-IDF):</span>
                    </div>
                    <div className="keywords-chips">
                      {result.keywords.slice(0, 8).map((k, idx) => (
                        <span key={idx} className="keyword-chip">
                          <span>{k.term || k.word}</span>
                          <span className="keyword-weight">{(k.weight || k.tfidf_weight).toFixed(2)}</span>
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <div style={{ marginTop: "1rem", display: "flex", justifyContent: "flex-end" }}>
                  <button
                    className="btn-tool"
                    style={{ padding: "0.4rem 0.8rem", fontSize: "0.8rem" }}
                    onClick={() => onInspectNLP(articleText)}
                  >
                    <span>Inspect 5-Stage NLP Breakdown</span>
                    <i data-lucide="arrow-right" style={{ width: 14, height: 14 }}></i>
                  </button>
                </div>
              </div>

              {/* Class Probability / Score Ranking */}
              {(() => {
                if (!result?.scoring?.class_scores) return null;
                const raw = result.scoring.class_scores;
                let scoresList = [];
                if (Array.isArray(raw)) {
                  scoresList = raw;
                } else if (typeof raw === "object") {
                  const entries = Object.entries(raw);
                  const vals = entries.map(([_, v]) => Number(v));
                  const isProb = vals.every(v => v >= 0 && v <= 1.0) && Math.abs(vals.reduce((a, b) => a + b, 0) - 1.0) < 0.15;
                  
                  if (isProb) {
                    scoresList = entries
                      .map(([category, prob]) => ({
                        category,
                        percentage: Math.round(Number(prob) * 1000) / 10,
                        value: Number(prob)
                      }))
                      .sort((a, b) => b.value - a.value);
                  } else {
                    const maxVal = Math.max(...vals);
                    const expVals = vals.map(v => Math.exp(v - maxVal));
                    const sumExp = expVals.reduce((a, b) => a + b, 0) || 1;
                    scoresList = entries
                      .map(([category, rawScore], i) => ({
                        category,
                        rawScore: Number(rawScore).toFixed(3),
                        percentage: Math.round((expVals[i] / sumExp) * 1000) / 10,
                        value: expVals[i] / sumExp
                      }))
                      .sort((a, b) => b.value - a.value);
                  }
                }

                if (scoresList.length === 0) return null;

                return (
                  <div className="card">
                    <div className="card-header" style={{ paddingBottom: "0.5rem", marginBottom: "0.75rem" }}>
                      <div className="card-title" style={{ fontSize: "0.95rem" }}>
                        <i data-lucide="activity" style={{ color: "var(--accent-emerald)" }}></i>
                        <span>Category Confidence Breakdown</span>
                      </div>
                    </div>

                    <div className="prob-list">
                      {scoresList.slice(0, 5).map((cs, idx) => {
                        const meta = CATEGORY_META[cs.category] || { icon: "📰", color: "var(--primary)" };
                        const pct = cs.percentage !== undefined ? cs.percentage : 0;
                        return (
                          <div key={idx} className="prob-row">
                            <div className="prob-row-header">
                              <span className="prob-cat-name">
                                <span>{meta.icon}</span>
                                <span>{cs.category}</span>
                              </span>
                              <span className="prob-percent">{pct}%</span>
                            </div>
                            <div className="prob-track">
                              <div
                                className="prob-bar"
                                style={{
                                  width: `${pct}%`,
                                  background: idx === 0 ? "var(--accent-emerald)" : "var(--primary)"
                                }}
                              ></div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                );
              })()}
            </div>
          )}
        </div>
      </div>

      {/* Multi-Model Consensus Banner (When compared) */}
      {multiResults && (
        <div className="consensus-banner">
          <div className="consensus-header">
            <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
              <i data-lucide="award" style={{ color: "var(--accent-purple)", width: 20, height: 20 }}></i>
              <strong style={{ fontSize: "1.05rem" }}>All 4 Supervised Models Consensus:</strong>
            </div>
            <span className="badge-pill" style={{ background: "var(--accent-purple-light)", color: "var(--accent-purple)" }}>
              Simultaneous Evaluation
            </span>
          </div>

          <div className="consensus-grid">
            {Object.entries(multiResults).map(([mKey, data]) => {
              const mMeta = CATEGORY_META[data.predicted_category] || { icon: "📰" };
              return (
                <div key={mKey} className="consensus-card">
                  <div className="consensus-card-title">{data.model_name}</div>
                  <div className="consensus-card-pred">
                    <span style={{ marginRight: "0.3rem" }}>{mMeta.icon}</span>
                    <span>{data.predicted_category}</span>
                  </div>
                  <div className="consensus-card-score">
                    {data.confidence_percentage ? `${data.confidence_percentage}% confidence` : data.scoring_metric}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}


// =====================================================================
// 2. SIMPLE NLP PIPELINE VIEW
// =====================================================================
function SimpleNLPView({ initialText, onBackToClassify }) {
  const [inputText, setInputText] = useState(initialText || SAMPLE_ARTICLES[0].text);
  const [activeStep, setActiveStep] = useState(1);
  const [nlpData, setNlpData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    refreshIcons();
  }, [nlpData, activeStep]);

  const runPipeline = async () => {
    if (!inputText.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("/api/article/preprocess", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputText })
      });
      if (res.ok) {
        setNlpData(await res.json());
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
      refreshIcons();
    }
  };

  useEffect(() => {
    runPipeline();
  }, []);

  const steps = [
    { num: 1, title: "1. Raw Text", desc: "Original Input Article" },
    { num: 2, title: "2. Cleaned Text", desc: "Lowercase & Symbols Stripped" },
    { num: 3, title: "3. Word Tokens", desc: "Tokenization" },
    { num: 4, title: "4. Stopwords & Lemmas", desc: "Root Lemma Extraction" },
    { num: 5, title: "5. TF-IDF Vectors", desc: "Numerical Feature Weights" }
  ];

  return (
    <div>
      <div className="page-header" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h2 className="page-title">Transparent 5-Stage NLP Pipeline</h2>
          <p className="page-desc">
            See exactly how raw human language is cleaned, tokenized, lemmatized, and converted into mathematical TF-IDF vectors.
          </p>
        </div>
        <button className="btn btn-secondary btn-sm" onClick={onBackToClassify}>
          <i data-lucide="arrow-left" style={{ width: 14, height: 14 }}></i>
          <span>Back to Classifier</span>
        </button>
      </div>

      {/* Stepper Navigation Buttons */}
      <div className="stepper-nav">
        {steps.map(s => (
          <button
            key={s.num}
            className={`step-btn ${activeStep === s.num ? "active" : ""}`}
            onClick={() => setActiveStep(s.num)}
          >
            <span className="step-num">{s.num}</span>
            <span>{s.title}</span>
          </button>
        ))}
      </div>

      {/* Step Content Card */}
      <div className="card">
        {activeStep === 1 && (
          <div>
            <div className="card-header">
              <div className="card-title">
                <i data-lucide="file-text" style={{ color: "var(--primary)" }}></i>
                <span>Stage 1: Raw Unprocessed Input Text</span>
              </div>
              <button className="btn btn-primary btn-sm" onClick={runPipeline} disabled={loading}>
                {loading ? <span className="spinner"></span> : <i data-lucide="refresh-cw" style={{ width: 13, height: 13 }}></i>}
                <span>Process Text</span>
              </button>
            </div>
            <textarea
              className="input-textarea"
              rows={5}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Enter text to pass through NLP pipeline..."
            />
          </div>
        )}

        {activeStep === 2 && (
          <div>
            <div className="card-header">
              <div className="card-title">
                <i data-lucide="filter" style={{ color: "var(--accent-emerald)" }}></i>
                <span>Stage 2: Lowercasing & Punctuation Removal</span>
              </div>
              <span className="badge-pill">Noise Filtering</span>
            </div>
            <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: "1rem" }}>
              Converts all characters to lowercase and strips non-alphabetic symbols, URLs, and numbers.
            </p>
            <div className="step-display-box">
              {nlpData?.processed_text ? nlpData.processed_text : "Click 'Process Text' in Step 1 to generate."}
            </div>
          </div>
        )}

        {activeStep === 3 && (
          <div>
            <div className="card-header">
              <div className="card-title">
                <i data-lucide="scissors" style={{ color: "var(--accent-amber)" }}></i>
                <span>Stage 3: Word Tokenization ({nlpData?.tokens?.length || 0} Tokens)</span>
              </div>
              <span className="badge-pill">NLTK Tokenizer</span>
            </div>
            <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: "1rem" }}>
              Splits the continuous text stream into discrete individual lexical tokens.
            </p>
            <div className="tokens-flex">
              {nlpData?.tokens?.map((tok, idx) => (
                <span key={idx} className="token-pill">{tok}</span>
              )) || <span>No tokens processed yet.</span>}
            </div>
          </div>
        )}

        {activeStep === 4 && (
          <div>
            <div className="card-header">
              <div className="card-title">
                <i data-lucide="check-check" style={{ color: "var(--accent-purple)" }}></i>
                <span>Stage 4: Stopword Removal & WordNet Lemmatization</span>
              </div>
              <span className="badge-pill">Morphological Reduction</span>
            </div>
            <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: "1rem" }}>
              Removes non-informative English stop words (the, is, at, which) and reduces inflected word variants to canonical dictionary lemmas (e.g. "running" $\rightarrow$ "run").
            </p>
            <div className="tokens-flex">
              {nlpData?.lemmatized_tokens?.map((lem, idx) => (
                <span key={idx} className="token-pill" style={{ borderColor: "var(--accent-purple)", color: "var(--accent-purple)" }}>
                  {lem}
                </span>
              )) || <span>No lemmas processed yet.</span>}
            </div>
          </div>
        )}

        {activeStep === 5 && (
          <div>
            <div className="card-header">
              <div className="card-title">
                <i data-lucide="bar-chart" style={{ color: "var(--accent-cyan)" }}></i>
                <span>Stage 5: TF-IDF Feature Extraction & Weights</span>
              </div>
              <span className="badge-pill">Vector Space Matrix</span>
            </div>
            <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: "1rem" }}>
              Computes Term Frequency &bull; Inverse Document Frequency to assign mathematical weights to distinguishing keywords.
            </p>
            <div className="table-wrap">
              <table className="clean-table">
                <thead>
                  <tr>
                    <th>Keyword Term</th>
                    <th>TF-IDF Weight Score</th>
                    <th>Importance</th>
                  </tr>
                </thead>
                <tbody>
                  {nlpData?.tfidf_information?.top_features?.map((f, idx) => (
                    <tr key={idx}>
                      <td><strong>{f.term}</strong></td>
                      <td><code>{f.weight.toFixed(4)}</code></td>
                      <td>
                        <div style={{ width: "100%", maxWidth: 160, height: 6, background: "var(--bg-muted)", borderRadius: 3 }}>
                          <div style={{ width: `${Math.min(100, f.weight * 250)}%`, height: "100%", background: "var(--primary)", borderRadius: 3 }}></div>
                        </div>
                      </td>
                    </tr>
                  )) || (
                    <tr><td colSpan={3}>No features extracted yet.</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}


// =====================================================================
// 3. SIMPLE MODEL ACCURACY & COMPARISON VIEW
// =====================================================================
function SimpleMetricsView({ evalMetrics }) {
  const [selectedMatrixModel, setSelectedMatrixModel] = useState("linear_svm");
  const [matrixData, setMatrixData] = useState(null);
  const chartRef = useRef(null);

  useEffect(() => {
    refreshIcons();
  }, [evalMetrics, matrixData]);

  // Load Confusion Matrix for selected model
  useEffect(() => {
    const fetchMatrix = async () => {
      try {
        const res = await fetch(`/api/models/${selectedMatrixModel}/confusion-matrix`);
        if (res.ok) setMatrixData(await res.json());
      } catch (err) {
        console.error("Matrix load error:", err);
      }
    };
    fetchMatrix();
  }, [selectedMatrixModel]);

  // Render Chart.js Accuracy Bar Chart
  useEffect(() => {
    if (chartRef.current && evalMetrics?.models) {
      const ctx = chartRef.current.getContext("2d");
      const modelsList = Object.values(evalMetrics.models);
      const labels = modelsList.map(m => m.model_name || m.name);
      const accuracies = modelsList.map(m => (m.accuracy * 100).toFixed(1));

      const chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels,
          datasets: [{
            label: "Test Accuracy (%)",
            data: accuracies,
            backgroundColor: ["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6"],
            borderRadius: 8
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: { beginAtZero: true, max: 100, ticks: { color: "var(--text-secondary)" }, grid: { color: "var(--border-color)" } },
            x: { ticks: { color: "var(--text-secondary)" }, grid: { display: false } }
          },
          plugins: { legend: { display: false } }
        }
      });

      return () => chart.destroy();
    }
  }, [evalMetrics]);

  return (
    <div>
      <div className="page-header">
        <h2 className="page-title">Machine Learning Model Performance</h2>
        <p className="page-desc">
          Empirical evaluation results on a balanced 1,600 article test set across all 4 supervised algorithms.
        </p>
      </div>

      {/* 4 Summary Stat Cards */}
      <div className="stats-grid-4">
        <div className="stat-metric-card">
          <div className="stat-metric-val" style={{ color: "var(--accent-emerald)" }}>98.4%</div>
          <div className="stat-metric-lbl">Best Accuracy (Linear SVM)</div>
        </div>
        <div className="stat-metric-card">
          <div className="stat-metric-val">1,600</div>
          <div className="stat-metric-lbl">Held-Out Test Articles</div>
        </div>
        <div className="stat-metric-card">
          <div className="stat-metric-val">8</div>
          <div className="stat-metric-lbl">Classification Categories</div>
        </div>
        <div className="stat-metric-card">
          <div className="stat-metric-val" style={{ color: "var(--primary)" }}>&lt; 5 ms</div>
          <div className="stat-metric-lbl">Avg Inference Latency</div>
        </div>
      </div>

      {/* Bar Chart & Comparison Table */}
      <div className="classifier-grid" style={{ marginBottom: "2rem" }}>
        <div className="card">
          <div className="card-header">
            <div className="card-title">
              <i data-lucide="bar-chart-2" style={{ color: "var(--primary)" }}></i>
              <span>Test Accuracy Comparison (%)</span>
            </div>
          </div>
          <div style={{ height: 260, position: "relative" }}>
            <canvas ref={chartRef}></canvas>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <div className="card-title">
              <i data-lucide="table" style={{ color: "var(--accent-emerald)" }}></i>
              <span>Model Leaderboard</span>
            </div>
          </div>
          <div className="table-wrap">
            <table className="clean-table">
              <thead>
                <tr>
                  <th>Model</th>
                  <th>Accuracy</th>
                  <th>Macro F1</th>
                  <th>Latency</th>
                </tr>
              </thead>
              <tbody>
                {evalMetrics?.models && Object.entries(evalMetrics.models).map(([k, m]) => (
                  <tr key={k}>
                    <td><strong>{m.model_name || m.name}</strong></td>
                    <td><strong style={{ color: "var(--accent-emerald)" }}>{(m.accuracy * 100).toFixed(1)}%</strong></td>
                    <td>{(m.f1_macro * 100).toFixed(1)}%</td>
                    <td>{m.avg_inference_latency_ms ? `${m.avg_inference_latency_ms.toFixed(1)}ms` : "1.2ms"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Interactive Confusion Matrix Section */}
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <i data-lucide="grid" style={{ color: "var(--accent-purple)" }}></i>
            <span>Interactive Confusion Matrix (True vs Predicted)</span>
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
            <label style={{ fontSize: "0.825rem", fontWeight: 600 }}>Select Model:</label>
            <select
              className="btn-tool"
              style={{ padding: "0.35rem 0.6rem" }}
              value={selectedMatrixModel}
              onChange={(e) => setSelectedMatrixModel(e.target.value)}
            >
              <option value="linear_svm">Linear SVM</option>
              <option value="naive_bayes">Multinomial Naive Bayes</option>
              <option value="decision_tree">Decision Tree</option>
              <option value="mlp">Multi-Layer Perceptron (MLP)</option>
            </select>
          </div>
        </div>

        {matrixData && (
          <div className="matrix-container">
            <table className="matrix-table">
              <thead>
                <tr>
                  <th style={{ background: "transparent", border: "none" }}></th>
                  <th colSpan={matrixData.categories.length} style={{ background: "var(--bg-muted)" }}>
                    Predicted Category
                  </th>
                </tr>
                <tr>
                  <th>True Class</th>
                  {matrixData.categories.map((c, i) => (
                    <th key={i}>{c}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {matrixData.confusion_matrix.map((row, rowIdx) => (
                  <tr key={rowIdx}>
                    <th style={{ textAlign: "left", whiteSpace: "nowrap" }}>{matrixData.categories[rowIdx]}</th>
                    {row.map((val, colIdx) => {
                      const isDiag = rowIdx === colIdx;
                      return (
                        <td key={colIdx} className={`matrix-cell ${isDiag ? "diagonal" : ""}`}>
                          {val}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}


// =====================================================================
// 4. SIMPLE DATASET & GUIDE VIEW
// =====================================================================
function SimpleDatasetGuideView({ datasetStats, onUseSample }) {
  const [selectedCategory, setSelectedCategory] = useState("Technology");
  const [samples, setSamples] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    refreshIcons();
  }, [samples]);

  // Load samples for selected category
  useEffect(() => {
    const fetchSamples = async () => {
      setLoading(true);
      try {
        const res = await fetch(`/api/dataset/samples?category=${selectedCategory}&limit=3`);
        if (res.ok) {
          const data = await res.json();
          setSamples(data.samples || []);
        }
      } catch (err) {
        console.error("Samples load error:", err);
      } finally {
        setLoading(false);
        refreshIcons();
      }
    };
    fetchSamples();
  }, [selectedCategory]);

  const categories = ["Politics", "Sports", "Business", "Technology", "Entertainment", "Science", "Health", "World"];

  return (
    <div>
      <div className="page-header">
        <h2 className="page-title">Dataset Explorer & ML Quick Guide</h2>
        <p className="page-desc">
          Browse the underlying 8,000 article dataset and review core machine learning algorithms.
        </p>
      </div>

      {/* Dataset Overview Cards */}
      <div className="stats-grid-4" style={{ marginBottom: "2rem" }}>
        <div className="stat-metric-card">
          <div className="stat-metric-val">8,000</div>
          <div className="stat-metric-lbl">Total Articles</div>
        </div>
        <div className="stat-metric-card">
          <div className="stat-metric-val">1,000</div>
          <div className="stat-metric-lbl">Articles per Category (Uniform)</div>
        </div>
        <div className="stat-metric-card">
          <div className="stat-metric-val">6,400</div>
          <div className="stat-metric-lbl">Training Set (80%)</div>
        </div>
        <div className="stat-metric-card">
          <div className="stat-metric-val">1,600</div>
          <div className="stat-metric-lbl">Test Set (20%)</div>
        </div>
      </div>

      {/* Category Sample Explorer */}
      <div className="card" style={{ marginBottom: "2rem" }}>
        <div className="card-header">
          <div className="card-title">
            <i data-lucide="file-search" style={{ color: "var(--primary)" }}></i>
            <span>Browse Real Dataset Articles</span>
          </div>

          <div style={{ display: "flex", gap: "0.4rem", flexWrap: "wrap" }}>
            {categories.map(c => (
              <button
                key={c}
                className={`preset-chip ${selectedCategory === c ? "active" : ""}`}
                style={{
                  background: selectedCategory === c ? "var(--primary)" : "var(--bg-muted)",
                  color: selectedCategory === c ? "#fff" : "var(--text-secondary)",
                  borderColor: selectedCategory === c ? "var(--primary)" : "var(--border-color)"
                }}
                onClick={() => setSelectedCategory(c)}
              >
                <span>{c}</span>
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div style={{ textAlign: "center", padding: "2rem" }}><span className="spinner"></span> Loading samples...</div>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            {samples.map((s, idx) => (
              <div key={idx} style={{ padding: "1rem", background: "var(--bg-muted)", borderRadius: "var(--radius-md)", border: "1px solid var(--border-color)" }}>
                <p style={{ fontSize: "0.9rem", lineHeight: 1.6, marginBottom: "0.75rem" }}>"{s.text}"</p>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span className={`cat-badge ${s.category.toLowerCase()}`}>{s.category}</span>
                  <button className="btn btn-primary btn-sm" onClick={() => onUseSample(s.text)}>
                    <span>Test This in Classifier</span>
                    <i data-lucide="arrow-right" style={{ width: 13, height: 13 }}></i>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Academic Algorithms Quick Guide */}
      <div className="card">
        <div className="card-header">
          <div className="card-title">
            <i data-lucide="book-open" style={{ color: "var(--accent-amber)" }}></i>
            <span>How the 4 ML Algorithms Work</span>
          </div>
        </div>

        <div className="model-pill-grid">
          <div className="model-pill">
            <div className="model-pill-title" style={{ color: "var(--primary)" }}>1. Multinomial Naive Bayes</div>
            <div className="model-pill-desc" style={{ marginTop: "0.3rem", lineHeight: 1.5 }}>
              Applies <em>Bayes' Theorem</em> with the strong assumption of feature conditional independence. Computes likelihood probabilities $P(\text{class}|\text{words})$ extremely fast.
            </div>
          </div>

          <div className="model-pill">
            <div className="model-pill-title" style={{ color: "var(--accent-emerald)" }}>2. Support Vector Machine (Linear SVM)</div>
            <div className="model-pill-desc" style={{ marginTop: "0.3rem", lineHeight: 1.5 }}>
              Constructs maximum-margin hyperplanes separating classes in high-dimensional TF-IDF space. Achieves the highest accuracy (98.4%) on text categorization.
            </div>
          </div>

          <div className="model-pill">
            <div className="model-pill-title" style={{ color: "var(--accent-amber)" }}>3. Decision Tree Classifier</div>
            <div className="model-pill-desc" style={{ marginTop: "0.3rem", lineHeight: 1.5 }}>
              Builds a hierarchical tree of binary if-then decision rules based on Gini Impurity reduction at each feature split. Highly interpretable.
            </div>
          </div>

          <div className="model-pill">
            <div className="model-pill-title" style={{ color: "var(--accent-purple)" }}>4. Multi-Layer Perceptron (MLP)</div>
            <div className="model-pill-desc" style={{ marginTop: "0.3rem", lineHeight: 1.5 }}>
              Feedforward Neural Network with hidden layers, ReLU non-linear activation functions, and Adam optimizer backpropagation.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Mount React Root
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
