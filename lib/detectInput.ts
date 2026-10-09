export type InputType = "url" | "text" | "empty";

/**
 * Detects whether the given input string is a URL, raw article text, or empty.
 */
export function detectInput(value: string): InputType {
  const trimmed = value.trim();
  if (!trimmed) return "empty";

  // URL regex — matches http(s)://... or bare domains
  const urlPattern = /^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w\-./?%&=#:]*)?$/i;

  // Check if the entire input is a single URL (no spaces except maybe one at start/end)
  const lines = trimmed.split(/\s+/);
  if (lines.length === 1 && urlPattern.test(lines[0])) {
    return "url";
  }

  return "text";
}


/**
 * Extracts a clean domain name for UI chips (e.g. "thehindu.com", "bbc.com")
 */
export function getDomain(url: string): string {
  try {
    let normalized = url.trim();
    if (!/^https?:\/\//i.test(normalized)) {
      normalized = "https://" + normalized;
    }
    const hostname = new URL(normalized).hostname;
    return hostname.replace(/^www\./i, "");
  } catch {
    return url.slice(0, 30);
  }
}

/**
 * Normalizes URL with https:// protocol if missing
 */
export function normalizeUrl(url: string): string {
  const trimmed = url.trim();
  if (!/^https?:\/\//i.test(trimmed)) {
    return `https://${trimmed}`;
  }
  return trimmed;
}
