"""
ML Models Prediction Demonstration Script
Runs predictions across Naive Bayes, Linear SVM, Decision Tree, and MLP on standard domain articles
and prints a side-by-side comparative testing table.
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.predict import predictor
from src.config import SUPPORTED_CATEGORIES

TEST_ARTICLES = [
    {
        "domain": "Sport",
        "expected": "Sport",
        "headline": "Football Championship Victory",
        "text": "The national football team won the premier league championship match with two late goals in the stadium."
    },
    {
        "domain": "Tech",
        "expected": "Tech",
        "headline": "AI Microprocessor Launch",
        "text": "Apple announced a new artificial intelligence microprocessor designed for next-generation laptops with neural engines."
    },
    {
        "domain": "Business",
        "expected": "Business",
        "headline": "Stock Market & Interest Rates",
        "text": "The central bank maintained benchmark interest rates as quarterly corporate earnings and stock market indices surged."
    },
    {
        "domain": "Entertainment",
        "expected": "Entertainment",
        "headline": "Film Box Office Record",
        "text": "The international film festival premiered a blockbuster cinema release that broke all weekend box office revenue records."
    },
    {
        "domain": "Politics",
        "expected": "Politics",
        "headline": "Parliament Voting Legislation",
        "text": "The national parliament convened an emergency legislative debate to pass bipartisan election integrity and voting reform."
    }
]


def main():
    print("\n" + "=" * 115)
    print("                      NEWSSENSE: MACHINE LEARNING MODELS PREDICTION BENCHMARK")
    print("=" * 115)
    print(f"{'#':<3} | {'Test Article Headline':<30} | {'Expected':<13} | {'Naive Bayes':<14} | {'Linear SVM':<14} | {'Decision Tree':<14} | {'MLP':<14}")
    print("-" * 115)

    all_passed = True
    for idx, item in enumerate(TEST_ARTICLES, 1):
        nb_res = predictor.predict(item["text"], model_name="naive_bayes")
        svm_res = predictor.predict(item["text"], model_name="linear_svm")
        dt_res = predictor.predict(item["text"], model_name="decision_tree")
        mlp_res = predictor.predict(item["text"], model_name="mlp")

        nb_pred = nb_res["predicted_category"]
        svm_pred = svm_res["predicted_category"]
        dt_pred = dt_res["predicted_category"]
        mlp_pred = mlp_res["predicted_category"]

        exp = item["expected"]
        print(f"{idx:<3} | {item['headline']:<30} | {exp:<13} | {nb_pred:<14} | {svm_pred:<14} | {dt_pred:<14} | {mlp_pred:<14}")

        if not (nb_pred == exp and svm_pred == exp and dt_pred == exp and mlp_pred == exp):
            all_passed = False

    print("=" * 115)

    print("\nMODEL INFERENCE & SCORING DETAILS:")
    print("-" * 80)
    sample = TEST_ARTICLES[1] # Tech sample
    print(f"Sample Text: \"{sample['text']}\"")
    print("-" * 80)

    for m_key, m_name in [("naive_bayes", "Naive Bayes"), ("linear_svm", "Linear SVM"), ("decision_tree", "Decision Tree"), ("mlp", "MLP")]:
        res = predictor.predict(sample["text"], model_name=m_key)
        sc = res["prediction_score"]
        score_display = f"{sc['confidence_value']:.4f} ({sc['confidence_percentage']})" if sc['is_calibrated_probability'] else f"{sc['confidence_value']:.4f} (Signed Distance)"
        print(f"[{m_name:<13}] -> Predicted: {res['predicted_category']:<12} | Scoring: {sc['label']:<22} | Score: {score_display}")

    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
