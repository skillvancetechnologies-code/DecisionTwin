import { Link, NavLink } from "react-router-dom";
import { useAppStore } from "../../store/appStore";

const linkClass = ({ isActive }) =>
  `relative px-3 py-2 text-sm font-medium rounded-lg transition-colors duration-200 ${
    isActive
      ? "text-brand-navy"
      : "text-brand-navy/60 hover:text-brand-navy hover:bg-white/60"
  }`;

function NavItem({ to, children }) {
  return (
    <NavLink to={to} className={linkClass}>
      {({ isActive }) => (
        <>
          {children}
          {isActive && (
            <span className="absolute inset-x-3 -bottom-px h-0.5 rounded-full bg-grad-orange" />
          )}
        </>
      )}
    </NavLink>
  );
}

function LogoMark() {
  return (
    <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-grad-navy shadow-card">
      <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" aria-hidden="true">
        <path
          d="M4 16.5 9 11l3.5 3.5L20 7"
          stroke="#E07B00"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <circle cx="20" cy="7" r="2" fill="#F2A33C" />
      </svg>
    </span>
  );
}

export default function Navbar() {
  const dataset = useAppStore((s) => s.dataset);

  return (
    <header className="glass sticky top-0 z-40 border-b">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link to="/" className="flex items-center gap-2.5">
          <LogoMark />
          <span className="text-xl font-extrabold tracking-tight">
            <span className="text-brand-navy">Decision</span>
            <span className="text-brand-orange">Twin</span>
          </span>
        </Link>
        <div className="flex items-center gap-1">
          <NavItem to="/upload">Upload</NavItem>
          {dataset && (
            <>
              <NavItem to={`/baseline/${dataset.dataset_id}`}>Baseline</NavItem>
              <NavItem to={`/simulate/${dataset.dataset_id}`}>Simulate</NavItem>
            </>
          )}
          <NavItem to="/dashboard">Dashboard</NavItem>
        </div>
      </nav>
    </header>
  );
}
