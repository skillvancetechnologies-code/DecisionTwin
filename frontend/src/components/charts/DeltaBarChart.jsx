import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { EmptyState } from "../ui/States";

// data: [{ kpi, before, after }]
export default function DeltaBarChart({ data = [] }) {
  if (!data.length) {
    return <EmptyState title="No deltas to chart" />;
  }
  return (
    <ResponsiveContainer width="100%" height={Math.max(180, data.length * 70)}>
      <BarChart data={data} layout="vertical" margin={{ left: 24, right: 16 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#F4F5F7" />
        <XAxis type="number" tick={{ fontSize: 12 }} />
        <YAxis type="category" dataKey="kpi" tick={{ fontSize: 12 }} width={90} />
        <Tooltip />
        <Legend />
        <Bar dataKey="before" fill="#9CA3AF" radius={[0, 4, 4, 0]} animationDuration={600} />
        <Bar dataKey="after" fill="#E07B00" radius={[0, 4, 4, 0]} animationDuration={600} />
      </BarChart>
    </ResponsiveContainer>
  );
}
