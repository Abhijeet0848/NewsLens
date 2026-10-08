import fs from "fs";
import path from "path";
import Papa from "papaparse";
import type { BBCArticle } from "./types";

export type { BBCArticle };

let cached: BBCArticle[] | null = null;

export function loadBBCDataset(): BBCArticle[] {
  if (cached) return cached;
  const csvPath = path.join(process.cwd(), "data", "bbc-news-data.csv");
  const file = fs.readFileSync(csvPath, "utf-8");
  const { data } = Papa.parse(file, {
    header: true,
    skipEmptyLines: true,
    delimiter: "\t",
  });
  cached = (data as any[])
    .filter((row) => row.category && (row.content || row.title))
    .map((row, i) => ({
      id: i,
      category: (row.category || "").trim().toLowerCase() as BBCArticle["category"],
      title: (row.title || "").trim(),
      content: (row.content || "").trim(),
    }));
  return cached;
}

export function getRandomSamples(count = 6): BBCArticle[] {
  const all = loadBBCDataset();
  return [...all].sort(() => 0.5 - Math.random()).slice(0, count);
}

export function getCategoryCounts(): Record<string, number> {
  return loadBBCDataset().reduce((acc, a) => {
    acc[a.category] = (acc[a.category] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
}

export function getSampleById(id: number): BBCArticle | undefined {
  const all = loadBBCDataset();
  return all.find((a) => a.id === id);
}

export function getSamplesByCategory(category: string, count = 5): BBCArticle[] {
  const all = loadBBCDataset();
  return all.filter((a) => a.category.toLowerCase() === category.toLowerCase()).slice(0, count);
}
