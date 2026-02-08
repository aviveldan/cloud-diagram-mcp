import React, { memo } from "react";
import { Handle, Position, type NodeProps } from "@xyflow/react";
import { getIcon } from "../icons";
import type { Action } from "../types";

export interface ResourceNodeData {
  label: string;
  resourceType: string;
  action: Action;
  address: string;
  [key: string]: unknown;
}

type ResourceNodeProps = NodeProps & { data: ResourceNodeData };

export const ResourceNode: React.FC<ResourceNodeProps> = memo(({ data, selected }) => {
  const Icon = getIcon(data.resourceType);
  return (
    <div className={`resource-node${selected ? " selected" : ""}`}>
      <Handle type="target" position={Position.Top} style={{ visibility: "hidden" }} />
      {data.action !== "no-op" && <div className={`action-dot ${data.action}`} />}
      <div className="node-icon"><Icon /></div>
      <div className="node-name">{data.label}</div>
      <div className="node-type">{data.resourceType}</div>
      <div className={`action-tag ${data.action}`}>{data.action}</div>
      <Handle type="source" position={Position.Bottom} style={{ visibility: "hidden" }} />
    </div>
  );
});

ResourceNode.displayName = "ResourceNode";
