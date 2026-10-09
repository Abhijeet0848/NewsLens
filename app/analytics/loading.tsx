export default function AnalyticsLoading() {
  return (
    <div className="mx-auto max-w-7xl px-5 md:px-8 pt-8 md:pt-12 pb-16 md:pb-20 space-y-6 md:space-y-10 animate-pulse">
      <div className="space-y-2">
        <div className="h-3 w-40 bg-[#f1efeb] rounded" />
        <div className="h-7 w-80 bg-[#f1efeb] rounded-lg" />
        <div className="h-4 w-96 bg-[#f1efeb] rounded" />
      </div>
      <div className="border-t border-[#e7e3dd]" />
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="h-28 bg-[#fdfcfb] border border-[#e7e3dd] rounded-2xl" />
        <div className="h-28 bg-[#fdfcfb] border border-[#e7e3dd] rounded-2xl" />
        <div className="h-28 bg-[#fdfcfb] border border-[#e7e3dd] rounded-2xl" />
        <div className="h-28 bg-[#fdfcfb] border border-[#e7e3dd] rounded-2xl" />
      </div>
      <div className="h-72 bg-[#fdfcfb] border border-[#e7e3dd] rounded-2xl" />
      <div className="h-64 bg-[#fdfcfb] border border-[#e7e3dd] rounded-2xl" />
    </div>
  );
}
