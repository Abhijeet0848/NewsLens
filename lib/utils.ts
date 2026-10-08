import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export type CategoryKey =
  | "Business"
  | "Entertainment"
  | "Politics"
  | "Sport"
  | "Tech";

export interface CategoryInfo {
  name: CategoryKey;
  icon: string;
  colorHex: string;
  bgLight: string;
  borderColor: string;
  badgeClass: string;
  borderClass: string;
  textClass: string;
  gradient: string;
}

export const CATEGORIES_CONFIG: Record<string, CategoryInfo> = {
  Business: {
    name: "Business",
    icon: "Briefcase",
    colorHex: "#d97706",
    bgLight: "#fffbeb",
    borderColor: "#fde68a",
    badgeClass: "bg-[#fffbeb] text-[#d97706] border-[#fde68a]",
    borderClass: "border-[#fde68a]",
    textClass: "text-[#d97706]",
    gradient: "from-[#fffbeb] to-[#fdfcfb]",
  },
  Entertainment: {
    name: "Entertainment",
    icon: "Film",
    colorHex: "#db2777",
    bgLight: "#fdf2f8",
    borderColor: "#fbcfe8",
    badgeClass: "bg-[#fdf2f8] text-[#db2777] border-[#fbcfe8]",
    borderClass: "border-[#fbcfe8]",
    textClass: "text-[#db2777]",
    gradient: "from-[#fdf2f8] to-[#fdfcfb]",
  },
  Politics: {
    name: "Politics",
    icon: "Landmark",
    colorHex: "#e11d48",
    bgLight: "#fff1f2",
    borderColor: "#fecdd3",
    badgeClass: "bg-[#fff1f2] text-[#e11d48] border-[#fecdd3]",
    borderClass: "border-[#fecdd3]",
    textClass: "text-[#e11d48]",
    gradient: "from-[#fff1f2] to-[#fdfcfb]",
  },
  Sport: {
    name: "Sport",
    icon: "Trophy",
    colorHex: "#059669",
    bgLight: "#ecfdf5",
    borderColor: "#a7f3d0",
    badgeClass: "bg-[#ecfdf5] text-[#059669] border-[#a7f3d0]",
    borderClass: "border-[#a7f3d0]",
    textClass: "text-[#059669]",
    gradient: "from-[#ecfdf5] to-[#fdfcfb]",
  },
  Tech: {
    name: "Tech",
    icon: "Cpu",
    colorHex: "#0891b2",
    bgLight: "#ecfeff",
    borderColor: "#a5f3fc",
    badgeClass: "bg-[#ecfeff] text-[#0891b2] border-[#a5f3fc]",
    borderClass: "border-[#a5f3fc]",
    textClass: "text-[#0891b2]",
    gradient: "from-[#ecfeff] to-[#fdfcfb]",
  },
};

export function getCategoryConfig(category: string): CategoryInfo {
  const norm = Object.keys(CATEGORIES_CONFIG).find((k) => {
    const kLower = k.toLowerCase();
    const cLower = (category || "").toLowerCase();
    return (
      kLower === cLower ||
      (kLower === "sport" && cLower === "sports") ||
      (kLower === "tech" && cLower === "technology")
    );
  });

  return (
    (norm ? CATEGORIES_CONFIG[norm] : null) || {
      name: "Tech",
      icon: "Newspaper",
      colorHex: "#0891b2",
      bgLight: "#ecfeff",
      borderColor: "#a5f3fc",
      badgeClass: "bg-[#ecfeff] text-[#0891b2] border-[#a5f3fc]",
      borderClass: "border-[#a5f3fc]",
      textClass: "text-[#0891b2]",
      gradient: "from-[#ecfeff] to-[#fdfcfb]",
    }
  );
}

export function formatPercent(num: number): string {
  if (num === null || num === undefined || isNaN(num)) return "0%";
  return `${(num * 100).toFixed(1)}%`;
}
