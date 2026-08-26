import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => ({
  plugins: [react()],
  base: mode === "production" ? "/static/spa/" : "/",
  server: {
    port: 5173,
    proxy: {
      "/api": "http://127.0.0.1:8000",
      "/accounts": "http://127.0.0.1:8000",
      "/copilot": "http://127.0.0.1:8000",
      "/billing/webhook": "http://127.0.0.1:8000",
      "/admin": "http://127.0.0.1:8000",
      "/static": "http://127.0.0.1:8000",
    },
  },
  build: {
    outDir: "../core/static/spa",
    emptyOutDir: true,
    sourcemap: false,
  },
}));
