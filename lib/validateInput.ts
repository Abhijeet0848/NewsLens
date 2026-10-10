export type ValidationResult = {
  valid: boolean;
  reason?: string;
  warning?: string;
  sanitized: string;
};

export function sanitizeForApi(text: string): string {
  return text
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, "")
    .replace(/<[^>]+>/g, "") // strip HTML tags
    .replace(/\u0000/g, "") // remove null bytes
    .trim();
}

export function validateInput(raw: string): ValidationResult {
  const cleanInitial = sanitizeForApi(raw || "");

  // 1. Empty or sanitized to empty (<script> tags, blank whitespace)
  if (!cleanInitial) {
    return {
      valid: false,
      reason: "Please paste an article first",
      sanitized: "",
    };
  }

  // 2. Too short
  if (cleanInitial.length < 20) {
    return {
      valid: false,
      reason: "Article too short — please provide at least 20 characters.",
      sanitized: cleanInitial,
    };
  }

  // 3. Too long — truncate to 50,000 characters
  const MAX = 50000;
  let sanitized = cleanInitial;
  let warning: string | undefined;

  if (cleanInitial.length > MAX) {
    sanitized = cleanInitial.slice(0, MAX);
    warning = `Article truncated to first ${MAX.toLocaleString()} characters.`;
  }

  // 4. No recognizable English words (gibberish / numbers / emoji only)
  if (!/[a-zA-Z]{2,}/.test(sanitized)) {
    return {
      valid: true,
      warning: "No recognizable English words detected — prediction may be unreliable.",
      sanitized,
    };
  }

  // 5. Too few unique words (repetitive spam)
  const words = sanitized.toLowerCase().match(/[a-z]+/g) || [];
  const unique = new Set(words);
  if (words.length > 5 && unique.size < 3) {
    return {
      valid: true,
      warning: "Repetitive input detected — prediction may be unreliable.",
      sanitized,
    };
  }

  // 6. Non-Latin script (Hindi, Chinese, Arabic, etc.)
  const latinMatches = sanitized.match(/[a-zA-Z]/g);
  const latinRatio = (latinMatches?.length || 0) / sanitized.length;
  if (latinRatio < 0.3 && sanitized.length > 30) {
    return {
      valid: true,
      warning: "Currently only supports English text — predictions on other languages may be unreliable.",
      sanitized,
    };
  }

  return { valid: true, sanitized, warning };
}
