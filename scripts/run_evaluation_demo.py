"""
Model Evaluation Benchmarking Demonstration Script
Loads the empirical evaluation results on 1,600 held-out test articles
and prints the complete evaluation table across all 4 machine learning models.
"""

import os
import sys
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.config import EVALUATION_RESULTS_PATH, SUPPORTED_CATEGORIES, MODEL_METADATA
from src.evaluate import load_evaluation_results


def main():
    if not os.path.exists(EVALUATION_RESULTS_PATH):
        print("Error: evaluation_results.json not found. Please train models first.")
        return

    data = load_evaluation_results(EVALUATION_RESULTS_PATH)
    meta = data.get("metadata", {})
    models = data.get("models", {})

    print("\n" + "=" * 105)
    print("                      NEWSSENSE: MODEL EVALUATION & BENCHMARKING REPORT")
    print("=" * 105)
    print(f"Dataset Split: {meta.get('test_samples', 1600)} Test Articles ({meta.get('test_split_ratio', 0.2)*100:.0f}% held-out test split, 200 per category)")
    print(f"TF-IDF Feature Space: {meta.get('feature_count', 6921)} unigrams and bigrams (Fitted strictly on 6,400 training samples)")
    print("=" * 105)

    # 1. Primary Model Comparison Table
    print(f"{'Model Name':<32} | {'Accuracy':<10} | {'Precision (M)':<14} | {'Recall (M)':<12} | {'F1 (Macro)':<12} | {'F1 (Weighted)':<14}")
    print("-" * 105)

    for m_key, m_info in MODEL_METADATA.items():
        if m_key in models:
            m = models[m_key]
            acc = f"{m['accuracy']*100:.2f}%"
            pm = f"{m['precision_macro']*100:.2f}%"
            rm = f"{m['recall_macro']*100:.2f}%"
            f1m = f"{m['f1_macro']*100:.2f}%"
            f1w = f"{m['f1_weighted']*100:.2f}%"
            print(f"{m_info['name']:<32} | {acc:<10} | {pm:<14} | {rm:<12} | {f1m:<12} | {f1w:<14}")

    print("=" * 105)

    # 2. Confusion Matrix Diagonal TP Summary
    print("\nCONFUSION MATRIX TRUE POSITIVE (TP) DIAGONAL ACCUMULATION (Out of 200 per category):")
    print("-" * 105)
    header = f"{'Category':<16} | " + " | ".join([f"{m_info['name'][:18]:<18}" for m_info in MODEL_METADATA.values()])
    print(header)
    print("-" * 105)

    for idx, cat in enumerate(SUPPORTED_CATEGORIES):
        row_str = f"{cat:<16} | "
        for m_key in MODEL_METADATA.keys():
            cm = models[m_key]["confusion_matrix"]
            tp = cm[idx][idx]
            tp_pct = (tp / 200.0) * 100.0
            row_str += f"{tp:>3}/200 ({tp_pct:5.1f}%)   | "
        print(row_str)

    print("=" * 105)

    # 3. Macro vs Weighted Averaging Formula Reference
    print("\nACADEMIC AVERAGING DEFINITIONS:")
    print("  * Macro Average   : (1/K) * Sum(Metric_k) -> Equal importance to all 8 classes.")
    print("  * Weighted Average: Sum(w_k * Metric_k)   -> Weighted by sample class support.")
    print("  * F1-Score        : 2 * (Precision * Recall) / (Precision + Recall)")
    print("=" * 105 + "\n")


if __name__ == "__main__":
    main()
