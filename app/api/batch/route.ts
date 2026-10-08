import { NextRequest, NextResponse } from "next/server";
import { processBatchCSV } from "@/lib/api";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { rows } = body;

    if (!Array.isArray(rows) || rows.length === 0) {
      return NextResponse.json(
        { error: "Invalid rows array. Please provide a list of article items." },
        { status: 400 }
      );
    }

    const results = await processBatchCSV(rows);
    return NextResponse.json({
      total: results.length,
      results,
    });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || "Batch processing failed" },
      { status: 500 }
    );
  }
}
