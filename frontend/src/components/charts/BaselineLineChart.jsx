import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { compactNumber, currency } from "../../lib/formatters";
import { EmptyState } from "../ui/States";

// data: [{ month, value }] (baseline.metrics.monthly_revenue)
export default function BaselineLineChart({ data = [] }) {
  if (!data.length) {
    return <EmptyState title="No revenue trend" hint="This dataset has no dated revenue series." />;
  }
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} margin={{ top: 8, right: 16, bottom: 0, left: 8 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#F4F5F7" />
        <XAxis dataKey="month" tick={{ fontSize: 12 }} />
        <YAxis tickFormatter={compactNumber} tick={{ fontSize: 12 }} width={48} />
        <Tooltip formatter={(v) => currency(v)} />
        <Line
          type="monotone"
          dataKey="value"
          stroke="#0D6E73"
          strokeWidth={2.5}
          dot={{ r: 3 }}
          isAnimationActive
          animationDuration={700}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
