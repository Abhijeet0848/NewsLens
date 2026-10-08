"""
NLP Preprocessing Pipeline for News Article Classification
Includes text cleaning, tokenization, stop-word removal, lemmatization, and TF-IDF extraction.
Provides detailed intermediate step tracking for academic inspectability and explainability.
"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Ensure required NLTK resources are available
def _ensure_nltk_resources():
    required_packages = ['punkt', 'punkt_tab', 'stopwords', 'wordnet', 'omw-1.4']
    for pkg in required_packages:
        try:
            nltk.data.find(f'tokenizers/{pkg}' if 'punkt' in pkg else f'corpora/{pkg}')
        except LookupError:
            try:
                import socket
                orig_timeout = socket.getdefaulttimeout()
                socket.setdefaulttimeout(1.0)
                nltk.download(pkg, quiet=True, raise_on_error=False)
                socket.setdefaulttimeout(orig_timeout)
            except Exception:
                pass

_ensure_nltk_resources()


class NLPPipeline:
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
        except Exception:
            # Fallback stop words in case NLTK corpus fails in a sandbox
            self.stop_words = {
                'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
                "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
                'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
                'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
                'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
                'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
                'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because',
                'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
                'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
                'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
                'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
                'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
                'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
                'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll',
                'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
                'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't",
                'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',
                "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
                'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
            }
        
        try:
            self.lemmatizer = WordNetLemmatizer()
        except Exception:
            self.lemmatizer = None

    def clean_text(self, text: str) -> str:
        """
        Cleans input raw text:
        - Removes URLs
        - Removes HTML tags
        - Removes email addresses
        - Removes non-alphabetic characters (preserving spaces)
        - Normalizes whitespace
        - Converts to lower case
        """
        if not isinstance(text, str):
            text = str(text or "")
        
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
        # Remove HTML tags
        text = re.sub(r'<.*?>+', ' ', text)
        # Remove email addresses
        text = re.sub(r'\S+@\S+', ' ', text)
        # Lowercase
        text = text.lower()
        # Keep only alphabetic characters and spaces
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        # Collapse multi-spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def tokenize(self, cleaned_text: str) -> list[str]:
        """Tokenize cleaned string into word tokens."""
        if not cleaned_text:
            return []
        try:
            tokens = word_tokenize(cleaned_text)
        except Exception:
            tokens = cleaned_text.split()
        return tokens

    def remove_stopwords(self, tokens: list[str]) -> tuple[list[str], list[str]]:
        """
        Filters stop words from token list.
        Returns (filtered_tokens, removed_stopwords)
        """
        filtered = []
        removed = []
        for token in tokens:
            if token in self.stop_words or len(token) <= 1:
                removed.append(token)
            else:
                filtered.append(token)
        return filtered, removed

    def lemmatize(self, tokens: list[str]) -> tuple[list[str], list[dict]]:
        """
        Lemmatizes tokens to dictionary base form.
        Returns (lemmatized_tokens, transformation_log)
        """
        lemmatized = []
        transformations = []
        for token in tokens:
            if self.lemmatizer:
                try:
                    # Lemmatize noun then verb
                    lemma_n = self.lemmatizer.lemmatize(token, pos='n')
                    lemma = self.lemmatizer.lemmatize(lemma_n, pos='v')
                except Exception:
                    lemma = token
            else:
                lemma = token

            lemmatized.append(lemma)
            if lemma != token:
                transformations.append({"original": token, "lemmatized": lemma})
                
        return lemmatized, transformations

    def preprocess_string(self, text: str) -> str:
        """Standard end-to-end preprocessing returning joined processed string for vectorizers."""
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        filtered, _ = self.remove_stopwords(tokens)
        lemmatized, _ = self.lemmatize(filtered)
        return " ".join(lemmatized)

    def process_with_steps(self, raw_text: str) -> dict:
        """
        Executes each pipeline step and captures full intermediate states
        for transparent academic inspection and visualization in the UI.
        """
        raw_char_count = len(raw_text)
        raw_word_count = len(raw_text.split())

        cleaned = self.clean_text(raw_text)
        cleaned_char_count = len(cleaned)
        
        tokens = self.tokenize(cleaned)
        total_tokens_count = len(tokens)

        filtered_tokens, removed_stopwords = self.remove_stopwords(tokens)
        filtered_count = len(filtered_tokens)
        removed_count = len(removed_stopwords)

        lemmatized_tokens, transformations = self.lemmatize(filtered_tokens)
        final_processed_text = " ".join(lemmatized_tokens)

        # Token frequencies
        token_freq = {}
        for t in lemmatized_tokens:
            token_freq[t] = token_freq.get(t, 0) + 1
        sorted_vocab = sorted(token_freq.items(), key=lambda x: x[1], reverse=True)

        return {
            "raw_text": raw_text,
            "raw_stats": {
                "character_count": raw_char_count,
                "word_count": raw_word_count
            },
            "cleaned_text": cleaned,
            "cleaned_stats": {
                "character_count": cleaned_char_count,
                "reduction_pct": round((1.0 - (cleaned_char_count / max(1, raw_char_count))) * 100, 2)
            },
            "tokens": tokens,
            "tokens_count": total_tokens_count,
            "filtered_tokens": filtered_tokens,
            "removed_stopwords": removed_stopwords,
            "removed_stopwords_count": removed_count,
            "lemmatized_tokens": lemmatized_tokens,
            "lemmatized_count": len(lemmatized_tokens),
            "lemmatization_changes": transformations,
            "final_processed_text": final_processed_text,
            "vocabulary_frequency": sorted_vocab[:25],
            "vocabulary_size": len(token_freq)
        }


# Global singleton instance
pipeline = NLPPipeline()
