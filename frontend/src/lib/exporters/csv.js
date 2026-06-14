import Papa from "papaparse";

function triggerDownload(content, filename, type) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

/** Export the comparison table (array of metric rows) to CSV, client-side. */
export function exportComparisonCsv(comparisonTable, scenarios, filename = "scenarios.csv") {
  if (!comparisonTable?.length) return;
  const idToName = Object.fromEntries((scenarios || []).map((s) => [s.id, s.name]));
  const rows = comparisonTable.map((row) => {
    const out = { Metric: row.metric };
    scenarios.forEach((s) => {
      out[idToName[s.id] || s.id] = row[s.id];
    });
    return out;
  });
  triggerDownload(Papa.unparse(rows), filename, "text/csv;charset=utf-8;");
}
