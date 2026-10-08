"""
Model Trainer for NewsSense Academic Project
Trains 4 Supervised Classification Models:
1. Multinomial Naive Bayes
2. Support Vector Machine (Linear SVM with Calibrated Probabilities)
3. Decision Tree Classifier
4. Multi-Layer Perceptron (MLP) Classifier

Calculates real academic evaluation metrics (Accuracy, Precision, Recall, F1, Confusion Matrix, Classification Report)
on a held-out test split, ensuring no data leakage.
Saves all artifacts to the models/ directory.
"""

import os
import sys
import json
import time
import joblib
import numpy as np
import pandas as pd

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from src.nlp_pipeline import pipeline
from src.data_loader import load_dataset, CATEGORIES

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
os.makedirs(MODELS_DIR, exist_ok=True)

MODEL_CONFIGS = {
    "naive_bayes": {
        "name": "Multinomial Naive Bayes",
        "description": "Probabilistic classifier applying Bayes' theorem with strong conditional independence assumptions between TF-IDF word features.",
        "complexity": "O(N * D) Linear Training Time",
        "class_type": "Probabilistic Generative",
        "hyperparameters": {"alpha": 0.1, "fit_prior": True}
    },
    "svm": {
        "name": "Support Vector Machine",
        "description": "Linear maximum-margin hyperplane classifier separating high-dimensional TF-IDF vectors with Platt probability scaling.",
        "complexity": "O(N^2 to N^3) Optimization",
        "class_type": "Max-Margin Discriminative",
        "hyperparameters": {"kernel": "linear", "C": 1.0, "probability": True}
    },
    "decision_tree": {
        "name": "Decision Tree Classifier",
        "description": "Non-parametric hierarchical tree classifier recursively splitting feature space using Gini impurity / Information Gain.",
        "complexity": "O(D * N log N) Tree Induction",
        "class_type": "Hierarchical Rule-Based",
        "hyperparameters": {"criterion": "gini", "max_depth": 35, "min_samples_split": 2}
    },
    "mlp": {
        "name": "Multi-Layer Perceptron",
        "description": "Feedforward artificial neural network with two hidden layers (100, 50 neurons), ReLU activations, and Adam gradient backpropagation.",
        "complexity": "O(E * N * H) Iterative Backprop",
        "class_type": "Deep Artificial Neural Network",
        "hyperparameters": {"hidden_layer_sizes": [100, 50], "activation": "relu", "max_iter": 300, "solver": "adam"}
    }
}


def build_models():
    """Instantiates fresh instances of the 4 target models."""
    return {
        "naive_bayes": MultinomialNB(alpha=0.1),
        "svm": SVC(kernel="linear", C=1.0, probability=True, random_state=42),
        "decision_tree": DecisionTreeClassifier(criterion="gini", max_depth=35, random_state=42),
        "mlp": MLPClassifier(hidden_layer_sizes=(100, 50), activation="relu", max_iter=300, random_state=42)
    }


