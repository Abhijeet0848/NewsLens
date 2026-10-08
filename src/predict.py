"""
Prediction and Inference Service for NewsSense
Accepts raw article text, applies NLP preprocessing with intermediate step capture,
extracts TF-IDF features, and performs inference using the requested model.
Distinguishes calibrated probabilities from raw decision scores.
"""

import os
import sys
import argparse
import joblib
import numpy as np

# Add parent directory to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.config import (
    VECTORIZER_PATH,
    LABEL_ENCODER_PATH,
    MODEL_PATHS,
    MODEL_METADATA
)
from src.preprocessing import preprocessor


class NewsClassifierPredictor:
    def __init__(self):
        self.vectorizer = None
        self.label_encoder = None
        self.models = {}
        self.is_loaded = False
        self.load_artifacts()

    def load_artifacts(self):
        """Loads serialized TF-IDF vectorizer, label encoder, and trained models."""
        if not os.path.exists(VECTORIZER_PATH) or not os.path.exists(LABEL_ENCODER_PATH):
            raise FileNotFoundError(
                "Model artifacts not found. Please execute training first via 'python src/train.py'."
            )

        self.vectorizer = joblib.load(VECTORIZER_PATH)
        self.label_encoder = joblib.load(LABEL_ENCODER_PATH)

        for model_key, model_path in MODEL_PATHS.items():
            if os.path.exists(model_path):
                self.models[model_key] = joblib.load(model_path)

        if not self.models:
            raise FileNotFoundError("No trained models found in models/ directory.")

        self.is_loaded = True

    def predict(self, raw_text: str, model_name: str = "naive_bayes") -> dict:
        """
        Executes inference on raw text:
        1. Validates input
        2. NLP preprocessing with intermediate outputs
        3. TF-IDF feature transformation
        4. Model prediction
        5. Score / Probability computation
        """
        if not self.is_loaded:
            self.load_artifacts()

        if not raw_text or not raw_text.strip():
            raise ValueError("Input article text cannot be empty.")

        cleaned_check = raw_text.strip()
        if len(cleaned_check.split()) < 3:
            raise ValueError("Article text is too short. Please provide at least 3 words for meaningful NLP analysis.")

        # Normalize model key
        model_key = model_name.lower().replace(" ", "_").replace("-", "_")
        if model_key == "svm":
            model_key = "linear_svm"

        if model_key not in self.models:
            valid_keys = list(self.models.keys())
            raise ValueError(f"Unknown model '{model_name}'. Available models: {valid_keys}")

        model = self.models[model_key]
        meta = MODEL_METADATA.get(model_key, {
            "name": model_key.title(),
            "type": "Supervised Classifier",
            "scoring_type": "score"
        })

        # 1. NLP Preprocessing with intermediate steps
        nlp_intermediate = preprocessor.preprocess_with_intermediate_steps(raw_text)
        processed_str = nlp_intermediate["processed_text"]

        if not processed_str.strip():
            raise ValueError("All words were filtered as stop-words or non-alphabetic tokens. Please provide more descriptive text.")

        # 2. TF-IDF Transformation
        tfidf_vec = self.vectorizer.transform([processed_str])

        # 3. Model Prediction
        pred_idx = int(model.predict(tfidf_vec)[0])
        predicted_category = self.label_encoder.inverse_transform([pred_idx])[0]
        class_names = list(self.label_encoder.classes_)

        # 4. Score / Probability Calculation (Distinguish calibrated probabilities vs raw decision margin)
        score_info = {
            "scoring_metric": meta["scoring_type"],
            "is_calibrated_probability": hasattr(model, "predict_proba"),
            "values": {}
        }

        if hasattr(model, "predict_proba"):
            # Probabilistic models (Naive Bayes, Decision Tree, MLP)
            probs = model.predict_proba(tfidf_vec)[0]
            top_score = float(probs[pred_idx])
            score_info["label"] = "Probability"
            score_info["confidence_value"] = round(top_score, 4)
            score_info["confidence_percentage"] = round(top_score * 100, 2)
            for idx, p in enumerate(probs):
                score_info["values"][class_names[idx]] = round(float(p), 4)
        elif hasattr(model, "decision_function"):
            # Non-probabilistic linear margin model (Linear SVM)
            dec_scores = model.decision_function(tfidf_vec)[0]
            if len(dec_scores.shape) > 0 and len(dec_scores) > 1:
                top_score = float(dec_scores[pred_idx])
                score_info["label"] = "Decision Margin Score"
                score_info["confidence_value"] = round(top_score, 4)
                score_info["confidence_percentage"] = None  # Explicitly do NOT invent a percentage for raw decision margins
                for idx, s in enumerate(dec_scores):
                    score_info["values"][class_names[idx]] = round(float(s), 4)
            else:
                score_info["label"] = "Decision Margin Score"
                score_info["confidence_value"] = round(float(dec_scores), 4)
                score_info["confidence_percentage"] = None
        else:
            score_info["label"] = "Deterministic Prediction"
            score_info["confidence_value"] = 1.0
            score_info["confidence_percentage"] = None

        return {
            "selected_model": {
                "id": model_key,
                "name": meta["name"],
                "type": meta["type"]
            },
            "predicted_category": predicted_category,
            "prediction_score": score_info,
            "intermediate_nlp": nlp_intermediate
        }


# Global instance
predictor = NewsClassifierPredictor()


def predict_article(text: str, model_name: str = "naive_bayes") -> dict:
    """Module-level function for inference."""
    return predictor.predict(text, model_name)


def main():
    parser = argparse.ArgumentParser(description="NewsSense Article Prediction Test Script")
    parser.add_argument(
        "--text",
        type=str,
        default="The Prime Minister addressed parliament on electoral reform and constitutional voting safeguards.",
        help="Raw news article text"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="naive_bayes",
        choices=["naive_bayes", "linear_svm", "decision_tree", "mlp"],
        help="Target classification model"
    )

    args = parser.parse_args()
    print("=" * 70)
    print("                   NEWSSENSE PREDICTION TEST                     ")
    print("=" * 70)
    print(f"Input Text:  {args.text}")
    print(f"Model:       {args.model}\n")

    result = predict_article(args.text, args.model)
    
    print(f"Selected Model:      {result['selected_model']['name']} ({result['selected_model']['type']})")
    print(f"Predicted Category:  {result['predicted_category']}")
    print(f"Score Metric:        {result['prediction_score']['label']}")
    print(f"Confidence Value:    {result['prediction_score']['confidence_value']}")
    if result['prediction_score']['confidence_percentage'] is not None:
        print(f"Confidence Pct:      {result['prediction_score']['confidence_percentage']}%")

    print("\n--- Intermediate NLP Preprocessing Pipeline Output ---")
    nlp = result["intermediate_nlp"]
    print(f"1. Original Text:       {nlp['original_text']}")
    print(f"2. Tokens:              {nlp['tokens']}")
    print(f"3. Without Stopwords:   {nlp['without_stopwords']}")
    print(f"4. Lemmatized Tokens:   {nlp['lemmatized_tokens']}")
    print(f"5. Final Processed:     {nlp['processed_text']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
