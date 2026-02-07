import { TerraformPlan, ResourceChange } from './types.js';

/**
 * Action styles for Mermaid diagram
 */
const ACTION_STYLES = {
  create: { color: 'green', style: 'fill:#90EE90,stroke:#2E7D32,stroke-width:2px' },
  delete: { color: 'red', style: 'fill:#FFB6C1,stroke:#C62828,stroke-width:2px,stroke-dasharray: 5 5' },
  update: { color: 'yellow', style: 'fill:#FFEB3B,stroke:#F57F17,stroke-width:2px' },
  replace: { color: 'purple', style: 'fill:#E1BEE7,stroke:#6A1B9A,stroke-width:4px' }
};

/**
 * Sanitize node ID for Mermaid
 */
function sanitizeId(id: string): string {
  return id.replace(/[^a-zA-Z0-9_]/g, '_');
}

/**
 * Get primary action from actions array
 */
function getPrimaryAction(actions: string[]): string {
  if (actions.includes('create') && actions.includes('delete')) {
    return 'replace';
  }
  if (actions.includes('delete')) {
    return 'delete';
  }
  if (actions.includes('create')) {
    return 'create';
  }
  if (actions.includes('update')) {
    return 'update';
  }
  return 'no-op';
}

/**
 * Generate Mermaid diagram from Terraform plan
 */
export function generateMermaidDiagram(plan: TerraformPlan): string {
  const lines: string[] = ['graph TD'];
  
  if (!plan.resource_changes || plan.resource_changes.length === 0) {
    lines.push('  Empty["No resource changes"]');
    return lines.join('\n');
  }

  // Group resources by type
  const resourcesByType: Record<string, ResourceChange[]> = {};
  const nodeIds: Map<string, string> = new Map();
  
  for (const resource of plan.resource_changes) {
    const action = getPrimaryAction(resource.change.actions);
    if (action === 'no-op') continue; // Skip no-op changes
    
    const type = resource.type;
    if (!resourcesByType[type]) {
      resourcesByType[type] = [];
    }
    resourcesByType[type].push(resource);
  }

  // Generate subgraphs for each resource type
  let nodeCounter = 0;
  for (const [type, resources] of Object.entries(resourcesByType)) {
    const subgraphId = sanitizeId(type);
    lines.push(`  subgraph ${subgraphId}["${type}"]`);
    
    for (const resource of resources) {
      const action = getPrimaryAction(resource.change.actions);
      const nodeId = `node${nodeCounter++}`;
      nodeIds.set(resource.address, nodeId);
      
      const label = `${resource.name}`;
      const actionIcon = getActionIcon(action);
      lines.push(`    ${nodeId}["${actionIcon} ${label}"]`);
    }
    
    lines.push('  end');
  }

  // Add dependencies as edges
  if (plan.configuration?.root_module?.resources) {
    for (const resource of plan.configuration.root_module.resources) {
      if (resource.depends_on && resource.depends_on.length > 0) {
        const sourceId = nodeIds.get(resource.address);
        if (sourceId) {
          for (const dep of resource.depends_on) {
            const targetId = nodeIds.get(dep);
            if (targetId) {
              lines.push(`  ${targetId} --> ${sourceId}`);
            }
          }
        }
      }
    }
  }

  // Add styling for each action type
  const styledNodes: Record<string, string[]> = {
    create: [],
    delete: [],
    update: [],
    replace: []
  };

  for (const resource of plan.resource_changes) {
    const action = getPrimaryAction(resource.change.actions);
    if (action !== 'no-op') {
      const nodeId = nodeIds.get(resource.address);
      if (nodeId) {
        styledNodes[action]?.push(nodeId);
      }
    }
  }

  // Apply styles
  for (const [action, nodes] of Object.entries(styledNodes)) {
    if (nodes.length > 0) {
      const style = ACTION_STYLES[action as keyof typeof ACTION_STYLES];
      if (style) {
        for (const nodeId of nodes) {
          lines.push(`  style ${nodeId} ${style.style}`);
        }
      }
    }
  }

  return lines.join('\n');
}

/**
 * Get icon for action
 */
function getActionIcon(action: string): string {
  const icons: Record<string, string> = {
    create: '✨',
    delete: '🗑️',
    update: '📝',
    replace: '🔄'
  };
  return icons[action] || '●';
}

/**
 * Get action counts from plan
 */
export function getActionCounts(plan: TerraformPlan): Record<string, number> {
  const counts: Record<string, number> = {
    create: 0,
    delete: 0,
    update: 0,
    replace: 0
  };

  if (!plan.resource_changes) {
    return counts;
  }

  for (const resource of plan.resource_changes) {
    const action = getPrimaryAction(resource.change.actions);
    if (action in counts) {
      counts[action]++;
    }
  }

  return counts;
}
