import { NextRequest, NextResponse } from "next/server";
import { sanitizeForApi } from "@/lib/validateInput";
import { spawn } from "child_process";
import path from "path";

export async function POST(req: NextRequest) {
  console.log("[classify] request received");
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

    // Call Python inference script via stdin piping to prevent Windows CLI arg issues
    const result = await new Promise((resolve, reject) => {
      const scriptPath = path.join(process.cwd(), "training", "predict.py");
      const py = spawn("python", [scriptPath, "--model", model]);

      let out = "";
      let err = "";

      const timeout = setTimeout(() => {
        py.kill();
        reject(new Error("Classification inference timed out after 10 seconds."));
      }, 10000);

      py.stdout.on("data", (d) => {
        out += d.toString();
      });

      py.stderr.on("data", (d) => {
        err += d.toString();
      });

      py.on("close", (code) => {
        clearTimeout(timeout);
        if (code === 0 && out.trim()) {
          try {
            resolve(JSON.parse(out.trim()));
          } catch (e) {
            reject(new Error(`Failed to parse prediction output: ${out}`));
          }
        } else {
          reject(new Error(`Prediction failed with code ${code}: ${err || out}`));
        }
      });

      py.stdin.write(sanitizedText);
      py.stdin.end();
    });

    console.log("[classify] returning:", (result as any)?.category, `${(result as any)?.confidence_percentage}%`);
    return NextResponse.json(result);
  } catch (error: any) {
    console.error("[classify] Classification route error:", error);
    return NextResponse.json(
      { error: error.message || "Server error. Please try again." },
      { status: 500 }
    );
  }
}
