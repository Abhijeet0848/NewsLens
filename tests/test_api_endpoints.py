"""
API Endpoint Test Suite for NewsSense FastAPI Backend
Tests all required GET and POST endpoints, validation schemas, and error responses.
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.api import app

client = TestClient(app)


def test_get_health_endpoint():
    """Test GET /api/health endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["models_loaded"] is True
    assert set(data["available_models"]) == {"naive_bayes", "linear_svm", "decision_tree", "mlp"}
    assert len(data["categories"]) == 8


def test_get_dataset_stats_endpoint():
    """Test GET /api/dataset/stats endpoint."""
    response = client.get("/api/dataset/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_articles"] == 8000
    assert data["total_categories"] == 8
    assert "word_count_stats" in data
    assert "category_distribution" in data


def test_get_models_evaluation_endpoint():
    """Test GET /api/models/evaluation endpoint."""
    response = client.get("/api/models/evaluation")
    assert response.status_code == 200
    data = response.json()
    assert "metadata" in data
    assert "models" in data
    for model_key in ["naive_bayes", "linear_svm", "decision_tree", "mlp"]:
        assert model_key in data["models"]
        m = data["models"][model_key]
        assert "accuracy" in m
        assert "precision_macro" in m
        assert "recall_macro" in m
        assert "f1_macro" in m
        assert "confusion_matrix" in m


def test_get_model_confusion_matrix_endpoint():
    """Test GET /api/models/{model_name}/confusion-matrix endpoint for all 4 models."""
    for model_name in ["naive_bayes", "linear_svm", "decision_tree", "mlp"]:
        response = client.get(f"/api/models/{model_name}/confusion-matrix")
        assert response.status_code == 200
        data = response.json()
        assert data["model_id"] == model_name
        assert "confusion_matrix" in data
        assert len(data["categories"]) == 8
        assert len(data["confusion_matrix"]) == 8
        assert "per_class_metrics" in data

    # Test invalid model name 404
    bad_resp = client.get("/api/models/unknown_model_xyz/confusion-matrix")
    assert bad_resp.status_code == 404


def test_post_article_preprocess_endpoint():
    """Test POST /api/article/preprocess endpoint returning all intermediate stages."""
    article_text = "Apple launched a new artificial intelligence microchip for next generation laptops."
    response = client.post("/api/article/preprocess", json={"text": article_text})
    
    assert response.status_code == 200
    data = response.json()
    assert data["original_text"] == article_text
    assert isinstance(data["tokens"], list)
    assert isinstance(data["stop_word_filtered_tokens"], list)
    assert isinstance(data["lemmatized_tokens"], list)
    assert isinstance(data["processed_text"], str)
    assert "tfidf_information" in data
    assert data["tfidf_information"]["active_features_count"] > 0
    assert len(data["tfidf_information"]["top_features"]) > 0


def test_post_article_classify_endpoint():
    """Test POST /api/article/classify with different models."""
    article_text = "The national football team won the championship match with two late goals."
    
    # Test Naive Bayes (Probabilistic)
    res_nb = client.post("/api/article/classify", json={"text": article_text, "model": "naive_bayes"})
    assert res_nb.status_code == 200
    data_nb = res_nb.json()
    assert data_nb["predicted_category"] == "Sports"
    assert data_nb["scoring"]["is_calibrated_probability"] is True
    assert data_nb["scoring"]["metric"] == "Probability"

    # Test Linear SVM (Decision Score)
    res_svm = client.post("/api/article/classify", json={"text": article_text, "model": "linear_svm"})
    assert res_svm.status_code == 200
    data_svm = res_svm.json()
    assert data_svm["predicted_category"] == "Sports"
    assert data_svm["scoring"]["is_calibrated_probability"] is False
    assert data_svm["scoring"]["metric"] == "Decision Margin Score"


def test_post_article_analyze_endpoint():
    """Test POST /api/article/analyze returning complete pipeline and multi-model consensus."""
    article_text = "Central bank kept benchmark interest rates steady as corporate earnings and stock market indices surged."
    response = client.post("/api/article/analyze", json={"text": article_text, "model": "naive_bayes"})
    
    assert response.status_code == 200
    data = response.json()
    assert "original_text" in data
    assert "preprocessing" in data
    assert "tfidf_representation" in data
    assert "primary_prediction" in data
    assert "multi_model_consensus" in data

    assert data["primary_prediction"]["predicted_category"] == "Business"
    assert len(data["multi_model_consensus"]) == 4


def test_validation_and_error_handling():
    """Test Pydantic validation errors for empty, too short, or invalid inputs."""
    # Empty text
    res_empty = client.post("/api/article/preprocess", json={"text": ""})
    assert res_empty.status_code == 422

    # Too short text (< 3 words)
    res_short = client.post("/api/article/classify", json={"text": "hello world"})
    assert res_short.status_code == 422

    # Invalid model identifier
    res_invalid_model = client.post("/api/article/classify", json={"text": "A valid article with multiple words", "model": "fake_model"})
    assert res_invalid_model.status_code == 422
