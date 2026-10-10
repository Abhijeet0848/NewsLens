export type ValidationResult = {
  valid: boolean;
  reason?: string;
  warning?: string;
  sanitized: string;
};

export function validateInput(raw: string): ValidationResult {
  const text = raw.trim();

  // 1. Empty
  if (!text) {
    return {
      valid: false,
      reason: "Please paste or type an article before classifying.",
      sanitized: "",
    };
  }

  // 2. Too short
  if (text.length < 20) {
    return {
      valid: false,
      reason: "Article too short. Please paste at least 20 characters.",
      sanitized: text,
    };
  }

  // 3. Too long — truncate
  const MAX = 50000;
  let sanitized = text;
  let warning: string | undefined;

  if (text.length > MAX) {
    sanitized = text.slice(0, MAX);
    warning = `Article truncated to first ${MAX.toLocaleString()} characters.`;
  }

  // 4. No letters at all (gibberish / numbers / emoji only)
  if (!/[a-zA-Z]{2,}/.test(text)) {
    return {
      valid: true,
      warning: "No recognizable English words detected — prediction may be unreliable.",
      sanitized,
    };
  }

  // 5. Too few unique words (repetitive spam)
  const words = text.toLowerCase().match(/[a-z]+/g) || [];
  const unique = new Set(words);
  if (words.length > 5 && unique.size < 3) {
    return {
      valid: true,
      warning: "Repetitive input detected — prediction may be unreliable.",
      sanitized,
    };
  }

  // 6. Non-Latin script (Hindi, Chinese, Arabic, etc.)
  const latinMatches = text.match(/[a-zA-Z]/g);
  const latinRatio = (latinMatches?.length || 0) / text.length;
  if (latinRatio < 0.3 && text.length > 30) {
    return {
      valid: true,
      warning: "Non-English text detected — model is trained on English only.",
      sanitized,
    };
  }

  return { valid: true, sanitized, warning };
}

export function sanitizeForApi(text: string): string {
  return text
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, "")
    .replace(/<[^>]+>/g, "") // strip HTML tags
    .replace(/\u0000/g, "") // remove null bytes
    .trim();
}
