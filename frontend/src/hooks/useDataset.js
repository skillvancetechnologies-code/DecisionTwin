import { useCallback, useState } from "react";
import { getBaseline, getPreview, uploadDataset } from "../api/datasets";
import { useAppStore } from "../store/appStore";

export function useDataset() {
  const sessionId = useAppStore((s) => s.sessionId);
  const setDataset = useAppStore((s) => s.setDataset);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const upload = useCallback(
    async ({ file, datasetName, fileType }) => {
      setLoading(true);
      setError(null);
      try {
        const result = await uploadDataset({
          file,
          datasetName,
          fileType,
          sessionId,
        });
        setDataset(result);
        return result;
      } catch (e) {
        setError(e.message);
        throw e;
      } finally {
        setLoading(false);
      }
    },
    [sessionId, setDataset]
  );

  return { upload, getPreview, getBaseline, loading, error };
}
