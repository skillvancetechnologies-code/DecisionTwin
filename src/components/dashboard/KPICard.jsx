export default function KPICard({
  title,
  value,
  change,
  color = "text-green-400",
}) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-8 backdrop-blur-xl text-white">
      <p className="text-gray-400">{title}</p>

      <h2 className="mt-4 text-4xl font-bold">
        {value}
      </h2>

      <p className={`mt-3 ${color}`}>
        {change}
      </p>
    </div>
  );
}