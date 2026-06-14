import { Link } from "react-router-dom";

const STEPS = [
  ["Upload", "Drop in your sales, HR, or marketing CSV.", "M12 16V4m0 0 4 4m-4-4-4 4M5 20h14"],
  ["Analyze", "See baseline KPIs computed instantly.", "M4 19V5m4 14V9m4 10V11m4 8V7"],
  ["Simulate", "Ask “what if…?” and get an ML-driven forecast.", "M12 3v2m0 14v2m9-9h-2M5 12H3m14.95 6.95-1.4-1.4M7.46 7.46 6.05 6.05m11.9 0-1.41 1.41M7.46 16.54l-1.41 1.41"],
  ["Compare", "Save scenarios and compare side-by-side.", "M9 17V7m6 10V7M4 21h16M4 3h16"],
];

const STATS = [
  ["3", "decision types"],
  ["<2s", "to first forecast"],
  ["Plain-English", "AI explanations"],
];

function StepIcon({ d }) {
  return (
    <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" aria-hidden="true">
      <path d={d} stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export default function LandingPage() {
  return (
    <div className="space-y-20">
      {/* --- Hero --- */}
      <section className="relative overflow-hidden">
        {/* Floating brand orbs */}
        <div className="pointer-events-none absolute -left-16 -top-10 h-56 w-56 rounded-full bg-brand-orange/20 blur-3xl animate-float" />
        <div
          className="pointer-events-none absolute -right-10 top-24 h-64 w-64 rounded-full bg-brand-teal/20 blur-3xl animate-float"
          style={{ animationDelay: "1.5s" }}
        />

        <div className="relative flex flex-col items-center gap-6 py-16 text-center">
          <span className="badge animate-fade-in">
            <span className="h-1.5 w-1.5 rounded-full bg-brand-orange" />
            AI decision-simulation copilot
          </span>

          <h1 className="max-w-3xl animate-fade-up text-4xl font-extrabold leading-[1.1] tracking-tight text-brand-navy sm:text-6xl">
            Simulate business decisions{" "}
            <span className="text-gradient">before</span> you make them.
          </h1>

          <p className="max-w-xl animate-fade-up text-lg text-brand-navy/60" style={{ animationDelay: "80ms" }}>
            DecisionTwin turns your company data into an AI copilot. Upload a CSV,
            ask a question, and see predicted revenue, churn, and risk — explained
            in plain English.
          </p>

          <div className="flex animate-fade-up flex-wrap items-center justify-center gap-3" style={{ animationDelay: "160ms" }}>
            <Link to="/upload" className="btn-primary text-base">
              Get started
              <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" aria-hidden="true">
                <path d="M5 12h14m-6-6 6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </Link>
            <Link to="/dashboard" className="btn-secondary text-base">
              View dashboard
            </Link>
          </div>

          {/* Trust / stat strip */}
          <div className="mt-8 grid w-full max-w-lg animate-fade-up grid-cols-3 divide-x divide-surface-border rounded-2xl border border-white/60 bg-white/70 py-4 backdrop-blur" style={{ animationDelay: "240ms" }}>
            {STATS.map(([value, label]) => (
              <div key={label} className="px-2">
                <p className="nums text-2xl font-extrabold text-brand-navy">{value}</p>
                <p className="mt-0.5 text-xs text-brand-navy/50">{label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* --- How it works --- */}
      <section className="space-y-8">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-brand-navy">How it works</h2>
          <p className="mt-1 text-sm text-brand-navy/50">From raw CSV to a defensible decision in four steps.</p>
        </div>

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {STEPS.map(([title, desc, icon], i) => (
            <div key={title} className="card-interactive group stagger" style={{ "--i": i }}>
              <div className="accent-bar mb-4" />
              <div className="mb-3 flex h-11 w-11 items-center justify-center rounded-xl bg-brand-navy/5 text-brand-teal transition-colors duration-200 group-hover:bg-grad-navy group-hover:text-brand-orange">
                <StepIcon d={icon} />
              </div>
              <div className="flex items-center gap-2">
                <span className="nums text-xs font-bold text-brand-orange">0{i + 1}</span>
                <h3 className="font-semibold text-brand-navy">{title}</h3>
              </div>
              <p className="mt-1 text-sm text-brand-navy/55">{desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
