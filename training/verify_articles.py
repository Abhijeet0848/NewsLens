import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from training.predict import predict

articles = [
    ("Sport", "Real Madrid won the Champions League final with a sensational victory over their rivals at Wembley Stadium."),
    ("Business", "The Federal Reserve raised interest rates to combat inflation as global stock markets and economic growth slowed."),
    ("Tech", "Apple unveiled the M4 chip at WWDC with powerful artificial intelligence and neural engine hardware features."),
    ("Politics", "Parliament passed the Renters Reform Bill after government ministers and MPs debated the new legislation in the House of Commons."),
    ("Entertainment", "The new Harry Potter series has cast its leading actors and director for the upcoming television show season.")
]

print("-" * 80)
print(f"{'Expected':<15} | {'Predicted':<15} | {'Confidence':<12} | {'Top Scores'}")
print("-" * 80)

all_passed = True
for expected, text in articles:
    res = predict(text, "svm")
    pred = res["category"]
    conf = res["confidence_percentage"]
    passed = pred.lower() == expected.lower() and conf >= 70.0
    if not passed:
        all_passed = False
    status = "PASS" if passed else "FAIL"
    top_scores = ", ".join([f"{k}: {v:.2f}" for k, v in res["all_scores"].items() if v > 0.05])
    print(f"{expected:<15} | {pred:<15} | {conf:>6.1f}% [{status}] | {top_scores}")

print("-" * 80)
print(f"Overall Status: {'ALL 5 ARTICLES VERIFIED SUCCESSFULLY' if all_passed else 'SOME ARTICLES FAILED'}")
