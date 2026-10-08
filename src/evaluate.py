"""
Evaluation Module for NewsSense ML Pipeline
Calculates real performance metrics (Accuracy, Precision, Recall, F1, Confusion Matrix, Classification Report)
using both Macro and Weighted averaging on held-out test data.
Persists evaluation results into machine-readable JSON format.
"""

import json
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


def compute_model_metrics(y_true, y_pred, class_names: list[str]) -> dict:
    """
    Computes standard academic classification metrics on test predictions.
    
    Averaging Method Documentation:
    - Macro Average: Computes the metric independently for each class and then takes the unweighted average.
      Treats all classes equally, penalizing poor performance on minority classes.
    - Weighted Average: Calculates metrics for each class and finds their average weighted by support (number of true instances).
      Accounts for class imbalance.
    """
    accuracy = float(accuracy_score(y_true, y_pred))
    
    # Macro Averaging (unweighted class average)
    precision_macro = float(precision_score(y_true, y_pred, average="macro", zero_division=0))
    recall_macro = float(recall_score(y_true, y_pred, average="macro", zero_division=0))
    f1_macro = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    
    # Weighted Averaging (support-weighted class average)
    precision_weighted = float(precision_score(y_true, y_pred, average="weighted", zero_division=0))
    recall_weighted = float(recall_score(y_true, y_pred, average="weighted", zero_division=0))
    f1_weighted = float(f1_score(y_true, y_pred, average="weighted", zero_division=0))
    
    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred, labels=range(len(class_names)))
    cm_normalized = np.round(cm.astype('float') / np.maximum(cm.sum(axis=1)[:, np.newaxis], 1), 4).tolist()
    
    # Detailed Classification Report
    report_dict = classification_report(
        y_true,
        y_pred,
        target_names=class_names,
        output_dict=True,
        zero_division=0
    )
    report_text = classification_report(
        y_true,
        y_pred,
        target_names=class_names,
        zero_division=0
    )

    # Per-class summary
    per_class = []
    for cat in class_names:
        if cat in report_dict:
            per_class.append({
                "category": cat,
                "precision": round(float(report_dict[cat]["precision"]), 4),
                "recall": round(float(report_dict[cat]["recall"]), 4),
                "f1_score": round(float(report_dict[cat]["f1-score"]), 4),
                "support": int(report_dict[cat]["support"])
            })

    return {
        "accuracy": round(accuracy, 4),
        "precision_macro": round(precision_macro, 4),
        "recall_macro": round(recall_macro, 4),
        "f1_macro": round(f1_macro, 4),
        "precision_weighted": round(precision_weighted, 4),
        "recall_weighted": round(recall_weighted, 4),
        "f1_weighted": round(f1_weighted, 4),
        "averaging_documentation": {
            "macro_average": "Unweighted arithmetic mean across all classes; treats all categories with equal importance.",
            "weighted_average": "Support-weighted mean across all classes; accounts for sample frequency distribution."
        },
        "confusion_matrix": cm.tolist(),
        "confusion_matrix_normalized": cm_normalized,
        "per_class_metrics": per_class,
        "classification_report_dict": report_dict,
        "classification_report_text": report_text
    }


def save_evaluation_results(results: dict, filepath: str):
    """Saves evaluation results dict to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved complete evaluation results to: {filepath}")


def load_evaluation_results(filepath: str) -> dict:
    """Loads evaluation results from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
