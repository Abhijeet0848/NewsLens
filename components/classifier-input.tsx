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
    <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-5 md:p-8 pb-8 shadow-[0_8px_24px_rgba(15,15,14,0.06),0_2px_6px_rgba(15,15,14,0.04)] flex flex-col justify-between h-full">
      <div className="space-y-6">
        {/* Header Row: Stacked on mobile */}
        <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
          <div className="flex items-start gap-3">
            <div className="flex size-9 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600 border border-indigo-100 flex-shrink-0">
              <FileText className="size-4" />
            </div>
            <div className="flex flex-col">
              <h3 className="text-base font-semibold text-[#0f0f0e] font-heading">
                Article Content Input
              </h3>
              <p className="text-[13px] text-[#6b6660] mt-0.5 max-w-xs leading-normal">
                Paste raw text, upload documents, or load BBC benchmark samples.
              </p>
            </div>
          </div>

          {/* Tab Pills: 3-column grid on mobile */}
          <div className="bg-[#f1efeb] rounded-lg p-0.5 grid grid-cols-3 md:flex gap-0.5 border border-[#e7e3dd] w-full md:w-auto flex-shrink-0 self-stretch md:self-start">
            {tabsList.map((tab) => {
              const isActive = activeInputTab === tab.id;
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  type="button"
                  onClick={() => setActiveInputTab(tab.id)}
                  className={cn(
                    "relative flex items-center justify-center px-2 md:px-3 py-1.5 rounded-md text-[11px] md:text-[13px] font-medium transition-colors z-10",
                    isActive ? "text-[#0f0f0e] font-semibold" : "text-[#6b6660] hover:text-[#0f0f0e]"
                  )}
                >
                  {isActive && (
                    <motion.div
                      layoutId="classifier-input-tab-pill"
                      transition={{ type: "spring", stiffness: 400, damping: 32 }}
                      className="absolute inset-0 rounded-md bg-[#fdfcfb] shadow-sm ring-1 ring-[#e7e3dd] -z-10"
                    />
                  )}
                  <Icon className="size-3 md:size-3.5 mr-1 md:mr-1.5 flex-shrink-0" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Input Body with AnimatePresence */}
        <div className="min-h-[200px] md:min-h-[260px] mt-4 md:mt-6">
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
                  className="w-full min-h-[200px] md:min-h-[260px] rounded-xl border border-[#e7e3dd] bg-[#f1efeb] p-4 md:p-5 text-[14px] md:text-[15px] leading-relaxed text-[#0f0f0e] shadow-[inset_0_1px_2px_rgba(15,15,14,0.03)] placeholder:text-[#8a847d] focus:bg-[#fdfcfb] focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/10 transition-all duration-200 resize-y"
                  placeholder="Paste or type any news article text here (business, entertainment, politics, sport, tech)..."
                  value={text}
                  onChange={(e) => onChangeText(e.target.value)}
                />

                {/* Footer Row */}
                <div className="mt-4 md:mt-5 flex flex-col md:flex-row md:items-center md:justify-between gap-3 text-xs">
                  {/* Left Group (3 button grid on mobile) */}
                  <div className="grid grid-cols-3 md:flex items-center gap-2 w-full md:w-auto">
                    <motion.button
                      whileHover={{ y: -1 }}
                      whileTap={{ scale: 0.97 }}
                      type="button"
                      onClick={handlePasteClipboard}
                      className="flex items-center justify-center gap-1.5 rounded-lg border border-[#e7e3dd] bg-[#fdfcfb] px-2 md:px-3 py-1.5 h-9 text-[12px] font-medium text-[#3f3d3a] hover:text-[#0f0f0e] hover:bg-[#f1efeb] shadow-sm transition-colors"
                    >
                      <Clipboard className="size-3.5 text-[#6b6660]" />
                      <span>Paste</span>
                    </motion.button>
                    <motion.button
                      whileHover={{ y: -1 }}
                      whileTap={{ scale: 0.97 }}
                      type="button"
                      onClick={handleRandomSample}
                      className="flex items-center justify-center gap-1.5 rounded-lg border border-[#e7e3dd] bg-[#fdfcfb] px-2 md:px-3 py-1.5 h-9 text-[12px] font-medium text-[#3f3d3a] hover:text-[#0f0f0e] hover:bg-[#f1efeb] shadow-sm transition-colors"
                    >
                      <Shuffle className="size-3.5 text-[#6b6660]" />
                      <span className="truncate">BBC Sample</span>
                    </motion.button>
                    <motion.button
                      whileHover={{ y: -1 }}
                      whileTap={{ scale: 0.97 }}
                      type="button"
                      onClick={handleClear}
                      className="flex items-center justify-center gap-1.5 rounded-lg border border-[#e7e3dd] bg-[#fdfcfb] px-2 md:px-3 py-1.5 h-9 text-[12px] font-medium text-[#3f3d3a] hover:text-[#dc2626] hover:bg-[#fff1f2] shadow-sm transition-colors"
                    >
                      <Trash2 className="size-3.5" />
                      <span>Clear</span>
                    </motion.button>
                  </div>

                  {/* Right Group */}
                  <div className="flex items-center justify-between md:justify-end gap-3 pt-1 md:pt-0">
                    <span className={cn("text-[11px] font-mono font-medium tabular-nums", isMinimumReached ? "text-[#059669]" : "text-[#6b6660]")}>
                      {wordCount} words &bull; {charCount} chars
                    </span>
                    <div className="hidden md:inline-flex items-center gap-1 text-[#3f3d3a]">
                      <span className="text-[#d6d1c9]">&bull;</span>
                      <kbd className="bg-[#f1efeb] border border-[#e7e3dd] rounded-md px-1.5 py-0.5 text-[11px] font-mono font-medium text-[#3f3d3a] shadow-[0_1px_0_rgba(15,15,14,0.04)]">
                        ⌘
                      </kbd>
                      <span className="text-[#6b6660] text-[11px]">+</span>
                      <kbd className="bg-[#f1efeb] border border-[#e7e3dd] rounded-md px-1.5 py-0.5 text-[11px] font-mono font-medium text-[#3f3d3a] shadow-[0_1px_0_rgba(15,15,14,0.04)]">
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
                  "flex min-h-[200px] md:min-h-[260px] cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed p-5 md:p-6 text-center transition-all",
                  dragOver
                    ? "border-indigo-400 bg-[#eef2ff]"
                    : "border-[#e7e3dd] bg-[#f1efeb] hover:bg-[#ebe8e3]"
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
                <div className="flex size-11 md:size-12 items-center justify-center rounded-xl bg-[#fdfcfb] text-indigo-600 mb-3 border border-[#e7e3dd] shadow-sm">
                  <Upload className="size-5 md:size-6 text-indigo-600" />
                </div>
                <p className="text-sm font-semibold text-[#0f0f0e]">
                  Drag & drop news document, or click to browse
                </p>
                <p className="text-[12px] md:text-[13px] text-[#6b6660] mt-1">Supports .txt, .csv, .json text payloads</p>
              </motion.div>
            )}

            {activeInputTab === "url" && (
              <motion.div
                key="tab-url"
                variants={tabContentVariant}
                initial="initial"
                animate="animate"
                exit="exit"
                className="space-y-3 py-6 min-h-[200px] md:min-h-[260px] flex flex-col justify-center"
              >
                <div className="flex flex-col sm:flex-row gap-2">
                  <input
                    type="url"
                    placeholder="https://www.bbc.com/news/..."
                    value={urlInput}
                    onChange={(e) => setUrlInput(e.target.value)}
                    className="flex-1 rounded-lg border border-[#e7e3dd] bg-[#f1efeb] px-4 py-2.5 text-sm text-[#0f0f0e] placeholder:text-[#8a847d] focus:bg-[#fdfcfb] focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/10 transition-all"
                  />
                  <Button
                    onClick={handleUrlFetch}
                    disabled={isFetchingUrl}
                    variant="secondary"
                    className="gap-1.5 h-11 sm:h-10 px-4 text-xs font-medium w-full sm:w-auto"
                  >
                    <Link2 className="size-4 text-indigo-600" />
                    <span>Fetch</span>
                  </Button>
                </div>
                <p className="text-[12px] md:text-[13px] text-[#6b6660]">
                  Enter an article URL or paste text directly.
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Model Selection Row: 2 columns on mobile, 3 on md+ */}
        <div className="space-y-3 pt-4 border-t border-[#e7e3dd]">
          <div className="flex items-center justify-between">
            <label className="text-[10px] md:text-[11px] font-semibold uppercase tracking-[0.14em] text-[#6b6660] font-mono block">
              Classification Architecture:
            </label>
            <span className="text-[11px] text-[#6b6660] font-mono font-medium">BBC News Models</span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-2 md:gap-3">
            {AVAILABLE_MODELS.map((m, index) => {
              const isSelected = selectedModel === m.id;
              return (
                <motion.button
                  key={m.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.35, delay: 0.05 + index * 0.05 }}
                  whileHover={{ y: -1 }}
                  whileTap={{ scale: 0.97 }}
                  type="button"
                  onClick={() => onChangeModel(m.id)}
                  className={cn(
                    "flex flex-col justify-between h-auto min-h-[70px] md:h-[76px] rounded-xl p-2.5 md:p-3 text-left transition-all border",
                    isSelected
                      ? "border-indigo-200 bg-indigo-50/40 text-[#0f0f0e] ring-1 ring-indigo-500/10 shadow-sm"
                      : "border-[#e7e3dd] bg-[#fdfcfb] text-[#3f3d3a] hover:bg-[#f1efeb]"
                  )}
                >
                  <div className="flex w-full items-start justify-between gap-1">
                    <span className="text-[12px] md:text-sm font-semibold text-[#0f0f0e] leading-snug">{m.name}</span>
                    <span className="text-[11px] md:text-xs font-mono font-medium text-[#3f3d3a] text-right mt-0.5 tabular-nums flex-shrink-0">
                      {m.tag}
                    </span>
                  </div>
                  <span className="text-[11px] md:text-xs text-[#6b6660] leading-snug line-clamp-1 mt-1">
                    {m.desc}
                  </span>
                </motion.button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Primary Submit Button */}
      <div className="pt-6">
        <motion.div whileHover={{ y: -1 }} whileTap={{ scale: 0.97 }}>
          <Button
            onClick={onClassify}
            disabled={!isMinimumReached || isLoading}
            size="lg"
            className="w-full h-12 rounded-xl gap-2 text-sm font-semibold shadow-[0_4px_16px_rgba(99,102,241,0.25)]"
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
                  <span className="size-4 animate-spin rounded-full border-2 border-[#fdfcfb] border-t-transparent" />
                  <span>Classifying Article...</span>
                </motion.div>
              ) : (
                <motion.div
                  key="idle"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex items-center gap-2"
                >
                  <Zap className="size-4 text-[#fdfcfb]" />
                  <span>Classify Article Now</span>
                </motion.div>
              )}
            </AnimatePresence>
          </Button>
        </motion.div>
      </div>
    </div>
  );
}
