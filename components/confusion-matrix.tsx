"use client";

import * as React from "react";

const BBC_CONFUSION_DATA = {
  categories: ["Business", "Entertainment", "Politics", "Sport", "Tech"],
  matrix: [
    [98, 0, 1, 0, 1],   // Business
    [0, 97, 1, 0, 2],   // Entertainment
    [1, 1, 96, 0, 2],   // Politics
    [0, 0, 0, 99, 1],   // Sport
    [2, 1, 1, 0, 96],   // Tech
  ],
};

export function ConfusionMatrix() {
  const [hoveredCell, setHoveredCell] = React.useState<{
    trueCat: string;
    predCat: string;
    count: number;
    pct: number;
  } | null>(null);

  const { categories, matrix } = BBC_CONFUSION_DATA;

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <h4 className="text-sm font-semibold text-[#0f0f0e] font-heading">
            5x5 BBC News Confusion Matrix Heatmap
          </h4>
          <p className="text-xs text-[#6b6660]">
            Hover over any intersection cell to inspect contingency counts across the 5 BBC news domains.
          </p>
        </div>
        {hoveredCell && (
          <div className="rounded-lg border border-[#a5f3fc] bg-[#ecfeff] px-3 py-1 text-xs font-mono text-[#0891b2]">
            True: <span className="font-bold">{hoveredCell.trueCat}</span> &bull; Pred:{" "}
            <span className="font-bold">{hoveredCell.predCat}</span> &bull; Count:{" "}
            <span className="font-bold">{hoveredCell.count}</span> ({hoveredCell.pct}%)
          </div>
        )}
      </div>

      <div className="overflow-x-auto rounded-xl border border-[#e7e3dd] bg-[#fdfcfb] p-4 shadow-sm">
        <table className="w-full border-collapse text-center text-xs font-mono">
          <thead>
            <tr>
              <th className="p-2.5 text-left text-[#8a847d] font-normal">True \ Pred</th>
              {categories.map((cat) => (
                <th key={cat} className="p-2.5 font-semibold text-[#3f3d3a] truncate max-w-[80px]">
                  {cat}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {matrix.map((row, rowIdx) => {
              const trueCategory = categories[rowIdx];
              const totalRow = row.reduce((a, b) => a + b, 0);

              return (
                <tr key={trueCategory} className="border-t border-[#e7e3dd]">
                  <td className="p-2.5 text-left font-semibold text-[#0f0f0e] whitespace-nowrap">
                    {trueCategory}
                  </td>
                  {row.map((val, colIdx) => {
                    const predCategory = categories[colIdx];
                    const isDiagonal = rowIdx === colIdx;
                    const pct = Math.round((val / totalRow) * 100);

                    let cellBg = "#fdfcfb";
                    let textColor = "text-[#8a847d]";

                    if (isDiagonal) {
                      cellBg = "#ecfdf5";
                      textColor = "text-[#059669] font-bold";
                    } else if (val > 0) {
                      cellBg = "#fff1f2";
                      textColor = "text-[#e11d48] font-bold";
                    }

                    return (
                      <td
                        key={colIdx}
                        onMouseEnter={() =>
                          setHoveredCell({
                            trueCat: trueCategory,
                            predCat: predCategory,
                            count: val,
                            pct,
                          })
                        }
                        onMouseLeave={() => setHoveredCell(null)}
                        className={`p-2.5 cursor-pointer transition-all duration-150 hover:ring-2 hover:ring-indigo-400 rounded ${textColor}`}
                        style={{ backgroundColor: cellBg }}
                      >
                        {val}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
