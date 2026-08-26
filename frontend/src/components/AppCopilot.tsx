import { lazy, Suspense, type ReactNode } from "react";
import { useSite } from "../auth/SiteContext";

const CopilotHost = lazy(() => import("./CopilotHost"));

export function AppCopilot({ children }: { children: ReactNode }) {
  const { copilot_enabled: enabled, loading } = useSite();
  if (!enabled || loading) {
    return <>{children}</>;
  }
  return (
    <Suspense fallback={<>{children}</>}>
      <CopilotHost>{children}</CopilotHost>
    </Suspense>
  );
}
