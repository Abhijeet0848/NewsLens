import { NextRequest, NextResponse } from "next/server";
import { sanitizeForApi } from "@/lib/validateInput";

const BACKEND = process.env.BACKEND_URL || "http://127.0.0.1:8000";

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

    const { text, model = "svm" } = body || {};

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

    // Proxy directly to persistent in-memory FastAPI backend (< 20ms)
    const res = await fetch(`${BACKEND}/classify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: sanitizedText, model }),
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      return NextResponse.json(
        { error: errData.detail || "Classification failed in backend server." },
        { status: res.status }
      );
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch (error: any) {
    console.error("[classify] Proxy error:", error);
    return NextResponse.json(
      {
        error:
          "Inference backend unavailable. Please ensure FastAPI is running (uvicorn api.main:app --port 8000).",
      },
      { status: 502 }
    );
  }
}
