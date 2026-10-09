"use client";

import * as React from "react";
import { BlockMath, InlineMath } from "react-katex";

export function MathBlock({ math }: { math: string }) {
  return (
    <div className="my-4 px-4 py-3 rounded-xl bg-[#f1efeb] border border-[#e7e3dd] text-[15px] text-[#0f0f0e] overflow-x-auto select-all">
      <BlockMath math={math} />
    </div>
  );
}

export function MathInline({ math }: { math: string }) {
  return <InlineMath math={math} />;
}
