export function Spinner({ label = "Loading…" }) {
  return (
    <div className="flex items-center gap-3 text-gray-500">
      <span className="h-5 w-5 animate-spin rounded-full border-2 border-surface-border border-t-brand-orange" />
      {label}
    </div>
  );
}

export function ErrorState({ message, onRetry }) {
  return (
    <div className="card border-risk-high/30 bg-risk-high/5">
      <p className="font-medium text-risk-high">{message || "Something went wrong."}</p>
      {onRetry && (
        <button className="btn-secondary mt-3" onClick={onRetry}>
          Try again
        </button>
      )}
    </div>
  );
}

export function EmptyState({ title, hint, action }) {
  return (
    <div className="card flex flex-col items-center gap-2 py-12 text-center">
      <p className="text-lg font-semibold">{title}</p>
      {hint && <p className="max-w-md text-sm text-gray-500">{hint}</p>}
      {action}
    </div>
  );
}

export function SkeletonCard() {
  return (
    <div className="card animate-pulse">
      <div className="mb-3 h-3 w-1/3 rounded bg-surface-muted" />
      <div className="h-8 w-2/3 rounded bg-surface-muted" />
    </div>
  );
}
