"use client";

import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  FileText,
  Upload,
  Link2,
  Trash2,
  Clipboard,
  Shuffle,
  Zap,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { fetchRandomSamples, fetchArticleFromUrl } from "@/lib/api";
import { toast } from "sonner";
import { tabContentVariant } from "@/lib/motion";
import { cn } from "@/lib/utils";

interface ClassifierInputProps {
  text: string;
  onChangeText: (val: string) => void;
  selectedModel: string;
  onChangeModel: (model: string) => void;
  onClassify: () => void;
  isLoading: boolean;
}

const AVAILABLE_MODELS = [
  {
    id: "distilbert",
    name: "DistilBERT",
    tag: "Neural",
    desc: "Transformer Attention",
  },
  {
    id: "linear_svm",
    name: "Linear SVM",
    tag: "Hyperplane",
    desc: "Maximum-Margin Boundary",
  },
  {
    id: "mlp",
    name: "Neural MLP",
    tag: "Baseline",
    desc: "Multi-Layer Perceptron",
  },
];

export function ClassifierInput({
  text,
  onChangeText,
  selectedModel,
  onChangeModel,
  onClassify,
  isLoading,
}: ClassifierInputProps) {
  const [activeInputTab, setActiveInputTab] = React.useState<"text" | "upload" | "url">("text");
  const [urlInput, setUrlInput] = React.useState("");
  const [isFetchingUrl, setIsFetchingUrl] = React.useState(false);
  const [dragOver, setDragOver] = React.useState(false);
  const fileInputRef = React.useRef<HTMLInputElement | null>(null);

  const charCount = text.length;
  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  const isMinimumReached = charCount >= 50;

  const handlePasteClipboard = async () => {
    try {
      if (navigator.clipboard && navigator.clipboard.readText) {
        const clip = await navigator.clipboard.readText();
        if (clip) {
          onChangeText(clip);
          toast.success("Pasted text from clipboard");
        }
      }
    } catch {
      toast.error("Clipboard permission required");
    }
  };

  const handleClear = () => {
    onChangeText("");
    toast.info("Input cleared");
  };

  const handleRandomSample = async () => {
    try {
      const samples = await fetchRandomSamples(1);
      if (samples && samples.length > 0) {
        const sample = samples[0];
        onChangeText(sample.content || sample.title);
        toast.success(`Loaded BBC ${sample.category.toUpperCase()}: "${sample.title.slice(0, 30)}..."`);
      }
    } catch {
      toast.error("Could not load sample article");
    }
  };

  const handleUrlFetch = async () => {
    if (!urlInput.trim()) {
      toast.error("Please enter a valid news URL");
      return;
    }
    setIsFetchingUrl(true);
    try {
      const extractedText = await fetchArticleFromUrl(urlInput);
      onChangeText(extractedText);
      setActiveInputTab("text");
      toast.success("Article extracted from URL");
    } catch (err: any) {
      toast.error(err.message || "Failed to parse URL article");
    } finally {
      setIsFetchingUrl(false);
    }
  };

  const handleFileUpload = (file: File) => {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      if (content) {
        onChangeText(content);
        setActiveInputTab("text");
        toast.success(`Uploaded "${file.name}"`);
      }
    };
    reader.readAsText(file);
  };

  // Keyboard shortcut: Cmd/Ctrl + Enter to classify
  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
        if (isMinimumReached && !isLoading) {
          e.preventDefault();
          onClassify();
        }
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isMinimumReached, isLoading, onClassify]);

  const tabsList = [
    { id: "text", label: "Paste Text", icon: FileText },
    { id: "upload", label: "Upload", icon: Upload },
    { id: "url", label: "URL", icon: Link2 },
  ] as const;

  return (
    <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-6 md:p-7 shadow-[0_1px_2px_rgba(28,27,26,0.04),0_8px_24px_-8px_rgba(28,27,26,0.06)] hover:shadow-[0_1px_2px_rgba(28,27,26,0.06),0_12px_32px_-8px_rgba(28,27,26,0.10)] transition-shadow duration-200 flex flex-col justify-between h-full">
      <div>
        {/* Card Header (icon + title + tabs) */}
        <div className="flex flex-col sm:flex-row items-start justify-between gap-4 mb-6">
          <div className="flex items-start gap-3">
            <div className="flex size-9 items-center justify-center rounded-lg bg-[#eef2ff] text-[#4f46e5] flex-shrink-0">
              <FileText className="size-4" />
            </div>
            <div>
              <h3 className="text-[15px] font-semibold text-[#0f0f0e]">
                Article Content Input
              </h3>
              <p className="text-[12px] text-[#a8a29e] mt-0.5 max-w-xs leading-normal">
                Paste raw text, upload documents, or load BBC benchmark samples.
              </p>
            </div>
          </div>

          {/* Tab Control */}
          <div className="bg-[#f1efeb] rounded-lg p-1 inline-flex gap-0.5 self-stretch sm:self-start flex-shrink-0">
            {tabsList.map((tab) => {
              const isActive = activeInputTab === tab.id;
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  type="button"
                  onClick={() => setActiveInputTab(tab.id)}
                  className={cn(
                    "relative h-8 px-3 rounded-md flex items-center justify-center gap-1.5 text-[12px] font-medium transition-colors z-10 flex-1 sm:flex-initial",
                    isActive
                      ? "bg-[#fdfcfb] text-[#0f0f0e] font-semibold shadow-[0_1px_2px_rgba(28,27,26,0.06)] ring-1 ring-inset ring-[#0f0f0e]/[0.04]"
                      : "text-[#6b6660] hover:text-[#0f0f0e]"
                  )}
                >
                  {isActive && (
                    <motion.div
                      layoutId="input-tab"
                      transition={{ type: "spring", stiffness: 400, damping: 32 }}
                      className="absolute inset-0 rounded-md bg-[#fdfcfb] shadow-[0_1px_2px_rgba(28,27,26,0.06)] ring-1 ring-inset ring-[#0f0f0e]/[0.04] -z-10"
                    />
                  )}
                  <Icon className="size-3.5 flex-shrink-0" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Input Body with AnimatePresence */}
        <div>
          <AnimatePresence mode="wait">
            {activeInputTab === "text" && (
              <motion.div
                key="tab-text"
                variants={tabContentVariant}
                initial="initial"
                animate="animate"
                exit="exit"
              >
                <textarea
                  className="w-full min-h-[220px] md:min-h-[260px] rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-5 text-[14px] leading-relaxed text-[#0f0f0e] shadow-[inset_0_1px_2px_rgba(28,27,26,0.02)] placeholder:text-[#a8a29e] focus:bg-[#fdfcfb] focus:border-[#4f46e5]/40 focus:outline-none focus:ring-4 focus:ring-[#4f46e5]/[0.08] transition-all duration-200 resize-y"
                  placeholder="Paste or type any news article text here (business, entertainment, politics, sport, tech)..."
                  value={text}
                  onChange={(e) => onChangeText(e.target.value)}
                />

                {/* Footer Row */}
                <div className="mt-4 flex flex-col md:flex-row md:items-center md:justify-between gap-3">
                  {/* Left Group */}
                  <div className="flex items-center gap-1.5 flex-wrap">
                    <button
                      type="button"
                      onClick={handlePasteClipboard}
                      className="h-8 px-3 rounded-md bg-transparent border border-[#e7e3dd] text-[12px] font-medium text-[#57534e] hover:bg-[#f1efeb] hover:text-[#0f0f0e] hover:border-[#d6d1c9] transition-colors duration-150 flex items-center gap-1.5 shadow-sm"
                    >
                      <Clipboard className="size-3.5 text-[#6b6660]" />
                      <span>Paste</span>
                    </button>
                    <button
                      type="button"
                      onClick={handleRandomSample}
                      className="h-8 px-3 rounded-md bg-transparent border border-[#e7e3dd] text-[12px] font-medium text-[#57534e] hover:bg-[#f1efeb] hover:text-[#0f0f0e] hover:border-[#d6d1c9] transition-colors duration-150 flex items-center gap-1.5 shadow-sm"
                    >
                      <Shuffle className="size-3.5 text-[#6b6660]" />
                      <span>BBC Sample</span>
                    </button>
                    <button
                      type="button"
                      onClick={handleClear}
                      className="h-8 px-3 rounded-md bg-transparent border border-[#e7e3dd] text-[12px] font-medium text-[#57534e] hover:bg-[#f1efeb] hover:text-[#dc2626] hover:border-[#d6d1c9] transition-colors duration-150 flex items-center gap-1.5 shadow-sm"
                    >
                      <Trash2 className="size-3.5" />
                      <span>Clear</span>
                    </button>
                  </div>

                  {/* Right Group */}
                  <div className="flex items-center justify-between md:justify-end gap-3">
                    <span className="text-[11px] font-mono text-[#a8a29e] tabular-nums">
                      {wordCount} words &bull; {charCount} chars
                    </span>
                    <div className="hidden md:inline-flex items-center gap-1 text-[#a8a29e] text-[11px]">
                      <span>&bull;</span>
                      <kbd className="bg-[#f1efeb] border border-[#e7e3dd] rounded px-1.5 py-0.5 text-[10px] font-mono text-[#57534e]">
                        ⌘
                      </kbd>
                      <span>+</span>
                      <kbd className="bg-[#f1efeb] border border-[#e7e3dd] rounded px-1.5 py-0.5 text-[10px] font-mono text-[#57534e]">
                        Enter
                      </kbd>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            {activeInputTab === "upload" && (
              <motion.div
                key="tab-upload"
                variants={tabContentVariant}
                initial="initial"
                animate="animate"
                exit="exit"
                onDragOver={(e) => {
                  e.preventDefault();
                  setDragOver(true);
                }}
                onDragLeave={() => setDragOver(false)}
                onDrop={(e) => {
                  e.preventDefault();
                  setDragOver(false);
                  if (e.dataTransfer.files?.[0]) {
                    handleFileUpload(e.dataTransfer.files[0]);
                  }
                }}
                onClick={() => fileInputRef.current?.click()}
                className={cn(
                  "flex min-h-[220px] md:min-h-[260px] cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed p-6 text-center transition-all",
                  dragOver
                    ? "border-[#4f46e5] bg-[#eef2ff]"
                    : "border-[#e7e3dd] bg-[#faf9f6] hover:bg-[#f1efeb]"
                )}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".txt,.csv,.json,.pdf,.doc"
                  className="hidden"
                  onChange={(e) => {
                    if (e.target.files?.[0]) {
                      handleFileUpload(e.target.files[0]);
                    }
                  }}
                />
                <div className="flex size-11 items-center justify-center rounded-xl bg-[#fdfcfb] text-[#4f46e5] mb-3 border border-[#e7e3dd] shadow-sm">
                  <Upload className="size-5 text-[#4f46e5]" />
                </div>
                <p className="text-[14px] font-semibold text-[#0f0f0e]">
                  Drag & drop news document, or click to browse
                </p>
                <p className="text-[12px] text-[#a8a29e] mt-1">Supports .txt, .csv, .json text payloads</p>
              </motion.div>
            )}

            {activeInputTab === "url" && (
              <motion.div
                key="tab-url"
                variants={tabContentVariant}
                initial="initial"
                animate="animate"
                exit="exit"
                className="space-y-3 py-6 min-h-[220px] md:min-h-[260px] flex flex-col justify-center"
              >
                <div className="flex flex-col sm:flex-row gap-2">
                  <input
                    type="url"
                    placeholder="https://www.bbc.com/news/..."
                    value={urlInput}
                    onChange={(e) => setUrlInput(e.target.value)}
                    className="flex-1 rounded-xl border border-[#e7e3dd] bg-[#faf9f6] px-4 py-2.5 text-[14px] text-[#0f0f0e] placeholder:text-[#a8a29e] focus:bg-[#fdfcfb] focus:border-[#4f46e5]/40 focus:outline-none focus:ring-4 focus:ring-[#4f46e5]/[0.08] transition-all"
                  />
                  <Button
                    onClick={handleUrlFetch}
                    disabled={isFetchingUrl}
                    variant="secondary"
                    className="gap-1.5 h-10 px-4 text-xs font-medium w-full sm:w-auto rounded-lg border border-[#e7e3dd] bg-[#fdfcfb] hover:bg-[#f1efeb]"
                  >
                    <Link2 className="size-4 text-[#4f46e5]" />
                    <span>Fetch</span>
                  </Button>
                </div>
                <p className="text-[12px] text-[#a8a29e]">
                  Enter an article URL or paste text directly.
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Model Selection Row */}
        <div className="border-t border-[#f1efeb] pt-5 mt-6">
          <label className="text-[10px] uppercase tracking-[0.14em] text-[#a8a29e] font-semibold mb-3 block">
            CLASSIFICATION ARCHITECTURE
          </label>

          <div className="grid grid-cols-3 gap-2">
            {AVAILABLE_MODELS.map((m) => {
              const isSelected = selectedModel === m.id;
              return (
                <button
                  key={m.id}
                  type="button"
                  onClick={() => onChangeModel(m.id)}
                  className={cn(
                    "relative h-[72px] p-3 rounded-xl text-left flex flex-col justify-between transition-all duration-200 cursor-pointer border",
                    isSelected
                      ? "bg-[#eef2ff] border-[#c7d2fe] ring-1 ring-[#4f46e5]/10 shadow-sm"
                      : "bg-[#faf9f6] border-[#e7e3dd] hover:bg-[#f1efeb] hover:border-[#d6d1c9] hover:-translate-y-px"
                  )}
                >
                  <div className="flex w-full items-center justify-between gap-1">
                    <span className="text-[12px] font-semibold text-[#0f0f0e] leading-snug">{m.name}</span>
                    <span className="text-[10px] font-mono text-[#a8a29e] tabular-nums flex-shrink-0">
                      {m.tag}
                    </span>
                  </div>
                  <span className="text-[10px] text-[#6b6660] leading-tight line-clamp-1">
                    {m.desc}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Classify Button — Solid Black, Confident CTA */}
      <div className="mt-5">
        <button
          type="button"
          onClick={onClassify}
          disabled={!isMinimumReached || isLoading}
          className="w-full h-12 rounded-xl bg-[#0f0f0e] text-white text-[14px] font-medium shadow-[0_2px_8px_rgba(15,15,14,0.15)] hover:bg-[#2a2a28] hover:shadow-[0_4px_12px_rgba(15,15,14,0.20)] hover:-translate-y-px active:scale-[0.99] transition-all duration-200 flex items-center justify-center disabled:opacity-50 disabled:pointer-events-none disabled:hover:translate-y-0"
        >
          <AnimatePresence mode="wait">
            {isLoading ? (
              <motion.div
                key="loading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex items-center gap-2"
              >
                <span className="size-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                <span>Classifying Article...</span>
              </motion.div>
            ) : (
              <motion.div
                key="idle"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex items-center"
              >
                <Zap className="size-4 mr-2 text-white" />
                <span>Classify Article Now</span>
              </motion.div>
            )}
          </AnimatePresence>
        </button>
      </div>
    </div>
  );
}
