import { NextRequest, NextResponse } from "next/server";
import { classifyArticle } from "@/lib/api";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { text, model = "linear-svm" } = body;

    if (!text || typeof text !== "string" || text.trim().length === 0) {
      return NextResponse.json(
        { error: "Invalid text input. Please provide article text." },
        { status: 400 }
      );
    }

    const result = await classifyArticle(text, model);
    return NextResponse.json(result);
  } catch (error: any) {
    console.error("Classification route error:", error);
    return NextResponse.json(
      { error: error.message || "Classification failed" },
      { status: 500 }
    );
  }
}
