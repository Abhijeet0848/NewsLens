"""
Training and Evaluation Pipeline for NewsSense
Loads dataset, analyzes statistics, applies stratified 80/20 train/test split,
fits TF-IDF strictly on training data, trains 4 supervised classifiers,
evaluates on held-out test data, and saves all artifacts.
"""

import os
import sys
import time
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier

# Add parent directory to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.config import (
    DATASET_PATH,
    TEST_SIZE,
    RANDOM_STATE,
    TFIDF_MAX_FEATURES,
    TFIDF_NGRAM_RANGE,
    TFIDF_MIN_DF,
    TFIDF_SUBLINEAR_TF,
    VECTORIZER_PATH,
    LABEL_ENCODER_PATH,
    MODEL_PATHS,
    EVALUATION_RESULTS_PATH,
    MODEL_METADATA
)
from src.preprocessing import preprocessor
from src.evaluate import compute_model_metrics, save_evaluation_results


def inspect_dataset(df: pd.DataFrame) -> dict:
    """
    Analyzes dataset integrity before training:
    - Total articles
    - Number of categories
    - Articles per category
    - Missing values count
    - Duplicate articles count
    """
    total_articles = len(df)
    categories_series = df["category"] if "category" in df.columns else df["label"]
    unique_categories = sorted(categories_series.unique().tolist())
    articles_per_cat = categories_series.value_counts().to_dict()
    
    missing_count = int(df.isnull().sum().sum())
    missing_per_col = df.isnull().sum().to_dict()
    duplicate_count = int(df.duplicated(subset=["text"]).sum()) if "text" in df.columns else 0

    print("=" * 65)
    print("           DATASET INTEGRITY & STATISTICAL SUMMARY            ")
    print("=" * 65)
    print(f"Total Articles:           {total_articles}")
    print(f"Number of Categories:     {len(unique_categories)}")
    print(f"Categories List:          {', '.join(unique_categories)}")
    print("\nArticles per Category Distribution:")
    for cat, count in articles_per_cat.items():
        print(f"  - {cat:<15}: {count:>4} articles ({count / total_articles * 100:.1f}%)")
    print(f"\nMissing Values:           {missing_count} (Breakdown: {missing_per_col})")
    print(f"Duplicate Articles:       {duplicate_count}")
    print("=" * 65)

    return {
        "total_articles": total_articles,
        "num_categories": len(unique_categories),
        "categories": unique_categories,
        "articles_per_category": articles_per_cat,
        "missing_values": missing_count,
        "duplicates": duplicate_count
    }


from src.data_loader import ensure_large_dataset_exists

def load_and_validate_dataset(filepath: str = DATASET_PATH) -> pd.DataFrame:
    """
    Loads dataset from CSV and validates structural requirements.
    Ensures 8,000 articles across 8 categories.
    """
    ensure_large_dataset_exists(8000)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Dataset file not found at '{filepath}'."
        )

    df = pd.read_csv(filepath, encoding="utf-8")
    
    # Check minimum columns
    text_col = "text" if "text" in df.columns else None
    cat_col = "category" if "category" in df.columns else ("label" if "label" in df.columns else None)

    if not text_col or not cat_col:
        raise ValueError(
            f"Dataset must contain 'text' and 'category' (or 'label') columns. Found columns: {list(df.columns)}"
        )

    # Standardize column names
    df = df.rename(columns={text_col: "text", cat_col: "category"})

    # Drop nulls or empty rows
    initial_len = len(df)
    df = df.dropna(subset=["text", "category"])
    df = df[df["text"].str.strip() != ""]
    if len(df) < initial_len:
        print(f"Removed {initial_len - len(df)} empty / null records.")

    # Remove exact duplicate texts to prevent train/test leakage
    df = df.drop_duplicates(subset=["text"]).reset_index(drop=True)

    if len(df) == 0:
        raise ValueError("Dataset contains 0 valid samples. Training cannot proceed.")

    return df


