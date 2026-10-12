import { NextRequest, NextResponse } from "next/server";
import { log } from "@/lib/debug";

export const runtime = "nodejs";        // ensure Node runtime, not Edge
export const dynamic = "force-dynamic"; // no caching

export async function POST(req: NextRequest) {
  const requestId = Math.random().toString(36).slice(2, 10);
  const TAG = `api/${requestId}`;

  log.info(TAG, "=== CLASSIFY REQUEST START ===");
  log.info(TAG, "Environment", {
    VERCEL_URL: process.env.VERCEL_URL,
    VERCEL_ENV: process.env.VERCEL_ENV,
    NODE_ENV: process.env.NODE_ENV,
    BACKEND_URL: process.env.BACKEND_URL,
    VERCEL: process.env.VERCEL,
  });

  try {
    // -------------------------------------
    // 1. Parse request body
    // -------------------------------------
    log.info(TAG, "Step 1: Parsing request body");
    const body = await req.json();
    log.success(TAG, "Body parsed", {
      textLength: body.text?.length,
      model: body.model,
    });

    // -------------------------------------
    // 2. Determine backend URL
    // -------------------------------------
    log.info(TAG, "Step 2: Determining backend URL");

    const isProd = !!process.env.VERCEL;
    const backendUrl = process.env.BACKEND_URL;
    const vercelUrl = process.env.VERCEL_URL;

    let targetUrl: string;

    if (backendUrl) {
      targetUrl = `${backendUrl.replace(/\/$/, "")}/api/classify`;
      log.info(TAG, "Using BACKEND_URL env var");
    } else if (vercelUrl) {
      // Direct call to Python serverless function to prevent self-loop
      targetUrl = `https://${vercelUrl}/api/classify.py`;
      log.info(TAG, "Using VERCEL_URL pointing to Python function /api/classify.py");
    } else {
      targetUrl = "http://127.0.0.1:8000/api/classify";
      log.info(TAG, "Using local FastAPI uvicorn fallback");
    }

    log.success(TAG, "Target URL resolved", {
      targetUrl,
      isProd,
      source: backendUrl ? "BACKEND_URL" : vercelUrl ? "VERCEL_URL" : "fallback",
    });

    // -------------------------------------
    // 3. Check if we're calling ourselves (infinite loop detection)
    // -------------------------------------
    const host = req.headers.get("host");
    const pathname = req.nextUrl?.pathname || "/api/classify";
    const selfCall = !backendUrl && !!host && targetUrl === `https://${host}${pathname}`;
    log.info(TAG, "Self-call check", { host, pathname, selfCall });

    if (selfCall) {
      log.error(TAG, "LOOP DETECTED: API route calling itself");
      log.error(TAG, "Fix: targeting direct Python serverless function /api/classify.py");
      targetUrl = `https://${host}/api/classify.py`;
    }

    // -------------------------------------
    // 4. Call the backend
    // -------------------------------------
    log.info(TAG, "Step 3: Calling backend", { targetUrl });
    const start = Date.now();

    let res: Response;
    try {
      res = await fetch(targetUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Request-ID": requestId,
        },
        body: JSON.stringify(body),
        signal: AbortSignal.timeout(35000),
      });
    } catch (fetchErr: any) {
      const elapsed = Date.now() - start;
      log.error(TAG, "Backend fetch failed", {
        error: String(fetchErr),
        name: fetchErr?.name,
        message: fetchErr?.message,
        elapsedMs: elapsed,
        targetUrl,
      });

      return NextResponse.json(
        {
          error: "Backend unreachable",
          debug: {
            targetUrl,
            elapsedMs: elapsed,
            errorName: fetchErr?.name,
            errorMessage: fetchErr?.message,
            requestId,
          },
        },
        { status: 503 }
      );
    }

    const elapsed = Date.now() - start;
    log.success(TAG, "Backend responded", {
      status: res.status,
      statusText: res.statusText,
      elapsedMs: elapsed,
      headers: Object.fromEntries(res.headers.entries()),
    });

    // -------------------------------------
    // 5. Parse response
    // -------------------------------------
    log.info(TAG, "Step 4: Parsing response body");

    const rawText = await res.text();
    log.info(TAG, "Raw response", {
      length: rawText.length,
      preview: rawText.slice(0, 200),
    });

    if (!res.ok) {
      log.error(TAG, "Backend returned error status", {
        status: res.status,
        body: rawText.slice(0, 500),
      });

      return NextResponse.json(
        {
          error: `Backend error: ${res.status}`,
          debug: {
            backendStatus: res.status,
            backendBody: rawText.slice(0, 500),
            requestId,
          },
        },
        { status: 502 }
      );
    }

    let data;
    try {
      data = JSON.parse(rawText);
    } catch (parseErr) {
      log.error(TAG, "Response is not valid JSON", {
        error: String(parseErr),
        rawText: rawText.slice(0, 500),
      });

      return NextResponse.json(
        {
          error: "Backend returned invalid JSON",
          debug: {
            rawText: rawText.slice(0, 500),
            requestId,
          },
        },
        { status: 502 }
      );
    }

    log.success(TAG, "Response parsed successfully", {
      category: data.category,
      confidence: data.confidence,
    });

    // -------------------------------------
    // 6. Return to client
    // -------------------------------------
    log.info(TAG, "=== CLASSIFY REQUEST END (SUCCESS) ===");

    return NextResponse.json({
      ...data,
      _debug: {
        requestId,
        targetUrl,
        backendLatencyMs: elapsed,
      },
    });
  } catch (err: any) {
    log.error(TAG, "Unhandled error in API route", {
      error: String(err),
      name: err?.name,
      message: err?.message,
      stack: err?.stack,
    });

    return NextResponse.json(
      {
        error: "Internal server error",
        debug: {
          message: err?.message,
          requestId,
        },
      },
      { status: 500 }
    );
  }
}

// GET endpoint for testing and diagnostic verification
export async function GET() {
  return NextResponse.json({
    status: "ok",
    route: "/api/classify",
    timestamp: new Date().toISOString(),
    env: {
      VERCEL: process.env.VERCEL,
      VERCEL_URL: process.env.VERCEL_URL,
      VERCEL_ENV: process.env.VERCEL_ENV,
      BACKEND_URL: process.env.BACKEND_URL,
      NODE_ENV: process.env.NODE_ENV,
    },
  });
}
