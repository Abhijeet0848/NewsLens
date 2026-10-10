"use client";

import * as React from "react";

interface ConfusionMatrixProps {
  categories: string[];
  matrix: number[][];
  title?: string;
  description?: string;
}

export function ConfusionMatrix({
  categories,
  matrix,
  title = "Confusion Matrix Heatmap",
  description = "Contingency counts across all supported news domains on the held-out test split.",
}: ConfusionMatrixProps) {
  const [hoveredCell, setHoveredCell] = React.useState<{
    trueCat: string;
    predCat: string;
    count: number;
    pct: number;
  } | null>(null);

  if (!categories || categories.length === 0 || !matrix || matrix.length === 0) {
    return null;
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <h2 className="text-sm font-semibold text-[#0f0f0e] font-heading">
            {title}
          </h2>
          <p className="text-xs text-[#57534e]">
            {description}
          </p>
        </div>
        {hoveredCell && (
          <div className="rounded-lg border border-[#a5f3fc] bg-[#ecfeff] px-3 py-1 text-xs font-mono text-[#0e7490]">
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
              <th className="p-2.5 text-left text-[#57534e] font-normal">True \ Pred</th>
              {categories.map((cat) => (
                <th key={cat} className="p-2.5 font-semibold text-[#3f3d3a] truncate max-w-[80px]">
                  {cat}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {matrix.map((row, rowIdx) => {
              const trueCategory = categories[rowIdx] || `Class ${rowIdx + 1}`;
              const totalRow = row.reduce((a, b) => a + b, 0);

              return (
                <tr key={trueCategory} className="border-t border-[#e7e3dd]">
                  <td className="p-2.5 text-left font-semibold text-[#0f0f0e] whitespace-nowrap">
                    {trueCategory}
                  </td>
                  {row.map((val, colIdx) => {
                    const predCategory = categories[colIdx] || `Class ${colIdx + 1}`;
                    const isDiagonal = rowIdx === colIdx;
                    const pct = totalRow > 0 ? Math.round((val / totalRow) * 100) : 0;

                    let cellBg = "#fdfcfb";
                    let textColor = "text-[#57534e]";

                    if (isDiagonal) {
                      cellBg = "#ecfdf5";
                      textColor = "text-[#047857] font-bold";
                    } else if (val > 0) {
                      cellBg = "#fff1f2";
                      textColor = "text-[#be123c] font-bold";
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
