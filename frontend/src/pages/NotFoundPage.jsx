import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <div className="flex flex-col items-center gap-4 py-24 text-center">
      <h1 className="text-6xl font-bold text-brand-navy">404</h1>
      <p className="text-gray-600">This page doesn’t exist.</p>
      <Link to="/" className="btn-primary">
        Back home
      </Link>
    </div>
  );
}
