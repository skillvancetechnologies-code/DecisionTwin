import {
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { useMemo } from "react";

// Direction of "good" per metric (execution doc §6.3).
const COLOR_DIRECTION = {
  "Revenue Delta %": "higher_is_better",
  "New Growth Rate": "higher_is_better",
  "Churn Delta %": "lower_is_better",
  "Risk Score": "lower_is_better",
  Confidence: "higher_is_better",
};

function cellColor(row, scenarioId) {
  if (scenarioId === row.best) return "bg-risk-low/15 text-risk-low font-semibold";
  if (scenarioId === row.worst) return "bg-risk-high/15 text-risk-high font-semibold";
  return "";
}

export default function ComparisonTable({ scenarios = [], comparisonTable = [] }) {
  const columns = useMemo(() => {
    const cols = [
      {
        header: "Metric",
        accessorKey: "metric",
        cell: (info) => <span className="font-medium">{info.getValue()}</span>,
      },
    ];
    scenarios.forEach((s) => {
      cols.push({
        id: s.id,
        header: s.name,
        accessorFn: (row) => row[s.id],
        cell: (info) => {
          const v = info.getValue();
          return (
            <span className={`rounded px-2 py-1 ${cellColor(info.row.original, s.id)}`}>
              {v == null ? "—" : Number(v).toFixed(1)}
            </span>
          );
        },
      });
    });
    return cols;
  }, [scenarios]);

  const table = useReactTable({
    data: comparisonTable,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (!scenarios.length) return null;

  return (
    <div className="overflow-x-auto rounded-xl border border-surface-border">
      <table className="min-w-full text-sm">
        <thead className="bg-brand-navy text-white">
          {table.getHeaderGroups().map((hg) => (
            <tr key={hg.id}>
              {hg.headers.map((h) => (
                <th key={h.id} className="px-4 py-2 text-left font-medium">
                  {flexRender(h.column.columnDef.header, h.getContext())}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id} className="border-t border-surface-border">
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id} className="px-4 py-2">
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export { COLOR_DIRECTION };
