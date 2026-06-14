import { useCallback, useState } from "react";
import { runSimulation } from "../api/simulate";
import { useAppStore } from "../store/appStore";

export function useSimulation() {
  const setLastSimulation = useAppStore((s) => s.setLastSimulation);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const simulate = useCallback(
    async (params) => {
      setLoading(true);
      setError(null);
      try {
        const data = await runSimulation(params);
        setResult(data);
        setLastSimulation({ ...data, request: params });
        return data;
      } catch (e) {
        setError(e.message);
        throw e;
      } finally {
        setLoading(false);
      }
    },
    [setLastSimulation]
  );

  return { simulate, result, loading, error };
}
