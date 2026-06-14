export const currency = (value, opts = {}) =>
  new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
    ...opts,
  }).format(Number(value) || 0);

export const percent = (value, digits = 1) =>
  `${(Number(value) || 0).toFixed(digits)}%`;

export const signedPercent = (value, digits = 1) => {
  const n = Number(value) || 0;
  return `${n > 0 ? "+" : ""}${n.toFixed(digits)}%`;
};

export const compactNumber = (value) =>
  new Intl.NumberFormat("en-US", { notation: "compact" }).format(
    Number(value) || 0
  );

export const formatDate = (value) => {
  if (!value) return "";
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? String(value) : d.toLocaleDateString();
};

export const riskColor = (level) => {
  const key = String(level || "").toLowerCase();
  if (key === "low") return "#10803F";
  if (key === "medium" || key === "mid") return "#B45309";
  if (key === "high") return "#B91C1C";
  return "#6B7280";
};
