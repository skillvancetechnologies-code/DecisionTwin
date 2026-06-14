// First rows of the dataset; sticky header; horizontal scroll for wide CSVs.
export default function DataPreviewTable({ headers = [], rows = [] }) {
  if (!headers.length) return null;
  return (
    <div className="max-h-96 overflow-auto rounded-xl border border-surface-border">
      <table className="min-w-full border-collapse text-sm">
        <thead className="sticky top-0 bg-brand-navy text-white">
          <tr>
            {headers.map((h) => (
              <th key={h} className="whitespace-nowrap px-4 py-2 text-left font-medium">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} className={i % 2 ? "bg-surface-muted" : "bg-white"}>
              {row.map((cell, j) => (
                <td key={j} className="whitespace-nowrap px-4 py-2 text-gray-700">
                  {cell === null || cell === undefined ? "—" : String(cell)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
