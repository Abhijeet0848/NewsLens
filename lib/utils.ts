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
    colorHex: "#a16207",
    bgLight: "#fffbeb",
    borderColor: "#fde68a",
    badgeClass: "bg-[#fffbeb] text-[#a16207] border-[#fde68a]",
    borderClass: "border-[#fde68a]",
    textClass: "text-[#a16207]",
    gradient: "from-[#fffbeb] to-[#fdfcfb]",
  },
  Entertainment: {
    name: "Entertainment",
    icon: "Film",
    colorHex: "#be185d",
    bgLight: "#fdf2f8",
    borderColor: "#fbcfe8",
    badgeClass: "bg-[#fdf2f8] text-[#be185d] border-[#fbcfe8]",
    borderClass: "border-[#fbcfe8]",
    textClass: "text-[#be185d]",
    gradient: "from-[#fdf2f8] to-[#fdfcfb]",
  },
  Politics: {
    name: "Politics",
    icon: "Landmark",
    colorHex: "#be123c",
    bgLight: "#fff1f2",
    borderColor: "#fecdd3",
    badgeClass: "bg-[#fff1f2] text-[#be123c] border-[#fecdd3]",
    borderClass: "border-[#fecdd3]",
    textClass: "text-[#be123c]",
    gradient: "from-[#fff1f2] to-[#fdfcfb]",
  },
  Sport: {
    name: "Sport",
    icon: "Trophy",
    colorHex: "#047857",
    bgLight: "#ecfdf5",
    borderColor: "#a7f3d0",
    badgeClass: "bg-[#ecfdf5] text-[#047857] border-[#a7f3d0]",
    borderClass: "border-[#a7f3d0]",
    textClass: "text-[#047857]",
    gradient: "from-[#ecfdf5] to-[#fdfcfb]",
  },
  Tech: {
    name: "Tech",
    icon: "Cpu",
    colorHex: "#0e7490",
    bgLight: "#ecfeff",
    borderColor: "#a5f3fc",
    badgeClass: "bg-[#ecfeff] text-[#0e7490] border-[#a5f3fc]",
    borderClass: "border-[#a5f3fc]",
    textClass: "text-[#0e7490]",
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
