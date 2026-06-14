import { Line, LineChart } from "recharts";
import { signedPercent } from "../../lib/formatters";

// title, value, optional delta (number, %), optional sparkline data [{value}]
export default function KPICard({ title, value, delta, spark = [] }) {
  const up = delta != null && delta >= 0;
  const deltaCls =
    delta == null
      ? ""
      : up
        ? "bg-risk-low/10 text-risk-low"
        : "bg-risk-high/10 text-risk-high";

  return (
    <div className="card-interactive group relative overflow-hidden">
      {/* gradient accent that brightens on hover */}
      <span className="absolute inset-x-0 top-0 h-1 bg-grad-teal opacity-70 transition-opacity duration-200 group-hover:opacity-100" />
      <div className="flex items-start justify-between">
        <p className="text-sm font-medium text-brand-navy/55">{title}</p>
        {spark.length > 1 && (
          <LineChart width={64} height={22} data={spark}>
            <Line
              type="monotone"
              dataKey="value"
              stroke="#0D6E73"
              strokeWidth={2}
              dot={false}
              isAnimationActive={false}
            />
          </LineChart>
        )}
      </div>
      <p className="nums mt-2 text-3xl font-extrabold tracking-tight text-brand-navy">
        {value}
      </p>
      {delta != null && (
        <span className={`nums mt-2 inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-semibold ${deltaCls}`}>
          <svg viewBox="0 0 24 24" className="h-3 w-3" fill="none" aria-hidden="true">
            <path
              d={up ? "M6 14l6-6 6 6" : "M6 10l6 6 6-6"}
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          {signedPercent(delta)} vs baseline
        </span>
      )}
    </div>
  );
}
