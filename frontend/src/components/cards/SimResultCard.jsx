import { useState } from "react";
import { currency, signedPercent } from "../../lib/formatters";
import RiskGauge from "../charts/RiskGauge";
import ConfidenceBand from "../charts/ConfidenceBand";
import DeltaBarChart from "../charts/DeltaBarChart";

const riskBadge = (level) => {
  const key = String(level).toLowerCase();
  if (key === "low") return "bg-risk-low/10 text-risk-low";
  if (key === "medium") return "bg-risk-mid/10 text-risk-mid";
  return "bg-risk-high/10 text-risk-high";
};

export default function SimResultCard({ result, onSave, saving }) {
  const [expanded, setExpanded] = useState(false);
  if (!result) return null;

  const k = result.predicted_kpis || {};
  const deltaData = [
    {
      kpi: "Revenue",
      before: result.deltas?.before?.revenue ?? 0,
      after: result.deltas?.after?.revenue ?? 0,
    },
    {
      kpi: "Growth %",
      before: result.deltas?.before?.growth_rate ?? 0,
      after: result.deltas?.after?.growth_rate ?? 0,
    },
    {
      kpi: "Churn %",
      before: result.deltas?.before?.churn ?? 0,
      after: result.deltas?.after?.churn ?? 0,
    },
  ];

  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Simulation Result</h3>
        <span
          className={`rounded-full px-3 py-1 text-sm font-medium ${riskBadge(
            result.risk_level
          )}`}
        >
          {result.risk_level} risk
        </span>
      </div>

      <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div>
          <p className="text-sm text-gray-500">Revenue Δ</p>
          <p className="text-2xl font-bold text-brand-navy">
            {signedPercent(k.revenue_delta_pct)}
          </p>
          <p className="text-xs text-gray-400">{currency(k.revenue_delta_abs)}</p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Churn Δ</p>
          <p className="text-2xl font-bold text-brand-navy">
            {signedPercent(k.churn_delta_pct)}
          </p>
        </div>
        <RiskGauge score={result.risk_score} variant="sm" />
      </div>

      <div className="mt-4">
        <ConfidenceBand score={result.confidence_score} />
      </div>

      <div className="mt-4 flex flex-wrap gap-3">
        <button className="btn-secondary" onClick={() => setExpanded((v) => !v)}>
          {expanded ? "Hide details" : "Expand details"}
        </button>
        {onSave && (
          <button className="btn-primary" onClick={onSave} disabled={saving}>
            {saving ? "Saving…" : "Save scenario"}
          </button>
        )}
      </div>

      {expanded && (
        <div className="mt-4 border-t border-surface-border pt-4">
          <DeltaBarChart data={deltaData} />
          {result.risk_factors?.length > 0 && (
            <ul className="mt-3 list-inside list-disc text-sm text-gray-600">
              {result.risk_factors.map((f) => (
                <li key={f}>{f}</li>
              ))}
            </ul>
          )}
          <p className="mt-2 text-xs text-gray-400">Model: {result.model_used}</p>
        </div>
      )}
    </div>
  );
}
