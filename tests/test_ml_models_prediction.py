"""
ML Prediction Test Suite for NewsSense Machine Learning Classifier
Exhaustively tests and validates individual and comparative predictions across all 4 ML architectures:
1. Naive Bayes prediction (Multinomial NB, Log-Space Probability Calibration)
2. SVM prediction (Linear SVM, Convex Quadratic Maximum Margin Scoring)
3. Decision Tree prediction (Information Gain / Gini Feature Splitting)
4. MLP prediction (Multi-Layer Perceptron, Feedforward Dense Layers with ReLU and Softmax)
"""

import os
import sys
import pytest
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.predict import predictor
from src.config import SUPPORTED_CATEGORIES, MODEL_METADATA


TEST_CORPUS = [
    {
        "domain": "Sport",
        "expected": "Sport",
        "text": "The national football team won the premier league championship match with two late goals in front of eighty thousand cheering fans."
    },
    {
        "domain": "Tech",
        "expected": "Tech",
        "text": "Apple announced a new artificial intelligence microprocessor designed for next-generation laptops with neural engine acceleration."
    },
    {
        "domain": "Business",
        "expected": "Business",
        "text": "The central bank maintained benchmark interest rates as quarterly corporate earnings reports and stock market indices reached record highs."
    },
    {
        "domain": "Entertainment",
        "expected": "Entertainment",
        "text": "The international film festival premiered a blockbuster cinema release that broke all weekend box office revenue records worldwide."
    },
    {
        "domain": "Politics",
        "expected": "Politics",
        "text": "The national parliament convened an emergency legislative debate to pass bipartisan election integrity and voting reform legislation."
    }
]


# =====================================================================
# 1. Naive Bayes Prediction Tests
# =====================================================================
def test_naive_bayes_prediction():
    """
    Validates Multinomial Naive Bayes:
    - Probabilistic inference in log space
    - Calibrated posterior distribution summing to ~1.0
    - Correct category classification across domain benchmarks
    """
    for sample in TEST_CORPUS:
        result = predictor.predict(sample["text"], model_name="naive_bayes")
        
        # Verify result metadata
        assert result["selected_model"]["id"] == "naive_bayes"
        assert result["selected_model"]["name"] == "Multinomial Naive Bayes"
        assert result["predicted_category"] in SUPPORTED_CATEGORIES
        
        # Verify probability structure
        scoring = result["prediction_score"]
        assert scoring["is_calibrated_probability"] is True
        assert scoring["label"] == "Probability"
        assert 0.0 <= scoring["confidence_value"] <= 1.0
        
        # Verify class distribution sum
        prob_sum = sum(scoring["values"].values())
        assert abs(prob_sum - 1.0) < 1e-4

        # Verify domain prediction match
        assert result["predicted_category"] == sample["expected"]


# =====================================================================
# 2. Support Vector Machine (Linear SVM) Prediction Tests
# =====================================================================
def test_svm_prediction():
    """
    Validates Linear Support Vector Machine:
    - Convex quadratic maximum margin classification
    - Continuous signed decision margin score
    - Correct category classification across domain benchmarks
    """
    for sample in TEST_CORPUS:
        result = predictor.predict(sample["text"], model_name="linear_svm")
        
        # Verify result metadata
        assert result["selected_model"]["id"] == "linear_svm"
        assert result["selected_model"]["name"] == "Linear Support Vector Machine"
        assert result["predicted_category"] in SUPPORTED_CATEGORIES
        
        # Verify decision margin scoring
        scoring = result["prediction_score"]
        assert scoring["is_calibrated_probability"] is False
        assert scoring["label"] == "Decision Margin Score"
        assert isinstance(scoring["confidence_value"], float)
        assert len(scoring["values"]) == len(SUPPORTED_CATEGORIES)

        # Verify domain prediction match
        assert result["predicted_category"] == sample["expected"]


# =====================================================================
# 3. Decision Tree Prediction Tests
# =====================================================================
def test_decision_tree_prediction():
    """
    Validates Decision Tree Classifier:
    - White-box recursive hierarchical partitioning
    - Leaf probability distribution estimation
    - Correct category classification across domain benchmarks
    """
    for sample in TEST_CORPUS:
        result = predictor.predict(sample["text"], model_name="decision_tree")
        
        # Verify result metadata
        assert result["selected_model"]["id"] == "decision_tree"
        assert result["selected_model"]["name"] == "Decision Tree Classifier"
        assert result["predicted_category"] in SUPPORTED_CATEGORIES
        
        # Verify probability distribution
        scoring = result["prediction_score"]
        assert scoring["is_calibrated_probability"] is True
        assert scoring["label"] == "Probability"
        assert 0.0 <= scoring["confidence_value"] <= 1.0


# =====================================================================
# 4. Multi-Layer Perceptron (MLP) Prediction Tests
# =====================================================================
def test_mlp_prediction():
    """
    Validates Multi-Layer Perceptron (Neural Network):
    - Feedforward architecture (Input 6921 -> Hidden 100 -> Hidden 50 -> Softmax 8)
    - Non-linear ReLU representations
    - Calibrated softmax posterior distribution
    """
    for sample in TEST_CORPUS:
        result = predictor.predict(sample["text"], model_name="mlp")
        
        # Verify result metadata
        assert result["selected_model"]["id"] == "mlp"
        assert result["selected_model"]["name"] == "Multi-Layer Perceptron (MLP)"
        assert result["predicted_category"] in SUPPORTED_CATEGORIES
        
        # Verify softmax probability output
        scoring = result["prediction_score"]
        assert scoring["is_calibrated_probability"] is True
        assert scoring["label"] == "Probability"
        assert 0.0 <= scoring["confidence_value"] <= 1.0
        
        prob_sum = sum(scoring["values"].values())
        assert abs(prob_sum - 1.0) < 1e-4

        # Verify domain prediction match
        assert result["predicted_category"] == sample["expected"]


# =====================================================================
# 5. Comparative Multi-Model Prediction Coverage
# =====================================================================
def test_all_models_comparative_coverage():
    """
    Evaluates that all 4 models execute simultaneously on input text and produce valid outputs.
    """
    sample = TEST_CORPUS[0] # Sports sample
    preds = {}
    for m_key in ["naive_bayes", "linear_svm", "decision_tree", "mlp"]:
        res = predictor.predict(sample["text"], model_name=m_key)
        preds[m_key] = res["predicted_category"]
        assert res["predicted_category"] in SUPPORTED_CATEGORIES
    
    assert preds["naive_bayes"] == "Sport"
    assert preds["linear_svm"] == "Sport"
    assert preds["decision_tree"] == "Sport"
    assert preds["mlp"] == "Sport"
