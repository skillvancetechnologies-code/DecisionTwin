// Horizontal segmented bar with a marker for the current confidence score.
export default function ConfidenceBand({ score = 0 }) {
  const value = Math.max(0, Math.min(100, Number(score) || 0));
  return (
    <div className="w-full">
      <div className="mb-1 flex justify-between text-xs text-gray-500">
        <span>Confidence</span>
        <span className="font-semibold text-brand-navy">{value}%</span>
      </div>
      <div className="relative h-3 w-full rounded-full bg-gradient-to-r from-risk-high via-risk-mid to-risk-low">
        <div
          className="absolute -top-1 h-5 w-1.5 -translate-x-1/2 rounded-full bg-brand-navy shadow"
          style={{ left: `${value}%` }}
          aria-label={`Confidence ${value}%`}
        />
      </div>
    </div>
  );
}
