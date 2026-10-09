import { NextRequest, NextResponse } from "next/server";
import * as cheerio from "cheerio";

// In-memory rate limit map (per process)
const rateLimits = new Map<string, number[]>();

function checkRateLimit(ip: string): boolean {
  const now = Date.now();
  const windowMs = 60_000; // 1 minute
  const maxRequests = 10; // 10 requests per minute

  const timestamps = rateLimits.get(ip) || [];
  const recent = timestamps.filter((t) => now - t < windowMs);

  if (recent.length >= maxRequests) return false;

  recent.push(now);
  rateLimits.set(ip, recent);
  return true;
}

export async function POST(req: NextRequest) {
  try {
    const ip = req.headers.get("x-forwarded-for")?.split(",")[0].trim() || "unknown";
    if (!checkRateLimit(ip)) {
      return NextResponse.json(
        { error: "Too many requests. Please slow down." },
        { status: 429 }
      );
    }

    const { url } = await req.json();

    // Validate URL
    if (!url || typeof url !== "string") {
      return NextResponse.json(
        { error: "URL is required" },
        { status: 400 }
      );
    }

    let rawUrl = (url || "").trim();
    if (!/^https?:\/\//i.test(rawUrl)) {
      rawUrl = `https://${rawUrl}`;
    }

    let parsed: URL;
    try {
      parsed = new URL(rawUrl);
    } catch {
      return NextResponse.json(
        { error: "Invalid URL format" },
        { status: 400 }
      );
    }

    // Only allow http/https
    if (!["http:", "https:"].includes(parsed.protocol)) {
      return NextResponse.json(
        { error: "Only HTTP and HTTPS URLs are allowed" },
        { status: 400 }
      );
    }

    // Fetch with browser-like headers
    let res: Response;
    try {
      res = await fetch(parsed.toString(), {
        headers: {
          "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
          Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
          "Accept-Language": "en-US,en;q=0.9",
        },
        redirect: "follow",
        cache: "no-store",
      });
    } catch (networkErr: any) {
      return NextResponse.json(
        { error: "Network error while connecting to URL. Check your connection or the link." },
        { status: 502 }
      );
    }

    if (res.status === 404) {
      return NextResponse.json(
        { error: "Page not found (404) at this URL." },
        { status: 404 }
      );
    }

    if (res.status === 403 || res.status === 401) {
      return NextResponse.json(
        { error: "This website blocks automated fetching. Please copy and paste the article text directly." },
        { status: 403 }
      );
    }

    if (!res.ok) {
      return NextResponse.json(
        { error: `Failed to fetch URL (HTTP ${res.status}). Try pasting the article text directly.` },
        { status: res.status }
      );
    }

    const contentType = res.headers.get("content-type") || "";
    if (contentType && !contentType.includes("text/html") && !contentType.includes("application/xhtml")) {
      return NextResponse.json(
        { error: "The provided URL is not an HTML webpage (e.g. image, PDF, or binary stream)." },
        { status: 415 }
      );
    }

    const html = await res.text();
    const $ = cheerio.load(html);

    // Remove noise elements
    $("script, style, nav, header, footer, aside, iframe, noscript, svg, form, [role='navigation'], [role='banner'], [role='contentinfo'], .advertisement, .ad, .social-share").remove();

    // Try common article containers
    const candidates = [
      "article",
      "main",
      "[role='main']",
      ".article-body",
      ".article-content",
      ".story-body",
      ".story-card",
      ".story-content",
      ".content-body",
      ".post-content",
      ".entry-content",
      "#article-body",
      "#story-body",
      "#content-body",
    ];

    let extractedText = "";
    for (const selector of candidates) {
      const el = $(selector).first();
      if (el.length) {
        // Collect paragraph text within candidate
        const pText = el.find("p").map((_, p) => $(p).text().trim()).get().filter(Boolean).join(" ");
        if (pText.length > 200) {
          extractedText = pText;
          break;
        }
        const fullElText = el.text().trim();
        if (fullElText.length > 300) {
          extractedText = fullElText;
          break;
        }
      }
    }

    // Fallback: all paragraphs across the document
    if (extractedText.length < 200) {
      extractedText = $("p")
        .map((_, el) => $(el).text().trim())
        .get()
        .filter((t) => t.length > 25) // filter out tiny disclaimer / cookie snippets
        .join(" ");
    }

    // Clean up whitespace
    extractedText = extractedText
      .replace(/\s+/g, " ")
      .replace(/\n+/g, "\n")
      .trim();

    if (extractedText.length < 100) {
      return NextResponse.json(
        { error: "Could not find sufficient article text on this page. Please copy and paste the article text." },
        { status: 422 }
      );
    }

    // Cap length to prevent abuse (e.g. 50k chars)
    if (extractedText.length > 50000) {
      extractedText = extractedText.slice(0, 50000);
    }

    const title = $("title").first().text().trim() || $("h1").first().text().trim() || "";

    return NextResponse.json({
      text: extractedText,
      title,
      length: extractedText.length,
    });
  } catch (err: any) {
    console.error("URL extraction error:", err);
    return NextResponse.json(
      { error: "Failed to fetch and process URL. Please paste the article text." },
      { status: 500 }
    );
  }
}
