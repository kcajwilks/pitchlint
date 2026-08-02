import { CopilotSidebar } from "@copilotkit/react-core/v2";

export default function Home() {
  return (
    <main style={{ padding: 24 }}>
      <h1 style={{ fontSize: 18, fontWeight: 600, marginBottom: 12 }}>CopilotKit + Agno (bolt-on)</h1>
      <p style={{ marginBottom: 16, color: "#666" }}>
        This is the standard CopilotKit sidebar UI connected to an Agno agent via the Copilot Runtime.
      </p>
      <CopilotSidebar defaultOpen />
    </main>
  );
}
