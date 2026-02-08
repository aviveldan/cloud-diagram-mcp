import React, { useMemo, useCallback } from "react";
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  BackgroundVariant,
  type Node,
  type Edge,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

import { ResourceNode, type ResourceNodeData } from "./ResourceNode";
import type { ResourceItem, Connection, Action } from "../types";
import { categorize, getCategoryLabel, providerOf } from "../icons";

const nodeTypes = { resource: ResourceNode };

const EDGE_COLORS: Record<string, string> = {
  create: "rgba(76,175,80,.7)",
  delete: "rgba(244,67,54,.7)",
  "no-op": "rgba(130,160,255,.4)",
};

interface DiagramViewProps {
  items: ResourceItem[];
  connections: Connection[] | null;
  onSelectResource: (item: ResourceItem) => void;
}

export const DiagramView: React.FC<DiagramViewProps> = ({ items, connections, onSelectResource }) => {
  const { nodes, edges } = useMemo(() => {
    // Group items by provider → category for layout
    const groups: Record<string, Record<string, ResourceItem[]>> = {};
    items.forEach((it) => {
      const prov = providerOf(it.type);
      const cat = categorize(it.type);
      if (!groups[prov]) groups[prov] = {};
      if (!groups[prov][cat]) groups[prov][cat] = [];
      groups[prov][cat].push(it);
    });

    const nodes: Node<ResourceNodeData>[] = [];
    let yOffset = 0;

    for (const [, cats] of Object.entries(groups)) {
      for (const [cat, list] of Object.entries(cats)) {
        // Add a group label node
        const groupId = `group-${cat}-${yOffset}`;
        nodes.push({
          id: groupId,
          type: "default",
          position: { x: 10, y: yOffset },
          data: {
            label: getCategoryLabel(cat),
            resourceType: "",
            action: "no-op" as Action,
            address: "",
          },
          style: {
            background: "rgba(255,255,255,.03)",
            border: "1px solid rgba(255,255,255,.08)",
            borderRadius: 10,
            fontSize: 10,
            color: "#777",
            fontWeight: 700,
            textTransform: "uppercase" as const,
            letterSpacing: "0.8px",
            padding: "4px 10px",
            width: "auto",
          },
          draggable: false,
          selectable: false,
        });

        // Place resource nodes in a row
        list.forEach((it, i) => {
          nodes.push({
            id: it.address,
            type: "resource",
            position: { x: 20 + i * 140, y: yOffset + 40 },
            data: {
              label: it.name,
              resourceType: it.type,
              action: it.action,
              address: it.address,
            },
          });
        });

        yOffset += 170;
      }
    }

    // Build edges
    const edges: Edge[] = [];
    const actionMap = Object.fromEntries(items.map((i) => [i.address, i.action]));

    if (connections) {
      // Architecture mode: explicit connections
      connections.forEach((c, idx) => {
        if (items.some(i => i.address === c.from) && items.some(i => i.address === c.to)) {
          const action = c.action || "no-op";
          edges.push({
            id: `e-${idx}`,
            source: c.from,
            target: c.to,
            label: c.label,
            style: { stroke: EDGE_COLORS[action] || EDGE_COLORS["no-op"] },
            animated: action !== "no-op",
          });
        }
      });
    } else {
      // Diff mode: deps
      items.forEach((item) => {
        (item.deps || []).forEach((dep, idx) => {
          if (!items.some(i => i.address === dep)) return;
          const srcAction = actionMap[item.address] || "no-op";
          const depAction = actionMap[dep] || "no-op";
          let edgeAction: Action = "no-op";
          if (srcAction === "create" || depAction === "create") edgeAction = "create";
          else if (srcAction === "delete" || depAction === "delete") edgeAction = "delete";

          edges.push({
            id: `e-${item.address}-${dep}-${idx}`,
            source: dep,
            target: item.address,
            style: { stroke: EDGE_COLORS[edgeAction] || EDGE_COLORS["no-op"], strokeDasharray: edgeAction === "no-op" ? "5 3" : undefined },
            animated: edgeAction !== "no-op",
          });
        });
      });
    }

    return { nodes, edges };
  }, [items, connections]);

  const handleNodeClick = useCallback((_event: React.MouseEvent, node: Node<ResourceNodeData>) => {
    const item = items.find((i) => i.address === node.id);
    if (item) onSelectResource(item);
  }, [items, onSelectResource]);

  return (
    <div className="canvas-wrap">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodeClick={handleNodeClick}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        proOptions={{ hideAttribution: true }}
        style={{ background: "#111" }}
      >
        <Background variant={BackgroundVariant.Dots} color="rgba(255,255,255,.03)" gap={20} size={1} />
        <Controls />
        <MiniMap
          nodeColor={(n) => {
            const action = (n.data as ResourceNodeData)?.action;
            if (action === "create") return "#4caf50";
            if (action === "delete") return "#f44336";
            if (action === "update") return "#ff9800";
            if (action === "replace") return "#9c27b0";
            return "#666";
          }}
          style={{ background: "#1a1a2e" }}
        />
      </ReactFlow>
    </div>
  );
};
