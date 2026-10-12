"use client";

import * as React from "react";
import { Bug, X, Trash2, ChevronUp, ChevronDown } from "lucide-react";

type LogEntry = {
  time: string;
  tag: string;
  message: string;
  data?: unknown;
  level: "info" | "warn" | "error" | "success";
};

export function DebugPanel() {
  const [logs, setLogs] = React.useState<LogEntry[]>([]);
  const [open, setOpen] = React.useState(false);
  const [enabled, setEnabled] = React.useState(false);

  React.useEffect(() => {
    // Enable if in development OR if ?debug=1 is in URL
    const isDev = process.env.NODE_ENV === "development";
    const urlDebug =
      typeof window !== "undefined" &&
      new URLSearchParams(window.location.search).get("debug") === "1";
    setEnabled(isDev || !!urlDebug);
  }, []);

  React.useEffect(() => {
    if (!enabled) return;

    const originalLog = console.log;
    const originalError = console.error;
    const originalWarn = console.warn;

    const capture =
      (level: LogEntry["level"]) =>
      (...args: unknown[]) => {
        const [firstArg, secondArg, data] = args;
        const msgStr = typeof firstArg === "string" ? firstArg : "";

        // Check if string has tag format like [%c[HH:MM:SS] [tag] message
        const match = msgStr.match(/\[([0-9:.]+)\]\s+\[([^\]]+)\]\s*(.*)/);
        if (match) {
          const [, time, tag, message] = match;
          setLogs((prev) => [
            ...prev.slice(-99),
            {
              time,
              tag,
              message: message || (typeof secondArg === "string" ? secondArg : ""),
              data: data !== undefined ? data : secondArg,
              level,
            },
          ]);
        } else if (msgStr.includes("[api/") || msgStr.includes("[ui/")) {
          setLogs((prev) => [
            ...prev.slice(-99),
            {
              time: new Date().toLocaleTimeString(),
              tag: "app",
              message: msgStr,
              data: secondArg,
              level,
            },
          ]);
        }

        originalLog(...args);
      };

    console.log = capture("info");
    console.error = capture("error");
    console.warn = capture("warn");

    return () => {
      console.log = originalLog;
      console.error = originalError;
      console.warn = originalWarn;
    };
  }, [enabled]);

  if (!enabled) return null;

  return (
    <div className="fixed bottom-4 left-4 z-[9999] max-w-md font-mono text-xs">
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1.5 bg-[#0f0f0e] text-white px-3 py-2 rounded-lg shadow-lg hover:bg-[#2a2a28] border border-white/10 transition-colors select-none cursor-pointer"
      >
        <Bug className="size-3.5 text-cyan-400" />
        <span>Debug ({logs.length})</span>
        {open ? <ChevronDown className="size-3 opacity-60" /> : <ChevronUp className="size-3 opacity-60" />}
      </button>

      {open && (
        <div className="mt-2 bg-[#0f0f0e] text-white rounded-lg shadow-2xl border border-white/10 w-80 sm:w-96 max-h-96 overflow-y-auto p-3">
          <div className="flex justify-between items-center mb-2 border-b border-white/10 pb-2">
            <span className="text-[10px] font-semibold tracking-wider uppercase text-white/60">
              Request Debug Log
            </span>
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setLogs([])}
                className="text-[10px] text-white/60 hover:text-white flex items-center gap-1 transition-colors cursor-pointer"
              >
                <Trash2 className="size-2.5" />
                <span>Clear</span>
              </button>
              <button
                type="button"
                onClick={() => setOpen(false)}
                className="text-white/60 hover:text-white transition-colors cursor-pointer"
              >
                <X className="size-3" />
              </button>
            </div>
          </div>

          {logs.length === 0 && (
            <p className="text-white/50 text-[11px] py-4 text-center">
              No logs yet. Click Classify to trace.
            </p>
          )}

          <div className="space-y-1.5">
            {logs.map((item, i) => (
              <div
                key={i}
                className={`py-1.5 border-b border-white/5 font-mono text-[11px] ${
                  item.level === "error"
                    ? "text-red-400"
                    : item.level === "warn"
                    ? "text-yellow-400"
                    : item.level === "success"
                    ? "text-green-400"
                    : "text-cyan-400"
                }`}
              >
                <div className="text-[9px] opacity-60 flex items-center justify-between">
                  <span>{item.time}</span>
                  <span className="bg-white/10 px-1 rounded text-[8px]">{item.tag}</span>
                </div>
                <div className="text-[11px] font-medium mt-0.5 break-words">{item.message}</div>
                {item.data !== undefined && (
                  <pre className="text-[9px] opacity-80 mt-1 bg-black/40 p-1.5 rounded whitespace-pre-wrap break-all border border-white/5 max-h-24 overflow-y-auto">
                    {typeof item.data === "object"
                      ? JSON.stringify(item.data, null, 2).slice(0, 400)
                      : String(item.data).slice(0, 400)}
                  </pre>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
