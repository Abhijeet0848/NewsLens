"""
FastAPI Backend Application for NewsSense – News Article Category Classifier
Exposes RESTful endpoints for dataset statistics, NLP preprocessing, model evaluation,
confusion matrices, article classification, and complete end-to-end pipeline analysis.
"""

import os
import sys
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

# Add parent directory to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.config import (
    DATASET_PATH,
    SUPPORTED_CATEGORIES,
    MODEL_METADATA,
    EVALUATION_RESULTS_PATH
)
from src.data_loader import get_dataset_stats, load_dataset
from src.preprocessing import preprocessor
from src.predict import predictor
from src.evaluate import load_evaluation_results

app = FastAPI(
    title="NewsSense API",
    description="MCA Academic Project REST API for News Article Classification & NLP Preprocessing Pipeline",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================================
# Pydantic Request & Response Schemas
# =====================================================================

class TextRequest(BaseModel):
    text: str = Field(..., description="Raw news article text")

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Article text cannot be empty.")
        if len(v.strip().split()) < 3:
            raise ValueError("Article text is too short. Please provide at least 3 words.")
        return v.strip()


class ClassifyRequest(BaseModel):
    text: str = Field(..., description="Raw news article text")
    model: Optional[str] = Field("naive_bayes", description="Target classification model (naive_bayes, linear_svm, decision_tree, mlp)")

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Article text cannot be empty.")
        if len(v.strip().split()) < 3:
            raise ValueError("Article text is too short. Please provide at least 3 words.")
        return v.strip()

    @field_validator("model")
    @classmethod
    def validate_model(cls, v: Optional[str]) -> str:
        norm = v.lower().replace(" ", "_").replace("-", "_") if v else "naive_bayes"
        if norm == "svm":
            norm = "linear_svm"
        valid_models = list(MODEL_METADATA.keys())
        if norm not in valid_models:
            raise ValueError(f"Invalid model '{v}'. Available models: {valid_models}")
        return norm


class AnalyzeRequest(BaseModel):
    text: str = Field(..., description="Raw news article text")
    model: Optional[str] = Field("naive_bayes", description="Primary model to use for prediction")

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Article text cannot be empty.")
        if len(v.strip().split()) < 3:
            raise ValueError("Article text is too short. Please provide at least 3 words.")
        return v.strip()


# =====================================================================
# API Endpoints
# =====================================================================

@app.get("/api/health", summary="Health Check")
def get_health():
    """Returns engine operational status, loaded models, and supported categories."""
    return {
        "status": "healthy",
        "service": "NewsSense Academic Classifier",
        "models_loaded": predictor.is_loaded,
        "available_models": list(MODEL_METADATA.keys()),
        "categories": SUPPORTED_CATEGORIES
    }


@app.get("/api/dataset/stats", summary="Dataset Summary Statistics")
def get_dataset_statistics():
    """Returns corpus metrics, category distribution, word length stats, and split breakdown."""
    try:
        stats = get_dataset_stats()
        if os.path.exists(EVALUATION_RESULTS_PATH):
            eval_data = load_evaluation_results(EVALUATION_RESULTS_PATH)
            if "metadata" in eval_data:
                stats["training_metadata"] = eval_data["metadata"]
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch dataset statistics: {str(e)}")


@app.get("/api/models/evaluation", summary="Model Evaluation Benchmarks")
def get_models_evaluation():
    """Returns empirical evaluation metrics (Accuracy, Precision, Recall, F1, Latency) on held-out test data."""
    if not os.path.exists(EVALUATION_RESULTS_PATH):
        raise HTTPException(status_code=404, detail="Evaluation results not found. Please train models first.")
    
    try:
        return load_evaluation_results(EVALUATION_RESULTS_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load evaluation metrics: {str(e)}")


@app.get("/api/models/{model_name}/confusion-matrix", summary="Confusion Matrix for Specific Model")
def get_model_confusion_matrix(
    model_name: str = Path(..., description="Model identifier (naive_bayes, linear_svm, decision_tree, mlp)")
):
    """Returns the confusion matrix contingency grid, normalized ratios, and per-class metrics for a model."""
    norm_name = model_name.lower().replace(" ", "_").replace("-", "_")
    if norm_name == "svm":
        norm_name = "linear_svm"

    if norm_name not in MODEL_METADATA:
        raise HTTPException(
            status_code=404,
            detail=f"Model '{model_name}' not recognized. Available: {list(MODEL_METADATA.keys())}"
        )

    if not os.path.exists(EVALUATION_RESULTS_PATH):
        raise HTTPException(status_code=404, detail="Evaluation results not found.")

    try:
        eval_data = load_evaluation_results(EVALUATION_RESULTS_PATH)
        models_dict = eval_data.get("models", {})
        
        if norm_name not in models_dict:
            raise HTTPException(status_code=404, detail=f"Evaluation metrics for '{model_name}' not available.")

        model_eval = models_dict[norm_name]
        categories = eval_data.get("metadata", {}).get("categories", SUPPORTED_CATEGORIES)

        return {
            "model_id": norm_name,
            "model_name": model_eval.get("model_name", MODEL_METADATA[norm_name]["name"]),
            "model_type": model_eval.get("model_type", MODEL_METADATA[norm_name]["type"]),
            "categories": categories,
            "accuracy": model_eval["accuracy"],
            "f1_macro": model_eval["f1_macro"],
            "confusion_matrix": model_eval["confusion_matrix"],
            "confusion_matrix_normalized": model_eval.get("confusion_matrix_normalized", []),
            "per_class_metrics": model_eval.get("per_class_metrics", []),
            "classification_report_text": model_eval.get("classification_report_text", "")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve confusion matrix: {str(e)}")


@app.post("/api/article/preprocess", summary="Intermediate NLP Preprocessing & TF-IDF Extraction")
def preprocess_article_endpoint(request: TextRequest):
    """
    Applies the transparent 5-stage NLP pipeline and returns all intermediate artifacts:
    Original Text -> Cleaned Text -> Tokens -> Stopword Removal -> Lemmatization -> TF-IDF Vector
    """
    try:
        if not predictor.is_loaded:
            predictor.load_artifacts()

        # Step-by-step intermediate preprocessing
        nlp_intermediate = preprocessor.preprocess_with_intermediate_steps(request.text)
        processed_str = nlp_intermediate["processed_text"]

        if not processed_str.strip():
            raise HTTPException(
                status_code=400,
                detail="All terms in the article were filtered out as stopwords or non-alphabetic characters."
            )

        # TF-IDF Feature Extraction
        tfidf_vec = predictor.vectorizer.transform([processed_str])
        feature_names = predictor.vectorizer.get_feature_names_out()
        
        cx = tfidf_vec.tocoo()
        active_features = sorted(
            [{"term": feature_names[c], "weight": round(float(v), 4)} for c, v in zip(cx.col, cx.data)],
            key=lambda x: x["weight"],
            reverse=True
        )

        return {
            "original_text": nlp_intermediate["original_text"],
            "tokens": nlp_intermediate["tokens"],
            "stop_word_filtered_tokens": nlp_intermediate["without_stopwords"],
            "lemmatized_tokens": nlp_intermediate["lemmatized_tokens"],
            "processed_text": nlp_intermediate["processed_text"],
            "tfidf_information": {
                "active_features_count": len(active_features),
                "vocabulary_total_size": len(predictor.vectorizer.vocabulary_),
                "vector_dimension": list(tfidf_vec.shape),
                "top_features": active_features[:20]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preprocessing failed: {str(e)}")


@app.post("/api/article/classify", summary="Article Classification")
def classify_article_endpoint(request: ClassifyRequest):
    """
    Classifies an input article using the selected ML model.
    Returns predicted category, model metadata, and honest score/probability output.
    """
    try:
        prediction_result = predictor.predict(request.text, model_name=request.model)
        
        return {
            "model": prediction_result["selected_model"]["name"],
            "model_id": prediction_result["selected_model"]["id"],
            "model_type": prediction_result["selected_model"]["type"],
            "predicted_category": prediction_result["predicted_category"],
            "scoring": {
                "metric": prediction_result["prediction_score"]["label"],
                "value": prediction_result["prediction_score"]["confidence_value"],
                "percentage": prediction_result["prediction_score"]["confidence_percentage"],
                "is_calibrated_probability": prediction_result["prediction_score"]["is_calibrated_probability"],
                "class_scores": prediction_result["prediction_score"]["values"]
            }
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")


@app.post("/api/article/analyze", summary="Complete End-to-End Pipeline Analysis")
def analyze_article_endpoint(request: AnalyzeRequest):
    """
    Executes and returns the complete transparent pipeline:
    Original Text -> Preprocessing Steps -> TF-IDF Vector Extraction -> Classification -> Multi-Model Consensus
    """
    try:
        if not predictor.is_loaded:
            predictor.load_artifacts()

        # 1. NLP Preprocessing
        nlp_intermediate = preprocessor.preprocess_with_intermediate_steps(request.text)
        processed_str = nlp_intermediate["processed_text"]

        if not processed_str.strip():
            raise HTTPException(
                status_code=400,
                detail="All terms in the article were filtered out as stopwords or non-alphabetic characters."
            )

        # 2. TF-IDF Feature Extraction
        tfidf_vec = predictor.vectorizer.transform([processed_str])
        feature_names = predictor.vectorizer.get_feature_names_out()
        cx = tfidf_vec.tocoo()
        tfidf_terms = sorted(
            [{"term": feature_names[c], "weight": round(float(v), 4)} for c, v in zip(cx.col, cx.data)],
            key=lambda x: x["weight"],
            reverse=True
        )

        # 3. Primary Prediction
        primary_pred = predictor.predict(request.text, model_name=request.model or "naive_bayes")

        # 4. Multi-Model Consensus (All 4 models evaluated simultaneously on the same TF-IDF vector)
        multi_model_predictions = {}
        for m_key in MODEL_METADATA.keys():
            res = predictor.predict(request.text, model_name=m_key)
            multi_model_predictions[m_key] = {
                "model_name": res["selected_model"]["name"],
                "model_type": res["selected_model"]["type"],
                "predicted_category": res["predicted_category"],
                "scoring_metric": res["prediction_score"]["label"],
                "score_value": res["prediction_score"]["confidence_value"],
                "confidence_percentage": res["prediction_score"]["confidence_percentage"]
            }

        return {
            "original_text": request.text,
            "preprocessing": {
                "cleaned_text": preprocessor.clean_text(request.text),
                "tokens": nlp_intermediate["tokens"],
                "without_stopwords": nlp_intermediate["without_stopwords"],
                "lemmatized_tokens": nlp_intermediate["lemmatized_tokens"],
                "processed_text": nlp_intermediate["processed_text"]
            },
            "tfidf_representation": {
                "active_features_count": len(tfidf_terms),
                "top_contributing_terms": tfidf_terms[:15],
                "vector_dimension": list(tfidf_vec.shape)
            },
            "primary_prediction": {
                "model_name": primary_pred["selected_model"]["name"],
                "model_type": primary_pred["selected_model"]["type"],
                "predicted_category": primary_pred["predicted_category"],
                "score_info": primary_pred["prediction_score"]
            },
            "multi_model_consensus": multi_model_predictions
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis pipeline failed: {str(e)}")


# Mount static directory for frontend web UI
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/")
    def serve_index():
        index_file = os.path.join(STATIC_DIR, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return JSONResponse({"message": "NewsSense API is running."})
