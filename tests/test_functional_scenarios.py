"""
Functional Test Suite for NewsSense Machine Learning Classifier
Exhaustively tests real-world edge cases and functional scenarios:
1. Empty article
2. Very short article (< 3 words)
3. Normal article (Standard news length)
4. Long article (Multi-paragraph 500+ words)
5. Invalid model identifier
6. API unavailable / degraded service simulation
7. Missing model artifact handling
8. Missing dataset handling
"""

import os
import sys
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.api import app
from src.predict import NewsClassifierPredictor, predictor
from src.data_loader import ensure_large_dataset_exists, load_dataset, DATASET_PATH
import pandas as pd

client = TestClient(app)


# =====================================================================
# Scenario 1: Empty Article
# =====================================================================
def test_scenario_1_empty_article():
    """Validates that empty strings, whitespace-only, and blank bodies are rejected with HTTP 422."""
    empty_payloads = [
        {"text": ""},
        {"text": "   "},
        {"text": "\t\n  \r\n"}
    ]
    for payload in empty_payloads:
        # Preprocess endpoint
        res_prep = client.post("/api/article/preprocess", json=payload)
        assert res_prep.status_code == 422, f"Failed on preprocess with payload {payload}"
        
        # Classify endpoint
        res_class = client.post("/api/article/classify", json={**payload, "model": "naive_bayes"})
        assert res_class.status_code == 422, f"Failed on classify with payload {payload}"
        
        # Analyze endpoint
        res_ana = client.post("/api/article/analyze", json=payload)
        assert res_ana.status_code == 422, f"Failed on analyze with payload {payload}"

    # Engine direct call validation
    with pytest.raises(ValueError, match="cannot be empty"):
        predictor.predict("", model_name="naive_bayes")


# =====================================================================
# Scenario 2: Very Short Article
# =====================================================================
def test_scenario_2_very_short_article():
    """Validates boundary handling: < 3 words rejected; 3-4 word minimal valid queries processed."""
    # Sub-boundary: 1 or 2 words (Rejected by validation)
    short_rejected = ["Hello", "AI chip"]
    for text in short_rejected:
        res = client.post("/api/article/classify", json={"text": text, "model": "naive_bayes"})
        assert res.status_code == 422
        assert "at least 3 words" in res.text

    # Boundary: Minimal valid 3-word article (Accepted and processed)
    minimal_valid = "Apple processor chip"
    res_min = client.post("/api/article/classify", json={"text": minimal_valid, "model": "naive_bayes"})
    assert res_min.status_code == 200
    data = res_min.json()
    assert "predicted_category" in data
    assert data["predicted_category"] in ["Technology", "Science", "Business"]


# =====================================================================
# Scenario 3: Normal Article
# =====================================================================
def test_scenario_3_normal_article():
    """Validates standard 30-100 word news articles across all 4 machine learning models."""
    normal_article = (
        "The national football team secured victory in the premier championship final today. "
        "The head coach praised the striker for scoring two remarkable second-half goals "
        "in front of eighty thousand cheering fans at the national stadium."
    )
    
    # 1. Test complete pipeline analysis
    res_ana = client.post("/api/article/analyze", json={"text": normal_article, "model": "linear_svm"})
    assert res_ana.status_code == 200
    data_ana = res_ana.json()
    assert data_ana["primary_prediction"]["predicted_category"] == "Sports"
    assert len(data_ana["multi_model_consensus"]) == 4
    
    # 2. Test each individual model on the normal article
    for model_key in ["naive_bayes", "linear_svm", "decision_tree", "mlp"]:
        res_clf = client.post("/api/article/classify", json={"text": normal_article, "model": model_key})
        assert res_clf.status_code == 200
        data_clf = res_clf.json()
        assert data_clf["predicted_category"] == "Sports"
        assert data_clf["scoring"]["value"] is not None


