import os
import joblib
import numpy as np

# Load model
vectorizer = joblib.load("models/vectorizer.pkl")
model = joblib.load("models/svm.pkl")
le = joblib.load("models/label_encoder.joblib") if os.path.exists("models/label_encoder.joblib") else None

# Test on a clear Sport article
test = "Real Madrid secured their 15th Champions League title on Saturday, defeating Borussia Dortmund 2-0 at Wembley."

# Vectorize and predict
X = vectorizer.transform([test])
probs = model.predict_proba(X)[0]

if le is not None and hasattr(le, "classes_") and isinstance(model.classes_[0], (int, np.integer)):
    pred_idx = probs.argmax()
    pred_label = le.inverse_transform([model.classes_[pred_idx]])[0].lower()
    class_labels = [str(c).lower() for c in le.classes_]
else:
    pred_idx = probs.argmax()
    pred_label = str(model.classes_[pred_idx]).lower()
    class_labels = [str(c).lower() for c in model.classes_]

print("Prediction:", pred_label)
print(f"Confidence: {probs.max():.2f}")
print("All scores:")
for cls, p in zip(class_labels, probs):
    print(f"  {cls}: {p:.3f}")
