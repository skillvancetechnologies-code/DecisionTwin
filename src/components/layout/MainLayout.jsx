export default function MainLayout({ children }) {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-slate-900 text-white p-4 text-2xl font-semibold">
        DecisionTwin
      </header>

      <main className="p-6">
        {children}
      </main>
    </div>
  );
}