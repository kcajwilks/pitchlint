import { useEffect, useMemo, useState, type ReactNode } from "react";
import { useLocation } from "react-router-dom";
import {
  CopilotKitProvider,
  CopilotSidebar,
  useAgentContext,
  useConfigureSuggestions,
} from "@copilotkit/react-core/v2";
import "@copilotkit/react-ui/v2/styles.css";
import { ensureCsrf, getCookie } from "../api/client";
import { useSite } from "../auth/SiteContext";

function CopilotContextBridge() {
  const location = useLocation();
  const projectMatch = location.pathname.match(/^\/workspace\/(\d+)/);
  const projectId = projectMatch ? Number(projectMatch[1]) : null;

  useAgentContext({
    description: "Current app route and selection",
    value: {
      pathname: location.pathname,
      projectId,
    },
  });

  useConfigureSuggestions({
    suggestions: [
      {
        title: "Create a project",
        message: "Create a new workspace project called Demo Launch with a short description.",
      },
      {
        title: "List my projects",
        message: "List my workspace projects and summarize what each is for.",
      },
      {
        title: "Improve this project",
        message:
          "Using the current project context if available, suggest a clearer name and description, then apply the update if I agree.",
      },
      {
        title: "Generate a brief",
        message: "Generate an AI brief for the current project (or ask which one if unclear).",
      },
    ],
  });

  return null;
}

export default function CopilotHost({ children }: { children: ReactNode }) {
  const { site_name: siteName } = useSite();
  const [csrfReady, setCsrfReady] = useState(Boolean(getCookie("csrftoken")));
  const properties = useMemo(
    () => ({
      surface: "app",
      siteName,
    }),
    [siteName],
  );

  useEffect(() => {
    void ensureCsrf()
      .then(() => setCsrfReady(true))
      .catch(() => setCsrfReady(Boolean(getCookie("csrftoken"))));
  }, []);

  if (!csrfReady) {
    return <>{children}</>;
  }

  return (
    <CopilotKitProvider
      runtimeUrl="/copilot"
      credentials="include"
      useSingleEndpoint={false}
      properties={properties}
      headers={() => ({ "X-CSRFToken": getCookie("csrftoken") || "" })}
      onError={({ code, error }) => {
        console.error("[copilot]", code, error.message);
      }}
    >
      <CopilotContextBridge />
      {children}
      <CopilotSidebar
        agentId="default"
        defaultOpen={true}
        labels={{
          title: `${siteName} Copilot`,
          initial:
            "Tell me what to build or change in your workspace. I can create projects, update them, and generate briefs.",
        }}
      />
    </CopilotKitProvider>
  );
}
