import { NextResponse } from "next/server";
import { loadBBCDataset, getRandomSamples, getCategoryCounts, getSampleById } from "@/lib/dataset";

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const mode = searchParams.get("mode") || "summary";
    const count = parseInt(searchParams.get("count") || "6", 10);
    const id = searchParams.get("id");

    if (id !== null) {
      const sample = getSampleById(parseInt(id, 10));
      if (!sample) {
        return NextResponse.json({ error: "Article not found" }, { status: 404 });
      }
      return NextResponse.json(sample);
    }

    if (mode === "samples") {
      const samples = getRandomSamples(count);
      return NextResponse.json(samples);
    }

    const all = loadBBCDataset();
    const counts = getCategoryCounts();
    const samples = getRandomSamples(count);

    return NextResponse.json({
      totalArticles: all.length,
      categoryCounts: counts,
      categories: Object.keys(counts),
      samples,
    });
  } catch (error: any) {
    return NextResponse.json(
      { error: "Failed to load BBC dataset", details: error.message },
      { status: 500 }
    );
  }
}
