"""
NLP Preprocessing Module for NewsSense
Implements Text Cleaning, Tokenization, Stop-word Removal, and Morphological Lemmatization.
Provides detailed intermediate step tracking for academic transparency.
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


def ensure_nltk_corpora():
    """Ensures required NLTK tokenizers and lexicons are available."""
    packages = ['punkt', 'punkt_tab', 'stopwords', 'wordnet', 'omw-1.4']
    for pkg in packages:
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

ensure_nltk_corpora()



class TextPreprocessor:
    """
    Reusable NLP text preprocessing pipeline providing both end-to-end transformation
    and intermediate step-by-step inspection.
    """
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
        except Exception:
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
        Cleans raw input text:
        - Removes URLs
        - Removes HTML tags
        - Removes email addresses
        - Converts to lower case
        - Filters non-alphabetic characters
        - Collapses redundant whitespace
        """
        if not isinstance(text, str):
            text = str(text or "")
        
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
        # Remove HTML markup
        text = re.sub(r'<.*?>+', ' ', text)
        # Remove email addresses
        text = re.sub(r'\S+@\S+', ' ', text)
        # Lowercase
        text = text.lower()
        # Keep alphabetic characters and spaces only
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        # Collapse multiple whitespace characters
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def tokenize(self, cleaned_text: str) -> list[str]:
        """Tokenizes text into discrete word tokens."""
        if not cleaned_text:
            return []
        try:
            return word_tokenize(cleaned_text)
        except Exception:
            return cleaned_text.split()

    def remove_stopwords(self, tokens: list[str]) -> list[str]:
        """Filters out high-frequency grammatical stop words and single characters."""
        return [t for t in tokens if t not in self.stop_words and len(t) > 1]

    def lemmatize(self, tokens: list[str]) -> list[str]:
        """Reduces tokens to their dictionary root form using WordNet."""
        if not self.lemmatizer:
            return tokens
        
        lemmas = []
        for token in tokens:
            try:
                # Morphological lemmatization (Noun -> Verb)
                lemma_noun = self.lemmatizer.lemmatize(token, pos='n')
                lemma = self.lemmatizer.lemmatize(lemma_noun, pos='v')
                lemmas.append(lemma)
            except Exception:
                lemmas.append(token)
        return lemmas

    def preprocess_with_intermediate_steps(self, text: str) -> dict:
        """
        Reusable function returning both the final processed text
        and all intermediate pipeline artifacts.
        
        Returns:
            dict with keys:
            - original_text
            - tokens
            - without_stopwords
            - lemmatized_tokens
            - processed_text
        """
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        without_stopwords = self.remove_stopwords(tokens)
        lemmatized_tokens = self.lemmatize(without_stopwords)
        processed_text = " ".join(lemmatized_tokens)

        return {
            "original_text": text,
            "tokens": tokens,
            "without_stopwords": without_stopwords,
            "lemmatized_tokens": lemmatized_tokens,
            "processed_text": processed_text
        }

    def preprocess(self, text: str) -> str:
        """Convenience method returning final joined string."""
        return self.preprocess_with_intermediate_steps(text)["processed_text"]


# Global default preprocessor instance
preprocessor = TextPreprocessor()


def preprocess_article(text: str) -> dict:
    """Module-level entry point for intermediate pipeline inspection."""
    return preprocessor.preprocess_with_intermediate_steps(text)


def clean_and_lemmatize(text: str) -> str:
    """Module-level entry point for batch string preprocessing."""
    return preprocessor.preprocess(text)
