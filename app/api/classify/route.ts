import { NextRequest, NextResponse } from "next/server";

function getBackendUrl() {
  if (process.env.BACKEND_URL) {
    return process.env.BACKEND_URL;
  }
  if (process.env.VERCEL_URL) {
    return `https://${process.env.VERCEL_URL}/api/index`;
  }
  return "http://127.0.0.1:8000/api/classify";
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const backendUrl = getBackendUrl();

    const res = await fetch(backendUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(35000),
    });

    if (!res.ok) {
      const errText = await res.text();
      console.error("[classify] Backend error:", errText);
      return NextResponse.json(
        { error: `Classification failed (${res.status})` },
        { status: 502 }
      );
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch (err: any) {
    console.error("[classify] Error:", err);
    return NextResponse.json(
      { error: "Backend unreachable. Please try again." },
      { status: 503 }
    );
  }
}
