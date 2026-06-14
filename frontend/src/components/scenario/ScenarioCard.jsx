import { signedPercent } from "../../lib/formatters";
import { downloadReport } from "../../api/scenarios";

const riskBadge = (level) => {
  const key = String(level).toLowerCase();
  if (key === "low") return "bg-risk-low/10 text-risk-low";
  if (key === "medium") return "bg-risk-mid/10 text-risk-mid";
  return "bg-risk-high/10 text-risk-high";
};

export default function ScenarioCard({ scenario }) {
  const k = scenario.kpis || {};
  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <h4 className="font-semibold">{scenario.name}</h4>
        <span className={`rounded-full px-2.5 py-0.5 text-xs ${riskBadge(scenario.risk)}`}>
          {scenario.risk}
        </span>
      </div>
      <p className="mt-2 text-sm text-gray-500">
        Revenue {signedPercent(k.revenue_delta_pct)} · Churn{" "}
        {signedPercent(k.churn_delta_pct)}
      </p>
      <button
        className="btn-secondary mt-3 text-sm"
        onClick={() => downloadReport(scenario.id)}
      >
        Download PDF
      </button>
    </div>
  );
}
