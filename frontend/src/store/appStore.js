import { create } from "zustand";

function getSessionId() {
  let id = localStorage.getItem("dt_session_id");
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem("dt_session_id", id);
  }
  return id;
}

export const useAppStore = create((set) => ({
  sessionId: getSessionId(),

  dataset: null, // { dataset_id, name, columns, row_count, quality_score, warnings }
  setDataset: (dataset) => set({ dataset }),

  lastSimulation: null,
  setLastSimulation: (lastSimulation) => set({ lastSimulation }),

  // Saved scenario ids for the comparison dashboard (persisted).
  savedScenarioIds: JSON.parse(localStorage.getItem("dt_scenarios") || "[]"),
  addScenarioId: (id) =>
    set((state) => {
      const ids = Array.from(new Set([...state.savedScenarioIds, id]));
      localStorage.setItem("dt_scenarios", JSON.stringify(ids));
      return { savedScenarioIds: ids };
    }),
  clearScenarios: () => {
    localStorage.removeItem("dt_scenarios");
    set({ savedScenarioIds: [] });
  },
}));
