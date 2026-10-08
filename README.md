# NewsSense – News Article Category Classifier
### MCA Academic Project in Machine Learning & Natural Language Processing

NewsSense is a functional, academic-grade Machine Learning and Natural Language Processing system for multi-class news article categorization. It implements a transparent 5-stage NLP pipeline and trains four distinct supervised classification models.

---

## 🌟 Key Features

1. **8 Configurable News Categories:**
   - Politics, Sports, Business, Technology, Entertainment, Science, Health, World.
2. **4 Supervised ML Models:**
   - **Multinomial Naive Bayes** (Probabilistic Generative)
   - **Support Vector Machine** (Linear SVM with Calibrated Probabilities)
   - **Decision Tree Classifier** (Gini Impurity / Information Gain)
   - **Multi-Layer Perceptron (MLP)** (Feedforward Neural Network with 2 Hidden Layers)
3. **Step-by-Step NLP Pipeline Inspection:**
   - Raw Text $\rightarrow$ Cleaned Text $\rightarrow$ Word Tokenization $\rightarrow$ Stop-Word Removal $\rightarrow$ Lemmatization $\rightarrow$ TF-IDF Feature Extraction.
4. **Transparent Model Evaluation Dashboard:**
   - Accuracy, Precision (Macro/Weighted), Recall, F1-Score, Training Duration, and Inference Latency measured on a held-out 20% test split.
5. **Interactive Confusion Matrix Heatmaps:**
   - Color-coded True vs Predicted contingency grid and per-class precision/recall breakdown.
6. **Academic Transparency & Viva Preparation:**
   - Mathematical formulas and explanations for TF-IDF, Bayes Theorem, SVM Hyperplanes, Decision Tree Entropy, and MLP Backpropagation.

---

## 🚀 Quick Start

### 1. Requirements
Ensure Python 3.10+ is installed along with required packages:
```bash
pip install fastapi uvicorn scikit-learn nltk pandas numpy joblib
```

### 2. Run the Application
Launch the server and interactive UI with a single command:
```bash
python run.py
```
Or start via Uvicorn:
```bash
uvicorn src.api:app --reload --port 8000
```
Open your browser and navigate to: **`http://localhost:8000`**

---

## 📁 Project Structure

```
NewsArticleClassifier/
│
├── data/
│   └── news_dataset.csv            # 600 balanced news articles across 8 categories
│
├── models/
│   ├── tfidf_vectorizer.joblib     # Pre-fitted TF-IDF vectorizer (no data leakage)
│   ├── label_encoder.joblib        # Class label encoder
│   ├── naive_bayes.joblib          # Trained Multinomial Naive Bayes
│   ├── svm.joblib                  # Trained Linear SVM
│   ├── decision_tree.joblib        # Trained Decision Tree
│   ├── mlp.joblib                  # Trained MLP Classifier
│   └── evaluation_metrics.json     # Empirical test evaluation metrics
│
├── src/
│   ├── __init__.py
│   ├── nlp_pipeline.py             # NLP preprocessing with step-by-step trace capture
│   ├── data_loader.py              # Dataset generator and statistics helper
│   ├── model_trainer.py            # Model training & reproducible evaluation script
│   ├── classifier.py               # Real-time inference service with probability distribution
│   └── api.py                      # FastAPI REST API endpoints
│
├── static/
│   ├── index.html                  # Main Single-Page Application interface
│   ├── style.css                   # Responsive dark/light theme CSS design system
│   └── app.js                      # Chart.js visualizations & frontend controller
│
├── docs/
│   └── ACADEMIC_PROJECT_REPORT.md  # Detailed MCA Academic Project Report & Viva Q&A
│
├── run.py                          # Application launcher
└── README.md                       # Project documentation
```

---

## 📊 API Endpoints

- `GET /api/health`: Health status & loaded model checklist.
- `GET /api/dataset/stats`: Total articles, word count distributions, split sizes.
- `GET /api/dataset/samples`: Retrieve sample articles filtered by category.
- `POST /api/nlp/preprocess`: Intermediate NLP step-by-step trace.
- `POST /api/classify`: Single-model prediction with probability distribution and top TF-IDF keywords.
- `POST /api/classify/all-models`: Parallel 4-model consensus evaluation for a given article.
- `GET /api/models/evaluation`: Evaluation benchmark for all models.
- `GET /api/models/confusion-matrix/{model_id}`: Confusion matrix heatmap data.
- `POST /api/models/retrain`: Retrain models dynamically.
