import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { viteSingleFile } from "vite-plugin-singlefile";

export default defineConfig({
  plugins: [react(), viteSingleFile()],
  build: {
    outDir: "../cloud_diagram_mcp/dist",
    emptyOutDir: true,
    rollupOptions: {
      input: "mcp-app.html",
    },
  },
});
