import { create } from "zustand";
import type { ClassificationResponse } from "./types";

export interface HistoryItem {
  id: string;
  textSnippet: string;
  category: string;
  confidence: number;
  timestamp: string;
}

interface ClassifierStore {
  currentText: string;
  selectedModel: string;
  result: ClassificationResponse | null;
  isLoading: boolean;
  history: HistoryItem[];
  totalClassifiedCount: number;
  commandPaletteOpen: boolean;
  setCurrentText: (text: string) => void;
  setSelectedModel: (model: string) => void;
  setResult: (result: ClassificationResponse | null) => void;
  setIsLoading: (loading: boolean) => void;
  addToHistory: (item: HistoryItem) => void;
  clearHistory: () => void;
  incrementCount: () => void;
  setCommandPaletteOpen: (open: boolean) => void;
  toggleCommandPalette: () => void;
}

export const useClassifierStore = create<ClassifierStore>((set) => ({
  currentText: "",
  selectedModel: "distilbert",
  result: null,
  isLoading: false,
  history: [],
  totalClassifiedCount: 2225,
  commandPaletteOpen: false,
  setCurrentText: (text) => set({ currentText: text }),
  setSelectedModel: (model) => set({ selectedModel: model }),
  setResult: (result) => set({ result }),
  setIsLoading: (isLoading) => set({ isLoading }),
  addToHistory: (item) =>
    set((state) => ({
      history: [item, ...state.history.slice(0, 19)],
    })),
  clearHistory: () => set({ history: [] }),
  incrementCount: () =>
    set((state) => ({ totalClassifiedCount: state.totalClassifiedCount + 1 })),
  setCommandPaletteOpen: (open) => set({ commandPaletteOpen: open }),
  toggleCommandPalette: () => set((state) => ({ commandPaletteOpen: !state.commandPaletteOpen })),
}));
