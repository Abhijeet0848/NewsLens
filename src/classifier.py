"""
Inference & Prediction Service for NewsSense Academic ML Project
Loads persisted artifacts and provides real-time inference, category probabilities,
top contributing TF-IDF keywords, and step-by-step NLP trace.
"""

import os
import sys
import json
import joblib
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.nlp_pipeline import pipeline
from src.model_trainer import MODELS_DIR, MODEL_CONFIGS

class ModelInferenceService:
    def __init__(self):
        self.vectorizer = None
        self.label_encoder = None
        self.models = {}
        self.metrics = {}
        self.loaded = False
        self.load_artifacts()

    def load_artifacts(self):
        """Loads all serialized artifacts from disk."""
        try:
            vec_path = os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib")
            le_path = os.path.join(MODELS_DIR, "label_encoder.joblib")
            metrics_path = os.path.join(MODELS_DIR, "evaluation_metrics.json")

            if not os.path.exists(vec_path) or not os.path.exists(le_path):
                print("Models not found on disk. Initiating training...")
                from src.model_trainer import train_and_evaluate
                train_and_evaluate()

            self.vectorizer = joblib.load(vec_path)
            self.label_encoder = joblib.load(le_path)

            for model_id in MODEL_CONFIGS.keys():
                model_path = os.path.join(MODELS_DIR, f"{model_id}.joblib")
                if os.path.exists(model_path):
                    self.models[model_id] = joblib.load(model_path)

            if os.path.exists(metrics_path):
                with open(metrics_path, "r", encoding="utf-8") as f:
                    self.metrics = json.load(f)

            self.loaded = True
            print("Successfully loaded vectorizer, label encoder, and models into inference service.")
        except Exception as e:
            print(f"Error loading model artifacts: {e}")
            self.loaded = False

    def predict(self, raw_text: str, model_id: str = "naive_bayes") -> dict:
        """
        Executes complete classification pipeline for a single article:
        1. Validates input
        2. NLP text preprocessing with step capture
        3. TF-IDF feature extraction
        4. Model prediction
        5. Probability / confidence score distribution
        6. Top contributing TF-IDF features
        """
        if not self.loaded:
            self.load_artifacts()
            if not self.loaded:
                raise RuntimeError("Model artifacts are not loaded. Please train models first.")

        if not raw_text or not raw_text.strip():
            raise ValueError("Input article text is empty. Please provide article content to classify.")

        cleaned_check = raw_text.strip()
        if len(cleaned_check.split()) < 3:
            raise ValueError("Article text is too short. Please provide at least 3 words for meaningful NLP analysis.")

        if model_id not in self.models:
            valid_ids = list(self.models.keys())
            raise ValueError(f"Unknown model identifier '{model_id}'. Available models: {valid_ids}")

        # 1. Step-by-step NLP trace
        nlp_trace = pipeline.process_with_steps(raw_text)
        processed_str = nlp_trace["final_processed_text"]

        if not processed_str.strip():
            raise ValueError("All words in the article were filtered out as stop-words or symbols. Please provide more descriptive news text.")

        # 2. TF-IDF Transformation
        tfidf_vec = self.vectorizer.transform([processed_str])
        
        # 3. Extract Top TF-IDF keywords for this document
        feature_names = self.vectorizer.get_feature_names_out()
        cx = tfidf_vec.tocoo()
        tfidf_features = []
        for col, val in zip(cx.col, cx.data):
            tfidf_features.append({
                "word": feature_names[col],
                "tfidf_weight": round(float(val), 4)
            })
        tfidf_features = sorted(tfidf_features, key=lambda x: x["tfidf_weight"], reverse=True)[:15]

        # 4. Model Prediction
        model = self.models[model_id]
        pred_idx = int(model.predict(tfidf_vec)[0])
        predicted_category = self.label_encoder.inverse_transform([pred_idx])[0]

        # 5. Probabilities / Confidence Scores
        class_names = list(self.label_encoder.classes_)
        probabilities = []
        confidence = 0.0

        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(tfidf_vec)[0]
            for idx, prob_val in enumerate(probs):
                cat_name = class_names[idx]
                p = round(float(prob_val), 4)
                probabilities.append({
                    "category": cat_name,
                    "probability": p,
                    "percentage": round(p * 100, 2)
                })
            confidence = round(float(probs[pred_idx]), 4)
        elif hasattr(model, "decision_function"):
            # Normalize decision function outputs via softmax for display
            dec = model.decision_function(tfidf_vec)[0]
            exp_dec = np.exp(dec - np.max(dec))
            softmax_probs = exp_dec / np.sum(exp_dec)
            for idx, prob_val in enumerate(softmax_probs):
                cat_name = class_names[idx]
                p = round(float(prob_val), 4)
                probabilities.append({
                    "category": cat_name,
                    "probability": p,
                    "percentage": round(p * 100, 2)
                })
            confidence = round(float(softmax_probs[pred_idx]), 4)
        else:
            # Fallback uniform pseudo-probability with 1.0 on prediction
            for idx, cat_name in enumerate(class_names):
                p = 1.0 if idx == pred_idx else 0.0
                probabilities.append({
                    "category": cat_name,
                    "probability": p,
                    "percentage": round(p * 100, 2)
                })
            confidence = 1.0

        # Sort probabilities descending
        probabilities = sorted(probabilities, key=lambda x: x["probability"], reverse=True)

        model_meta = MODEL_CONFIGS.get(model_id, {
            "name": model_id.title(),
            "description": "",
            "class_type": "Supervised Classifier"
        })

        return {
            "model_id": model_id,
            "model_name": model_meta["name"],
            "model_type": model_meta["class_type"],
            "predicted_category": predicted_category,
            "confidence_score": confidence,
            "confidence_percentage": round(confidence * 100, 2),
            "probabilities": probabilities,
            "top_tfidf_features": tfidf_features,
            "nlp_pipeline": nlp_trace
        }


# Global singleton inference service
inference_service = ModelInferenceService()
