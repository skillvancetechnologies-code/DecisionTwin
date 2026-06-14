import { Link, NavLink } from "react-router-dom";
import { useAppStore } from "../../store/appStore";

const linkClass = ({ isActive }) =>
  `px-3 py-2 text-sm font-medium rounded-lg transition ${
    isActive ? "bg-brand-navy text-white" : "text-brand-navy hover:bg-surface-muted"
  }`;

export default function Navbar() {
  const dataset = useAppStore((s) => s.dataset);

  return (
    <header className="border-b border-surface-border bg-white">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link to="/" className="flex items-center gap-2">
          <span className="text-xl font-bold text-brand-navy">Decision</span>
          <span className="text-xl font-bold text-brand-orange">Twin</span>
        </Link>
        <div className="flex items-center gap-1">
          <NavLink to="/upload" className={linkClass}>
            Upload
          </NavLink>
          {dataset && (
            <>
              <NavLink to={`/baseline/${dataset.dataset_id}`} className={linkClass}>
                Baseline
              </NavLink>
              <NavLink to={`/simulate/${dataset.dataset_id}`} className={linkClass}>
                Simulate
              </NavLink>
            </>
          )}
          <NavLink to="/dashboard" className={linkClass}>
            Dashboard
          </NavLink>
        </div>
      </nav>
    </header>
  );
}
