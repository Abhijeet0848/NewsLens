"use client";

import * as React from "react";
import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, Check, Sparkles, X } from "lucide-react";
import { MODELS, ModelId, ModelInfo, DEFAULT_MODEL } from "@/lib/models";

export interface ModelSelectorProps {
  value: ModelId;
  onChange: (id: ModelId) => void;
  className?: string;
}

const MODEL_LIST: ModelInfo[] = Object.values(MODELS);

export function ModelSelector({
  value,
  onChange,
  className = "",
}: ModelSelectorProps) {
  const [open, setOpen] = useState(false);
  const [focusedIndex, setFocusedIndex] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);
  const listboxRef = useRef<HTMLDivElement>(null);

  const active = MODELS[value] || MODELS[DEFAULT_MODEL];

  // Sync focused index with current value when opened
  useEffect(() => {
    if (open) {
      const idx = MODEL_LIST.findIndex((m) => m.id === value);
      setFocusedIndex(idx >= 0 ? idx : 0);
    }
  }, [open, value]);

  // Close on outside click (desktop)
  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (
        containerRef.current &&
        !containerRef.current.contains(e.target as Node)
      ) {
        setOpen(false);
      }
    }
    if (open) {
      document.addEventListener("mousedown", onClick);
      return () => document.removeEventListener("mousedown", onClick);
    }
  }, [open]);

  // Keyboard navigation
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (!open) {
        if (e.key === "Enter" || e.key === " " || e.key === "ArrowDown") {
          e.preventDefault();
          setOpen(true);
        }
        return;
      }

      switch (e.key) {
        case "ArrowDown":
          e.preventDefault();
          setFocusedIndex((prev) => (prev + 1) % MODEL_LIST.length);
          break;
        case "ArrowUp":
          e.preventDefault();
          setFocusedIndex(
            (prev) => (prev - 1 + MODEL_LIST.length) % MODEL_LIST.length
          );
          break;
        case "Enter":
        case " ":
          e.preventDefault();
          if (MODEL_LIST[focusedIndex]) {
            onChange(MODEL_LIST[focusedIndex].id);
            setOpen(false);
          }
          break;
        case "Escape":
          e.preventDefault();
          setOpen(false);
          break;
        case "Tab":
          setOpen(false);
          break;
      }
    },
    [open, focusedIndex, onChange]
  );

  return (
    <div
      ref={containerRef}
      className={`relative inline-block ${className}`}
      onKeyDown={handleKeyDown}
    >
      {/* Trigger button */}
      <button
        type="button"
        onClick={() => setOpen(!open)}
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-label={`Selected model: ${active.name}`}
        className="group flex items-center gap-2 sm:gap-3 h-11 pl-3 pr-2.5 
                   rounded-xl bg-[#fdfcfb] border border-[#e7e3dd] 
                   hover:bg-[#f1efeb] hover:border-[#d6d1c9] 
                   focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#4f46e5]/20 focus-visible:border-[#4f46e5]
                   shadow-xs cursor-pointer select-none transition-all duration-150 shrink-0"
      >
        {/* Model indicator dot */}
        <span className="size-2 rounded-full bg-[#4f46e5] shrink-0" />

        {/* Label on Desktop */}
        <div className="hidden sm:flex flex-col items-start text-left">
          <span className="text-[10px] uppercase tracking-wider text-[#6b6660] font-mono leading-none">
            Model
          </span>
          <span className="text-[13px] font-medium text-[#0f0f0e] leading-tight mt-0.5">
            {active.name}
          </span>
        </div>

        {/* Label on Mobile */}
        <div className="flex sm:hidden items-center gap-1.5 text-left text-[12px] font-medium text-[#0f0f0e]">
          <span className="text-[#6b6660] font-mono text-[11px]">Model:</span>
          <span>{active.name}</span>
        </div>

        {/* Accuracy badge (Desktop only) */}
        <span className="hidden sm:inline-block text-[11px] font-mono text-[#6b6660] tabular-nums ml-0.5 bg-[#f1efeb] px-1.5 py-0.5 rounded border border-[#e7e3dd]/60">
          {active.metric}
        </span>

        {/* Chevron */}
        <ChevronDown
          className={`size-4 text-[#6b6660] transition-transform duration-200 shrink-0 ${
            open ? "rotate-180" : ""
          }`}
        />
      </button>

      {/* Dropdown Menu (Desktop) & Bottom Sheet (Mobile) */}
      <AnimatePresence>
        {open && (
          <>
            {/* Mobile Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setOpen(false)}
              className="fixed inset-0 bg-[#0f0f0e]/30 backdrop-blur-xs z-50 sm:hidden"
            />

            {/* Content Container: Bottom sheet on mobile, Dropdown on desktop */}
            <motion.div
              ref={listboxRef}
              role="listbox"
              aria-label="Model Selection"
              initial={{ opacity: 0, y: 12, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 12, scale: 0.98 }}
              transition={{ duration: 0.15, ease: [0.22, 1, 0.36, 1] }}
              className="fixed bottom-0 left-0 right-0 z-50 rounded-t-2xl sm:rounded-xl sm:absolute sm:bottom-auto sm:top-full sm:right-0 sm:left-auto sm:mt-2 sm:w-72 
                         bg-[#fdfcfb] border border-[#e7e3dd] 
                         shadow-[0_12px_32px_rgba(28,27,26,0.14),0_2px_6px_rgba(28,27,26,0.06)] 
                         overflow-hidden"
            >
              {/* Mobile Header */}
              <div className="flex sm:hidden items-center justify-between px-4 py-3 border-b border-[#e7e3dd]">
                <div className="flex items-center gap-2">
                  <span className="size-2 rounded-full bg-[#4f46e5]" />
                  <span className="text-xs font-semibold uppercase tracking-wider text-[#0f0f0e] font-mono">
                    Select ML Architecture
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => setOpen(false)}
                  className="p-1 rounded-md text-[#6b6660] hover:bg-[#f1efeb]"
                >
                  <X className="size-4" />
                </button>
              </div>

              {/* Model Options */}
              <div className="p-1.5 space-y-1 max-h-[60vh] sm:max-h-none overflow-y-auto">
                {MODEL_LIST.map((m, idx) => {
                  const isActive = m.id === value;
                  const isFocused = idx === focusedIndex;
                  return (
                    <button
                      key={m.id}
                      role="option"
                      aria-selected={isActive}
                      type="button"
                      onClick={() => {
                        onChange(m.id);
                        setOpen(false);
                      }}
                      onMouseEnter={() => setFocusedIndex(idx)}
                      className={`w-full flex items-start gap-2.5 p-2.5 rounded-lg text-left transition-colors duration-150 cursor-pointer ${
                        isActive
                          ? "bg-[#f1efeb] text-[#0f0f0e]"
                          : isFocused
                          ? "bg-[#faf9f6] text-[#0f0f0e]"
                          : "text-[#3f3d3a] hover:bg-[#faf9f6]"
                      }`}
                    >
                      {/* Check icon or spacer */}
                      <div className="mt-0.5 shrink-0 flex items-center justify-center size-4">
                        {isActive ? (
                          <Check className="size-4 text-[#4f46e5] stroke-[2.5]" />
                        ) : (
                          <span className="size-1.5 rounded-full bg-[#d6d1c9]" />
                        )}
                      </div>

                      {/* Model Information */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-1.5 flex-wrap">
                          <span className="text-[13px] font-semibold text-[#0f0f0e] leading-snug">
                            {m.name}
                          </span>
                          {m.role === "champion" && (
                            <span className="inline-flex items-center gap-1 text-[10px] font-medium text-[#92400e] bg-[#fef3c7] border border-[#fde68a] rounded-full px-1.5 py-0.2">
                              <Sparkles className="size-2.5 text-[#d97706]" />
                              Champion
                            </span>
                          )}
                          {m.role === "default" && (
                            <span className="inline-flex items-center text-[10px] font-medium text-[#4f46e5] bg-[#eef2ff] border border-[#c7d2fe] rounded-full px-1.5 py-0.2">
                              Default
                            </span>
                          )}
                        </div>
                        <p className="text-[11px] text-[#6b6660] mt-0.5 leading-tight">
                          {m.subtitle}
                        </p>
                        <p className="text-[10px] text-[#8a847d] mt-1 leading-tight">
                          {m.description}
                        </p>
                      </div>

                      {/* Performance Telemetry */}
                      <div className="shrink-0 text-right pl-2">
                        <p className="text-[12px] font-mono font-semibold text-[#0f0f0e] tabular-nums">
                          {m.metric}
                        </p>
                        <p className="text-[10px] font-mono text-[#8a847d] tabular-nums mt-0.5">
                          {m.latency}ms
                        </p>
                      </div>
                    </button>
                  );
                })}
              </div>

              {/* Footer hint */}
              <div className="border-t border-[#f1efeb] px-3 py-2 bg-[#faf9f6]">
                <p className="text-[10px] text-[#8a847d] leading-normal font-sans">
                  Linear SVM is the default — optimal speed-accuracy balance.
                </p>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
}
