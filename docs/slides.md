---
marp: true
theme: default
paginate: true
backgroundColor: #f7f6f3
color: #0f0f0e
style: |
  section {
    font-family: 'Inter', 'Helvetica Neue', sans-serif;
    padding: 60px;
  }
  h1 {
    color: #0f0f0e;
    font-size: 42px;
    font-weight: 700;
  }
  h2 {
    color: #4f46e5;
    font-size: 22px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }
  h3 {
    color: #0f0f0e;
    font-size: 28px;
    font-weight: 600;
  }
  strong {
    color: #4f46e5;
  }
  code {
    background: #f1efeb;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9em;
  }
  pre {
    background: #f1efeb;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e7e3dd;
  }
  table {
    font-size: 20px;
  }
  th {
    background: #4f46e5;
    color: white;
    padding: 12px;
  }
  td {
    padding: 10px 14px;
    border-bottom: 1px solid #e7e3dd;
  }
  section.lead {
    text-align: center;
  }
  section.lead h1 {
    font-size: 64px;
  }
---

<!-- _class: lead -->

# NewsScope
### An Interactive News Article Category Classifier

<br>

**Submitted by:** Abhijeet (NewsLens AI)
**Department of Computer Science & Engineering**
**Academic Year 2024–2025**

---

## Agenda

1. Introduction & Motivation
2. Problem Statement
3. Objectives
4. System Architecture
5. NLP Pipeline
6. Mathematical Foundations
7. Dataset
8. Experimental Results
9. Live Demo
10. Viva Q&A Highlights
11. Limitations & Future Scope
12. Conclusion

---

## Introduction & Motivation

### Why News Classification?
- 📰 **500M+** news articles published daily worldwide
- 🏷️ Manual tagging is **slow**, **inconsistent**, and **not scalable**
- 🎯 Automated classification enables:
  - Personalized feeds
  - Media monitoring
  - Content routing
  - Trend analytics

### The Gap
Most classifiers are **black boxes** — they give a label but no explanation.

### Our Goal
Build a **transparent** classifier that shows *why* it made a decision.

---

## Problem Statement

### The Core Challenge
Design and benchmark an ML system that classifies news articles into **5 domains**:

| Domain | Example Headline |
|--------|------------------|
| Business | "Fed raises interest rates by 0.25%" |
| Entertainment | "New Harry Potter series tops box office" |
| Politics | "Parliament passes landmark climate bill" |
| Sport | "Champions League final ends in penalties" |
| Technology | "Apple unveils new AI chip for iPhone" |

### Requirements
- ✅ High accuracy on held-out test data
- ✅ Fast inference (< 20ms per article)
- ✅ Explainable predictions
- ✅ Zero data leakage

---

## Objectives

### Five Key Objectives

**1. Pipeline Transparency**
Expose every NLP stage — tokenization, stop-word removal, lemmatization, vectorization.

**2. Multi-Model Benchmarking**
Compare Naive Bayes, SVM, MLP, and DistilBERT on identical data.

**3. Zero Data Leakage**
Fit vectorizer ONLY on training set; test set transformed using fitted vocabulary.

**4. Interactive Dashboard**
Real-time classification, probability distributions, confusion matrices.

**5. Explainability**
Keyword saliency + per-class confidence shown for every prediction.

---

## System Architecture

### End-to-End Pipeline

```
┌──────────────────┐
│   Raw Article    │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ 1. Text Cleaning │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ 2. Tokenization  │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ 3. Stop-Words    │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ 4. Lemmatization │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ 5. TF-IDF        │
└────────┬─────────┘
         ↓
┌──────────────────────────────────────┐
│  NB   │   SVM   │   MLP  │ DistilBERT│
└──────────────────────────────────────┘
         ↓
┌──────────────────────────────┐
│ Prediction + Confidence +    │
│ Keyword Saliency             │
└──────────────────────────────┘
```

**Deployment:** FastAPI backend + Next.js frontend

---

## NLP Preprocessing Pipeline

### 5 Stages of Text Transformation

| Stage | Input | Output |
|-------|-------|--------|
| **1. Cleaning** | "Apple's NEW iPhone @ $999!" | "apples new iphone 999" |
| **2. Tokenization** | "apples new iphone 999" | ["apples", "new", "iphone", "999"] |
| **3. Stop-Words** | ["apples", "new", "iphone", "999"] | ["apples", "iphone", "999"] |
| **4. Lemmatization** | ["apples", "iphone", "999"] | ["apple", "iphone", "999"] |
| **5. TF-IDF** | ["apple", "iphone", "999"] | [0.42, 0.61, 0.28, ...] |

### Why This Order Matters
- Cleaning first → fewer tokens
- Stop-word removal → faster processing
- Lemmatization last → reduces vocabulary size

---

## Mathematical Foundations

### Model Equations

