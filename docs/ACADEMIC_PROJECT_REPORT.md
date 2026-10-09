
# ACADEMIC PROJECT REPORT

## PROJECT TITLE: NewsScope — An Interactive News Article Category Classifier

**Degree:** Master of Computer Applications (MCA)
**Domain:** Natural Language Processing (NLP) & Machine Learning (ML)
**Technology Stack:** Python, FastAPI, Scikit-learn, NLTK, Pandas, NumPy, PyTorch, Hugging Face Transformers, Next.js, TypeScript, Tailwind CSS, Chart.js

---

## 1. ABSTRACT

Automated text categorization is a fundamental task in Information Retrieval and Natural Language Processing. With the rapid expansion of online journalism, manually tagging news articles into categories such as Business, Entertainment, Politics, Sport, and Technology has become increasingly labour-intensive and prone to human error.

This project, **NewsScope**, presents an end-to-end machine learning system that ingests raw news articles, applies a transparent multi-stage NLP preprocessing pipeline, and evaluates multiple supervised classification paradigms on a benchmark corpus. The system implements a five-stage preprocessing workflow — text normalization, tokenization, stop-word removal, WordNet lemmatization, and TF-IDF vectorization — followed by comparative evaluation of four classifiers:

1. **Multinomial Naive Bayes** — Probabilistic Generative
2. **Linear Support Vector Machine (SVM)** — Maximum-Margin Hyperplane
3. **Multi-Layer Perceptron (MLP)** — Feedforward Neural Network
4. **DistilBERT (fine-tuned)** — Transformer-based Deep Learning

All evaluation metrics — Accuracy, Macro Precision, Recall, F1-score, and Confusion Matrices — are computed empirically on a held-out 20% test split of the BBC News corpus, with strict prevention of data leakage. The interactive web interface exposes intermediate NLP representations, probability distributions, and multi-model consensus predictions, providing transparency for both end users and academic evaluation.

---

## 2. PROBLEM STATEMENT & OBJECTIVES

The core objective is to design, implement, and rigorously benchmark an automated classification engine capable of categorizing heterogeneous news texts into **five distinct domains** drawn from the BBC News corpus:

- **Business**
- **Entertainment**
- **Politics**
- **Sport**
- **Technology**

### Key System Objectives

1. **Pipeline Transparency** — Expose every intermediate stage of NLP preprocessing, allowing users to inspect token transformations, filtered stop-words, and lemmatization changes.
2. **Multi-Model Benchmarking** — Train and evaluate multiple supervised algorithms on identical training features, tested on identical held-out data.
3. **Zero Data Leakage** — Ensure the vectorizer vocabulary and IDF weights are learned strictly from the training set and applied to the test set without contamination.
4. **Interactive Dashboard** — Provide real-time classification, probability distribution analysis, confusion matrix heatmaps, and dataset exploration.
5. **Explainability** — Surface keyword saliency and per-class confidence so predictions are not treated as a black box.

---

## 3. LITERATURE REVIEW

News classification has evolved through three distinct eras:

| Era | Approach | Representative Work |
|-----|----------|---------------------|
| **Classical IR** | Bag-of-Words + TF-IDF with linear models | Joachims (1998) — SVMs for text |
| **Statistical ML** | Naive Bayes, Decision Trees, MLPs | Sebastiani (2002) — Text categorization survey |
| **Deep Learning** | RNNs, CNNs, Transformers | Devlin et al. (2019) — BERT; Sanh et al. (2019) — DistilBERT |

**Key findings from the literature:**

- Linear models perform near-optimally on high-dimensional sparse TF-IDF vectors (Joachims, 1998).
- Transformer-based models such as BERT and DistilBERT outperform classical models on complex semantic tasks but require significantly greater computational resources (Devlin et al., 2019).
- The BBC News corpus (Greene & Cunningham, 2006) is a well-established benchmark for multi-class news categorization, with reported accuracies of 96–98% for linear models and higher for fine-tuned transformers.

This project extends the classical pipeline with modern transformer baselines and adds an interactive explainability layer.

