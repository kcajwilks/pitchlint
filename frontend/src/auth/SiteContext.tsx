import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { api } from "../api/client";

type SiteConfig = {
  site_name: string;
  copilot_enabled: boolean;
};

type SiteState = SiteConfig & { loading: boolean };

const SiteContext = createContext<SiteState>({
  site_name: "SaaS Starter",
  copilot_enabled: false,
  loading: true,
});

export function SiteProvider({ children }: { children: ReactNode }) {
  const [config, setConfig] = useState<SiteConfig>({
    site_name: import.meta.env.VITE_SITE_NAME || "SaaS Starter",
    copilot_enabled: import.meta.env.VITE_COPILOT_ENABLED === "1",
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api<SiteConfig>("/api/config/")
      .then((data) => {
        setConfig(data);
        document.title = data.site_name;
      })
      .catch(() => {
        /* keep env/default */
      })
      .finally(() => setLoading(false));
  }, []);

  const value = useMemo(() => ({ ...config, loading }), [config, loading]);
  return <SiteContext.Provider value={value}>{children}</SiteContext.Provider>;
}

export function useSite() {
  return useContext(SiteContext);
}
