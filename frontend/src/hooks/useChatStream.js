import { useCallback, useRef, useState } from "react";
import { sendChatMessage } from "../api/chat";
import { useAppStore } from "../store/appStore";

export function useChatStream() {
  const sessionId = useAppStore((s) => s.sessionId);
  const [messages, setMessages] = useState([]);
  const [streaming, setStreaming] = useState(false);
  const [error, setError] = useState(null);
  const abortRef = useRef(null);

  const send = useCallback(
    async (userMessage, simulationResult = null) => {
      setError(null);
      setStreaming(true);
      abortRef.current = new AbortController();

      setMessages((prev) => [
        ...prev,
        { role: "user", content: userMessage },
        { role: "assistant", content: "" },
      ]);

      const history = messages.map((m) => ({ role: m.role, content: m.content }));

      try {
        await sendChatMessage(
          {
            user_session_id: sessionId,
            user_message: userMessage,
            simulation_result: simulationResult,
            chat_history: history,
          },
          {
            signal: abortRef.current.signal,
            onToken: (delta) =>
              setMessages((prev) => {
                const next = [...prev];
                next[next.length - 1] = {
                  role: "assistant",
                  content: next[next.length - 1].content + delta,
                };
                return next;
              }),
            onDone: (payload) =>
              setMessages((prev) => {
                const next = [...prev];
                next[next.length - 1] = {
                  role: "assistant",
                  content: payload.ai_response || next[next.length - 1].content,
                  meta: payload,
                };
                return next;
              }),
          }
        );
      } catch (e) {
        if (e.name !== "AbortError") setError(e.message);
      } finally {
        setStreaming(false);
      }
    },
    [messages, sessionId]
  );

  const stop = useCallback(() => abortRef.current?.abort(), []);

  return { messages, send, stop, streaming, error };
}
