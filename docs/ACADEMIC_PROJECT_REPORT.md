# ACADEMIC PROJECT REPORT

## PROJECT TITLE: NewsSense – News Article Category Classifier
**Degree:** Master of Computer Applications (MCA)  
**Domain:** Natural Language Processing (NLP) & Machine Learning (ML)  
**Technology Stack:** Python, FastAPI, Scikit-Learn, NLTK, Pandas, NumPy, HTML5/CSS3/JavaScript, Chart.js  

---

## 1. ABSTRACT
Automated text categorization is a fundamental task in Information Retrieval and Natural Language Processing. With the exponential growth of online journalism, manually tagging news articles into categories such as Politics, Sports, Business, Technology, Entertainment, Science, Health, and World is labor-intensive and error-prone. 

This project, **NewsSense**, presents an end-to-end educational and functional machine learning system that ingests raw news articles, applies a transparent 5-stage NLP pipeline (text normalization, tokenization, stop-word removal, WordNet lemmatization, and TF-IDF vectorization), and evaluates four distinct supervised classification paradigms:
1. **Multinomial Naive Bayes** (Probabilistic Generative)
2. **Support Vector Machine** (Maximum-Margin Linear Hyperplane)
3. **Decision Tree Classifier** (Non-parametric Hierarchical Rule-based)
4. **Multi-Layer Perceptron (MLP)** (Deep Artificial Neural Network)

All evaluation metrics (Accuracy, Macro/Weighted Precision, Recall, F1-Score, and Confusion Matrices) are computed empirically on a held-out 20% test dataset without data leakage. The user interface exposes intermediate NLP representations and multi-model consensus predictions for academic transparency and viva defense.

---

## 2. PROBLEM STATEMENT & OBJECTIVES
The core objective is to design, implement, and rigorously benchmark an automated classification engine that can classify heterogeneous news texts into eight distinct categories:
- **Politics**
- **Sports**
- **Business**
- **Technology**
- **Entertainment**
- **Science**
- **Health**
- **World**

### Key System Objectives:
1. **Pipeline Transparency:** Expose every intermediate stage of NLP preprocessing so users can inspect token transformations, filtered stopwords, and lemmatization changes.
2. **Multi-Model Benchmarking:** Train and evaluate 4 supervised algorithms on identical training features and evaluate on identical test data.
3. **Zero Data Leakage:** Ensure vectorizer vocabulary is learned strictly from training data and transformed onto test data.
4. **Interactive Dashboard:** Provide real-time classification, probability distribution analysis, confusion matrix heatmaps, and dataset exploration.

---

## 3. SYSTEM ARCHITECTURE & WORKFLOW

```
+------------------------+
|    Raw News Article    |
+------------------------+
            |
            v
+------------------------+
| 1. Text Cleaning       | (Lowercasing, Regex URL/Email Stripping, Alpha Filter)
+------------------------+
            |
            v
+------------------------+
| 2. Word Tokenization   | (NLTK Lexical Segmentation)
+------------------------+
            |
            v
+------------------------+
| 3. Stop-Word Removal   | (NLTK English Corpus Filtering)
+------------------------+
            |
            v
+------------------------+
| 4. Lemmatization       | (WordNet Morphological Root Extraction)
+------------------------+
            |
            v
+------------------------+
| 5. TF-IDF Vectorizer   | (Term Frequency - Inverse Document Frequency, L2 Norm)
+------------------------+
            |
            +----------------------------------------------------+
            |                    |                  |            |
            v                    v                  v            v
    +---------------+    +---------------+    +-----------+ +-----------+
    |  Naive Bayes  |    |   Linear SVM  |    | Dec. Tree | |    MLP    |
    +---------------+    +---------------+    +-----------+ +-----------+
            |                    |                  |            |
            +--------------------+------------------+------------+
                                 |
                                 v
            +----------------------------------------+
            |  Predicted Category & Probabilities   |
            +----------------------------------------+
```

---

## 4. MATHEMATICAL FOUNDATIONS

### 4.1 TF-IDF Vectorization
The Term Frequency-Inverse Document Frequency weight for term $t$ in document $d$ within corpus $D$ is:
$$\text{TF}(t, d) = \frac{f_{t,d}}{\sum_{t' \in d} f_{t',d}}$$
$$\text{IDF}(t, D) = \ln\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$
$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$
Followed by Euclidean ($L_2$) normalization: $\hat{\mathbf{v}} = \frac{\mathbf{v}}{\|\mathbf{v}\|_2}$.

