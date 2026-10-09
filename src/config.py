"""
Configuration settings and global constants for NewsSense ML Pipeline.
"""

import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Ensure required directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Dataset Paths
DATASET_PATH = os.path.join(DATA_DIR, "bbc-news-data.csv")

# Supported Standard Categories (5 BBC News Domains)
SUPPORTED_CATEGORIES = [
    "Business",
    "Entertainment",
    "Politics",
    "Sport",
    "Tech"
]


# Train / Test Splitting Parameters
TEST_SIZE = 0.20
RANDOM_STATE = 42

# TF-IDF Feature Extraction Parameters
TFIDF_MAX_FEATURES = 20000
TFIDF_NGRAM_RANGE = (1, 2)
TFIDF_MIN_DF = 2
TFIDF_SUBLINEAR_TF = True

# Model Storage Paths
VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib")
LABEL_ENCODER_PATH = os.path.join(MODELS_DIR, "label_encoder.joblib")
EVALUATION_RESULTS_PATH = os.path.join(MODELS_DIR, "evaluation_results.json")

MODEL_PATHS = {
    "naive_bayes": os.path.join(MODELS_DIR, "naive_bayes_model.joblib"),
    "linear_svm": os.path.join(MODELS_DIR, "linear_svm_model.joblib"),
    "decision_tree": os.path.join(MODELS_DIR, "decision_tree_model.joblib"),
    "mlp": os.path.join(MODELS_DIR, "mlp_model.joblib")
}

# Model Descriptions and Metadata
MODEL_METADATA = {
    "naive_bayes": {
        "name": "Multinomial Naive Bayes",
        "type": "Probabilistic Generative",
        "scoring_type": "probability"
    },
    "linear_svm": {
        "name": "Linear Support Vector Machine",
        "type": "Maximum-Margin Discriminative",
        "scoring_type": "decision_score"
    },
    "decision_tree": {
        "name": "Decision Tree Classifier",
        "type": "Hierarchical Non-Parametric",
        "scoring_type": "probability"
    },
    "mlp": {
        "name": "Multi-Layer Perceptron (MLP)",
        "type": "Artificial Neural Network",
        "scoring_type": "probability"
    }
}