def train_models_pipeline(dataset_path: str = DATASET_PATH) -> dict:
    """
    Executes complete Stage 1 ML pipeline:
    1. Dataset validation & inspection
    2. NLP text preprocessing
    3. Stratified 80/20 train/test split
    4. TF-IDF feature extraction (Fit on train only, transform test)
    5. Model training for 4 algorithms
    6. Evaluation on held-out test split
    7. Artifact persistence
    """
    start_time = time.time()
    print("\n>>> Stage 1: Initializing NewsSense ML Training Pipeline...")

    # 1. Load and Inspect Dataset
    df = load_and_validate_dataset(dataset_path)
    stats = inspect_dataset(df)

    # 2. Text Preprocessing
    print("\n[Step 1/5] Applying NLP Preprocessing (Cleaning, Tokenization, Stopwords, Lemmatization)...")
    t0 = time.time()
    df["processed_text"] = df["text"].apply(preprocessor.preprocess)
    print(f"NLP preprocessing completed in {time.time() - t0:.2f} seconds.")

    # 3. Stratified Train / Test Split
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(df["category"])
    class_names = list(label_encoder.classes_)

    print(f"\n[Step 2/5] Performing Stratified Train/Test Split (Train: {int((1-TEST_SIZE)*100)}%, Test: {int(TEST_SIZE*100)}%)...")
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        df["processed_text"],
        y_encoded,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y_encoded
    )
    print(f"  - Training Samples:  {len(X_train_raw)} records ({100*(1-TEST_SIZE):.0f}%)")
    print(f"  - Testing Samples:   {len(X_test_raw)} records ({100*TEST_SIZE:.0f}%)")
    print(f"  - Random Seed:       {RANDOM_STATE}")

    # 4. TF-IDF Feature Extraction (Fit strictly on Train, transform Test)
    print("\n[Step 3/5] Fitting TF-IDF Vectorizer strictly on Training Data...")
    vectorizer = TfidfVectorizer(
        max_features=TFIDF_MAX_FEATURES,
        ngram_range=TFIDF_NGRAM_RANGE,
        min_df=TFIDF_MIN_DF,
        sublinear_tf=TFIDF_SUBLINEAR_TF
    )
    X_train_tfidf = vectorizer.fit_transform(X_train_raw)
    X_test_tfidf = vectorizer.transform(X_test_raw)

    vocab_size = len(vectorizer.vocabulary_)
    feature_names = vectorizer.get_feature_names_out()
    
    # Calculate top TF-IDF terms across corpus
    mean_tfidf = np.asarray(X_train_tfidf.mean(axis=0)).ravel()
    top_indices = mean_tfidf.argsort()[::-1][:15]
    top_terms = [(feature_names[i], round(float(mean_tfidf[i]), 4)) for i in top_indices]

    print(f"  - Vocabulary Size:          {vocab_size} unique n-gram features")
    print(f"  - Training Matrix Shape:    {X_train_tfidf.shape}")
    print(f"  - Testing Matrix Shape:     {X_test_tfidf.shape}")
    print(f"  - Top 10 Corpus Keywords:   {', '.join([f'{w} ({s})' for w, s in top_terms[:10]])}")

    # 5. Model Training & Evaluation
    print("\n[Step 4/5] Training 4 Supervised Classification Models...")
    
    model_definitions = {
        "naive_bayes": MultinomialNB(alpha=0.1),
        "linear_svm": LinearSVC(C=1.0, random_state=RANDOM_STATE),
        "decision_tree": DecisionTreeClassifier(criterion="gini", max_depth=35, random_state=RANDOM_STATE),
        "mlp": MLPClassifier(hidden_layer_sizes=(100, 50), activation="relu", max_iter=300, random_state=RANDOM_STATE)
    }

    trained_models = {}
    evaluation_payload = {
        "metadata": {
            "trained_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "dataset_stats": stats,
            "train_samples": int(len(X_train_raw)),
            "test_samples": int(len(X_test_raw)),
            "test_size": TEST_SIZE,
            "random_state": RANDOM_STATE,
            "vocabulary_size": vocab_size,
            "feature_dimensions": list(X_train_tfidf.shape),
            "categories": class_names,
            "top_corpus_terms": top_terms
        },
        "models": {}
    }

    print("-" * 75)
    print(f"{'Model Name':<28} | {'Accuracy':<9} | {'Macro F1':<9} | {'Train Time':<10}")
    print("-" * 75)

    for model_key, model_obj in model_definitions.items():
        meta = MODEL_METADATA[model_key]
        
        # Fit model
        t_train_start = time.time()
        model_obj.fit(X_train_tfidf, y_train)
        train_duration = time.time() - t_train_start

        # Inference on test set
        t_inf_start = time.time()
        y_pred = model_obj.predict(X_test_tfidf)
        inf_latency_per_sample = ((time.time() - t_inf_start) / max(1, len(y_test))) * 1000  # ms

        # Compute empirical metrics
        metrics = compute_model_metrics(y_test, y_pred, class_names)
        metrics["training_time_seconds"] = round(train_duration, 4)
        metrics["avg_inference_latency_ms"] = round(inf_latency_per_sample, 3)
        metrics["model_name"] = meta["name"]
        metrics["model_type"] = meta["type"]
        metrics["scoring_type"] = meta["scoring_type"]

        evaluation_payload["models"][model_key] = metrics
        trained_models[model_key] = model_obj

        print(
            f"{meta['name']:<28} | "
            f"{metrics['accuracy']*100:>7.2f}% | "
            f"{metrics['f1_macro']*100:>7.2f}% | "
            f"{train_duration:>8.3f} s"
        )

    print("-" * 75)

    # 6. Save Artifacts
    print("\n[Step 5/5] Persisting Model Artifacts to Disk...")
    joblib.dump(vectorizer, VECTORIZER_PATH)
    joblib.dump(label_encoder, LABEL_ENCODER_PATH)
    print(f"  - Saved TF-IDF Vectorizer: {VECTORIZER_PATH}")
    print(f"  - Saved Label Encoder:     {LABEL_ENCODER_PATH}")

    for model_key, model_obj in trained_models.items():
        save_path = MODEL_PATHS[model_key]
        joblib.dump(model_obj, save_path)
        print(f"  - Saved {MODEL_METADATA[model_key]['name']:<25} -> {save_path}")

    save_evaluation_results(evaluation_payload, EVALUATION_RESULTS_PATH)

    # Export formatted data/metrics.json for the Next.js Analytics dashboard
    import json
    data_metrics_export = {}
    for m_key, m_val in evaluation_payload["models"].items():
        data_metrics_export[m_key] = {
            "accuracy": m_val["accuracy"],
            "f1_macro": m_val["f1_macro"],
            "precision": m_val["precision_macro"],
            "recall": m_val["recall_macro"],
            "latency_ms": m_val.get("avg_inference_latency_ms", 1.0),
            "confusion_matrix": m_val["confusion_matrix"],
            "classes": class_names,
            "paradigm": m_val.get("model_type", "Machine Learning"),
            "per_class": m_val.get("per_class_metrics", [])
        }
    data_metrics_path = os.path.join(DATA_DIR, "metrics.json")
    with open(data_metrics_path, "w", encoding="utf-8") as f:
        json.dump(data_metrics_export, f, indent=2)
    print(f"  - Saved Analytics Metrics: {data_metrics_path}")

    total_pipeline_time = time.time() - start_time
    print(f"\n>>> Stage 1 Training & Evaluation Pipeline Completed Successfully in {total_pipeline_time:.2f}s!")
    return evaluation_payload


if __name__ == "__main__":
    train_models_pipeline()
