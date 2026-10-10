import { NextRequest, NextResponse } from "next/server";
import { classifyArticle } from "@/lib/api";
import { sanitizeForApi } from "@/lib/validateInput";

export async function POST(req: NextRequest) {
  try {
    let body;
    try {
      body = await req.json();
    } catch {
      return NextResponse.json(
        { error: "Invalid JSON in request body." },
        { status: 400 }
      );
    }

    const { text, model = "linear-svm" } = body || {};

    if (!text || typeof text !== "string") {
      return NextResponse.json(
        { error: "Text is required. Please paste or type an article." },
        { status: 400 }
      );
    }

    const trimmed = text.trim();

    if (trimmed.length < 20) {
      return NextResponse.json(
        { error: "Article too short. Please provide at least 20 characters." },
        { status: 400 }
      );
    }

    const MAX_LENGTH = 50000;
    const sanitizedText = sanitizeForApi(
      trimmed.length > MAX_LENGTH ? trimmed.slice(0, MAX_LENGTH) : trimmed
    );

    if (sanitizedText.length < 5) {
      return NextResponse.json(
        { error: "Article contains no readable text after sanitization." },
        { status: 400 }
      );
    }

    const result = await classifyArticle(sanitizedText, model);
    return NextResponse.json(result);
  } catch (error: any) {
    console.error("Classification route error:", error);
    return NextResponse.json(
      { error: error.message || "Server error. Please try again." },
      { status: 500 }
    );
  }
}
