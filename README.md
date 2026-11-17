# NewsScope — News Article Classifier

An end-to-end machine learning system that classifies news articles into 5 BBC domains: **Business, Entertainment, Politics, Sport, and Technology**.

**Live Demo:** [https://abhijeetkumar.dpdns.org](https://abhijeetkumar.dpdns.org)  
**Google Colab Notebook:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Abhijeet0848/NewsLens/blob/main/notebooks/NewsScope_Classifier.ipynb)  
**Author:** Abhijeet Kumar  
**Guide:** Project Guide, Department of Computer Applications  
**Department:** Computer Applications  
**Academic Year:** 2025–2026  

---

## 📊 Performance

| Model | Paradigm | Accuracy | F1 Macro | Latency | Role |
|-------|----------|----------|----------|---------|------|
| **Linear SVM** ⭐ | Max-Margin Hyperplane | **96.4%** | 0.963 | 1.2 ms | **Production Winner** |
| **Naive Bayes** | Probabilistic Generative | **92.1%** | 0.920 | 0.5 ms | Fast Probabilistic Baseline |
| **Decision Tree** | Rule-Based Flowchart | **83.8%** | 0.835 | 0.8 ms | Interpretable Tree Baseline |

## ✅ Live Test Results

Validated on 5 real news articles after deployment:

| # | Article | Predicted | Confidence |
|---|---------|-----------|------------|
| 1 | Real Madrid wins Champions League | Sport ✅ | 86.1% |
| 2 | Apple unveils M4 chip at WWDC | Tech ✅ | 85.8% |
| 3 | Fed raises interest rates | Business ✅ | 91.3% |
| 4 | Parliament passes Renters Bill | Politics ✅ | 80.0% |
| 5 | Harry Potter TV series announced | Entertainment ✅ | 64.4% |

**Accuracy: 5/5 · Average confidence: 81.5% · Average latency: 3.7 ms**

---

## 🏗️ Architecture

```text
User Input → Next.js Frontend → FastAPI Backend → scikit-learn Model
             (Vercel)            (Vercel)          (TF-IDF + SVM)
```

## 🛠️ Tech Stack

- **Frontend:** Next.js 14, TypeScript, Tailwind CSS, Framer Motion
- **Backend:** FastAPI, scikit-learn, NumPy
- **Model:** TF-IDF (10,000 features) + CalibratedClassifierCV(LinearSVC)
- **Dataset:** BBC News (2,225 articles, 5 categories)
- **Deployment:** Vercel (Python runtime)

## ✨ Features

- Real-time classification with probability distribution
- Top keyword saliency (TF-IDF weights)
- Batch CSV upload for bulk processing
- Analytics dashboard with model comparison
- 3-model comparison (Linear SVM, Naive Bayes, Decision Tree)
- Mobile responsive, dark-mode ready
- Handles edge cases (empty, gibberish, non-English)

## 🚀 Local Setup

```bash
# Clone
git clone https://github.com/Abhijeet0848/NewsScope.git
cd NewsScope

# Install dependencies
npm install
pip install -r requirements.txt

# Run both Backend (FastAPI :8000) and Frontend (Next.js :3000) together
npm run dev

# Or run separately if preferred:
# npm run dev:backend   (FastAPI on http://127.0.0.1:8000)
# npm run dev:frontend  (Next.js on http://localhost:3000)
```

Open [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

```text
newsscope/
├── app/
│   ├── page.tsx               # Homepage
│   ├── classifier/            # Classification UI
│   ├── batch/                 # CSV batch upload
│   ├── analytics/             # Metrics dashboard
│   ├── architecture/          # Model documentation
│   └── api/classify/          # API proxy
├── components/
│   ├── Navbar.tsx
│   ├── ModelSelector.tsx
│   └── ...
├── lib/
│   ├── validateInput.ts       # Input validation
│   └── debug.ts               # Debug utilities
├── api/
│   └── index.py               # FastAPI backend
├── models/
│   ├── vectorizer.pkl         # TF-IDF vectorizer
│   └── svm.pkl                # Trained SVM
├── data/
│   ├── bbc-news-data.csv      # 2,225 articles
│   └── metrics.json           # Real evaluation metrics
├── training/
│   └── train.py               # Reproducible training
├── requirements.txt
├── vercel.json
└── README.md
```

## 📈 Model Training

```bash
python training/train.py
```

Reproduces the model on the BBC dataset with:
- 80/20 train/test split (stratified, random_state=42)
- TF-IDF vectorization (10K features, unigrams + bigrams)
- Zero data leakage (vectorizer fit on train only)
- Calibrated probability outputs

## 📄 License

MIT License

## 🙏 Acknowledgments

- BBC News Dataset (University College Dublin)
- scikit-learn, FastAPI, Next.js, Vercel
