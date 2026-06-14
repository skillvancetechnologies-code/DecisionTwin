export default function Footer() {
  return (
    <footer className="border-t border-surface-border bg-white">
      <div className="mx-auto max-w-6xl px-4 py-4 text-center text-sm text-gray-500">
        DecisionTwin — AI decision-simulation copilot · {new Date().getFullYear()}
      </div>
    </footer>
  );
}
