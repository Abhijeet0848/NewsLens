"use client";

import * as React from "react";
import { useRouter } from "next/navigation";

const ROUTES = ["/", "/classify", "/batch", "/analytics", "/about"];

export function RoutePrefetcher() {
  const router = useRouter();

  React.useEffect(() => {
    // Eagerly prefetch main routes on client idle
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
