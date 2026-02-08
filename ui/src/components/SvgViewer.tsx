import React, { useRef, useEffect, useCallback, memo } from "react";
import type { ResourceItem } from "../types";

interface SvgViewerProps {
  svgContent: string;
  items: ResourceItem[];
  selectedAddress: string | null;
  onSelectResource: (item: ResourceItem) => void;
}

export const SvgViewer: React.FC<SvgViewerProps> = memo(({ svgContent, items, selectedAddress, onSelectResource }) => {
  const vpRef = useRef<HTMLDivElement>(null);
  const scaleRef = useRef(1);
  const panRef = useRef({ x: 0, y: 0 });
  const panningRef = useRef(false);
  const startRef = useRef({ x: 0, y: 0 });
  const onSelectRef = useRef(onSelectResource);
  const zoomPctRef = useRef<HTMLDivElement>(null);
  const nodeMapRef = useRef<Map<string, Element>>(new Map());
  const svgInsertedRef = useRef(false);

  // Keep callback ref current without re-wiring DOM events
  onSelectRef.current = onSelectResource;

  const applyTransform = useCallback(() => {
    const svg = vpRef.current?.querySelector("svg");
    if (!svg) return;
    svg.style.transform = `translate(${panRef.current.x}px,${panRef.current.y}px) scale(${scaleRef.current})`;
    if (zoomPctRef.current) zoomPctRef.current.textContent = Math.round(scaleRef.current * 100) + "%";
  }, []);

  const fitSvg = useCallback(() => {
    const vp = vpRef.current;
    const svg = vp?.querySelector("svg");
    if (!vp || !svg) return;
    const vb = svg.getAttribute("viewBox");
    if (!vb) return;
    const parts = vb.split(/[\s,]+/).map(Number);
    const cr = vp.getBoundingClientRect();
    if (cr.width === 0 || cr.height === 0) return;
    scaleRef.current = Math.min(cr.width / parts[2], cr.height / parts[3]) * 0.92;
    panRef.current = {
      x: (cr.width - parts[2] * scaleRef.current) / 2,
      y: (cr.height - parts[3] * scaleRef.current) / 2,
    };
    applyTransform();
  }, [applyTransform]);

  // Insert SVG into DOM manually (not via dangerouslySetInnerHTML) to avoid re-creation on re-render
  useEffect(() => {
    const vp = vpRef.current;
    if (!vp) return;
    vp.innerHTML = svgContent;
    svgInsertedRef.current = true;

    const svg = vp.querySelector("svg");
    if (!svg) return;

    // Set viewBox if missing
    if (!svg.getAttribute("viewBox")) {
      const w = parseFloat(svg.getAttribute("width") || "800");
      const h = parseFloat(svg.getAttribute("height") || "600");
      svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
    }
    // Use viewBox dimensions as fixed size so flex-resize doesn't cause reflow
    const vb = svg.getAttribute("viewBox")!;
    const parts = vb.split(/[\s,]+/).map(Number);
    svg.removeAttribute("width");
    svg.removeAttribute("height");
    svg.style.width = parts[2] + "px";
    svg.style.height = parts[3] + "px";

    // Build node map and wire click handlers
    nodeMapRef.current.clear();
    // Index items by address for fast lookup
    const itemsByAddr = new Map(items.map((it) => [it.address, it]));

    svg.querySelectorAll(".node").forEach((g) => {
      let matched: ResourceItem | null = null;

      // Primary: match via <title> element which contains the full resource address
      const titleEl = g.querySelector("title");
      const titleText = titleEl?.textContent?.trim() || "";
      if (titleText && itemsByAddr.has(titleText)) {
        matched = itemsByAddr.get(titleText)!;
      }

      // Fallback: match via text content (for SVGs without address in title)
      if (!matched) {
        g.querySelectorAll("text").forEach((t) => {
          const raw = (t.textContent || "").trim().replace(/^\[[+\-~*]\]\s*/, "").trim();
          if (!matched) {
            for (const it of items) {
              if (it.name === raw || it.address.includes(raw)) {
                matched = it;
                break;
              }
            }
          }
        });
      }

      if (matched) {
        (g as HTMLElement).style.cursor = "pointer";
        const m: ResourceItem = matched;
        nodeMapRef.current.set(m.address, g);
        g.addEventListener("click", (e) => {
          e.stopPropagation();
          onSelectRef.current(m);
        });
      }
    });

    setTimeout(fitSvg, 50);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [svgContent]);

  // Apply/remove highlight based on selectedAddress prop from parent
  useEffect(() => {
    if (!svgInsertedRef.current) return;
    const svg = vpRef.current?.querySelector("svg");
    if (!svg) return;
    // Clear all highlights
    nodeMapRef.current.forEach((g) => {
      (g as HTMLElement).style.filter = "";
      (g as HTMLElement).style.outline = "";
    });
    // Apply highlight to selected
    if (selectedAddress) {
      const g = nodeMapRef.current.get(selectedAddress);
      if (g) {
        (g as HTMLElement).style.filter = "brightness(1.2) drop-shadow(0 0 6px rgba(102,126,234,.6))";
        (g as HTMLElement).style.outline = "2px solid rgba(102,126,234,.8)";
        (g as HTMLElement).style.outlineOffset = "3px";
      }
    }
  }, [selectedAddress]);

  // Wheel zoom — no React state, just refs + direct DOM
  useEffect(() => {
    const vp = vpRef.current;
    if (!vp) return;
    const handleWheel = (e: WheelEvent) => {
      e.preventDefault();
      const rect = vp.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;
      const old = scaleRef.current;
      scaleRef.current = e.deltaY < 0
        ? Math.min(old * 1.1, 5)
        : Math.max(old / 1.1, 0.2);
      panRef.current = {
        x: mx - (mx - panRef.current.x) * (scaleRef.current / old),
        y: my - (my - panRef.current.y) * (scaleRef.current / old),
      };
      applyTransform();
    };
    vp.addEventListener("wheel", handleWheel, { passive: false });
    return () => vp.removeEventListener("wheel", handleWheel);
  }, [applyTransform]);

  // Pan — pure DOM, no React re-renders
  useEffect(() => {
    const vp = vpRef.current;
    if (!vp) return;

    const onDown = (e: MouseEvent) => {
      if ((e.target as HTMLElement).closest(".node")) return;
      panningRef.current = true;
      startRef.current = { x: e.clientX - panRef.current.x, y: e.clientY - panRef.current.y };
    };
    const onMove = (e: MouseEvent) => {
      if (!panningRef.current) return;
      panRef.current = { x: e.clientX - startRef.current.x, y: e.clientY - startRef.current.y };
      applyTransform();
    };
    const onUp = () => { panningRef.current = false; };

    vp.addEventListener("mousedown", onDown);
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onUp);
    return () => {
      vp.removeEventListener("mousedown", onDown);
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseup", onUp);
    };
  }, [applyTransform]);

  // Resize
  useEffect(() => {
    const handler = () => setTimeout(fitSvg, 100);
    window.addEventListener("resize", handler);
    return () => window.removeEventListener("resize", handler);
  }, [fitSvg]);

  return (
    <div className="canvas-wrap" style={{ position: "relative" }}>
      <div className="svg-viewport" ref={vpRef} />
      <div className="zoom-controls">
        <button className="zoom-btn" onClick={() => { scaleRef.current = Math.min(scaleRef.current * 1.25, 5); applyTransform(); }}>+</button>
        <div className="zoom-pct" ref={zoomPctRef}>100%</div>
        <button className="zoom-btn" onClick={() => { scaleRef.current = Math.max(scaleRef.current / 1.25, 0.2); applyTransform(); }}>−</button>
        <button className="zoom-btn" onClick={fitSvg} style={{ fontSize: 12 }}>⊞</button>
      </div>
    </div>
  );
});