def train_and_evaluate(test_size: float = 0.20, random_state: int = 42):
    """
    Complete ML Pipeline:
    1. Loads dataset
    2. Runs text preprocessing via NLPPipeline
    3. Splits into Train & Test sets (stratified)
    4. Fits TF-IDF vectorizer strictly on training data
    5. Transforms test data
    6. Trains 4 models and records training durations
    7. Evaluates real metrics on test split
    8. Persists all artifacts to disk
    """
    print("=" * 60)
    print("Starting NewsSense Academic Model Training & Evaluation")
    print("=" * 60)

    # 1. Load Data
    df = load_dataset()
    print(f"Loaded {len(df)} total articles across categories: {df['category'].unique().tolist()}")

    # 2. Text Preprocessing
    print("Executing NLP text preprocessing (cleaning, stopword removal, lemmatization)...")
    start_nlp = time.time()
    df["processed_text"] = df["text"].apply(pipeline.preprocess_string)
    print(f"NLP preprocessing completed in {time.time() - start_nlp:.2f}s")

    # 3. Label Encoding
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(df["category"])
    class_names = list(label_encoder.classes_)

    # 4. Stratified Train / Test Split
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        df["processed_text"],
        y_encoded,
        test_size=test_size,
        random_state=random_state,
        stratify=y_encoded
    )
    print(f"Dataset split: Training={len(X_train_raw)} articles ({100*(1-test_size):.0f}%), Testing={len(X_test_raw)} articles ({100*test_size:.0f}%)")

    # 5. TF-IDF Feature Extraction (Fit strictly on Train, transform Test)
    print("Fitting TF-IDF Vectorizer on training data...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=2
    )
    X_train_tfidf = vectorizer.fit_transform(X_train_raw)
    X_test_tfidf = vectorizer.transform(X_test_raw)
    print(f"Extracted {X_train_tfidf.shape[1]} TF-IDF feature vocabulary dimensions.")

    # 6. Train Models and Compute Real Evaluation Metrics
    models = build_models()
    evaluation_results = {
        "metadata": {
            "trained_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "train_samples": int(len(X_train_raw)),
            "test_samples": int(len(X_test_raw)),
            "total_samples": int(len(df)),
            "test_size": test_size,
            "random_state": random_state,
            "vocabulary_size": int(X_train_tfidf.shape[1]),
            "categories": class_names
        },
        "models": {}
    }

    trained_model_objects = {}

    for model_id, model in models.items():
        config = MODEL_CONFIGS[model_id]
        print(f"\n--- Training {config['name']} ({model_id}) ---")
        
        # Train & Measure Training Time
        t0 = time.time()
        model.fit(X_train_tfidf, y_train)
        train_duration = time.time() - t0
        
        # Test Inference & Measure Latency
        t_inf_start = time.time()
        y_pred = model.predict(X_test_tfidf)
        inf_duration = (time.time() - t_inf_start) / max(1, len(y_test)) * 1000  # ms per sample

        # Calculate exact academic performance metrics
        acc = float(accuracy_score(y_test, y_pred))
        prec_macro = float(precision_score(y_test, y_pred, average="macro", zero_division=0))
        prec_weighted = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
        rec_macro = float(recall_score(y_test, y_pred, average="macro", zero_division=0))
        rec_weighted = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
        f1_mac = float(f1_score(y_test, y_pred, average="macro", zero_division=0))
        f1_wt = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))

        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred, labels=range(len(class_names)))
        cm_normalized = np.round(cm.astype('float') / np.maximum(cm.sum(axis=1)[:, np.newaxis], 1), 4).tolist()

        # Detailed per-class classification report
        clf_rep = classification_report(y_test, y_pred, target_names=class_names, output_dict=True, zero_division=0)

        # Per-class summary list
        per_class_metrics = []
        for cat in class_names:
            if cat in clf_rep:
                per_class_metrics.append({
                    "category": cat,
                    "precision": round(float(clf_rep[cat]["precision"]), 4),
                    "recall": round(float(clf_rep[cat]["recall"]), 4),
                    "f1_score": round(float(clf_rep[cat]["f1-score"]), 4),
                    "support": int(clf_rep[cat]["support"])
                })

        print(f"Accuracy: {acc*100:.2f}% | Macro F1: {f1_mac*100:.2f}% | Train Time: {train_duration:.3f}s")

        evaluation_results["models"][model_id] = {
            "id": model_id,
            "name": config["name"],
            "description": config["description"],
            "class_type": config["class_type"],
            "complexity": config["complexity"],
            "hyperparameters": config["hyperparameters"],
            "accuracy": round(acc, 4),
            "precision_macro": round(prec_macro, 4),
            "precision_weighted": round(prec_weighted, 4),
            "recall_macro": round(rec_macro, 4),
            "recall_weighted": round(rec_weighted, 4),
            "f1_macro": round(f1_mac, 4),
            "f1_weighted": round(f1_wt, 4),
            "training_time_seconds": round(train_duration, 4),
            "avg_inference_latency_ms": round(inf_duration, 3),
            "confusion_matrix": cm.tolist(),
            "confusion_matrix_normalized": cm_normalized,
            "per_class_metrics": per_class_metrics,
            "classification_report": clf_rep
        }

        trained_model_objects[model_id] = model

    # 7. Persist Artifacts Locally
    print("\nSaving trained artifacts to disk...")
    joblib.dump(vectorizer, os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib"))
    joblib.dump(label_encoder, os.path.join(MODELS_DIR, "label_encoder.joblib"))

    for model_id, model_obj in trained_model_objects.items():
        joblib.dump(model_obj, os.path.join(MODELS_DIR, f"{model_id}.joblib"))

    metrics_path = os.path.join(MODELS_DIR, "evaluation_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(evaluation_results, f, indent=2)

    print(f"Saved vectorizer, 4 models, and evaluation metrics to {MODELS_DIR}")
    print("Training and Evaluation pipeline finished successfully!")
    return evaluation_results


if __name__ == "__main__":
    train_and_evaluate()
