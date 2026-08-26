export function getCookie(name: string): string | undefined {
  const match = document.cookie.match(
    new RegExp(`(?:^|; )${name.replace(/[$()*+.?[\\\]^{|}-]/g, "\\$&")}=([^;]*)`),
  );
  return match ? decodeURIComponent(match[1]) : undefined;
}

export async function ensureCsrf(): Promise<string> {
  const existing = getCookie("csrftoken");
  if (existing) return existing;
  const res = await fetch("/api/csrf/", { credentials: "include" });
  if (!res.ok) throw new Error("Failed to fetch CSRF token");
  const data = await res.json();
  return data.csrfToken as string;
}

export async function api<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const method = (options.method || "GET").toUpperCase();
  const headers = new Headers(options.headers || {});
  if (!headers.has("Content-Type") && options.body) {
    headers.set("Content-Type", "application/json");
  }
  if (method !== "GET" && method !== "HEAD") {
    const csrf = await ensureCsrf();
    headers.set("X-CSRFToken", csrf);
  }
  const res = await fetch(path, {
    ...options,
    headers,
    credentials: "include",
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const data = await res.json();
      detail = data.detail || JSON.stringify(data);
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

export type User = {
  id: number;
  email: string;
  username: string;
  is_staff: boolean;
};

export type MeResponse = {
  authenticated: boolean;
  user: User | null;
};

export type Project = {
  id: number;
  name: string;
  description: string;
  ai_brief: string;
  ai_brief_updated_at: string | null;
  created_at: string;
  updated_at: string;
};
