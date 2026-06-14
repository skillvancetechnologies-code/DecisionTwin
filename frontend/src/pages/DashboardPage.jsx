import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import ComparisonTable from "../components/scenario/ComparisonTable";
import ScenarioCard from "../components/scenario/ScenarioCard";
import ScenarioTimeline from "../components/charts/ScenarioTimeline";
import { EmptyState, ErrorState, Spinner } from "../components/ui/States";
import { compareScenarios } from "../api/scenarios";
import { exportComparisonCsv } from "../lib/exporters/csv";
import { exportDashboardSnapshot } from "../lib/exporters/pdf";
import { useAppStore } from "../store/appStore";

export default function DashboardPage() {
  const savedScenarioIds = useAppStore((s) => s.savedScenarioIds);
  const clearScenarios = useAppStore((s) => s.clearScenarios);
  // status: "loading" | "ready" | "error"
  const [state, setState] = useState({ status: "loading", data: null, error: null });
  const [reloadKey, setReloadKey] = useState(0);
  const dashRef = useRef(null);
  const hasScenarios = savedScenarioIds.length > 0;

  useEffect(() => {
    let cancelled = false;
    if (!hasScenarios) return undefined;
    compareScenarios(savedScenarioIds)
      .then((data) => {
        if (!cancelled) setState({ status: "ready", data, error: null });
      })
      .catch((e) => {
        if (!cancelled) setState({ status: "error", data: null, error: e.message });
      });
    return () => {
      cancelled = true;
    };
  }, [savedScenarioIds, reloadKey, hasScenarios]);

  const retry = () => {
    setState({ status: "loading", data: null, error: null });
    setReloadKey((k) => k + 1);
  };

  if (!hasScenarios) {
    return (
      <EmptyState
        title="No saved scenarios yet"
        hint="Run a simulation and save it to compare scenarios here."
        action={
          <Link to="/upload" className="btn-primary mt-2">
            Upload a dataset
          </Link>
        }
      />
    );
  }
  if (state.status === "loading") return <Spinner label="Loading scenarios…" />;
  if (state.status === "error") return <ErrorState message={state.error} onRetry={retry} />;
  if (!state.data?.scenarios?.length) {
    return (
      <EmptyState
        title="No matching scenarios"
        hint="Saved scenarios could not be found on the server."
      />
    );
  }

  const { data } = state;
  const timeline = data.scenarios.map((s) => ({
    name: s.name,
    revenueDelta: s.kpis?.revenue_delta_pct ?? 0,
    riskScore: s.kpis?.risk_score ?? 50,
  }));

  return (
    <div className="space-y-6" ref={dashRef}>
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-brand-navy">
            Scenario <span className="text-gradient">comparison</span>
          </h1>
          <p className="mt-1 text-sm text-brand-navy/50">
            {data.scenarios.length} saved scenario{data.scenarios.length === 1 ? "" : "s"} · best/worst per metric highlighted below.
          </p>
        </div>
        <div className="flex gap-2">
          <button
            className="btn-secondary"
            onClick={() => exportComparisonCsv(data.comparison_table, data.scenarios)}
          >
            Download CSV
          </button>
          <button
            className="btn-secondary"
            onClick={() => exportDashboardSnapshot(dashRef.current)}
          >
            Download PDF
          </button>
          <button className="btn-secondary" onClick={clearScenarios}>
            Clear
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {data.scenarios.map((s, i) => (
          <div key={s.id} className="stagger" style={{ "--i": i }}>
            <ScenarioCard scenario={s} />
          </div>
        ))}
      </div>

      <div className="card">
        <h3 className="mb-4 font-semibold">Metric comparison</h3>
        <ComparisonTable scenarios={data.scenarios} comparisonTable={data.comparison_table} />
      </div>

      <div className="card">
        <h3 className="mb-4 font-semibold">Scenario timeline</h3>
        <ScenarioTimeline data={timeline} />
      </div>
    </div>
  );
}
