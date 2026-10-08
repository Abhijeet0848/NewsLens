"""
NLP Pipeline Stages Step-by-Step Demonstration Script
Executes and prints each transformation stage of the transparent NLP pipeline:
Raw Text -> Tokenization -> Stop-word Removal -> Lemmatization -> TF-IDF Vectorization -> Classification
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocessing import preprocessor
from src.predict import predictor


SAMPLE_ARTICLE = (
    "Apple announced a new artificial intelligence processor for its next generation of laptops. "
    "The company said the new chip will improve computing performance and energy efficiency."
)


def print_section(stage_num: int, stage_name: str, content: str, details: str = ""):
    print("\n" + "=" * 80)
    print(f"  STAGE {stage_num}: {stage_name.upper()}")
    print("=" * 80)
    print(f"Output:\n  {content}")
    if details:
        print(f"\nDetails:\n  {details}")


def main():
    print("\n" + "#" * 80)
    print("        NEWSSENSE: TRANSPARENT 5-STAGE NLP PREPROCESSING PIPELINE DEMO")
    print("#" * 80)

    # 1. Original Raw Text
    print_section(1, "Original Raw News Article", f'"{SAMPLE_ARTICLE}"', f"Raw length: {len(SAMPLE_ARTICLE)} characters, {len(SAMPLE_ARTICLE.split())} words")

    # 2. Tokenization
    cleaned = preprocessor.clean_text(SAMPLE_ARTICLE)
    tokens = preprocessor.tokenize(cleaned)
    print_section(
        2,
        "Tokenization & Cleaning (Lowercase + Regex Stripping)",
        f"{tokens}",
        f"Token count: {len(tokens)} discrete unigrams extracted\nCleaned string: '{cleaned}'"
    )

    # 3. Stop-word Removal
    without_stopwords = preprocessor.remove_stopwords(tokens)
    removed_stopwords = [t for t in tokens if t not in without_stopwords]
    print_section(
        3,
        "Stop-Word Removal (NLTK English Lexicon Filter)",
        f"{without_stopwords}",
        f"Retained tokens: {len(without_stopwords)} content terms\nFiltered stop-words ({len(removed_stopwords)}): {removed_stopwords}"
    )

    # 4. Lemmatization
    lemmatized = preprocessor.lemmatize(without_stopwords)
    transformations = [f"{orig} -> {lemma}" for orig, lemma in zip(without_stopwords, lemmatized) if orig != lemma]
    print_section(
        4,
        "Morphological Lemmatization (WordNet Lemmatizer)",
        f"{lemmatized}",
        f"Processed text string: '\"{' '.join(lemmatized)}\"'\nMorphological root reductions: {', '.join(transformations) if transformations else 'None'}"
    )

    # 5. TF-IDF Vectorization
    if not predictor.is_loaded:
        predictor.load_artifacts()

    processed_str = " ".join(lemmatized)
    tfidf_vec = predictor.vectorizer.transform([processed_str])
    feature_names = predictor.vectorizer.get_feature_names_out()

    cx = tfidf_vec.tocoo()
    sorted_features = sorted(
        [(feature_names[c], v) for c, v in zip(cx.col, cx.data)],
        key=lambda x: x[1],
        reverse=True
    )

    tfidf_summary = "\n  ".join([f"* '{term}': {weight:.4f}" for term, weight in sorted_features])
    print_section(
        5,
        "TF-IDF Feature Vectorization (20,000 Vocab Capacity)",
        f"Sparse Matrix Dimension: {tfidf_vec.shape} (1 sample x {len(feature_names)} features)\n  Active non-zero features: {len(cx.data)}\n  Top TF-IDF Weights:\n  {tfidf_summary}",
        "Formula: TF(t, d) * (ln((1 + N) / (1 + DF(t))) + 1) with L2 Euclidean unit normalization."
    )

    # Final Classification Output
    res = predictor.predict(SAMPLE_ARTICLE, model_name="naive_bayes")
    print("\n" + "=" * 80)
    print("  FINAL CLASSIFICATION RESULT")
    print("=" * 80)
    print(f"  * Model Used        : {res['selected_model']['name']}")
    print(f"  * Predicted Category: \033[92m{res['predicted_category']}\033[0m")
    print(f"  * Confidence Score  : {res['prediction_score']['confidence_value']:.4f} ({res['prediction_score']['confidence_percentage']})")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
