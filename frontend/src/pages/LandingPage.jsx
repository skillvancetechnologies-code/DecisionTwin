import { Link } from "react-router-dom";

const STEPS = [
  ["Upload", "Drop in your sales, HR, or marketing CSV."],
  ["Analyze", "See baseline KPIs computed instantly."],
  ["Simulate", "Ask “what if…?” and get an ML-driven forecast."],
  ["Compare", "Save scenarios and compare side-by-side."],
];

export default function LandingPage() {
  return (
    <div className="space-y-16">
      <section className="flex flex-col items-center gap-6 py-12 text-center">
        <h1 className="max-w-3xl text-4xl font-bold leading-tight text-brand-navy sm:text-5xl">
          Simulate business decisions{" "}
          <span className="text-brand-orange">before</span> you make them.
        </h1>
        <p className="max-w-xl text-lg text-gray-600">
          DecisionTwin turns your company data into an AI copilot. Upload a CSV,
          ask a question, and see the predicted revenue, churn, and risk —
          explained in plain English.
        </p>
        <Link to="/upload" className="btn-primary text-lg">
          Get started →
        </Link>
      </section>

      <section className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {STEPS.map(([title, desc], i) => (
          <div key={title} className="card">
            <div className="mb-2 flex h-8 w-8 items-center justify-center rounded-full bg-brand-navy font-bold text-white">
              {i + 1}
            </div>
            <h3 className="font-semibold">{title}</h3>
            <p className="mt-1 text-sm text-gray-500">{desc}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
