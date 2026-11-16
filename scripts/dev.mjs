import { spawn } from "node:child_process";

const isWindows = process.platform === "win32";

console.log("\n🚀 Starting NewsScope (Backend + Frontend)...\n");

// 1. Start Python FastAPI backend (port 8000)
const backend = spawn(
  "python",
  ["-m", "uvicorn", "api.index:app", "--port", "8000", "--reload"],
  {
    stdio: "inherit",
    shell: isWindows,
  }
);

// 2. Start Next.js frontend (port 3000)
const frontend = spawn(
  isWindows ? "npx.cmd" : "npx",
  ["next", "dev", "--port", "3000"],
  {
    stdio: "inherit",
    shell: isWindows,
  }
);

// Helper to reliably kill process tree on Windows or POSIX
function shutdown() {
  console.log("\n🛑 Stopping NewsScope services...");

  const killProc = (proc) => {
    if (!proc || proc.killed) return;
    if (isWindows && proc.pid) {
      try {
        spawn("taskkill", ["/pid", proc.pid.toString(), "/f", "/t"]);
      } catch {}
    } else {
      try {
        proc.kill("SIGINT");
      } catch {}
    }
  };

  killProc(backend);
  killProc(frontend);
  process.exit(0);
}

process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
process.on("exit", shutdown);

backend.on("error", (err) => {
  console.error("❌ Failed to start FastAPI backend:", err.message);
});

frontend.on("error", (err) => {
  console.error("❌ Failed to start Next.js frontend:", err.message);
});
