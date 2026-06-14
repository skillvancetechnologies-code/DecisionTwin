export default function Footer() {
  return (
    <footer className="glass border-t">
      <div className="mx-auto max-w-6xl px-4 py-4 text-center text-sm text-brand-navy/50">
        DecisionTwin — AI decision-simulation copilot · {new Date().getFullYear()}
      </div>
    </footer>
  );
}
