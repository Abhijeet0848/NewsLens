import joblib
import numpy as np

v = joblib.load("models/vectorizer.pkl")
m = joblib.load("models/svm.pkl")
le = joblib.load("models/label_encoder.pkl")
class_names = [str(c).lower() for c in le.classes_]

print("=" * 60)
print("MODEL TYPE:", type(m).__name__)
print("CLASSES:", class_names)
if hasattr(m, "coef_"):
    print("COEF SHAPE:", m.coef_.shape)
    print("INTERCEPT:", m.intercept_)
elif hasattr(m, "calibrated_classifiers_"):
    print("Calibrated classifiers count:", len(m.calibrated_classifiers_))
print("=" * 60)

# Test on a clear Sport article
text = "Real Madrid secured their 15th Champions League title on Saturday, defeating Borussia Dortmund 2-0 at Wembley Stadium. Goals from Dani Carvajal and Vinicius Junior sealed the victory."

X = v.transform([text])
print(f"Non-zero features: {X.nnz}")

# Raw decision function
if hasattr(m, "decision_function"):
    scores = m.decision_function(X)[0]
    print(f"Decision function: {scores}")
    print(f"Argmax: {class_names[scores.argmax()]}")

# Probability output
if hasattr(m, "predict_proba"):
    probs = m.predict_proba(X)[0]
    print(f"Predict_proba: {probs}")
    best_idx = probs.argmax()
    print(f"Argmax: {class_names[best_idx]}")
    for c, p in zip(class_names, probs):
        print(f"  {c}: {p * 100:.2f}%")
    print(f"-> Predicts {class_names[best_idx].capitalize()} with {probs[best_idx] * 100:.1f}% confidence")
else:
    print("NO predict_proba() — this is LinearSVC, not SVC")
