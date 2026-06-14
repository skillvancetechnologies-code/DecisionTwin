import { PolarAngleAxis, RadialBar, RadialBarChart } from "recharts";

// Semicircular 0-100 gauge with a color band. (Execution doc §6.2)
export default function RiskGauge({ score = 0, variant = "md" }) {
  const value = Math.max(0, Math.min(100, Number(score) || 0));
  const color = value < 34 ? "#10803F" : value < 67 ? "#B45309" : "#B91C1C";
  const data = [{ name: "risk", value, fill: color }];
  const size = variant === "lg" ? 240 : variant === "sm" ? 120 : 180;

  return (
    <div className="flex flex-col items-center">
      <RadialBarChart
        width={size}
        height={size / 2 + 20}
        innerRadius="80%"
        outerRadius="100%"
        startAngle={180}
        endAngle={0}
        data={data}
      >
        <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
        <RadialBar background dataKey="value" cornerRadius={6} />
      </RadialBarChart>
      <div className="text-3xl font-bold" style={{ color }}>
        {value}
      </div>
      <div className="text-sm text-gray-500">Risk Score</div>
    </div>
  );
}