# =====================================================================
# Scenario 4: Long Article (Multi-paragraph 500+ words)
# =====================================================================
def test_scenario_4_long_article():
    """Validates high-volume multi-paragraph text with diverse vocabulary."""
    long_paragraph = (
        "The global aerospace and space exploration agency announced an ambitious deep space astrophysics mission "
        "designed to deploy advanced infrared space telescope instrumentation into lunar orbit. International "
        "physicists, planetary researchers, and space engineers convened at the science convention to outline "
        "plans for observing distant exoplanets, gravitational radiation, and cosmological quantum phenomena. "
        "The scientific payload incorporates high-resolution spectrographs, cryogenic thermal radiation shields, "
        "and quantum computational processors to process galactic telemetry signals in real-time. "
    )
    # Replicate to create a 600+ word multi-paragraph document
    long_article = "\n\n".join([long_paragraph] * 8)
    assert len(long_article.split()) > 500

    res = client.post("/api/article/analyze", json={"text": long_article, "model": "linear_svm"})
    assert res.status_code == 200
    data = res.json()
    assert data["primary_prediction"]["predicted_category"] == "Science"
    assert len(data["preprocessing"]["tokens"]) > 300
    assert data["tfidf_representation"]["active_features_count"] > 10
    assert len(data["multi_model_consensus"]) == 4


# =====================================================================
# Scenario 5: Invalid Model Identifier
# =====================================================================
def test_scenario_5_invalid_model():
    """Validates that invalid or unsupported model keys return HTTP 422 with descriptive error."""
    invalid_models = ["random_forest", "gpt4", "xgboost_v2", "deep_seek"]
    article = "The federal reserve announced interest rate cuts following economic inflation reports."
    
    for bad_model in invalid_models:
        res = client.post("/api/article/classify", json={"text": article, "model": bad_model})
        assert res.status_code == 422
        assert "Invalid model" in res.text or "Available models" in res.text

    # Confusion matrix endpoint invalid model returns 404
    res_cm = client.get("/api/models/invalid_model_xyz/confusion-matrix")
    assert res_cm.status_code == 404


# =====================================================================
# Scenario 6: API Unavailable / Degraded Simulation
# =====================================================================
def test_scenario_6_api_unavailable_simulation():
    """Simulates API service disruption / unhandled server error and health check response."""
    # 1. Health check returns models loaded status
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"

    # 2. Simulate internal predictor failure during analysis
    with patch.object(predictor, 'predict', side_effect=RuntimeError("ML Inference Engine memory allocation failure")):
        res_error = client.post("/api/article/classify", json={
            "text": "Stock markets rose sharply following quarterly earnings announcements.",
            "model": "naive_bayes"
        })
        assert res_error.status_code == 500
        assert "ML Inference Engine memory allocation failure" in res_error.json()["detail"]


# =====================================================================
# Scenario 7: Missing Model Artifact Handling
# =====================================================================
def test_scenario_7_missing_model_artifact():
    """Validates that missing model files raise FileNotFoundError with actionable instructions."""
    temp_predictor = NewsClassifierPredictor.__new__(NewsClassifierPredictor)
    temp_predictor.vectorizer = None
    temp_predictor.label_encoder = None
    temp_predictor.models = {}
    temp_predictor.is_loaded = False

    # Simulate missing vectorizer path
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError, match="Model artifacts not found"):
            temp_predictor.load_artifacts()


# =====================================================================
# Scenario 8: Missing Dataset Handling
# =====================================================================
def test_scenario_8_missing_dataset_handling(tmp_path):
    """Validates that if dataset is missing, data loader regenerates/handles missing CSV gracefully."""
    fake_csv = os.path.join(tmp_path, "missing_news.csv")
    
    # Check that ensure_large_dataset_exists generates a clean valid CSV when missing
    with patch("src.data_loader.DATASET_PATH", fake_csv):
        created_path = ensure_large_dataset_exists(target_samples=16)
        assert os.path.exists(created_path)
        df = pd.read_csv(created_path)
        assert len(df) == 16
        assert "text" in df.columns
        assert "category" in df.columns
