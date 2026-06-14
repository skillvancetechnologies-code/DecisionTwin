import { useState } from "react";
import { useNavigate } from "react-router-dom";
import UploadDropzone from "../components/forms/UploadDropzone";
import DataPreviewTable from "../components/forms/DataPreviewTable";
import { ErrorState, Spinner } from "../components/ui/States";
import { useDataset } from "../hooks/useDataset";
import { getPreview } from "../api/datasets";

const FILE_TYPES = ["sales", "hr", "marketing", "customer", "ops", "financial"];

export default function UploadPage() {
  const navigate = useNavigate();
  const { upload, loading, error } = useDataset();
  const [file, setFile] = useState(null);
  const [datasetName, setDatasetName] = useState("");
  const [fileType, setFileType] = useState("sales");
  const [result, setResult] = useState(null);
  const [preview, setPreview] = useState(null);

  const handleUpload = async () => {
    if (!file) return;
    const res = await upload({
      file,
      datasetName: datasetName || file.name.replace(/\.csv$/i, ""),
      fileType,
    });
    setResult(res);
    try {
      setPreview(await getPreview(res.dataset_id));
    } catch {
      /* preview is best-effort */
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Upload a dataset</h1>

      <UploadDropzone file={file} onFile={setFile} />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label className="mb-1 block text-sm font-medium">Dataset name</label>
          <input
            value={datasetName}
            onChange={(e) => setDatasetName(e.target.value)}
            placeholder="Q3 Sales Data"
            className="w-full rounded-lg border border-surface-border px-3 py-2"
          />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium">File type</label>
          <select
            value={fileType}
            onChange={(e) => setFileType(e.target.value)}
            className="w-full rounded-lg border border-surface-border px-3 py-2"
          >
            {FILE_TYPES.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <button className="btn-primary" onClick={handleUpload} disabled={!file || loading}>
          {loading ? "Uploading…" : "Upload & validate"}
        </button>
        {loading && <Spinner label="Validating CSV…" />}
      </div>

      {error && <ErrorState message={error} />}

      {result && (
        <div className="card space-y-3">
          <div className="flex flex-wrap items-center gap-4">
            <h3 className="text-lg font-semibold">{result.name}</h3>
            <span className="rounded-full bg-risk-low/10 px-3 py-1 text-sm text-risk-low">
              Quality {result.quality_score}
            </span>
            <span className="text-sm text-gray-500">{result.row_count} rows</span>
          </div>
          {result.warnings?.length > 0 && (
            <ul className="list-inside list-disc text-sm text-risk-mid">
              {result.warnings.map((w) => (
                <li key={w}>{w}</li>
              ))}
            </ul>
          )}
          {preview && (
            <DataPreviewTable headers={preview.headers} rows={preview.rows} />
          )}
          <div className="flex gap-3">
            <button
              className="btn-primary"
              onClick={() => navigate(`/baseline/${result.dataset_id}`)}
            >
              View baseline →
            </button>
            <button
              className="btn-secondary"
              onClick={() => navigate(`/simulate/${result.dataset_id}`)}
            >
              Go to simulation
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
