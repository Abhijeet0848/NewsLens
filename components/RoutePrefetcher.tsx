"use client";

import * as React from "react";
import { useRouter } from "next/navigation";

const ROUTES = ["/", "/classify", "/batch", "/analytics", "/about"];

export function RoutePrefetcher() {
  const router = useRouter();

  React.useEffect(() => {
    // Only prefetch in production. In development (next dev), prefetching
    // triggers simultaneous on-demand compilation of all 5 routes,
    // which spikes dev server CPU and causes navbar clicks to freeze.
    if (process.env.NODE_ENV !== "production") return;

    if (typeof window !== "undefined" && "requestIdleCallback" in window) {
      window.requestIdleCallback(() => {
        ROUTES.forEach((route) => {
          try {
            router.prefetch(route);
          } catch {}
        });
      });
    } else {
      ROUTES.forEach((route) => {
        try {
          router.prefetch(route);
        } catch {}
      });
    }
  }, [router]);

  return null;
}
