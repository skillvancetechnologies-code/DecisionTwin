import client, { API_BASE_URL } from "./client";

export async function saveScenario(payload) {
  const { data } = await client.post("/scenarios/save", payload);
  return data;
}

export async function compareScenarios(ids) {
  const { data } = await client.get("/scenarios/compare", {
    params: { ids: ids.join(",") },
  });
  return data;
}

export function reportUrl(scenarioId) {
  return `${API_BASE_URL}/scenarios/${scenarioId}/report`;
}

export async function downloadReport(scenarioId) {
  const res = await fetch(reportUrl(scenarioId));
  if (!res.ok) throw new Error("Failed to fetch PDF report");
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `scenario_${scenarioId}.pdf`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}
