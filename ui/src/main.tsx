import React, { StrictMode, useState, useEffect } from "react";
import { createRoot } from "react-dom/client";
import { App as McpApp } from "@modelcontextprotocol/ext-apps";
import { App } from "./components/App";
import type { PlanData } from "./types";
import "./styles/global.css";

const APP_INFO = { name: "Cloud Diagram", version: "3.0.0" };

function Root() {
  const [planData, setPlanData] = useState<PlanData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Test mode: use injected data directly (no MCP SDK needed)
    const testData = (window as any).__TEST_PLAN_DATA__;
    if (testData) {
      setPlanData(testData);
      return;
    }

    // Singleton: only create one MCP app instance
    if ((window as any).__mcpApp) return;
    const app = new McpApp(APP_INFO);
    (window as any).__mcpApp = app;

    app.ontoolresult = ({ content }) => {
      const text = content?.find((c: { type: string }) => c.type === "text") as { text: string } | undefined;
      if (text) {
        try {
          setPlanData(JSON.parse(text.text));
        } catch (e) {
          setError("Error parsing data: " + (e as Error).message);
        }
      }
    };

    app.onhostcontextchanged = (ctx: { safeAreaInsets?: { top: number; right: number; bottom: number; left: number } }) => {
      if (ctx.safeAreaInsets) {
        document.body.style.paddingTop = ctx.safeAreaInsets.top + "px";
        document.body.style.paddingRight = ctx.safeAreaInsets.right + "px";
        document.body.style.paddingBottom = ctx.safeAreaInsets.bottom + "px";
        document.body.style.paddingLeft = ctx.safeAreaInsets.left + "px";
      }
    };

    app.connect().then(() => {
      const ctx = app.getHostContext() as { safeAreaInsets?: { top: number; right: number; bottom: number; left: number } } | null;
      if (ctx?.safeAreaInsets) {
        document.body.style.paddingTop = ctx.safeAreaInsets.top + "px";
        document.body.style.paddingRight = ctx.safeAreaInsets.right + "px";
        document.body.style.paddingBottom = ctx.safeAreaInsets.bottom + "px";
        document.body.style.paddingLeft = ctx.safeAreaInsets.left + "px";
      }
      app.sendSizeChanged({ height: 800 }).catch(() => {});
    });
  }, []);

  if (error) {
    return <div className="waiting" style={{ color: "#f44336" }}>{error}</div>;
  }

  if (!planData) {
    return (
      <div className="waiting">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M2 15s2-4 5-4c1.5 0 2.5 1 3 2 .5-3 2-6 5-6s5 3 5 6-3 6-5 6H7c-3 0-5-2-5-4z" />
        </svg>
        Waiting for plan data&hellip;
      </div>
    );
  }

  return <App planData={planData} />;
}

const rootEl = document.getElementById("root")!;

// Guard against duplicate initialization (VS Code may re-run the script)
if (!(rootEl as any).__reactRoot) {
  const root = createRoot(rootEl);
  (rootEl as any).__reactRoot = root;
  root.render(
    <StrictMode>
      <Root />
    </StrictMode>
  );
}
