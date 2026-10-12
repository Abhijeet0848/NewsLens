"""
NewsScope - FastAPI backend running on Vercel Python runtime.
Handles /api/classify requests from the Next.js frontend.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import time
import re
from pathlib import Path
from typing import Optional, List, Dict, Any

app = FastAPI(title="NewsScope API")

# CORS - same-domain but keep permissive for preview URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------
# Load models ONCE at module import.
# Vercel caches this between warm invocations.
# ---------------------------------------------
MODEL_DIR = Path(__file__).parent.parent / "models"

print(f"[startup] Loading models from {MODEL_DIR}")

vectorizer = joblib.load(MODEL_DIR / "vectorizer.pkl")
feature_names = vectorizer.get_feature_names_out()

models = {
    "linear-svm": joblib.load(MODEL_DIR / "svm.pkl"),
    "svm": joblib.load(MODEL_DIR / "svm.pkl"),
    "naive-bayes": joblib.load(MODEL_DIR / "nb.pkl"),
    "nb": joblib.load(MODEL_DIR / "nb.pkl"),
    "neural-mlp": joblib.load(MODEL_DIR / "mlp.pkl"),
    "mlp": joblib.load(MODEL_DIR / "mlp.pkl"),
}

le_path = MODEL_DIR / "label_encoder.pkl"
if not le_path.exists():
    le_path = MODEL_DIR / "label_encoder.joblib"

if le_path.exists():
    try:
        le = joblib.load(le_path)
        CLASSES = [str(c).capitalize() for c in le.classes_]
    except Exception:
        CLASSES = ["Business", "Entertainment", "Politics", "Sport", "Tech"]
else:
    CLASSES = ["Business", "Entertainment", "Politics", "Sport", "Tech"]

print(f"[startup] Models loaded. Classes: {CLASSES}")


class ClassifyRequest(BaseModel):
    text: str
    model: str = "linear-svm"


class KeywordItem(BaseModel):
    word: str
    weight: float


class AttentionTokenItem(BaseModel):
    token: str
    weight: float
    isKeyword: bool


class ExplanationItem(BaseModel):
    top_factors: List[str]
    summary: str
    model_version: str
    linguistic_cues: List[str]


class ClassifyResponse(BaseModel):
    category: str
    confidence: float
    confidence_percentage: float
    all_scores: dict
    latency_ms: float
    tokens: int
    tokens_count: int
    model: str
    model_id: str
    keywords: List[KeywordItem]
    explanation: ExplanationItem
    attention_tokens: List[AttentionTokenItem]
    timestamp: str


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "models": list(models.keys()),
        "classes": CLASSES,
    }


@app.post("/api/classify", response_model=ClassifyResponse)
def classify(req: ClassifyRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(400, "Text is required")

    norm_model = req.model.lower().replace("_", "-")
    if norm_model not in models:
        norm_model = "linear-svm"

    clf = models[norm_model]

    t0 = time.perf_counter()
    raw_text = req.text.strip()
    X = vectorizer.transform([raw_text])

    if hasattr(clf, "predict_proba"):
        probs = clf.predict_proba(X)[0]
    elif hasattr(clf, "decision_function"):
        import numpy as np
        df = clf.decision_function(X)[0]
        exp_df = np.exp(df - np.max(df))
        probs = exp_df / np.sum(exp_df)
    else:
        pred_raw = clf.predict(X)[0]
        import numpy as np
        probs = np.zeros(len(CLASSES))
        probs[int(pred_raw) if str(pred_raw).isdigit() else 0] = 1.0

    pred_idx = int(probs.argmax())
    latency = (time.perf_counter() - t0) * 1000

    category_name = CLASSES[pred_idx] if pred_idx < len(CLASSES) else str(clf.classes_[pred_idx])
    confidence_val = float(probs[pred_idx])

    all_scores_dict = {
        (CLASSES[i] if i < len(CLASSES) else str(c)): round(float(p), 4)
        for i, (c, p) in enumerate(zip(clf.classes_, probs))
    }

    # Extract top keywords
    cx = X.tocoo()
    sorted_features = sorted(
        [{"word": str(feature_names[c]), "weight": round(float(v), 4)} for c, v in zip(cx.col, cx.data)],
        key=lambda x: x["weight"],
        reverse=True
    )
    keywords = sorted_features[:8]

    # Attention tokens
    raw_tokens = raw_text.split()[:80]
    kw_words = set(k["word"] for k in keywords)
    attention_tokens = [
        {
            "token": tok,
            "weight": 0.85 if re.sub(r"[^a-zA-Z]", "", tok).lower() in kw_words else 0.15,
            "isKeyword": re.sub(r"[^a-zA-Z]", "", tok).lower() in kw_words
        }
        for tok in raw_tokens
    ]

    model_display_name = (
        "Linear SVM (Calibrated)" if "svm" in norm_model else (
            "Multinomial Naive Bayes" if "nb" in norm_model or "bayes" in norm_model else "Neural MLP"
        )
    )

    return ClassifyResponse(
        category=category_name,
        confidence=round(confidence_val, 4),
        confidence_percentage=round(confidence_val * 100, 1),
        all_scores=all_scores_dict,
        latency_ms=round(latency, 2),
        tokens=int(X.nnz),
        tokens_count=len(raw_text.split()),
        model=req.model,
        model_id=req.model,
        keywords=keywords,
        explanation=ExplanationItem(
            top_factors=[f'Salient term: "{k["word"]}" (weight: {k["weight"]:.3f})' for k in keywords[:5]],
            summary=f"Classified as {category_name} with {confidence_val * 100:.1f}% confidence via {model_display_name}.",
            model_version=model_display_name,
            linguistic_cues=["Corpus alignment: BBC News 5-Class Taxonomy", "Empirical TF-IDF Feature Projection"]
        ),
        attention_tokens=attention_tokens,
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    )


@app.get("/")
def root():
    return {"service": "NewsScope API", "status": "ok"}
