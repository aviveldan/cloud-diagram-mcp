import { TerraformPlan, ResourceChange } from './types.js';

/**
 * Risk levels for different resource types and actions
 */
const RISK_WEIGHTS = {
  // Resource type multipliers
  resourceTypes: {
    'aws_instance': 3,
    'aws_db_instance': 5,
    'aws_rds_cluster': 5,
    'aws_elasticache_cluster': 4,
    'aws_s3_bucket': 2,
    'aws_security_group': 4,
    'aws_iam_role': 4,
    'aws_iam_policy': 4,
    'aws_lambda_function': 2,
    'aws_vpc': 5,
    'aws_subnet': 3,
    'default': 1
  },
  // Action multipliers
  actions: {
    'delete': 10,
    'replace': 8,
    'update': 3,
    'create': 1
  }
};

/**
 * Generate risk summary from Terraform plan
 */
export function generateRiskSummary(plan: TerraformPlan): string {
  if (!plan.resource_changes || plan.resource_changes.length === 0) {
    return '## Risk Summary\n\n✅ **No changes detected** - No infrastructure modifications planned.';
  }

  const changes = analyzeChanges(plan.resource_changes);
  const riskScore = calculateRiskScore(plan.resource_changes);
  const riskLevel = getRiskLevel(riskScore);

  const lines: string[] = [
    '## Risk Summary',
    '',
    `### Overall Risk: ${riskLevel.emoji} ${riskLevel.label}`,
    `**Risk Score:** ${riskScore}/100`,
    ''
  ];

  // Change summary
  lines.push('### Changes');
  lines.push('');
  if (changes.create > 0) {
    lines.push(`- ✨ **Create:** ${changes.create} resource${changes.create > 1 ? 's' : ''}`);
  }
  if (changes.update > 0) {
    lines.push(`- 📝 **Update:** ${changes.update} resource${changes.update > 1 ? 's' : ''}`);
  }
  if (changes.delete > 0) {
    lines.push(`- 🗑️ **Delete:** ${changes.delete} resource${changes.delete > 1 ? 's' : ''}`);
  }
  if (changes.replace > 0) {
    lines.push(`- 🔄 **Replace:** ${changes.replace} resource${changes.replace > 1 ? 's' : ''}`);
  }
  lines.push('');

  // High-risk changes
  const highRiskChanges = identifyHighRiskChanges(plan.resource_changes);
  if (highRiskChanges.length > 0) {
    lines.push('### ⚠️ High-Risk Changes');
    lines.push('');
    for (const change of highRiskChanges) {
      lines.push(`- **${change.address}** (${change.type}): ${change.reason}`);
    }
    lines.push('');
  }

  // Recommendations
  lines.push('### Recommendations');
  lines.push('');
  if (riskScore >= 70) {
    lines.push('- ⚠️ **Review carefully** before applying changes');
    lines.push('- 🔍 Verify all resource dependencies');
    lines.push('- 💾 Ensure backups are in place');
    lines.push('- 👥 Consider peer review for critical changes');
  } else if (riskScore >= 40) {
    lines.push('- ✅ Changes appear moderate - review before applying');
    lines.push('- 🔍 Verify critical resource configurations');
  } else {
    lines.push('- ✅ Changes appear low-risk');
    lines.push('- 📋 Standard review recommended');
  }

  return lines.join('\n');
}

/**
 * Analyze changes by action type
 */
function analyzeChanges(resourceChanges: ResourceChange[]): Record<string, number> {
  const counts: Record<string, number> = {
    create: 0,
    delete: 0,
    update: 0,
    replace: 0
  };

  for (const resource of resourceChanges) {
    const actions = resource.change.actions;
    if (actions.includes('create') && actions.includes('delete')) {
      counts.replace++;
    } else if (actions.includes('delete')) {
      counts.delete++;
    } else if (actions.includes('create')) {
      counts.create++;
    } else if (actions.includes('update')) {
      counts.update++;
    }
  }

  return counts;
}

/**
 * Calculate overall risk score (0-100)
 */
function calculateRiskScore(resourceChanges: ResourceChange[]): number {
  let totalRisk = 0;
  let maxPossibleRisk = 0;

  for (const resource of resourceChanges) {
    const actions = resource.change.actions;
    let action = 'create';
    
    if (actions.includes('create') && actions.includes('delete')) {
      action = 'replace';
    } else if (actions.includes('delete')) {
      action = 'delete';
    } else if (actions.includes('update')) {
      action = 'update';
    }

    const resourceTypeWeight = RISK_WEIGHTS.resourceTypes[resource.type as keyof typeof RISK_WEIGHTS.resourceTypes] 
      || RISK_WEIGHTS.resourceTypes.default;
    const actionWeight = RISK_WEIGHTS.actions[action as keyof typeof RISK_WEIGHTS.actions] || 1;
    
    const resourceRisk = resourceTypeWeight * actionWeight;
    totalRisk += resourceRisk;
    
    // Max possible risk is delete action on highest risk resource type
    maxPossibleRisk += 5 * 10; // Max resource type (5) * delete action (10)
  }

  if (maxPossibleRisk === 0) return 0;
  
  const score = Math.min(100, Math.round((totalRisk / maxPossibleRisk) * 100));
  return score;
}

/**
 * Get risk level from score
 */
function getRiskLevel(score: number): { label: string; emoji: string } {
  if (score >= 70) {
    return { label: 'HIGH', emoji: '🔴' };
  } else if (score >= 40) {
    return { label: 'MEDIUM', emoji: '🟡' };
  } else {
    return { label: 'LOW', emoji: '🟢' };
  }
}

/**
 * Identify high-risk changes
 */
function identifyHighRiskChanges(resourceChanges: ResourceChange[]): Array<{
  address: string;
  type: string;
  reason: string;
}> {
  const highRisk: Array<{ address: string; type: string; reason: string }> = [];

  for (const resource of resourceChanges) {
    const actions = resource.change.actions;
    const type = resource.type;
    
    // Check for deletions of important resources
    if (actions.includes('delete')) {
      const resourceWeight = RISK_WEIGHTS.resourceTypes[type as keyof typeof RISK_WEIGHTS.resourceTypes] 
        || RISK_WEIGHTS.resourceTypes.default;
      
      if (resourceWeight >= 4) {
        highRisk.push({
          address: resource.address,
          type: type,
          reason: 'Critical resource deletion'
        });
        continue;
      }
    }

    // Check for replacements
    if (actions.includes('create') && actions.includes('delete')) {
      highRisk.push({
        address: resource.address,
        type: type,
        reason: 'Resource will be replaced (recreated)'
      });
      continue;
    }

    // Check for security-sensitive updates
    if (type.includes('security_group') || type.includes('iam')) {
      if (actions.includes('update') || actions.includes('delete')) {
        highRisk.push({
          address: resource.address,
          type: type,
          reason: 'Security-sensitive resource modification'
        });
      }
    }
  }

  return highRisk;
}
