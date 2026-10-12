/**
 * Debug logger for NewsScope.
 * Logs to console with timestamp + tag.
 * Works in both browser and server environments.
 */

type DebugLevel = "info" | "warn" | "error" | "success";

const COLORS = {
  info: "\x1b[36m",     // cyan
  warn: "\x1b[33m",     // yellow
  error: "\x1b[31m",    // red
  success: "\x1b[32m",  // green
  reset: "\x1b[0m",
};

function timestamp(): string {
  return new Date().toISOString().split("T")[1].slice(0, 12);
}

export function debug(
  tag: string,
  message: string,
  data?: unknown,
  level: DebugLevel = "info"
) {
  const prefix = `[${timestamp()}] [${tag}]`;
  const isServer = typeof window === "undefined";

  // Browser: colorized console output
  if (!isServer) {
    const style =
      level === "error"
        ? "color: #dc2626; font-weight: bold"
        : level === "warn"
        ? "color: #d97706; font-weight: bold"
        : level === "success"
        ? "color: #059669; font-weight: bold"
        : "color: #0891b2; font-weight: bold";

    if (data !== undefined) {
      console.log(`%c${prefix} ${message}`, style, data);
    } else {
      console.log(`%c${prefix} ${message}`, style);
    }
    return;
  }

  // Server: plain console output (Vercel captures this)
  const color = COLORS[level];
  if (data !== undefined) {
    console.log(`${color}${prefix} ${message}${COLORS.reset}`, data);
  } else {
    console.log(`${color}${prefix} ${message}${COLORS.reset}`);
  }
}

export const log = {
  info: (tag: string, msg: string, data?: unknown) =>
    debug(tag, msg, data, "info"),
  warn: (tag: string, msg: string, data?: unknown) =>
    debug(tag, msg, data, "warn"),
  error: (tag: string, msg: string, data?: unknown) =>
    debug(tag, msg, data, "error"),
  success: (tag: string, msg: string, data?: unknown) =>
    debug(tag, msg, data, "success"),
};
