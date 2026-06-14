import { signedPercent } from "../../lib/formatters";
import { downloadReport } from "../../api/scenarios";

const riskBadge = (level) => {
  const key = String(level).toLowerCase();
  if (key === "low") return "border-risk-low/20 bg-risk-low/10 text-risk-low";
  if (key === "medium") return "border-risk-mid/20 bg-risk-mid/10 text-risk-mid";
  return "border-risk-high/20 bg-risk-high/10 text-risk-high";
};

export default function ScenarioCard({ scenario }) {
  const k = scenario.kpis || {};
  return (
    <div className="card-interactive group">
      <div className="flex items-center justify-between gap-2">
        <h4 className="font-semibold text-brand-navy">{scenario.name}</h4>
        <span className={`rounded-full border px-2.5 py-0.5 text-xs font-semibold ${riskBadge(scenario.risk)}`}>
          {scenario.risk}
        </span>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-2">
        <div className="rounded-xl bg-surface-muted/70 p-3">
          <p className="text-[11px] font-medium uppercase tracking-wide text-brand-navy/45">Revenue</p>
          <p className="nums mt-0.5 font-bold text-brand-navy">{signedPercent(k.revenue_delta_pct)}</p>
        </div>
        <div className="rounded-xl bg-surface-muted/70 p-3">
          <p className="text-[11px] font-medium uppercase tracking-wide text-brand-navy/45">Churn</p>
          <p className="nums mt-0.5 font-bold text-brand-navy">{signedPercent(k.churn_delta_pct)}</p>
        </div>
      </div>

      <button
        className="btn-secondary mt-4 w-full text-sm"
        onClick={() => downloadReport(scenario.id)}
      >
        <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" aria-hidden="true">
          <path d="M12 3v12m0 0 4-4m-4 4-4-4M5 21h14" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        Download PDF
      </button>
    </div>
  );
}
