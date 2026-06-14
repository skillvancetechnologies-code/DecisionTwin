import ChatWindow from "../components/chat/ChatWindow";
import { ErrorState } from "../components/ui/States";
import { useChatStream } from "../hooks/useChatStream";
import { useAppStore } from "../store/appStore";

export default function ChatPage() {
  const { messages, send, streaming, error } = useChatStream();
  const lastSimulation = useAppStore((s) => s.lastSimulation);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Decision copilot</h1>
      {lastSimulation && (
        <p className="text-sm text-gray-500">
          Context: last simulation ({lastSimulation.risk_level} risk) is attached.
        </p>
      )}
      {error && <ErrorState message={error} />}
      <ChatWindow
        messages={messages}
        streaming={streaming}
        onSend={(text) => send(text, lastSimulation)}
      />
    </div>
  );
}
