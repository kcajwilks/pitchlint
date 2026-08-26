import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { api, type MeResponse, type User } from "../api/client";

type AuthState = {
  user: User | null;
  loading: boolean;
  refresh: () => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    const me = await api<MeResponse>("/api/me/");
    setUser(me.authenticated ? me.user : null);
  }, []);

  useEffect(() => {
    refresh()
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, [refresh]);

  const login = useCallback(async (email: string, password: string) => {
    const data = await api<MeResponse>("/api/auth/login/", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    setUser(data.user);
  }, []);

  const signup = useCallback(async (email: string, password: string) => {
    const data = await api<MeResponse>("/api/auth/signup/", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    setUser(data.user);
  }, []);

  const logout = useCallback(async () => {
    await api("/api/auth/logout/", { method: "POST" });
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({ user, loading, refresh, login, signup, logout }),
    [user, loading, refresh, login, signup, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth requires AuthProvider");
  return ctx;
}
