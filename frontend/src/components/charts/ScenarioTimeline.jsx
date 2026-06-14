import {
  CartesianGrid,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
  ZAxis,
} from "recharts";
import { EmptyState } from "../ui/States";

// data: [{ name, savedAt, revenueDelta, riskScore }]
export default function ScenarioTimeline({ data = [] }) {
  if (!data.length) {
    return <EmptyState title="No scenarios yet" hint="Save a simulation to see it here." />;
  }
  const points = data.map((d, i) => ({ ...d, x: i + 1 }));
  return (
    <ResponsiveContainer width="100%" height={280}>
      <ScatterChart margin={{ top: 16, right: 16, bottom: 8, left: 8 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#F4F5F7" />
        <XAxis
          type="number"
          dataKey="x"
          name="Scenario"
          tick={{ fontSize: 12 }}
          domain={[0, points.length + 1]}
          tickFormatter={(v) => points[v - 1]?.name || ""}
        />
        <YAxis
          type="number"
          dataKey="revenueDelta"
          name="Revenue Δ%"
          tick={{ fontSize: 12 }}
        />
        <ZAxis type="number" dataKey="riskScore" range={[80, 400]} name="Risk" />
        <Tooltip
          cursor={{ strokeDasharray: "3 3" }}
          formatter={(v, n) => [v, n]}
          labelFormatter={() => ""}
        />
        <Scatter data={points} fill="#E07B00" animationDuration={700} />
      </ScatterChart>
    </ResponsiveContainer>
  );
}
