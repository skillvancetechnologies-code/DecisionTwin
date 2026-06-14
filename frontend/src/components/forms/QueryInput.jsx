import { useState } from "react";

const DECISION_TYPES = [
  { value: "price_change", label: "Price change" },
  { value: "headcount", label: "Headcount" },
  { value: "marketing", label: "Marketing" },
];

const PARAM_BY_TYPE = {
  price_change: "price_per_unit",
  headcount: "headcount",
  marketing: "marketing_spend",
};

export default function QueryInput({ onSubmit, loading }) {
  const [query, setQuery] = useState("What if I raise prices by 10%?");
  const [decisionType, setDecisionType] = useState("price_change");
  const [magnitude, setMagnitude] = useState(10);

  const submit = (e) => {
    e.preventDefault();
    onSubmit({
      query,
      decision_type: decisionType,
      parameter: PARAM_BY_TYPE[decisionType],
      magnitude: Number(magnitude),
      magnitude_type: "percentage",
    });
  };

  return (
    <form onSubmit={submit} className="card space-y-4">
      <div>
        <label className="mb-1 block text-sm font-medium" htmlFor="query">
          Decision question
        </label>
        <textarea
          id="query"
          rows={2}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full rounded-lg border border-surface-border px-3 py-2 focus:border-brand-teal focus:outline-none focus:ring-1 focus:ring-brand-teal"
        />
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div>
          <label className="mb-1 block text-sm font-medium" htmlFor="dtype">
            Decision type
          </label>
          <select
            id="dtype"
            value={decisionType}
            onChange={(e) => setDecisionType(e.target.value)}
            className="w-full rounded-lg border border-surface-border px-3 py-2"
          >
            {DECISION_TYPES.map((d) => (
              <option key={d.value} value={d.value}>
                {d.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium" htmlFor="mag">
            Magnitude: {magnitude}%
          </label>
          <input
            id="mag"
            type="range"
            min={-50}
            max={50}
            value={magnitude}
            onChange={(e) => setMagnitude(e.target.value)}
            className="w-full accent-brand-orange"
          />
        </div>
      </div>

      <button type="submit" className="btn-primary" disabled={loading}>
        {loading ? "Simulating…" : "Run simulation"}
      </button>
    </form>
  );
}
