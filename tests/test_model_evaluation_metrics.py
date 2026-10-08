"""
Evaluation Metrics Test Suite for NewsSense ML System
Tests and validates statistical evaluation metrics:
1. Accuracy (Overall ratio of correct classifications on held-out test data)
2. Precision (Macro-averaged and Weighted-averaged)
3. Recall (Macro-averaged and Weighted-averaged)
4. F1-Score (Harmonic mean of precision and recall)
5. Confusion Matrix (8x8 matrix dimensions, diagonal TP dominance, row sum support conservation)
"""

import os
import sys
import pytest
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.config import EVALUATION_RESULTS_PATH, SUPPORTED_CATEGORIES, MODEL_METADATA
from src.evaluate import load_evaluation_results, compute_model_metrics


@pytest.fixture(scope="module")
def eval_data():
    """Loads serialized evaluation results on 1,600 held-out test articles."""
    assert os.path.exists(EVALUATION_RESULTS_PATH), "evaluation_results.json not found on disk"
    data = load_evaluation_results(EVALUATION_RESULTS_PATH)
    return data


# =====================================================================
# 1. Accuracy Tests
# =====================================================================
def test_evaluation_accuracy(eval_data):
    """
    Validates accuracy computation:
    - Values are bounded in [0.0, 1.0]
    - Accurate calculation from confusion matrix diagonal: sum(diag) / sum(total)
    """
    models = eval_data["models"]
    for model_key in MODEL_METADATA.keys():
        assert model_key in models
        m = models[model_key]
        
        acc = m["accuracy"]
        assert 0.0 <= acc <= 1.0, f"Accuracy {acc} out of range for {model_key}"
        
        # Verify accuracy against raw confusion matrix
        cm = np.array(m["confusion_matrix"])
        computed_acc = float(np.trace(cm) / np.sum(cm))
        assert np.isclose(acc, round(computed_acc, 4), atol=1e-3), f"Accuracy mismatch in {model_key}"


# =====================================================================
# 2. Precision Tests (Macro & Weighted)
# =====================================================================
def test_evaluation_precision(eval_data):
    """
    Validates Precision metrics:
    - Precision = TP / (TP + FP)
    - Macro precision: unweighted mean across all 8 classes
    - Weighted precision: sample-weighted mean across all 8 classes
    """
    models = eval_data["models"]
    for model_key in MODEL_METADATA.keys():
        m = models[model_key]
        
        p_macro = m["precision_macro"]
        p_weighted = m["precision_weighted"]
        
        assert 0.0 <= p_macro <= 1.0
        assert 0.0 <= p_weighted <= 1.0

        # Verify from per-class metrics
        per_class_precisions = [cls["precision"] for cls in m["per_class_metrics"]]
        assert len(per_class_precisions) == len(SUPPORTED_CATEGORIES)
        calculated_macro = float(np.mean(per_class_precisions))
        assert np.isclose(p_macro, round(calculated_macro, 4), atol=1e-2)


# =====================================================================
# 3. Recall Tests (Macro & Weighted)
# =====================================================================
def test_evaluation_recall(eval_data):
    """
    Validates Recall metrics:
    - Recall = TP / (TP + FN)
    - Macro recall: unweighted mean across all 8 classes
    - Weighted recall: sample-weighted mean across all 8 classes
    """
    models = eval_data["models"]
    for model_key in MODEL_METADATA.keys():
        m = models[model_key]
        
        r_macro = m["recall_macro"]
        r_weighted = m["recall_weighted"]
        
        assert 0.0 <= r_macro <= 1.0
        assert 0.0 <= r_weighted <= 1.0

        # Verify from per-class metrics
        per_class_recalls = [cls["recall"] for cls in m["per_class_metrics"]]
        assert len(per_class_recalls) == len(SUPPORTED_CATEGORIES)
        calculated_macro = float(np.mean(per_class_recalls))
        assert np.isclose(r_macro, round(calculated_macro, 4), atol=1e-2)


# =====================================================================
# 4. F1-Score Tests (Macro & Weighted)
# =====================================================================
def test_evaluation_f1_score(eval_data):
    """
    Validates F1-Score metrics:
    - Harmonic Mean: F1 = 2 * (Precision * Recall) / (Precision + Recall)
    - Macro F1 and Weighted F1 properties
    """
    models = eval_data["models"]
    for model_key in MODEL_METADATA.keys():
        m = models[model_key]
        
        f1_macro = m["f1_macro"]
        f1_weighted = m["f1_weighted"]
        
        assert 0.0 <= f1_macro <= 1.0
        assert 0.0 <= f1_weighted <= 1.0

        # Verify from per-class metrics
        per_class_f1s = [cls["f1_score"] for cls in m["per_class_metrics"]]
        assert len(per_class_f1s) == len(SUPPORTED_CATEGORIES)
        calculated_macro = float(np.mean(per_class_f1s))
        assert np.isclose(f1_macro, round(calculated_macro, 4), atol=1e-2)


# =====================================================================
# 5. Confusion Matrix Tests
# =====================================================================
def test_evaluation_confusion_matrix(eval_data):
    """
    Validates Confusion Matrix:
    - Dimension is strictly 8x8 (corresponding to all 8 news domains)
    - Row sums equal test support per class (1,600 / 8 = 200 per category)
    - Normalized confusion matrix row sums equal 1.0
    - Non-negative integer counts
    """
    models = eval_data["models"]
    for model_key in MODEL_METADATA.keys():
        m = models[model_key]
        
        cm = np.array(m["confusion_matrix"])
        cm_norm = np.array(m["confusion_matrix_normalized"])
        
        # 1. 8x8 dimension
        assert cm.shape == (8, 8), f"Expected (8, 8) confusion matrix, got {cm.shape}"
        assert cm_norm.shape == (8, 8)
        
        # 2. Total test samples conservation
        total_test_samples = int(np.sum(cm))
        assert total_test_samples == 1600, f"Expected 1600 test samples, got {total_test_samples}"
        
        # 3. Stratified test row balance (200 test samples per category)
        row_sums = np.sum(cm, axis=1)
        for r_sum in row_sums:
            assert r_sum == 200, f"Row support mismatch: expected 200, got {r_sum}"
            
        # 4. Normalized row sums ~1.0
        norm_row_sums = np.sum(cm_norm, axis=1)
        for nr_sum in norm_row_sums:
            assert np.isclose(nr_sum, 1.0, atol=1e-2)
