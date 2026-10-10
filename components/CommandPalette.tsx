"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { Command } from "cmdk";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  Home,
  FileText,
  Layers,
  BarChart3,
  BookOpen,
  Cpu,
  Clipboard,
  Sparkles,
  ArrowRight,
  CornerDownLeft,
} from "lucide-react";
import { useClassifierStore } from "@/lib/store";
import { fetchRandomSamples } from "@/lib/api";
import type { BBCArticle } from "@/lib/types";
import type { ModelId } from "@/lib/models";
import { toast } from "sonner";
import { ease } from "@/lib/motion";

export function CommandPalette() {
  const router = useRouter();
  const {
    commandPaletteOpen,
    setCommandPaletteOpen,
    setCurrentText,
    setSelectedModel,
  } = useClassifierStore();

  const [search, setSearch] = React.useState("");
  const [samples, setSamples] = React.useState<BBCArticle[]>([]);

  React.useEffect(() => {
    if (commandPaletteOpen && samples.length === 0) {
      fetchRandomSamples(5)
        .then((res) => setSamples(res))
        .catch(() => {});
    }
  }, [commandPaletteOpen, samples.length]);

  // Global keyboard shortcut listener for Cmd+K / Ctrl+K
  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setCommandPaletteOpen(!commandPaletteOpen);
      }
      if (e.key === "Escape" && commandPaletteOpen) {
        e.preventDefault();
        setCommandPaletteOpen(false);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [commandPaletteOpen, setCommandPaletteOpen]);

  const handleSelectRoute = (path: string) => {
    setCommandPaletteOpen(false);
    router.push(path);
  };

  const handleLoadSample = (sample: BBCArticle) => {
    setCurrentText(sample.content || sample.title);
    setCommandPaletteOpen(false);
    router.push("/classify");
    toast.success(`Loaded BBC ${sample.category.toUpperCase()} article`);
  };

  const handlePasteClipboard = async () => {
    setCommandPaletteOpen(false);
    try {
      if (navigator.clipboard && navigator.clipboard.readText) {
        const text = await navigator.clipboard.readText();
        if (text) {
          setCurrentText(text);
          router.push("/classify");
          toast.success("Pasted clipboard text into classifier");
        }
      }
    } catch {
      toast.error("Clipboard permission required");
    }
  };

  const handleSelectModel = (modelId: string, modelName: string) => {
    setSelectedModel(modelId as ModelId);
    setCommandPaletteOpen(false);
    router.push("/classify");
    toast.success(`Active architecture: ${modelName}`);
  };

  return (
    <AnimatePresence>
      {commandPaletteOpen && (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4 sm:px-6">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            onClick={() => setCommandPaletteOpen(false)}
            className="fixed inset-0 bg-[#0f0f0e]/30 backdrop-blur-sm"
          />

          {/* Modal Card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.96, y: -10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.96, y: -10 }}
            transition={{ duration: 0.2, ease: ease.smooth }}
            className="relative w-full max-w-lg overflow-hidden rounded-2xl border border-[#e7e3dd] bg-[#fdfcfb] shadow-2xl z-10 select-none"
          >
            <Command
              className="w-full"
              loop
              value={search}
              onValueChange={setSearch}
            >
              {/* Search Input */}
              <div className="flex items-center border-b border-[#e7e3dd] px-4 py-3 gap-3 bg-[#fdfcfb]">
                <Search aria-hidden="true" className="size-4 text-[#57534e] flex-shrink-0" />
                <Command.Input
                  placeholder="Type a command or search BBC news..."
                  aria-label="Type a command or search BBC news"
                  className="w-full bg-transparent text-sm text-[#0f0f0e] placeholder:text-[#8a847d] focus:outline-none font-sans"
                  autoFocus
                />
                <kbd className="rounded-md border border-[#e7e3dd] bg-[#f1efeb] px-1.5 py-0.5 text-[10px] font-mono text-[#57534e]">
                  ESC
                </kbd>
              </div>

              {/* Suggestions List */}
              <Command.List className="max-h-80 overflow-y-auto p-2 space-y-1">
                <Command.Empty className="py-8 text-center text-xs text-[#57534e] font-sans">
                  No matching actions or news samples found.
                </Command.Empty>

                {/* Group 1: Navigation */}
                <Command.Group
                  heading={
                    <span className="px-2 py-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-[#57534e] font-mono block">
                      Navigation
                    </span>
                  }
                >
                  <Command.Item
                    onSelect={() => handleSelectRoute("/")}
                    className="group flex cursor-pointer items-center justify-between rounded-xl px-3 py-2 text-sm text-[#3f3d3a] aria-selected:bg-[#f1efeb] aria-selected:text-[#0f0f0e] transition-colors"
                  >
                    <div className="flex items-center gap-2.5">
                      <Home aria-hidden="true" className="size-4 text-[#57534e] group-aria-selected:text-indigo-600" />
                      <span className="font-medium">Home Page</span>
                    </div>
                    <span className="text-xs font-mono text-[#57534e]">/</span>
                  </Command.Item>

                  <Command.Item
                    onSelect={() => handleSelectRoute("/classify")}
                    className="group flex cursor-pointer items-center justify-between rounded-xl px-3 py-2 text-sm text-[#3f3d3a] aria-selected:bg-[#f1efeb] aria-selected:text-[#0f0f0e] transition-colors"
                  >
                    <div className="flex items-center gap-2.5">
                      <FileText aria-hidden="true" className="size-4 text-[#57534e] group-aria-selected:text-indigo-600" />
                      <span className="font-medium">Interactive Classifier</span>
                    </div>
                    <span className="text-xs font-mono text-[#57534e]">/classify</span>
                  </Command.Item>

                  <Command.Item
                    onSelect={() => handleSelectRoute("/batch")}
                    className="group flex cursor-pointer items-center justify-between rounded-xl px-3 py-2 text-sm text-[#3f3d3a] aria-selected:bg-[#f1efeb] aria-selected:text-[#0f0f0e] transition-colors"
                  >
                    <div className="flex items-center gap-2.5">
                      <Layers aria-hidden="true" className="size-4 text-[#57534e] group-aria-selected:text-indigo-600" />
                      <span className="font-medium">Batch CSV Processing</span>
                    </div>
                    <span className="text-xs font-mono text-[#57534e]">/batch</span>
                  </Command.Item>

                  <Command.Item
                    onSelect={() => handleSelectRoute("/analytics")}
                    className="group flex cursor-pointer items-center justify-between rounded-xl px-3 py-2 text-sm text-[#3f3d3a] aria-selected:bg-[#f1efeb] aria-selected:text-[#0f0f0e] transition-colors"
                  >
                    <div className="flex items-center gap-2.5">
                      <BarChart3 aria-hidden="true" className="size-4 text-[#57534e] group-aria-selected:text-indigo-600" />
                      <span className="font-medium">Metrics & Confusion Matrix</span>
                    </div>
                    <span className="text-xs font-mono text-[#57534e]">/analytics</span>
                  </Command.Item>

                  <Command.Item
                    onSelect={() => handleSelectRoute("/architecture")}
                    className="group flex cursor-pointer items-center justify-between rounded-xl px-3 py-2 text-sm text-[#3f3d3a] aria-selected:bg-[#f1efeb] aria-selected:text-[#0f0f0e] transition-colors"
                  >
                    <div className="flex items-center gap-2.5">
                      <BookOpen aria-hidden="true" className="size-4 text-[#57534e] group-aria-selected:text-indigo-600" />
                      <span className="font-medium">Architecture &amp; ML Syllabus</span>
                    </div>
                    <span className="text-xs font-mono text-[#57534e]">/architecture</span>
                  </Command.Item>

                  <Command.Item
                    onSelect={() => handleSelectRoute("/viva")}
                    className="group flex cursor-pointer items-center justify-between rounded-xl px-3 py-2 text-sm text-[#3f3d3a] aria-selected:bg-[#f1efeb] aria-selected:text-[#0f0f0e] transition-colors"
                  >
                    <div className="flex items-center gap-2.5">
                      <BookOpen aria-hidden="true" className="size-4 text-[#57534e] group-aria-selected:text-indigo-600" />
                      <span className="font-medium">Viva Defense Guide (Q&amp;A)</span>
                    </div>
                    <span className="text-xs font-mono text-[#57534e]">/viva</span>
                  </Command.Item>
                </Command.Group>

                {/* Group 2: Actions & Models */}
                <Command.Group
                  heading={
                    <span className="px-2 py-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-[#57534e] font-mono block mt-2">
                      Actions & Models
                    </span>
                  }
                >
                  <Command.Item
                    onSelect={handlePasteClipboard}
                    className="group flex cursor-pointer items-center justify-between rounded-xl px-3 py-2 text-sm text-[#3f3d3a] aria-selected:bg-[#f1efeb] aria-selected:text-[#0f0f0e] transition-colors"
                  >
                    <div className="flex items-center gap-2.5">
                      <Clipboard aria-hidden="true" className="size-4 text-[#57534e] group-aria-selected:text-indigo-600" />
                      <span className="font-medium">Paste Text from Clipboard</span>
                    </div>
                    <kbd className="rounded bg-[#f1efeb] border border-[#e7e3dd] px-1.5 py-0.5 text-[10px] font-mono text-[#57534e]">
                      ⌘V
                    </kbd>
                  </Command.Item>

                  <Command.Item
                    onSelect={() => handleSelectModel("distilbert", "DistilBERT")}
                    className="group flex cursor-pointer items-center justify-between rounded-xl px-3 py-2 text-sm text-[#3f3d3a] aria-selected:bg-[#f1efeb] aria-selected:text-[#0f0f0e] transition-colors"
                  >
                    <div className="flex items-center gap-2.5">
                      <Cpu aria-hidden="true" className="size-4 text-[#57534e] group-aria-selected:text-indigo-600" />
                      <span className="font-medium">Switch Model: DistilBERT</span>
                    </div>
                    <span className="text-xs font-mono text-[#0e7490]">Transformer</span>
                  </Command.Item>

                  <Command.Item
                    onSelect={() => handleSelectModel("linear_svm", "Linear SVM")}
                    className="group flex cursor-pointer items-center justify-between rounded-xl px-3 py-2 text-sm text-[#3f3d3a] aria-selected:bg-[#f1efeb] aria-selected:text-[#0f0f0e] transition-colors"
                  >
                    <div className="flex items-center gap-2.5">
                      <Cpu aria-hidden="true" className="size-4 text-[#57534e] group-aria-selected:text-indigo-600" />
                      <span className="font-medium">Switch Model: Linear SVM</span>
                    </div>
                    <span className="text-xs font-mono text-[#047857]">Hyperplane</span>
                  </Command.Item>
                </Command.Group>

                {/* Group 3: Real BBC Samples */}
                {samples.length > 0 && (
                  <Command.Group
                    heading={
                      <span className="px-2 py-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-[#57534e] font-mono block mt-2">
                        BBC News Samples
                      </span>
                    }
                  >
                    {samples.map((sample) => (
                      <Command.Item
                        key={sample.id}
                        onSelect={() => handleLoadSample(sample)}
                        className="group flex cursor-pointer items-center justify-between rounded-xl px-3 py-2 text-sm text-[#3f3d3a] aria-selected:bg-[#f1efeb] aria-selected:text-[#0f0f0e] transition-colors"
                      >
                        <div className="flex items-center gap-2.5 truncate pr-2">
                          <Sparkles aria-hidden="true" className="size-4 text-indigo-500 flex-shrink-0" />
                          <span className="font-semibold text-xs capitalize text-[#0f0f0e]">{sample.category}:</span>
                          <span className="truncate font-medium text-xs">{sample.title}</span>
                        </div>
                        <ArrowRight aria-hidden="true" className="size-3.5 opacity-0 group-aria-selected:opacity-100 text-[#57534e] flex-shrink-0" />
                      </Command.Item>
                    ))}
                  </Command.Group>
                )}
              </Command.List>

              {/* Palette Footer */}
              <div className="flex items-center justify-between border-t border-[#e7e3dd] bg-[#f1efeb] px-4 py-2 text-xs text-[#57534e] font-sans">
                <div className="flex items-center gap-3">
                  <span className="flex items-center gap-1">
                    <kbd className="rounded bg-[#fdfcfb] border border-[#e7e3dd] px-1 text-[10px] font-mono">↑</kbd>
                    <kbd className="rounded bg-[#fdfcfb] border border-[#e7e3dd] px-1 text-[10px] font-mono">↓</kbd>
                    <span>navigate</span>
                  </span>
                  <span className="flex items-center gap-1">
                    <kbd className="rounded bg-[#fdfcfb] border border-[#e7e3dd] px-1 text-[10px] font-mono flex items-center">
                      <CornerDownLeft aria-hidden="true" className="size-2.5" />
                    </kbd>
                    <span>select</span>
                  </span>
                </div>
                <span className="font-mono text-[11px]">NewsScope BBC Engine</span>
              </div>
            </Command>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
