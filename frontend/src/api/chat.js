import { API_BASE_URL } from "./client";

/**
 * Stream a chat response via fetch + ReadableStream, parsing SSE frames.
 * Calls onToken(delta) for each token event and onDone(payload) at the end.
 */
export async function sendChatMessage(body, { onToken, onDone, signal } = {}) {
  const res = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal,
  });
  if (!res.ok || !res.body) throw new Error("Chat request failed");

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    const frames = buffer.split("\n\n");
    buffer = frames.pop() || "";

    for (const frame of frames) {
      const eventMatch = frame.match(/^event:\s*(.+)$/m);
      const dataMatch = frame.match(/^data:\s*(.+)$/m);
      if (!dataMatch) continue;
      const event = eventMatch ? eventMatch[1].trim() : "message";
      let payload;
      try {
        payload = JSON.parse(dataMatch[1]);
      } catch {
        continue;
      }
      if (event === "token") onToken?.(payload.delta || "");
      else if (event === "done") onDone?.(payload);
    }
  }
}
