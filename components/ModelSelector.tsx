"use client";

import * as React from "react";
import { useState, useRef, useEffect, useCallback } from "react";
import { createPortal } from "react-dom";
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
  const [mounted, setMounted] = useState(false);
  const [focusedIndex, setFocusedIndex] = useState(0);
  const [coords, setCoords] = useState<{ top: number; right: number } | null>(null);

  const triggerRef = useRef<HTMLButtonElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const active = MODELS[value] || MODELS[DEFAULT_MODEL];

  // Mount check for createPortal SSR safety
  useEffect(() => {
    setMounted(true);
  }, []);

  // Update positioning relative to trigger (aligning right edges)
  const updatePosition = useCallback(() => {
    if (triggerRef.current) {
      const rect = triggerRef.current.getBoundingClientRect();
      setCoords({
        top: rect.bottom + 8,
        right: Math.max(16, window.innerWidth - rect.right),
      });
    }
  }, []);

  // Sync focused index and update coordinates when opened
  useEffect(() => {
    if (open) {
      const idx = MODEL_LIST.findIndex((m) => m.id === value);
      setFocusedIndex(idx >= 0 ? idx : 0);
      updatePosition();

      const handleScrollOrResize = () => updatePosition();
      window.addEventListener("scroll", handleScrollOrResize, true);
      window.addEventListener("resize", handleScrollOrResize);

      return () => {
        window.removeEventListener("scroll", handleScrollOrResize, true);
        window.removeEventListener("resize", handleScrollOrResize);
      };
    }
  }, [open, value, updatePosition]);

  // Close on outside click
  useEffect(() => {
    function onClick(e: MouseEvent) {
      const target = e.target as Node;
      if (
        triggerRef.current &&
        !triggerRef.current.contains(target) &&
        dropdownRef.current &&
        !dropdownRef.current.contains(target)
      ) {
        setOpen(false);
      }
    }
    if (open) {
      document.addEventListener("mousedown", onClick);
      return () => document.removeEventListener("mousedown", onClick);
    }
  }, [open]);

  // Keyboard navigation & accessibility
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
            triggerRef.current?.focus();
          }
          break;
        case "Escape":
          e.preventDefault();
          setOpen(false);
          triggerRef.current?.focus();
          break;
        case "Tab":
          setOpen(false);
          break;
      }
    },
    [open, focusedIndex, onChange]
  );

  return (
    <div className={`relative inline-block ${className}`} onKeyDown={handleKeyDown}>
      {/* Trigger button */}
      <button
        ref={triggerRef}
        type="button"
        onClick={() => setOpen(!open)}
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-label={`Selected model: ${active.name}`}
        className="group flex items-center gap-3 h-11 pl-3 pr-3 rounded-lg 
                   bg-[#fdfcfb] border border-[#e7e3dd] 
                   hover:bg-[#f1efeb] hover:border-[#d6d1c9] 
                   focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#4f46e5]/20 focus-visible:border-[#4f46e5]
                   shadow-xs cursor-pointer select-none transition-colors duration-150 shrink-0"
      >
        {/* Dot */}
        <span className="size-2.5 rounded-full bg-[#4f46e5] shrink-0" />

        {/* Label stack */}
        <div className="flex flex-col items-start text-left">
          <span className="text-[10px] uppercase tracking-wider text-[#6b6660] font-mono leading-none">
            Model
          </span>
          <span className="text-[13px] font-medium text-[#0f0f0e] leading-tight mt-0.5 whitespace-nowrap">
            {active.name}
          </span>
        </div>

        {/* Accuracy badge */}
        <span className="text-[11px] font-mono font-medium text-[#6b6660] bg-[#f1efeb] rounded-md px-2 py-1 tabular-nums ml-1 shrink-0">
          {active.metric}
        </span>

        {/* Chevron (closed: rotate-0 points down, open: rotate-180 points up) */}
        <ChevronDown
          className={`size-4 text-[#6b6660] transition-transform duration-200 shrink-0 ${
            open ? "rotate-180" : "rotate-0"
          }`}
        />
      </button>

      {/* Dropdown Menu (Desktop) & Bottom Sheet (Mobile) rendered via Portal */}
      {mounted &&
        createPortal(
          <AnimatePresence>
            {open && (
              <>
                {/* Mobile Backdrop */}
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.15 }}
                  onClick={() => setOpen(false)}
                  className="fixed inset-0 bg-[#0f0f0e]/30 backdrop-blur-xs z-[9998] sm:hidden"
                />

                {/* Dropdown container: 95% opacity, backdrop-blur-md, strong shadow */}
                <motion.div
                  ref={dropdownRef}
                  role="listbox"
                  aria-label="Model Selection"
                  initial={{ opacity: 0, y: -4, scale: 0.98 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -4, scale: 0.98 }}
                  transition={{ duration: 0.15, ease: [0.22, 1, 0.36, 1] }}
                  style={
                    coords
                      ? ({
                          "--desktop-top": `${coords.top}px`,
                          "--desktop-right": `${coords.right}px`,
                        } as React.CSSProperties)
                      : undefined
                  }
                  className="fixed bottom-0 left-0 right-0 z-[9999] rounded-t-2xl 
                             sm:fixed sm:bottom-auto sm:left-auto sm:top-[var(--desktop-top)] sm:right-[var(--desktop-right)] sm:w-80 sm:rounded-xl 
                             bg-[#fdfcfb]/95 backdrop-blur-md 
                             border border-[#e7e3dd] 
                             shadow-[0_16px_48px_-12px_rgba(28,27,26,0.20),0_8px_16px_-8px_rgba(28,27,26,0.12)] 
                             overflow-hidden"
                >
                  {/* Mobile Sheet Header */}
                  <div className="flex sm:hidden items-center justify-between px-4 py-3 border-b border-[#e7e3dd]/70">
                    <div className="flex items-center gap-2">
                      <span className="size-2.5 rounded-full bg-[#4f46e5]" />
                      <span className="text-xs font-semibold uppercase tracking-wider text-[#0f0f0e] font-mono">
                        Select ML Architecture
                      </span>
                    </div>
                    <button
                      type="button"
                      onClick={() => setOpen(false)}
                      className="p-1 rounded-md text-[#6b6660] hover:bg-[#f1efeb]/70"
                    >
                      <X className="size-4" />
                    </button>
                  </div>

                  {/* Model Options List (Uniform padding & subtle bottom separator) */}
                  <div className="max-h-[60vh] sm:max-h-none overflow-y-auto">
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
                            triggerRef.current?.focus();
                          }}
                          onMouseEnter={() => setFocusedIndex(idx)}
                          className={`w-full flex items-start gap-3 px-3.5 py-3 text-left transition-colors duration-150 cursor-pointer border-b border-[#f1efeb]/50 last:border-b-0 ${
                            isActive
                              ? "bg-[#f1efeb]/60 text-[#0f0f0e]"
                              : isFocused
                              ? "bg-[#faf9f6]/80 text-[#0f0f0e]"
                              : "text-[#3f3d3a] hover:bg-[#f1efeb]/80"
                          }`}
                        >
                          {/* Indicator: Check mark for active, clearly visible 1.5 dot for inactive */}
                          <div className="mt-0.5 w-4 h-4 flex items-center justify-center shrink-0">
                            {isActive ? (
                              <Check className="size-4 text-[#4f46e5]" />
                            ) : (
                              <span className="size-1.5 rounded-full bg-[#a8a29e]" />
                            )}
                          </div>

                          {/* Model Details */}
                          <div className="flex-1 min-w-0">
                            {/* Row 1: Name + Badge */}
                            <div className="flex items-center gap-2 flex-wrap">
                              <span className="text-[13px] font-medium text-[#0f0f0e] leading-snug">
                                {m.name}
                              </span>
                              {m.role === "champion" && (
                                <span className="inline-flex items-center gap-1 text-[10px] font-semibold uppercase tracking-wide rounded-full px-2 py-0.5 leading-none border h-5 bg-[#fef3c7] text-[#92400e] border-[#fde68a]">
                                  <Sparkles className="size-3 text-[#d97706]" />
                                  Champion
                                </span>
                              )}
                              {m.role === "default" && (
                                <span className="inline-flex items-center gap-1 text-[10px] font-semibold uppercase tracking-wide rounded-full px-2 py-0.5 leading-none border h-5 bg-[#eef2ff] text-[#4f46e5] border-[#c7d2fe]">
                                  Default
                                </span>
                              )}
                            </div>

                            {/* Row 2: Subtitle */}
                            <p className="text-[11px] text-[#6b6660] mt-1 leading-tight">
                              {m.subtitle}
                            </p>

                            {/* Row 3: Description */}
                            <p className="text-[10px] text-[#a8a29e] mt-1 leading-tight">
                              {m.description}
                            </p>
                          </div>

                          {/* Right Column: Accuracy & Latency Metrics */}
                          <div className="shrink-0 text-right pl-2">
                            <p className="text-[12px] font-mono font-semibold text-[#0f0f0e] tabular-nums">
                              {m.metric}
                            </p>
                            <p className="text-[10px] font-mono text-[#a8a29e] tabular-nums mt-0.5">
                              {m.latency}ms
                            </p>
                          </div>
                        </button>
                      );
                    })}
                  </div>

                  {/* Shortened Footer Hint with generous padding */}
                  <div className="px-3.5 py-2.5 bg-[#f1efeb]/60 border-t border-[#e7e3dd]/60">
                    <p className="text-[10px] text-[#6b6660] leading-tight font-sans">
                      Default: Linear SVM (best speed-accuracy balance)
                    </p>
                  </div>
                </motion.div>
              </>
            )}
          </AnimatePresence>,
          document.body
        )}
    </div>
  );
}