---

## 4. SYSTEM ARCHITECTURE

```
+----------------------------+
|     Raw News Article       |
+-------------+--------------+
              |
              v
+----------------------------+
| 1. Text Cleaning           |  Lowercasing, URL/email stripping,
|                            |  punctuation removal, alpha filtering
+-------------+--------------+
              |
              v
+----------------------------+
| 2. Word Tokenization       |  NLTK word_tokenize
+-------------+--------------+
              |
              v
+----------------------------+
| 3. Stop-Word Removal       |  NLTK English corpus
+-------------+--------------+
              |
              v
+----------------------------+
| 4. Lemmatization           |  WordNet Lemmatizer
+-------------+--------------+
              |
              v
+----------------------------+
| 5. TF-IDF Vectorization    |  L2-normalized, unigrams + bigrams
+-------------+--------------+
              |
              +--------------------+-----------------+--------------+
              |                    |                 |              |
              v                    v                 v              v
      +---------------+    +---------------+  +-------------+  +-------------+
      | Multinomial   |    |  Linear SVM   |  |     MLP     |  |  DistilBERT |
      | Naive Bayes   |    |               |  |             |  | (fine-tuned)|
      +-------+-------+    +-------+-------+  +------+------+  +------+------+
              |                    |                 |                |
              +--------------------+-----------------+----------------+
                                   |
                                   v
              +----------------------------------------+
              |  Predicted Category + Confidence       |
              |  Keyword Saliency + Explainability     |
              +----------------------------------------+
```

---

## 5. MATHEMATICAL FOUNDATIONS

### 5.1 TF-IDF Vectorization

Term Frequency–Inverse Document Frequency weight for term t in document d across corpus D:

**TF(t, d) = f(t,d) / Σ(t'∈d) f(t',d)**

**IDF(t, D) = ln( (1 + |D|) / (1 + |{d ∈ D : t ∈ d}|) ) + 1**

**TF-IDF(t, d, D) = TF(t, d) × IDF(t, D)**

Followed by L₂ normalization:

**v̂ = v / ‖v‖₂**

### 5.2 Multinomial Naive Bayes

Posterior probability under conditional independence with Laplace smoothing (α = 0.1):

**P(cₖ | x) ∝ P(cₖ) · ∏ᵢ₌₁ⁿ P(xᵢ | cₖ)^fᵢ**

**θₖᵢ = ( Σ(d∈cₖ) x(d,i) + α ) / ( Σⱼ Σ(d∈cₖ) x(d,j) + α·|V| )**

### 5.3 Linear Support Vector Machine

Primal quadratic programming formulation:

**min(w, b, ξ) ½‖w‖² + C · Σᵢ₌₁ᴺ ξᵢ**

subject to:

**yᵢ(wᵀ·xᵢ + b) ≥ 1 − ξᵢ  ,  ξᵢ ≥ 0**

### 5.4 Multi-Layer Perceptron

Feedforward neural network with ReLU activations and softmax output:

**h⁽¹⁾ = ReLU(W⁽¹⁾·x + b⁽¹⁾)**

**h⁽²⁾ = ReLU(W⁽²⁾·h⁽¹⁾ + b⁽²⁾)**

**ŷₖ = exp(zₖ) / Σⱼ₌₁ᴷ exp(zⱼ)**

Cross-entropy loss:

**ℒ = −Σₖ₌₁ᴷ yₖ · ln(ŷₖ)**

### 5.5 DistilBERT Fine-Tuning

DistilBERT (Sanh et al., 2019) is a distilled version of BERT — 40% smaller, 60% faster, retaining ~97% of BERT's performance. Fine-tuning minimizes cross-entropy over the classification head:

**ℒ_CLS = −(1/N) · Σᵢ₌₁ᴺ log P(yᵢ | CLS(hᵢ))**

where CLS(hᵢ) is the final [CLS] token representation from the last transformer layer.

---

## 6. DATASET

**Source:** BBC News Dataset (Greene & Cunningham, 2006), University College Dublin.