**TF-IDF:**
$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$
where $\text{IDF}(t, D) = \ln\left(\frac{1+|D|}{1+\text{df}(t)}\right) + 1$

**Naive Bayes:**
$$P(c_k \mid x) \propto P(c_k) \cdot \prod_{i=1}^n P(x_i \mid c_k)^{f_i} \quad (\text{Laplace smoothing } \alpha = 0.1)$$

**Linear SVM:**
$$\min_{w, b, \xi} \frac{1}{2}\|w\|^2 + C\sum_{i=1}^N \xi_i \quad \text{s.t. } y_i(w^\top x_i + b) \ge 1 - \xi_i$$

**MLP:**
$$h = \text{ReLU}(W_1 x + b_1) \implies \hat{y} = \text{softmax}(W_2 h + b_2)$$

**DistilBERT Attention:**
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^\top}{\sqrt{d_k}}\right) V$$

---

## Dataset

### BBC News Corpus (Greene & Cunningham, 2006)

| Attribute | Value |
|-----------|-------|
| Total articles | 2,225 |
| Categories | 5 |
| Train split | 1,780 (80%) |
| Test split | 445 (20%) |
| Avg. article length | ~2,200 chars |
| Language | English |

### Class Distribution
```
Sport          ████████████████████ 511
Business       ███████████████████  510
Politics       ████████████████     417
Tech           ███████████████      401
Entertainment  ██████████████       386
```

**Preprocessing:** Cleaning → Tokenization → Stop-words → Lemmatization → TF-IDF (10K features, unigrams + bigrams)

---

## Experimental Results

### Model Performance on Test Split (445 articles)

| Model | Accuracy | Macro F1 | Latency |
|-------|----------|----------|---------|
| Naive Bayes | 92.1% | 0.920 | 0.5 ms |
| Linear SVM | 96.4% | 0.963 | 1.2 ms |
| MLP (128) | 95.1% | 0.948 | 3.2 ms |
| **DistilBERT** | **97.8%** | **0.976** | **12.4 ms** |

### Key Findings
- 🥇 **DistilBERT wins on accuracy** — best F1 across all classes
- ⚡ **SVM wins on speed** — 10× faster than DistilBERT
- 🎯 **SVM + TF-IDF** is near-optimal for this corpus
- 📊 **Naive Bayes** is a strong interpretable baseline

**Confusion Matrix Highlights:**
- Sports: 99% precision (distinct vocabulary)
- Politics ↔ Business: 1–2% mutual confusion (overlapping economic terms)

---

## Live Demo

### What We'll Show

**1. Home Page**
Hero + 5-domain taxonomy + sample articles

**2. Classifier Page**
Paste an article → instant prediction
Probability distribution across 5 domains
Keyword saliency highlighting

**3. Batch Upload**
Upload CSV → get predictions for every row
Download results as CSV

**4. Analytics Dashboard**
Metric cards (Accuracy, F1, Precision, Recall)
Confusion matrix heatmap
Model comparison leaderboard

**5. Architecture Page**
System design + mathematical formulas

---

## Limitations & Future Scope

### Current Limitations
- ⚠️ Trained on a small corpus (2,225 articles)
- ⚠️ English-only classification
- ⚠️ Single-label only (real articles can span multiple topics)
- ⚠️ No live news ingestion
- ⚠️ BBC corpus is historical (2004–2005)

### Future Enhancements
- 🔮 **Multi-label** classification
- 🌍 **Multilingual** (XLM-RoBERTa)
- 📡 **Live ingestion** (RSS + streaming APIs)
- 🎯 **Active learning** for uncertain samples
- 👁️ **Attention visualization** from DistilBERT
- 📱 **Model quantization** for edge deployment

---

## Conclusion

### What We Built
✅ An end-to-end ML system for news classification
✅ Transparent 5-stage NLP pipeline
✅ Benchmark of 4 models on identical data
✅ Interactive dashboard with real-time inference
✅ Explainable predictions via keyword saliency

### Key Takeaways
- Linear SVM is **near-optimal** for TF-IDF text features
- DistilBERT gives **+1.4% accuracy** at 10× latency cost
- Transparency + accuracy = **defensible ML system**

### Thank You
*Questions?*

---

## Backup — Viva Q&A

### Anticipated Questions & Answers

**Q: Why TF-IDF over Bag-of-Words?**
A: CountVectorizer lets frequent generic words dominate. TF-IDF downweights them via IDF.

**Q: How do you prevent data leakage?**
A: `TfidfVectorizer` fitted ONLY on training data. Test set transformed with pre-fit vectorizer.

**Q: Why Linear SVM works so well?**
A: TF-IDF vectors are high-dimensional & sparse → classes are linearly separable in 5,000-D space.

**Q: Why DistilBERT over BERT?**
A: 40% smaller, 60% faster, retains 97% of BERT's accuracy.

**Q: What are the main limitations?**
A: English-only, single-label, small corpus, no drift handling.
