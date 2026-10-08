"""
Unit Tests for NewsSense ML Pipeline (Stage 1)
Tests preprocessing, feature extraction, model inference, and intermediate data contracts.
"""

import os
import sys
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.config import DATASET_PATH, SUPPORTED_CATEGORIES, MODEL_PATHS
from src.preprocessing import preprocessor, preprocess_article
from src.train import load_and_validate_dataset, train_models_pipeline
from src.predict import predictor, predict_article


def test_nlp_intermediate_steps_contract():
    """Verify that preprocessing returns all required intermediate dictionary keys."""
    sample_text = "The NASA scientists launched a new deep space orbital satellite into Mars orbit!"
    result = preprocess_article(sample_text)

    assert "original_text" in result
    assert "tokens" in result
    assert "without_stopwords" in result
    assert "lemmatized_tokens" in result
    assert "processed_text" in result

    assert result["original_text"] == sample_text
    assert isinstance(result["tokens"], list)
    assert isinstance(result["without_stopwords"], list)
    assert isinstance(result["lemmatized_tokens"], list)
    assert isinstance(result["processed_text"], str)

    # Stopwords like 'the', 'a', 'into' should not be in without_stopwords
    assert "the" not in result["without_stopwords"]
    assert "into" not in result["without_stopwords"]


def test_text_cleaning_removes_urls_and_symbols():
    raw_text = "Check http://news.com for breaking <b>Politics</b> update! Email: editor@press.org"
    cleaned = preprocessor.clean_text(raw_text)
    assert "http" not in cleaned
    assert "<b>" not in cleaned
    assert "editor@press.org" not in cleaned
    assert "!" not in cleaned


def test_dataset_loading():
    """Ensure dataset loads valid non-empty dataframe with supported categories."""
    df = load_and_validate_dataset(DATASET_PATH)
    assert len(df) > 0
    assert "text" in df.columns
    assert "category" in df.columns
    categories = df["category"].unique().tolist()
    assert len(categories) >= 4


def test_model_training_and_artifacts():
    """Verify that model training pipeline generates valid metrics and artifacts."""
    eval_payload = train_models_pipeline(DATASET_PATH)
    
    assert "models" in eval_payload
    for model_key in ["naive_bayes", "linear_svm", "decision_tree", "mlp"]:
        assert model_key in eval_payload["models"]
        metrics = eval_payload["models"][model_key]
        assert 0.0 <= metrics["accuracy"] <= 1.0
        assert 0.0 <= metrics["f1_macro"] <= 1.0
        assert "confusion_matrix" in metrics
        assert os.path.exists(MODEL_PATHS[model_key])


def test_prediction_all_models():
    """Verify prediction across all 4 models on a representative sample."""
    sample_article = "Premier football league players celebrate dramatic late winner in title race match."
    
    for model_name in ["naive_bayes", "linear_svm", "decision_tree", "mlp"]:
        res = predict_article(sample_article, model_name=model_name)
        assert res["predicted_category"] in SUPPORTED_CATEGORIES
        assert "prediction_score" in res
        assert "intermediate_nlp" in res
        assert res["intermediate_nlp"]["processed_text"] != ""


def test_prediction_error_handling():
    """Test validation and clear error reporting for empty or short text."""
    with pytest.raises(ValueError):
        predict_article("")

    with pytest.raises(ValueError):
        predict_article("hi")

    with pytest.raises(ValueError):
        predict_article("Sample text with enough words", model_name="unsupported_model")
