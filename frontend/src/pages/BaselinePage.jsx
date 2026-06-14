import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import KPICard from "../components/cards/KPICard";
import BaselineLineChart from "../components/charts/BaselineLineChart";
import { ErrorState, SkeletonCard } from "../components/ui/States";
import { getBaseline } from "../api/datasets";
import { compactNumber, currency, percent } from "../lib/formatters";

export default function BaselinePage() {
  const { datasetId } = useParams();
  // status: "loading" | "ready" | "error"
  const [state, setState] = useState({ status: "loading", metrics: null, error: null });
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    getBaseline(datasetId)
      .then((data) => {
        if (!cancelled) setState({ status: "ready", metrics: data.metrics, error: null });
      })
      .catch((e) => {
        if (!cancelled) setState({ status: "error", metrics: null, error: e.message });
      });
    return () => {
      cancelled = true;
    };
  }, [datasetId, reloadKey]);

  const retry = () => {
    setState({ status: "loading", metrics: null, error: null });
    setReloadKey((k) => k + 1);
  };

  if (state.status === "loading") {
    return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <SkeletonCard key={i} />
        ))}
      </div>
    );
  }
  if (state.status === "error") return <ErrorState message={state.error} onRetry={retry} />;

  const metrics = state.metrics;
  const cards = metrics.kpi_cards || {};
  const spark = (metrics.monthly_revenue || []).map((m) => ({ value: m.value }));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Baseline analytics</h1>
        <Link to={`/simulate/${datasetId}`} className="btn-primary">
          Run a simulation →
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KPICard
          title={cards.revenue_total?.label || "Total Revenue"}
          value={currency(cards.revenue_total?.value)}
          spark={spark}
        />
        <KPICard
          title={cards.growth?.label || "Growth %"}
          value={percent(cards.growth?.value)}
          delta={cards.growth?.value}
        />
        <KPICard
          title={cards.churn?.label || "Churn %"}
          value={percent(cards.churn?.value)}
        />
        <KPICard title={cards.cac?.label || "Avg CAC"} value={currency(cards.cac?.value)} />
      </div>

      <div className="card">
        <h3 className="mb-4 font-semibold">Monthly revenue trend</h3>
        <BaselineLineChart data={metrics.monthly_revenue || []} />
      </div>

      <p className="text-sm text-gray-500">
        Trend: <span className="font-medium">{metrics.trend}</span> · Months:{" "}
        {compactNumber((metrics.monthly_revenue || []).length)}
      </p>
    </div>
  );
}
