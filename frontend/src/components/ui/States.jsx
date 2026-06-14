export function Spinner({ label = "Loading…" }) {
  return (
    <div className="flex items-center gap-3 text-brand-navy/60">
      <span className="h-5 w-5 animate-spin rounded-full border-2 border-surface-border border-t-brand-orange" />
      {label}
    </div>
  );
}

export function ErrorState({ message, onRetry }) {
  return (
    <div className="card animate-fade-up border-risk-high/30 bg-risk-high/5">
      <div className="flex items-start gap-3">
        <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-risk-high/10 text-risk-high">
          <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" aria-hidden="true">
            <path d="M12 9v4m0 4h.01M10.3 3.9 2 18a2 2 0 0 0 1.7 3h16.6A2 2 0 0 0 22 18L13.7 3.9a2 2 0 0 0-3.4 0Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </span>
        <div>
          <p className="font-semibold text-risk-high">{message || "Something went wrong."}</p>
          {onRetry && (
            <button className="btn-secondary mt-3" onClick={onRetry}>
              Try again
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export function EmptyState({ title, hint, action }) {
  return (
    <div className="card animate-fade-up flex flex-col items-center gap-3 py-14 text-center">
      <span className="flex h-12 w-12 items-center justify-center rounded-2xl bg-brand-navy/5 text-brand-teal">
        <svg viewBox="0 0 24 24" className="h-6 w-6" fill="none" aria-hidden="true">
          <path d="M3 7v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-7L9.5 4.5A2 2 0 0 0 8 4H5a2 2 0 0 0-2 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </span>
      <p className="text-lg font-semibold text-brand-navy">{title}</p>
      {hint && <p className="max-w-md text-sm text-brand-navy/55">{hint}</p>}
      {action}
    </div>
  );
}

export function SkeletonCard() {
  return (
    <div className="card relative overflow-hidden">
      <div className="mb-3 h-3 w-1/3 rounded bg-surface-muted" />
      <div className="h-8 w-2/3 rounded bg-surface-muted" />
      {/* shimmer sweep */}
      <span className="absolute inset-0 -translate-x-full bg-gradient-to-r from-transparent via-white/60 to-transparent animate-[shimmer_1.5s_infinite]" />
    </div>
  );
}
