"use client";

import * as React from "react";
import {
  Upload,
  FileSpreadsheet,
  Download,
  Search,
  RefreshCw,
  Zap,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { fetchRandomSamples, processBatchCSV } from "@/lib/api";
import { getCategoryConfig } from "@/lib/utils";
import { toast } from "sonner";

interface BatchRowResult {
  id: string;
  title: string;
  text: string;
  predicted_category: string;
  confidence: number;
  keywords: string;
  latency_ms: number;
}

export default function BatchUploadPage() {
  const [file, setFile] = React.useState<File | null>(null);
  const [isProcessing, setIsProcessing] = React.useState(false);
  const [progress, setProgress] = React.useState(0);
  const [completedCount, setCompletedCount] = React.useState(0);
  const [totalCount, setTotalCount] = React.useState(0);
  const [results, setResults] = React.useState<BatchRowResult[]>([]);
  const [searchQuery, setSearchQuery] = React.useState("");
  const [categoryFilter, setCategoryFilter] = React.useState("All");
  const fileInputRef = React.useRef<HTMLInputElement | null>(null);

  // Load real BBC sample batch dataset
  const handleLoadDemoCSV = async () => {
    setIsProcessing(true);
    setProgress(0);
    setResults([]);

    try {
      const bbcSamples = await fetchRandomSamples(10);
      const demoRows = bbcSamples.map((s, idx) => ({
        id: `bbc-${idx + 1}`,
        title: s.title,
        text: s.content || s.title,
      }));

      setTotalCount(demoRows.length);

      const res = await processBatchCSV(demoRows, (completed, total) => {
        setCompletedCount(completed);
        setProgress(Math.round((completed / total) * 100));
      });
      setResults(res);
      toast.success(`Processed ${res.length} real BBC articles!`);
    } catch {
      toast.error("Batch processing failed");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = e.target.files?.[0];
    if (!uploadedFile) return;

    setFile(uploadedFile);
    const text = await uploadedFile.text();
    const lines = text.split("\n").filter((l) => l.trim().length > 0);

    const parsedRows = lines.slice(1).map((line, idx) => {
      const parts = line.split(",");
      const title = parts[0]?.replace(/"/g, "") || `Item #${idx + 1}`;
      const bodyText = parts.slice(1).join(",").replace(/"/g, "") || title;
      return { id: `row-${idx + 1}`, title, text: bodyText };
    });

    if (parsedRows.length === 0) {
      toast.error("No valid data rows found in CSV.");
      return;
    }

    setIsProcessing(true);
    setProgress(0);
    setTotalCount(parsedRows.length);
    setResults([]);

    try {
      const res = await processBatchCSV(parsedRows, (completed, total) => {
        setCompletedCount(completed);
        setProgress(Math.round((completed / total) * 100));
      });
      setResults(res);
      toast.success(`Processed ${res.length} rows from CSV!`);
    } catch {
      toast.error("Batch processing error");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleExportCSV = () => {
    if (results.length === 0) return;
    const header = "id,title,predicted_category,confidence_pct,keywords,latency_ms\n";
    const rows = results
      .map(
        (r) =>
          `"${r.id}","${r.title.replace(/"/g, '""')}","${r.predicted_category}","${r.confidence}","${r.keywords}","${r.latency_ms}"`
      )
      .join("\n");
    const blob = new Blob([header + rows], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `newsscope-batch-results-${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
    toast.success("CSV results exported!");
  };

  const filteredResults = results.filter((r) => {
    const matchSearch =
      r.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.keywords.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.predicted_category.toLowerCase().includes(searchQuery.toLowerCase());
    const matchCat =
      categoryFilter === "All" || r.predicted_category === categoryFilter;
    return matchSearch && matchCat;
  });

  const avgConfidence = results.length
    ? Math.round(
        results.reduce((acc, r) => acc + r.confidence, 0) / results.length
      )
    : 0;

  const categoryDistribution = results.reduce((acc, r) => {
    acc[r.predicted_category] = (acc[r.predicted_category] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  return (
    <div className="mx-auto max-w-7xl px-5 md:px-8 pt-8 md:pt-12 pb-16 md:pb-20 space-y-6 md:space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div className="space-y-1">
          <span className="text-[10px] md:text-[11px] uppercase tracking-widest text-[#0891b2] font-mono font-semibold block">
            BULK PROCESSING PIPELINE
          </span>
          <h1 className="font-heading text-2xl sm:text-3xl font-semibold tracking-tight text-[#0f0f0e]">
            Batch CSV Classifier
          </h1>
          <p className="text-[13px] md:text-sm text-[#3f3d3a] max-w-2xl leading-relaxed">
            Upload CSV datasets with article headlines and text columns. Process hundreds of news items simultaneously.
          </p>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <Button
            variant="secondary"
            size="sm"
            onClick={handleLoadDemoCSV}
            disabled={isProcessing}
            className="gap-2 h-11 sm:h-10 px-4 rounded-xl text-xs font-medium w-full sm:w-auto border border-[#e7e3dd] shadow-sm text-[#3f3d3a]"
          >
            <Zap className="size-4 text-indigo-600" />
            <span>Load Sample Dataset</span>
          </Button>
        </div>
      </div>

      <div className="border-t border-[#e7e3dd]" />

      {/* Drag Drop CSV Upload Box */}
      <div
        onClick={() => fileInputRef.current?.click()}
        className="flex min-h-[180px] cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-[#e7e3dd] bg-[#fdfcfb] p-8 text-center shadow-sm hover:border-indigo-400 hover:bg-[#f1efeb] transition-all"
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv,.txt"
          className="hidden"
          onChange={handleFileChange}
        />
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#f1efeb] text-indigo-600 mb-3 border border-[#e7e3dd]">
          <FileSpreadsheet className="size-6" />
        </div>
        <p className="text-sm font-medium text-[#1c1b1a]">
          Drop your news article CSV here, or click to upload
        </p>
        <p className="text-xs text-[#57534e] mt-1 font-mono">
          Required header columns: <code>title, text</code>
        </p>
      </div>

      {/* Progress Bar */}
      {isProcessing && (
        <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-6 shadow-md space-y-3">
          <div className="flex items-center justify-between text-xs font-mono">
            <span className="text-[#1c1b1a] font-medium flex items-center gap-2">
              <RefreshCw className="size-3.5 animate-spin text-indigo-600" />
              Processing Batch Stream: {completedCount} / {totalCount} articles
            </span>
            <span className="text-[#0891b2] font-bold">{progress}%</span>
          </div>
          <Progress value={progress} />
        </div>
      )}

      {/* Summary Stat Cards */}
      {results.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="rounded-xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 shadow-sm">
            <span className="text-xs font-mono text-[#a8a29e]">Total Classified</span>
            <div className="font-heading text-2xl font-semibold text-[#1c1b1a] mt-1">
              {results.length}
            </div>
          </div>
          <div className="rounded-xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 shadow-sm">
            <span className="text-xs font-mono text-[#a8a29e]">Average Confidence</span>
            <div className="font-heading text-2xl font-semibold text-[#059669] mt-1">
              {avgConfidence}%
            </div>
          </div>
          <div className="rounded-xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 shadow-sm">
            <span className="text-xs font-mono text-[#a8a29e]">Distinct Domains</span>
            <div className="font-heading text-2xl font-semibold text-[#0891b2] mt-1">
              {Object.keys(categoryDistribution).length}
            </div>
          </div>
          <div className="rounded-xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 shadow-sm flex items-center justify-center">
            <Button
              variant="default"
              size="sm"
              onClick={handleExportCSV}
              className="gap-2 w-full text-xs h-10"
            >
              <Download className="size-4" />
              <span>Export CSV</span>
            </Button>
          </div>
        </div>
      )}

      {/* Filter & Table */}
      {results.length > 0 && (
        <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] shadow-lg p-6 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="relative flex-1 max-w-sm">
              <Search className="absolute left-3 top-2.5 size-4 text-[#a8a29e]" />
              <input
                type="text"
                placeholder="Search by title, category, keyword..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full rounded-lg border border-[#e7e3dd] bg-[#f1efeb] pl-9 pr-4 py-2 text-xs text-[#1c1b1a] placeholder:text-[#a8a29e] focus:bg-[#fdfcfb] focus:border-indigo-400 focus:outline-none"
              />
            </div>

            <div className="flex items-center gap-2">
              <span className="text-xs text-[#57534e] font-mono">Category Filter:</span>
              <select
                value={categoryFilter}
                onChange={(e) => setCategoryFilter(e.target.value)}
                className="rounded-lg border border-[#e7e3dd] bg-[#fdfcfb] px-3 py-1.5 text-xs text-[#1c1b1a] focus:outline-none focus:border-indigo-400"
              >
                <option value="All">All Categories</option>
                {Object.keys(categoryDistribution).map((cat) => (
                  <option key={cat} value={cat}>
                    {cat} ({categoryDistribution[cat]})
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="overflow-x-auto rounded-xl border border-[#e7e3dd]">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#f1efeb] text-[#57534e] font-mono uppercase tracking-wider">
                <tr>
                  <th className="p-3">#</th>
                  <th className="p-3">Article Title</th>
                  <th className="p-3">Category</th>
                  <th className="p-3">Confidence</th>
                  <th className="p-3">Salient Keywords</th>
                  <th className="p-3">Latency</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#e7e3dd] font-sans">
                {filteredResults.map((row, idx) => {
                  const cfg = getCategoryConfig(row.predicted_category);
                  return (
                    <tr
                      key={row.id}
                      className="hover:bg-[#f1efeb] transition-colors"
                    >
                      <td className="p-3 font-mono text-[#a8a29e]">{idx + 1}</td>
                      <td className="p-3 font-medium text-[#1c1b1a] max-w-xs truncate">
                        {row.title}
                      </td>
                      <td className="p-3">
                        <span
                          className={`inline-flex items-center px-2 py-0.5 rounded border text-[11px] font-medium ${cfg.badgeClass}`}
                        >
                          {row.predicted_category}
                        </span>
                      </td>
                      <td className="p-3 font-mono text-[#1c1b1a] font-semibold">
                        {row.confidence}%
                      </td>
                      <td className="p-3 font-mono text-[#57534e] max-w-xs truncate text-[11px]">
                        {row.keywords}
                      </td>
                      <td className="p-3 font-mono text-[#0891b2] text-[11px]">
                        {row.latency_ms}ms
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