| Attribute | Value |
|-----------|-------|
| Total articles | 2,225 |
| Categories | 5 |
| Train split (80%) | 1,780 |
| Test split (20%) | 445 |
| Average article length | ~2,200 characters |
| Language | English |

**Class distribution:**

| Category | Count |
|----------|-------|
| Sport | 511 |
| Business | 510 |
| Politics | 417 |
| Tech | 401 |
| Entertainment | 386 |
| **Total** | **2,225** |

**Preprocessing pipeline:** lowercasing → URL/email/punctuation stripping → NLTK tokenization → stop-word removal → WordNet lemmatization → TF-IDF vectorization (max 10,000 features, unigrams + bigrams).

---

## 7. EXPERIMENTAL RESULTS

Evaluated on the held-out 20% test split (445 articles, stratified across all 5 classes).

| Model | Paradigm | Accuracy | Macro F1 | Latency |
|-------|----------|----------|----------|---------|
| Multinomial Naive Bayes | Probabilistic Generative | 92.1% | 0.92 | 0.5 ms |
| Linear SVM | Max-Margin Hyperplane | 96.4% | 0.963 | 1.2 ms |
| MLP (128 hidden) | Feedforward Neural Net | 95.1% | 0.948 | 3.2 ms |
| DistilBERT (fine-tuned) | Transformer | **97.8%** | **0.976** | 12.4 ms |

> **Note:** All numbers above must be regenerated from your actual training run. The report should contain only metrics produced by your pipeline — no placeholder or estimated values.

**Observations:**

- Linear SVM achieves near-optimal accuracy on TF-IDF features with sub-millisecond latency, making it ideal for real-time applications.
- DistilBERT achieves the highest accuracy but requires ~10× more inference time and ~100× more training time.
- Naive Bayes serves as a fast, interpretable baseline.
- MLP sits between SVM and DistilBERT in both accuracy and speed.

---

## 8. VIVA VOCE QUESTIONS & MODEL ANSWERS

**Q1. Why is TF-IDF preferred over simple Bag-of-Words for text classification?**
*Answer:* CountVectorizer captures raw frequency, causing frequent domain-generic words ("the", "news") to dominate the feature space. TF-IDF downweights such terms via IDF while emphasizing discriminative keywords, producing a more informative and separable feature representation.

**Q2. How do you prevent data leakage during vectorization?**
*Answer:* The TfidfVectorizer is fit exclusively on the training set, learning the vocabulary and IDF weights only from training samples. The test set is then transformed using the pre-fitted vectorizer. This ensures no test-set information influences training.

**Q3. What is the difference between stemming and lemmatization?**
*Answer:* Stemming applies heuristic affix stripping (e.g., "studies" → "studi"), often producing non-dictionary tokens. Lemmatization uses morphological analysis backed by lexical databases such as WordNet to produce valid dictionary lemmas ("studies" → "study").

**Q4. Why does Linear SVM perform so well on TF-IDF features?**
*Answer:* TF-IDF vectors are high-dimensional (~10,000 features) and sparse. In such spaces, classes are often linearly separable, so a maximum-margin hyperplane achieves excellent generalization without requiring expensive non-linear kernels.

**Q5. Why DistilBERT over BERT?**
*Answer:* DistilBERT retains ~97% of BERT's performance while being 40% smaller and 60% faster, making it practical for interactive web deployment without sacrificing accuracy.

**Q6. How is overfitting mitigated in the MLP?**
*Answer:* Through early stopping on a validation split, L2 weight regularization (or dropout), and limiting hidden-layer capacity. Additionally, TF-IDF's high dimensionality combined with L2 normalization naturally regularizes the input space.

**Q7. What are the limits of this system?**
*Answer:* (1) BBC is a small, well-balanced corpus — real-world news is noisier and skewed; (2) English-only; (3) single-label classification — real articles often span multiple categories; (4) no temporal drift handling — news vocabulary evolves over time.

---

## 9. LIMITATIONS & FUTURE SCOPE

### Current Limitations

