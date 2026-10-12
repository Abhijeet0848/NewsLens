# NewsScope — News Article Classifier

An end-to-end machine learning system that classifies news articles into 5 BBC domains: **Business, Entertainment, Politics, Sport, and Technology**.

**Live Demo:** [https://abhijeetkumar.dpdns.org](https://abhijeetkumar.dpdns.org)  
**Author:** Abhijeet Kumar  
**Guide:** Project Guide, Department of Computer Applications  
**Department:** Computer Applications  
**Academic Year:** 2025–2026  

---

## 📊 Performance

| Model | Accuracy | F1 Macro | Latency |
|-------|----------|----------|---------|
| **Linear SVM** ⭐ | **96.4%** | 0.963 | 1.2 ms |
| Naive Bayes | 92.1% | 0.920 | 0.5 ms |
| Neural MLP | 95.1% | 0.948 | 3.2 ms |
| DistilBERT | 97.8% | 0.976 | 12.4 ms |

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
- 4-model comparison (SVM, NB, MLP, DistilBERT)
- Mobile responsive, dark-mode ready
- Handles edge cases (empty, gibberish, non-English)

## 🚀 Local Setup

```bash
# Clone
git clone https://github.com/Abhijeet0848/NewsLens.git
cd NewsLens

# Install frontend
npm install

# Install backend
pip install -r requirements.txt

# Run frontend
npm run dev

# Run backend (in another terminal)
uvicorn api.index:app --port 8000 --reload
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
