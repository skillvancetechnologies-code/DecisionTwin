import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import QueryInput from "../components/forms/QueryInput";
import SimResultCard from "../components/cards/SimResultCard";
import { ErrorState } from "../components/ui/States";
import { useSimulation } from "../hooks/useSimulation";
import { saveScenario } from "../api/scenarios";
import { useAppStore } from "../store/appStore";

export default function SimulatePage() {
  const { datasetId } = useParams();
  const navigate = useNavigate();
  const { simulate, result, loading, error } = useSimulation();
  const sessionId = useAppStore((s) => s.sessionId);
  const addScenarioId = useAppStore((s) => s.addScenarioId);
  const [lastQuery, setLastQuery] = useState("");
  const [saving, setSaving] = useState(false);
  const [savedMsg, setSavedMsg] = useState(null);

  const handleSubmit = async ({ query, ...params }) => {
    setLastQuery(query);
    setSavedMsg(null);
    await simulate({ dataset_id: datasetId, ...params });
  };

  const handleSave = async () => {
    if (!result) return;
    setSaving(true);
    try {
      const res = await saveScenario({
        scenario_name: lastQuery.slice(0, 60) || "Untitled scenario",
        user_query: lastQuery,
        simulation_result: result,
        dataset_id: datasetId,
        user_session_id: sessionId,
      });
      addScenarioId(res.scenario_id);
      setSavedMsg("Scenario saved ✓");
    } catch (e) {
      setSavedMsg(e.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Run a simulation</h1>
      <QueryInput onSubmit={handleSubmit} loading={loading} />
      {error && <ErrorState message={error} />}
      {result && (
        <>
          <SimResultCard result={result} onSave={handleSave} saving={saving} />
          {savedMsg && (
            <div className="flex items-center gap-4">
              <span className="text-sm font-medium text-risk-low">{savedMsg}</span>
              <button className="btn-secondary" onClick={() => navigate("/dashboard")}>
                Go to dashboard →
              </button>
              <button
                className="btn-secondary"
                onClick={() => navigate(`/chat/${sessionId}`)}
              >
                Discuss in chat →
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
