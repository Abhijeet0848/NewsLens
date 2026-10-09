export default function BatchLoading() {
  return (
    <div className="mx-auto max-w-7xl px-5 md:px-8 pt-8 md:pt-12 pb-16 md:pb-20 space-y-6 md:space-y-8 animate-pulse">
      <div className="space-y-2">
        <div className="h-3 w-32 bg-[#f1efeb] rounded" />
        <div className="h-7 w-64 bg-[#f1efeb] rounded-lg" />
        <div className="h-4 w-96 bg-[#f1efeb] rounded" />
      </div>
      <div className="border-t border-[#e7e3dd]" />
      <div className="h-44 bg-[#fdfcfb] border-2 border-dashed border-[#e7e3dd] rounded-2xl" />
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="h-24 bg-[#fdfcfb] border border-[#e7e3dd] rounded-xl" />
        <div className="h-24 bg-[#fdfcfb] border border-[#e7e3dd] rounded-xl" />
        <div className="h-24 bg-[#fdfcfb] border border-[#e7e3dd] rounded-xl" />
        <div className="h-24 bg-[#fdfcfb] border border-[#e7e3dd] rounded-xl" />
      </div>
    </div>
  );
}
