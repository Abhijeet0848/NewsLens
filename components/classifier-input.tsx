"use client";

import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  FileText,
  Upload,
  Link2,
  Trash2,
  Clipboard,
  Loader2,
  Check,
  AlertCircle,
  X,
  CornerDownLeft,
} from "lucide-react";
import { fetchArticleFromUrl } from "@/lib/api";
import { detectInput, getDomain } from "@/lib/detectInput";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

import { ModelSelector } from "@/components/ModelSelector";
import { ModelId, DEFAULT_MODEL } from "@/lib/models";

interface ClassifierInputProps {
  text: string;
  onChangeText: (val: string) => void;
  selectedModel: ModelId | string;
  onChangeModel: (model: ModelId) => void;
  onClassify: () => void;
  isLoading: boolean;
}

export type InputState =
  | { kind: "empty" }
  | { kind: "text"; text: string }
  | { kind: "url-loading"; url: string }
  | { kind: "url-loaded"; url: string; text: string }
  | { kind: "url-error"; url: string; message: string };

export function ClassifierInput({
  text,
  onChangeText,
  selectedModel,
  onChangeModel,
  onClassify,
  isLoading,
}: ClassifierInputProps) {
  const [inputState, setInputState] = React.useState<InputState>(() =>
    text.trim() ? { kind: "text", text } : { kind: "empty" }
  );
  const [isUrlTyped, setIsUrlTyped] = React.useState(false);
  const [dragOver, setDragOver] = React.useState(false);
  const fileInputRef = React.useRef<HTMLInputElement | null>(null);
  const textareaRef = React.useRef<HTMLTextAreaElement | null>(null);

  const charCount = text.length;
  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  const isMinimumReached = charCount >= 20;

  // Live detection debounce for typed URLs (500ms)
  React.useEffect(() => {
    if (inputState.kind === "url-loading" || inputState.kind === "url-loaded") {
      setIsUrlTyped(false);
      return;
    }
    const timer = setTimeout(() => {
      const type = detectInput(text);
      setIsUrlTyped(type === "url");
    }, 400);

    return () => clearTimeout(timer);
  }, [text, inputState]);

  // Synchronize state when external text resets
  React.useEffect(() => {
    if (!text && inputState.kind !== "url-loading" && inputState.kind !== "url-error") {
      setInputState({ kind: "empty" });
    }
  }, [text, inputState.kind]);

  // Fetch URL and populate textarea
  const fetchUrlAndFill = async (rawUrl: string) => {
    const trimmed = rawUrl.trim();
    if (!trimmed) return;

    setInputState({ kind: "url-loading", url: trimmed });
    onChangeText(""); // Clear previous text while loading
    setIsUrlTyped(false);

    try {
      const extractedText = await fetchArticleFromUrl(trimmed);
      setInputState({ kind: "url-loaded", url: trimmed, text: extractedText });
      onChangeText(extractedText);
      const extractedWords = extractedText.split(/\s+/).length;
      toast.success(`Article extracted (${extractedWords} words)`);
    } catch (err: any) {
      const msg =
        err.message ||
        "Could not find article text on this page. The site may block automated access. Please paste the text manually.";
      setInputState({ kind: "url-error", url: trimmed, message: msg });
      toast.error("Failed to fetch article from URL");
    }
  };

  // Intercept Paste events in the textarea
  const handlePaste = async (e: React.ClipboardEvent<HTMLTextAreaElement>) => {
    const pasted = e.clipboardData.getData("text");
    const type = detectInput(pasted);

    if (type === "url") {
      e.preventDefault();
      await fetchUrlAndFill(pasted);
    } else {
      // Normal text paste
      setInputState({ kind: "text", text: pasted });
    }
  };

  // Paste button from clipboard
  const handlePasteClipboard = async () => {
    try {
      if (navigator.clipboard && navigator.clipboard.readText) {
        const clip = await navigator.clipboard.readText();
        if (!clip) return;
        const type = detectInput(clip);
        if (type === "url") {
          await fetchUrlAndFill(clip);
        } else {
          onChangeText(clip);
          setInputState({ kind: "text", text: clip });
          toast.success("Pasted text from clipboard");
        }
      }
    } catch {
      toast.error("Clipboard permission required");
    }
  };

  // Textarea Change handler
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const val = e.target.value;
    onChangeText(val);

    if (!val.trim()) {
      setInputState({ kind: "empty" });
    } else if (inputState.kind !== "url-loaded") {
      setInputState({ kind: "text", text: val });
    }
  };

  // Clear input
  const handleClear = () => {
    onChangeText("");
    setInputState({ kind: "empty" });
    setIsUrlTyped(false);
    toast.info("Input cleared");
  };

  // File Upload handler
  const handleFileUpload = (file: File) => {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      if (content) {
        onChangeText(content);
        setInputState({ kind: "text", text: content });
        toast.success(`Uploaded "${file.name}"`);
      }
    };
    reader.readAsText(file);
  };

  // Textarea Keydown (Enter to fetch if URL typed, Cmd/Ctrl+Enter to classify)
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (isUrlTyped && e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      fetchUrlAndFill(text);
      return;
    }

    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      if (isMinimumReached && !isLoading && inputState.kind !== "url-loading") {
        e.preventDefault();
        onClassify();
      }
    }
  };

  // Global shortcut: Cmd/Ctrl + Enter
  React.useEffect(() => {
    const handleGlobalKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
        if (isMinimumReached && !isLoading && inputState.kind !== "url-loading") {
          e.preventDefault();
          onClassify();
        }
      }
    };
    window.addEventListener("keydown", handleGlobalKeyDown);
    return () => window.removeEventListener("keydown", handleGlobalKeyDown);
  }, [isMinimumReached, isLoading, inputState.kind, onClassify]);

  const isUrlState =
    inputState.kind === "url-loading" ||
    inputState.kind === "url-loaded" ||
    inputState.kind === "url-error";

  return (
    <div className="rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] p-6 md:p-7 shadow-[0_1px_2px_rgba(28,27,26,0.04),0_8px_24px_-8px_rgba(28,27,26,0.06)] hover:shadow-[0_1px_2px_rgba(28,27,26,0.06),0_12px_32px_-8px_rgba(28,27,26,0.10)] transition-shadow duration-200 flex flex-col justify-between h-full">
      <div>
        {/* Card Header (Icon + Title + Description) */}
        <div className="flex items-start justify-between gap-4 mb-5">
          <div className="flex items-start gap-3">
            <div className="flex size-9 items-center justify-center rounded-lg bg-[#eef2ff] text-[#4f46e5] flex-shrink-0">
              <FileText className="size-4" />
            </div>
            <div>
              <h3 className="text-[15px] font-semibold text-[#0f0f0e]">
                Article Content Input
              </h3>
              <p className="text-[13px] text-[#3f3d3a] mt-0.5 max-w-md leading-relaxed">
                Paste raw text, upload a document, or enter a URL to classify.
              </p>
            </div>
          </div>
        </div>

        {/* Hidden File Input */}
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

        {/* URL Chip Section (when URL state active) */}
        <AnimatePresence>
          {isUrlState && (
            <motion.div
              initial={{ opacity: 0, y: -6, height: 0 }}
              animate={{ opacity: 1, y: 0, height: "auto" }}
              exit={{ opacity: 0, y: -6, height: 0 }}
              transition={{ duration: 0.18 }}
              className="mb-3 overflow-hidden"
            >
              <div className="flex flex-col gap-1.5">
                <div className="flex items-center gap-2 flex-wrap">
                  {inputState.kind === "url-loading" && (
                    <div className="inline-flex items-center gap-2 h-7 px-3 rounded-full bg-[#f1efeb] border border-[#e7e3dd] text-[12px] font-medium text-[#6b6660] max-w-full">
                      <Loader2 className="size-3.5 animate-spin text-[#4f46e5]" />
                      <span className="truncate">
                        Fetching {getDomain(inputState.url)}...
                      </span>
                    </div>
                  )}

                  {inputState.kind === "url-loaded" && (
                    <div className="inline-flex items-center gap-2 h-7 px-3 rounded-full bg-[#ecfdf5] border border-[#a7f3d0] text-[12px] font-medium text-[#047857] max-w-full">
                      <Check className="size-3.5 text-[#047857] flex-shrink-0" />
                      <span className="truncate">{getDomain(inputState.url)}</span>
                      <button
                        type="button"
                        onClick={handleClear}
                        title="Remove URL"
                        className="text-[#047857]/70 hover:text-[#047857] transition-colors p-0.5 ml-0.5 rounded-full hover:bg-[#a7f3d0]/40"
                      >
                        <X className="size-3.5" />
                      </button>
                    </div>
                  )}

                  {inputState.kind === "url-error" && (
                    <div className="inline-flex items-center gap-2 h-7 px-3 rounded-full bg-[#fef2f2] border border-[#fecdd3] text-[12px] font-medium text-[#be123c] max-w-full">
                      <AlertCircle className="size-3.5 text-[#be123c] flex-shrink-0" />
                      <span className="truncate">{getDomain(inputState.url)}</span>
                      <button
                        type="button"
                        onClick={handleClear}
                        title="Dismiss error"
                        className="text-[#be123c]/70 hover:text-[#be123c] transition-colors p-0.5 ml-0.5 rounded-full hover:bg-[#fecdd3]/50"
                      >
                        <X className="size-3.5" />
                      </button>
                    </div>
                  )}
                </div>

                {inputState.kind === "url-error" && (
                  <p className="text-[12px] text-[#be123c] mt-0.5 leading-snug">
                    {inputState.message}
                  </p>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Unified Smart Textarea */}
        <div
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
          className={cn(
            "relative rounded-xl transition-all duration-200",
            dragOver && "ring-2 ring-[#4f46e5] ring-offset-2"
          )}
        >
          <textarea
            ref={textareaRef}
            rows={8}
            className={cn(
              "w-full min-h-[200px] md:min-h-[240px] rounded-xl border border-[#e7e3dd] bg-[#faf9f6] p-5 text-[15px] leading-relaxed text-[#0f0f0e] shadow-[inset_0_1px_2px_rgba(28,27,26,0.02)] placeholder:text-[#8a847d] focus:bg-[#fdfcfb] focus:border-[#4f46e5]/40 focus:outline-none focus:ring-4 focus:ring-[#4f46e5]/[0.08] transition-all duration-200 resize-y",
              inputState.kind === "url-loading" && "opacity-60 cursor-wait"
            )}
            placeholder="Paste article text or a URL..."
            value={text}
            onChange={handleChange}
            onPaste={handlePaste}
            onKeyDown={handleKeyDown}
            disabled={inputState.kind === "url-loading"}
          />

          {/* Live Auto-detect URL Typing Hint */}
          <AnimatePresence>
            {isUrlTyped && inputState.kind !== "url-loading" && (
              <motion.div
                initial={{ opacity: 0, y: -4 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -4 }}
                className="flex items-center gap-1.5 text-[11px] text-[#6b6660] font-medium mt-1.5 px-1"
              >
                <Link2 className="size-3.5 text-[#4f46e5]" />
                <span>Detected URL — press</span>
                <kbd className="inline-flex items-center gap-0.5 bg-[#f1efeb] border border-[#e7e3dd] rounded px-1.5 py-0.5 text-[10px] font-mono font-semibold text-[#0f0f0e]">
                  Enter <CornerDownLeft className="size-2.5" />
                </kbd>
                <span>to fetch article</span>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Footer Row (simplified) */}
        <div className="mt-4 flex flex-col md:flex-row md:items-center md:justify-between gap-3">
          {/* Left Actions: Paste | Upload | Clear */}
          <div className="flex items-center gap-1.5 flex-wrap">
            <button
              type="button"
              onClick={handlePasteClipboard}
              className="h-8 px-3 rounded-md bg-[#fdfcfb] border border-[#e7e3dd] text-[12px] font-medium text-[#0f0f0e] hover:bg-[#f1efeb] hover:border-[#d6d1c9] transition-colors duration-150 flex items-center gap-1.5 shadow-sm active:scale-[0.98]"
            >
              <Clipboard className="size-3.5 text-[#57534e]" />
              <span>Paste</span>
            </button>
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="h-8 px-3 rounded-md bg-[#fdfcfb] border border-[#e7e3dd] text-[12px] font-medium text-[#0f0f0e] hover:bg-[#f1efeb] hover:border-[#d6d1c9] transition-colors duration-150 flex items-center gap-1.5 shadow-sm active:scale-[0.98]"
            >
              <Upload className="size-3.5 text-[#57534e]" />
              <span>Upload</span>
            </button>
            <button
              type="button"
              onClick={handleClear}
              disabled={!text && inputState.kind === "empty"}
              className="h-8 px-3 rounded-md bg-[#fdfcfb] border border-[#e7e3dd] text-[12px] font-medium text-[#0f0f0e] hover:bg-[#f1efeb] hover:text-[#dc2626] hover:border-[#d6d1c9] transition-colors duration-150 flex items-center gap-1.5 shadow-sm disabled:opacity-50 disabled:pointer-events-none active:scale-[0.98]"
            >
              <Trash2 className="size-3.5 text-[#57534e]" />
              <span>Clear</span>
            </button>
          </div>

          {/* Right Stats & Shortcut Hint */}
          <div className="flex items-center justify-between md:justify-end gap-3">
            <span className="text-[12px] font-mono text-[#3f3d3a] tabular-nums font-medium">
              {wordCount} words &bull; {charCount} chars
            </span>
            <div className="hidden md:inline-flex items-center gap-1 text-[#3f3d3a] text-[11px] font-medium">
              <span className="text-[#6b6660]">&bull;</span>
              <kbd className="bg-[#f1efeb] border border-[#e7e3dd] rounded px-1.5 py-0.5 text-[11px] font-mono font-medium text-[#3f3d3a]">
                ⌘
              </kbd>
              <span className="text-[#6b6660]">+</span>
              <kbd className="bg-[#f1efeb] border border-[#e7e3dd] rounded px-1.5 py-0.5 text-[11px] font-mono font-medium text-[#3f3d3a]">
                Enter
              </kbd>
            </div>
          </div>
        </div>

      </div>

      {/* Footer Actions: Model Selector + Classify Button */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 mt-5">
        <ModelSelector
          value={(selectedModel as ModelId) || DEFAULT_MODEL}
          onChange={onChangeModel}
        />
        <button
          type="button"
          onClick={onClassify}
          disabled={!text.trim() || isLoading || inputState.kind === "url-loading"}
          className="flex-1 h-11 sm:h-12 rounded-xl bg-[#0f0f0e] disabled:bg-[#0f0f0e]/40 text-white text-[14px] font-medium shadow-[0_2px_8px_rgba(15,15,14,0.15)] hover:bg-[#2a2a28] hover:shadow-[0_4px_12px_rgba(15,15,14,0.20)] hover:-translate-y-px active:scale-[0.99] disabled:cursor-not-allowed disabled:hover:bg-[#0f0f0e]/40 disabled:hover:translate-y-0 disabled:hover:shadow-[0_2px_8px_rgba(15,15,14,0.15)] transition-all duration-200 flex items-center justify-center cursor-pointer select-none"
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
                className="flex items-center justify-center"
              >
                <span>Classify Article Now</span>
              </motion.div>
            )}
          </AnimatePresence>
        </button>
      </div>
    </div>
  );
}
