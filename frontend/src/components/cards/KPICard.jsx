import { Line, LineChart } from "recharts";
import { signedPercent } from "../../lib/formatters";

// title, value, optional delta (number, %), optional sparkline data [{value}]
export default function KPICard({ title, value, delta, spark = [] }) {
  const deltaColor =
    delta == null ? "" : delta >= 0 ? "text-risk-low" : "text-risk-high";

  return (
    <div className="card">
      <div className="flex items-start justify-between">
        <p className="text-sm font-medium text-gray-500">{title}</p>
        {spark.length > 1 && (
          <LineChart width={60} height={20} data={spark}>
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
      <p className="mt-2 text-3xl font-bold text-brand-navy">{value}</p>
      {delta != null && (
        <p className={`mt-1 text-sm font-medium ${deltaColor}`}>
          {signedPercent(delta)} vs baseline
        </p>
      )}
    </div>
  );
}