- Trained on a single 5-class English corpus (BBC News, 2004–2005)
- Single-label classification only (no multi-label)
- Batch processing limited to CSV format
- No multilingual support
- No active learning or drift detection

### Future Enhancements

1. **Multi-label classification** — allow articles to belong to multiple domains.
2. **Multilingual support** — leverage XLM-RoBERTa for cross-lingual news categorization.
3. **Active learning** — prioritize uncertain samples for human review and retraining.
4. **Real-time ingestion** — RSS/API integration for live news streams.
5. **Attention visualization** — display token-level attention from DistilBERT for deeper explainability.
6. **Model compression** — quantize DistilBERT for edge deployment.

---

## 10. CONCLUSION

**NewsScope** demonstrates a rigorous, transparent, and reproducible NLP pipeline for multi-class news article categorization. By combining classical TF-IDF-based models with a fine-tuned transformer baseline, the project offers both interpretability and state-of-the-art accuracy.

The interactive interface exposes every stage of the pipeline — from raw text to lemmatized tokens, from TF-IDF features to final predictions — enabling academic transparency and viva-ready defence.

The project successfully bridges theory and implementation, delivering:

- A **production-ready classification API** (FastAPI + PyTorch)
- An **interactive dashboard** for real-time inference and analytics
- A **reproducible benchmark** comparing four distinct ML paradigms
- A **transparent NLP pipeline** exposing intermediate representations

---

## 11. REFERENCES

1. Greene, D., & Cunningham, P. (2006). *Practical Solutions to the Problem of Diagonal Dominance in Kernel Document Clustering.* ICML.
2. Joachims, T. (1998). *Text Categorization with Support Vector Machines.* ECML.
3. Sebastiani, F. (2002). *Machine Learning in Automated Text Categorization.* ACM Computing Surveys, 34(1), 1–47.
4. Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* NAACL.
5. Sanh, V., Debut, L., Chaumond, J., & Wolf, T. (2019). *DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter.* arXiv:1910.01108.
6. Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* JMLR, 12, 2825–2830.
7. Bird, S., Klein, E., & Loper, E. (2009). *Natural Language Processing with Python.* O'Reilly Media.

---

## 12. APPENDIX — Project Structure

```
newsscope/
├── app/                    # Next.js 14 routes
│   ├── page.tsx            # Home
│   ├── classifier/         # Real-time classifier
│   ├── batch/              # CSV batch upload
│   ├── analytics/          # Metrics dashboard
│   └── architecture/       # System design & math
├── components/             # UI components
├── lib/                    # Utilities, data loaders
├── data/
│   ├── bbc-news-data.csv   # 2,225-article corpus
│   └── metrics.json        # Real training metrics
├── training/
│   └── train.py            # Reproducible training script
├── api/                    # FastAPI backend
│   └── main.py
└── README.md
```

---

## 📋 Unicode Math Reference (If You Need More)

| Symbol | Meaning | Unicode |
|--------|---------|---------|
| × | multiplication | U+00D7 |
| · | middle dot (product) | U+00B7 |
| ∝ | proportional to | U+221D |
| ∑ | summation | U+2211 |
| ∏ | product | U+220F |
| √ | square root | U+221A |
| ½ | one-half | U+00BD |
| ⁻¹ | superscript -1 | U+207B U+00B9 |
| ᵀ | superscript T (transpose) | U+1D40 |
| ₖ, ᵢ, ⱼ | subscripts | U+2096, U+1D62, U+2C7C |
| ⁽¹⁾ ⁽²⁾ | superscript (1), (2) | U+207D U+00B9 U+207E |
| ‖·‖ | norm | U+2016 |
| ∈ | element of | U+2208 |
| ≥ ≤ | greater/less than or equal | U+2265, U+2264 |
| ≠ | not equal | U+2260 |
| → | arrow | U+2192 |
| ℒ | script L (loss) | U+2112 |
| θ | theta | U+03B8 |
| α | alpha | U+03B1 |
| ξ | xi | U+03BE |
| φ | phi | U+03C6 |
| ŷ | y-hat | U+0177 |

---

