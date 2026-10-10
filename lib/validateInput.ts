export type Validation = {
  ok: boolean;
  reason?: string;
  warning?: string;
  confidence_penalty?: number;
  sanitized?: string;
};

// Top 100+ most common English words for vocabulary density testing
const ENGLISH_COMMON = new Set([
  "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with",
  "is", "are", "was", "were", "be", "been", "being", "have", "has",
  "had", "do", "does", "did", "will", "would", "could", "should",
  "this", "that", "these", "those", "it", "its", "as", "at", "by",
  "from", "not", "but", "if", "then", "than", "so", "what", "which",
  "who", "whom", "whose", "when", "where", "why", "how", "all", "any",
  "both", "each", "few", "more", "most", "other", "some", "such",
  "no", "nor", "only", "own", "same", "too", "very", "can", "just",
  "about", "after", "again", "also", "back", "because", "come", "day",
  "even", "find", "first", "get", "give", "go", "good", "great",
  "he", "her", "here", "him", "his", "into", "know", "last", "like",
  "look", "make", "man", "many", "me", "much", "my", "new", "now",
  "one", "our", "out", "over", "people", "say", "see", "she", "take",
  "tell", "their", "them", "there", "they", "think", "time", "two",
  "up", "use", "us", "want", "way", "we", "well", "work", "year", "you", "your"
]);

export function sanitizeForApi(text: string): string {
  return text
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, "")
    .replace(/<[^>]+>/g, "") // strip HTML tags
    .replace(/\u0000/g, "") // remove null bytes
    .trim();
}

export function validateInput(raw: string): Validation {
  const sanitized = sanitizeForApi(raw || "");

  // 1. Empty or sanitized to empty
  if (!sanitized) {
    return { ok: false, reason: "Please enter an article to classify.", sanitized: "" };
  }

  // 2. Extract English letter sequences (ignoring emojis/numbers/symbols)
  const words = sanitized.match(/[a-zA-Z]+/g) || [];
  const lower = words.map((w) => w.toLowerCase());

  // 4. Non-Latin script detection (Hindi, Chinese, Arabic, Russian, etc.)
  const latinLetters = (sanitized.match(/[a-zA-Z]/g) || []).length;
  const nonWhitespaceCount = sanitized.replace(/\s+/g, "").length;
  if (nonWhitespaceCount > 20 && latinLetters / nonWhitespaceCount < 0.3) {
    return {
      ok: true,
      warning: "Currently only supports English text — predictions on other languages may be unreliable.",
      confidence_penalty: 0.7,
      sanitized,
    };
  }

  // 5. Not enough real words
  if (words.length < 8) {
    return {
      ok: false,
      reason: "Not enough words to classify reliably.",
      sanitized,
    };
  }

  // 5. Repetitive word check
  const uniqueWords = new Set(lower);
  if (words.length >= 6 && uniqueWords.size < 4) {
    return {
      ok: true,
      warning: "Repetitive input detected — prediction may be unreliable.",
      confidence_penalty: 0.6,
      sanitized,
    };
  }

  // 5. English stopword density & real word structure check
  const englishHits = lower.filter((w) => ENGLISH_COMMON.has(w)).length;
  const englishRatio = words.length > 0 ? englishHits / words.length : 0;

  // Real English words must have vowels and lack abnormal consonant clusters or keyboard smashing (asdfghjkl)
  const plausibleWords = lower.filter((w) => {
    if (w.length < 2) return w === "a" || w === "i";
    const hasVowel = /[aeiouy]/.test(w);
    const hasExcessiveConsonants = /[bcdfghjklmnpqrstvwxz]{5,}/.test(w);
    const hasExcessiveRepeats = /(.)\1{2,}/.test(w);
    return hasVowel && !hasExcessiveConsonants && !hasExcessiveRepeats;
  });
  const realWordRatio = words.length > 0 ? plausibleWords.length / words.length : 0;

  if (englishRatio < 0.05 || realWordRatio < 0.6) {
    return {
      ok: true,
      warning: "This doesn't look like natural English text. Predictions may be unreliable.",
      confidence_penalty: 0.7, // reduce confidence by 70%
      sanitized,
    };
  }

  // 6. Emoji / symbol density (> 50% non-alpha characters)
  const nonAlpha = sanitized.replace(/[a-zA-Z\s]/g, "").length;
  if (nonAlpha / sanitized.length > 0.5) {
    return {
      ok: true,
      warning: "Input is mostly non-letter characters. Predictions may be unreliable.",
      confidence_penalty: 0.7,
      sanitized,
    };
  }

  // 7. Repeated characters (aaaaa, hhhhhhh)
  if (/(.)\1{5,}/.test(sanitized)) {
    return {
      ok: true,
      warning: "Repeated characters detected. Predictions may be unreliable.",
      confidence_penalty: 0.6,
      sanitized,
    };
  }

  // 8. Non-Latin script (Hindi, Chinese, Arabic, etc.)
  const latinRatio = words.join("").length / sanitized.length;
  if (latinRatio < 0.3 && sanitized.length > 30) {
    return {
      ok: true,
      warning: "Currently only supports English text — predictions on other languages may be unreliable.",
      confidence_penalty: 0.7,
      sanitized,
    };
  }

  return { ok: true, sanitized };
}
