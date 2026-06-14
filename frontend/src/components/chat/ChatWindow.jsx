import { useEffect, useRef, useState } from "react";
import MessageBubble from "./MessageBubble";

export default function ChatWindow({ messages, onSend, streaming }) {
  const [input, setInput] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const submit = (e) => {
    e.preventDefault();
    const text = input.trim();
    if (!text || streaming) return;
    onSend(text);
    setInput("");
  };

  return (
    <div className="flex h-[70vh] flex-col rounded-xl border border-surface-border bg-surface-muted">
      <div className="flex-1 space-y-3 overflow-y-auto p-4">
        {messages.length === 0 && (
          <p className="mt-8 text-center text-sm text-gray-500">
            Ask the copilot about your simulation.
          </p>
        )}
        {messages.map((m, i) => (
          <MessageBubble key={i} role={m.role} content={m.content} />
        ))}
        <div ref={bottomRef} />
      </div>

      <form onSubmit={submit} className="flex gap-2 border-t border-surface-border p-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message…"
          className="flex-1 rounded-lg border border-surface-border px-3 py-2 focus:border-brand-teal focus:outline-none"
        />
        <button type="submit" className="btn-primary" disabled={streaming}>
          Send
        </button>
      </form>
    </div>
  );
}
