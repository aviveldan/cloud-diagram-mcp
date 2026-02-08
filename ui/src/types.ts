/* ---- Types for Terraform plan / architecture data received from MCP tool ---- */

export interface ResourceChange {
  address: string;
  type: string;
  name: string;
  change: {
    actions: string[];
    before: Record<string, unknown> | null;
    after: Record<string, unknown> | null;
  };
}

export interface Connection {
  from: string;
  to: string;
  label?: string;
  action?: Action;
}

export type Action = "create" | "delete" | "update" | "replace" | "no-op";

export interface ResourceItem {
  address: string;
  type: string;
  name: string;
  action: Action;
  before: Record<string, unknown> | null;
  after: Record<string, unknown> | null;
  deps: string[];
}

/** Data shape received from ext-apps tool result */
export interface PlanData {
  _mode?: "architecture";
  _server_svg?: string;
  terraform_version?: string;
  title?: string;
  resource_changes?: ResourceChange[];
  resources?: Array<{
    address: string;
    type: string;
    name?: string;
    config?: Record<string, unknown>;
  }>;
  connections?: Connection[];
  configuration?: {
    root_module?: {
      resources?: Array<{
        address: string;
        depends_on?: string[];
      }>;
    };
  };
}

export interface ActionCounts {
  create: number;
  update: number;
  delete: number;
  replace: number;
}

/* ---- Helpers ---- */

export function classifyAction(actions: string[]): Action {
  if (actions.includes("create") && actions.includes("delete")) return "replace";
  if (actions.includes("delete")) return "delete";
  if (actions.includes("create")) return "create";
  if (actions.includes("update")) return "update";
  return "no-op";
}

export function parsePlanData(planData: PlanData): {
  items: ResourceItem[];
  counts: ActionCounts;
  connections: Connection[] | null;
  isArchMode: boolean;
} {
  const isArchMode = planData._mode === "architecture";
  const counts: ActionCounts = { create: 0, update: 0, delete: 0, replace: 0 };

  let items: ResourceItem[];
  let connections: Connection[] | null;

  if (isArchMode) {
    const resources = planData.resources || [];
    connections = planData.connections || [];
    items = resources.map((r) => ({
      address: r.address,
      type: r.type,
      name: r.name || r.address,
      action: "no-op" as Action,
      before: null,
      after: r.config || null,
      deps: [],
    }));
  } else {
    const changes = planData.resource_changes || [];
    const depMap = (
      planData.configuration?.root_module?.resources || []
    ).reduce<Record<string, string[]>>((m, r) => {
      m[r.address] = r.depends_on || [];
      return m;
    }, {});
    connections = null;
    items = changes.map((r) => {
      const action = classifyAction(r.change.actions);
      if (action in counts) counts[action as keyof ActionCounts]++;
      return {
        address: r.address,
        type: r.type,
        name: r.name,
        action,
        before: r.change.before,
        after: r.change.after,
        deps: depMap[r.address] || [],
      };
    });
  }

  return { items, counts, connections, isArchMode };
}
