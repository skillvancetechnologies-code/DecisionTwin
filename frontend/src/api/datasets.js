import client from "./client";

export async function uploadDataset({ file, datasetName, fileType, sessionId }) {
  const form = new FormData();
  form.append("file", file);
  form.append("dataset_name", datasetName);
  form.append("file_type", fileType);
  if (sessionId) form.append("user_session_id", sessionId);

  const { data } = await client.post("/datasets/upload", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function getPreview(datasetId) {
  const { data } = await client.get(`/datasets/${datasetId}/preview`);
  return data;
}

export async function getBaseline(datasetId) {
  const { data } = await client.get(`/analytics/baseline/${datasetId}`);
  return data;
}