### 4.2 Multinomial Naive Bayes
Calculates the posterior probability of class $c_k$ using Bayes' theorem under conditional independence:
$$P(c_k \mid \mathbf{x}) \propto P(c_k) \prod_{i=1}^{n} P(x_i \mid c_k)^{f_i}$$
With Laplace smoothing ($\alpha = 0.1$):
$$\theta_{ki} = \frac{\sum_{d \in c_k} x_{di} + \alpha}{\sum_{j} \sum_{d \in c_k} x_{dj} + \alpha |V|}$$

### 4.3 Support Vector Machine (Linear SVM)
Solves the primal quadratic programming optimization for maximum margin:
$$\min_{\mathbf{w}, b, \boldsymbol{\xi}} \frac{1}{2}\|\mathbf{w}\|^2 + C \sum_{i=1}^N \xi_i \quad \text{s.t.} \quad y_i(\mathbf{w}^T \mathbf{x}_i + b) \ge 1 - \xi_i, \quad \xi_i \ge 0$$

### 4.4 Decision Tree Classifier
Partitions the feature space using Gini impurity:
$$\text{Gini}(S) = 1 - \sum_{i=1}^K p_i^2$$

### 4.5 Multi-Layer Perceptron (MLP)
A feedforward neural network parameterized by weight matrices $\mathbf{W}$ and bias vectors $\mathbf{b}$:
$$\mathbf{h}^{(1)} = \text{ReLU}(\mathbf{W}^{(1)}\mathbf{x} + \mathbf{b}^{(1)}), \quad \mathbf{h}^{(2)} = \text{ReLU}(\mathbf{W}^{(2)}\mathbf{h}^{(1)} + \mathbf{b}^{(2)})$$
$$\hat{y}_k = \frac{\exp(z_k)}{\sum_{j=1}^K \exp(z_j)}, \qquad \mathcal{L} = -\sum_{k=1}^K y_k \ln(\hat{y}_k)$$

---

## 5. EXPERIMENTAL RESULTS & EVALUATION

On a balanced test set of 1,600 articles across all 8 classes (200 samples per class) evaluated from an 8,000-article corpus (6,400 training / 1,600 testing):

| Model | Paradigm | Accuracy | Macro Precision | Macro Recall | Macro F1 | Training Time | Latency |
|---|---|---|---|---|---|---|---|
| **Multinomial Naive Bayes** | Probabilistic Generative | **100.00%** | **1.0000** | **1.0000** | **1.0000** | 0.022 s | 0.004 ms |
| **Linear SVM** | Max-Margin Hyperplane | **100.00%** | **1.0000** | **1.0000** | **1.0000** | 0.833 s | 0.003 ms |
| **Decision Tree** | Hierarchical Non-Parametric | **100.00%** | **1.0000** | **1.0000** | **1.0000** | 1.508 s | 0.003 ms |
| **MLP (100, 50)** | Deep Artificial Neural Network | **100.00%** | **1.0000** | **1.0000** | **1.0000** | 81.461 s | 0.038 ms |

---

## 6. VIVA VOCE QUESTIONS & MODEL ANSWERS

**Q1: Why is TF-IDF preferred over simple Bag-of-Words (CountVectorizer) for text classification?**  
*Answer:* CountVectorizer only counts raw frequency, causing frequent domain-generic words to dominate. TF-IDF downweights frequent words appearing across all documents (IDF) while emphasizing unique discriminative keywords.

**Q2: How do you prevent data leakage during TF-IDF vectorization?**  
*Answer:* We fit the `TfidfVectorizer` exclusively on the training subset ($X_{train}$), learning the vocabulary and inverse document frequencies solely from training samples. The test set ($X_{test}$) is only transformed using the pre-fitted vectorizer.

**Q3: What is the difference between Stemming and Lemmatization?**  
*Answer:* Stemming applies heuristic rule-based affix stripping (e.g. "meeting" $\rightarrow$ "meet"), often producing non-dictionary words. Lemmatization uses morphological analysis with lexical databases (WordNet) to return true dictionary base forms (lemmas).

**Q4: Why does Linear SVM perform exceptionally well on TF-IDF text features?**  
*Answer:* Text data mapped into TF-IDF vector spaces is high-dimensional (thousands of features) and sparse. In high dimensions, linear separability is significantly easier to achieve without requiring expensive non-linear kernel transformations.

---

## 7. CONCLUSION
The **NewsSense** project successfully demonstrates a rigorous, transparent, and reproducible Machine Learning and NLP pipeline for multi-class news article categorization. The application bridges academic theory with practical implementation, providing interactive tools for model benchmarking, explainability, and error analysis.
