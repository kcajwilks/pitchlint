import React from "react";
import { createRoot } from "react-dom/client";
import { CopilotChat, CopilotKit, CopilotPopup, CopilotSidebar, useAgent } from "@copilotkit/react-core/v2";
import "@copilotkit/react-ui/v2/styles.css";

function getMountEls(): HTMLElement[] {
  return Array.from(document.querySelectorAll<HTMLElement>("[data-copilot-mount], #copilot-root"));
}

function readDataset(el: HTMLElement) {
  const surfaceKey = el.dataset.surfaceKey || "workspace_project_detail";
  const projectId = el.dataset.projectId ? Number(el.dataset.projectId) : undefined;
  const variant = el.dataset.variant || "inline";
  return { surfaceKey, projectId, variant };
}

async function postJson(url: string, body: unknown) {
  const resp = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") || "" },
    credentials: "include",
    body: JSON.stringify(body),
  });
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(text || `Request failed (${resp.status})`);
  }
  return await resp.json();
}

function getCookie(name: string): string | undefined {
  const match = document.cookie.match(new RegExp(`(?:^|; )${name.replace(/[$()*+.?[\\\]^{|}-]/g, "\\$&")}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : undefined;
}

function App() {
  // Note: the Copilot Runtime uses AG-UI SSE endpoints under `/copilot/*`.
  // We additionally provide a lightweight reset endpoint for the cookiecutter demo.
  const mount = document.getElementById("copilot-root");
  const { surfaceKey, variant } = mount
    ? readDataset(mount)
    : { surfaceKey: "workspace_project_detail", variant: "inline", projectId: undefined };

  const { agent } = useAgent({ agentId: "default" });

  React.useEffect(() => {
    const btn = document.querySelector<HTMLButtonElement>("[data-copilot-reset]");
    if (!btn) return;

    const onClick = async () => {
      try {
        await postJson("/copilot/reset", { threadId: agent.threadId });
        window.location.reload();
      } catch (e) {
        // eslint-disable-next-line no-console
        console.error(e);
      }
    };
    btn.addEventListener("click", onClick);
    return () => btn.removeEventListener("click", onClick);
  }, [agent.threadId, surfaceKey]);

  return (
    <CopilotKit
      runtimeUrl="/copilot"
      agent="default"
      credentials="include"
      headers={() => ({ "X-CSRFToken": getCookie("csrftoken") || "" })}
    >
      {variant === "sidebar" ? (
        <CopilotSidebar defaultOpen={true} />
      ) : variant === "popup" ? (
        <CopilotPopup defaultOpen={true} />
      ) : (
        <CopilotChat className="h-100" />
      )}
    </CopilotKit>
  );
}

const mounts = getMountEls();
for (const el of mounts) {
  if (el.id !== "copilot-root") continue;
  createRoot(el).render(<App />);
}

