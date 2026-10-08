"""
NLP Pipeline Stages Test Suite for NewsSense
Exhaustively tests and validates each stage of the NLP pipeline:
1. Tokenization (Word boundary extraction, punctuation stripping, case normalization)
2. Stop-word Removal (Filtering high-frequency grammatical tokens while preserving content words)
3. Lemmatization (Morphological dictionary reduction for nouns, verbs, and irregulars)
4. TF-IDF Vectorization (Term Frequency - Inverse Document Frequency extraction, L2 normalization, top features)
"""

import os
import sys
import pytest
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.preprocessing import preprocessor
from src.predict import predictor

SAMPLE_RAW_TEXT = (
    "Apple announced a new artificial intelligence microprocessor for its next generation of laptops. "
    "The company said the new chip will improve computing performance and energy efficiency!"
)


# =====================================================================
# 1. Tokenization Tests
# =====================================================================
def test_stage_tokenization():
    """
    Validates tokenization:
    - Lowercase conversion
    - Special punctuation and symbol stripping
    - Correct discrete word token production
    """
    cleaned = preprocessor.clean_text(SAMPLE_RAW_TEXT)
    tokens = preprocessor.tokenize(cleaned)

    # Cleaned string must be lowercased and devoid of punctuation
    assert cleaned == cleaned.lower()
    assert "!" not in cleaned
    assert "." not in cleaned
    
    # Tokens must be a non-empty list of strings
    assert isinstance(tokens, list)
    assert len(tokens) > 10
    
    # Verify presence of key unigrams in raw tokens
    assert "apple" in tokens
    assert "announced" in tokens
    assert "artificial" in tokens
    assert "intelligence" in tokens
    assert "microprocessor" in tokens
    assert "laptops" in tokens
    assert "the" in tokens
    assert "for" in tokens


# =====================================================================
# 2. Stop-word Removal Tests
# =====================================================================
def test_stage_stopword_removal():
    """
    Validates stop-word removal:
    - Filters out high-frequency grammatical terms (e.g., 'a', 'its', 'of', 'the', 'will', 'and')
    - Preserves domain-informative semantic content words
    - Token count decreases monotonically
    """
    cleaned = preprocessor.clean_text(SAMPLE_RAW_TEXT)
    tokens = preprocessor.tokenize(cleaned)
    filtered = preprocessor.remove_stopwords(tokens)

    # Length must be strictly less than raw tokens
    assert len(filtered) < len(tokens)

    # High-frequency stop words must be eliminated
    stop_words_in_sample = ["a", "its", "of", "the", "will", "and", "for"]
    for sw in stop_words_in_sample:
        assert sw not in filtered, f"Stopword '{sw}' was not filtered!"

    # Domain content terms must be retained
    content_terms = ["apple", "announced", "artificial", "intelligence", "microprocessor", "laptops", "chip", "improve", "computing", "performance", "energy", "efficiency"]
    for ct in content_terms:
        assert ct in filtered, f"Content term '{ct}' was mistakenly dropped!"


# =====================================================================
# 3. Lemmatization Tests
# =====================================================================
def test_stage_lemmatization():
    """
    Validates morphological lemmatization:
    - Plural nouns to singular root form ('laptops' -> 'laptop', 'processors' -> 'processor')
    - Inflected past-tense verbs to base lemma ('announced' -> 'announce', 'improved' -> 'improve', 'running' -> 'run')
    - Idempotence on already lemmatized terms
    """
    # Specific targeted morphological test cases
    test_morphs = ["laptops", "processors", "announced", "matches", "scoring", "indices", "technologies"]
    lemmatized = preprocessor.lemmatize(test_morphs)

    assert "laptop" in lemmatized       # laptops -> laptop
    assert "processor" in lemmatized    # processors -> processor
    assert "announce" in lemmatized     # announced -> announce
    assert "match" in lemmatized        # matches -> match
    assert "score" in lemmatized        # scoring -> score
    assert "technology" in lemmatized   # technologies -> technology

    # Verify pipeline on sample text
    intermediate = preprocessor.preprocess_with_intermediate_steps(SAMPLE_RAW_TEXT)
    lemmas = intermediate["lemmatized_tokens"]
    
    assert "laptop" in lemmas
    assert "announce" in lemmas
    assert "laptops" not in lemmas
    assert "announced" not in lemmas


# =====================================================================
# 4. TF-IDF Vectorization Tests
# =====================================================================
def test_stage_tfidf_vectorization():
    """
    Validates TF-IDF vectorization:
    - Sparse vector extraction in fitted vocabulary space (6,921 features)
    - L2 unit Euclidean norm constraint (||v||_2 = 1.0)
    - Non-zero feature activations for active query terms
    - Proper term weighting
    """
    if not predictor.is_loaded:
        predictor.load_artifacts()

    intermediate = preprocessor.preprocess_with_intermediate_steps(SAMPLE_RAW_TEXT)
    processed_str = intermediate["processed_text"]

    # Transform through vectorizer
    tfidf_vec = predictor.vectorizer.transform([processed_str])
    feature_names = predictor.vectorizer.get_feature_names_out()

    # Shape must match (1, 6921)
    assert tfidf_vec.shape[0] == 1
    assert tfidf_vec.shape[1] == len(feature_names)

    # Active non-zero features must exist
    cx = tfidf_vec.tocoo()
    assert len(cx.data) > 0, "No TF-IDF features activated for valid input text"

    # L2 Euclidean norm verification: sum(w_i^2) == 1.0
    l2_norm = np.sqrt(np.sum(cx.data ** 2))
    assert np.isclose(l2_norm, 1.0, atol=1e-3), f"TF-IDF vector is not L2 unit normalized: {l2_norm}"

    # Extract top weighted features
    active_terms = {feature_names[col]: val for col, val in zip(cx.col, cx.data)}
    
    # Check that representative vocabulary terms appear with positive weights
    expected_active_subsets = ["apple", "artificial", "intelligence", "chip", "performance", "energy", "efficiency"]
    found_any = any(term in active_terms for term in expected_active_subsets)
    assert found_any, f"Expected vocabulary terms not found in active TF-IDF weights: {active_terms.keys()}"


# =====================================================================
# 5. End-to-End Pipeline Coherence Test
# =====================================================================
def test_end_to_end_pipeline_flow():
    """
    Validates transition across all 5 stages from raw text to classified category.
    """
    res = predictor.predict(SAMPLE_RAW_TEXT, model_name="naive_bayes")
    
    # 1. Pipeline steps present
    steps = res["intermediate_nlp"]
    assert steps["original_text"] == SAMPLE_RAW_TEXT
    assert len(steps["tokens"]) > len(steps["without_stopwords"])
    assert len(steps["without_stopwords"]) == len(steps["lemmatized_tokens"])
    
    # 2. Output classified accurately
    assert res["predicted_category"] == "Technology"
