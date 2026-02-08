import React from "react";
import type { ResourceItem } from "../types";
import { getIcon } from "../icons";

function esc(s: unknown): string {
  return String(s ?? "");
}

function propsHTML(obj: Record<string, unknown>): React.ReactNode {
  return Object.entries(obj)
    .filter(([, v]) => v !== null)
    .map(([k, v]) => (
      <div className="prop" key={k}>
        <span className="key">{k}</span>{" "}
        <span className="val">{esc(JSON.stringify(v, null, 2))}</span>
      </div>
    ));
}

interface DetailPanelProps {
  item: ResourceItem | null;
  onClose: () => void;
}

export const DetailPanel: React.FC<DetailPanelProps> = ({ item, onClose }) => {
  if (!item) return null;

  const labels: Record<string, string> = {
    create: "Creating", delete: "Destroying", update: "Updating", replace: "Replacing",
  };
  const label = labels[item.action] || item.action;
  const Icon = getIcon(item.type);

  let body: React.ReactNode = null;

  if (item.action === "create" && item.after) {
    body = (
      <>
        <div className="section-title">New Configuration</div>
        {propsHTML(item.after)}
      </>
    );
  } else if (item.action === "delete" && item.before) {
    body = (
      <>
        <div className="section-title">Removed Configuration</div>
        {propsHTML(item.before)}
      </>
    );
  } else if ((item.action === "update" || item.action === "replace") && item.before && item.after) {
    const keys = new Set([
      ...Object.keys(item.before || {}),
      ...Object.keys(item.after || {}),
    ]);
    const diffs: React.ReactNode[] = [];
    for (const k of keys) {
      const bv = JSON.stringify((item.before as Record<string, unknown>)?.[k] ?? null, null, 2);
      const av = JSON.stringify((item.after as Record<string, unknown>)?.[k] ?? null, null, 2);
      if (bv !== av) {
        diffs.push(
          <div className="prop" key={k}>
            <div className="key">{k}</div>
            <div className="old">− {esc(bv)}</div>
            <div className="new">+ {esc(av)}</div>
          </div>
        );
      }
    }
    body = (
      <>
        <div className="section-title">Changes</div>
        {diffs}
      </>
    );
  }

  const deps = item.deps?.length ? (
    <>
      <div className="section-title">Dependencies</div>
      {item.deps.map((d) => (
        <div className="prop" key={d}>
          <span className="val">{d}</span>
        </div>
      ))}
    </>
  ) : null;

  return (
    <div className="sidebar">
      <button className="sidebar-close" onClick={onClose} title="Close">✕</button>
      <div className={`detail-card ${item.action}`}>
        <h3>
          <Icon />
          {item.name}
        </h3>
        <div className="dtype">{item.address}</div>
        <div className={`action-tag ${item.action}`} style={{ marginBottom: 10 }}>
          {label}
        </div>
        {body}
        {deps}
      </div>
    </div>
  );
};
