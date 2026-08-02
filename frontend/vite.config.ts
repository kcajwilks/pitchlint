import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/static/frontend/",
  build: {
    outDir: "../core/static/frontend",
    emptyOutDir: true,
    sourcemap: true,
    rollupOptions: {
      input: "src/copilot.tsx",
      output: {
        entryFileNames: "copilot.js",
        chunkFileNames: "chunks/[name].js",
        assetFileNames: "[name][extname]",
      },
    },
  },
});
