#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';
import { z } from 'zod';
import { generateMermaidDiagram, getActionCounts } from './utils/mermaid-generator.js';
import { TerraformPlan } from './utils/types.js';

/**
 * Cloud Diff MCP Server
 * Analyzes Terraform plans and visualizes infrastructure changes
 */

// Schema for analyze_tf_plan tool
const AnalyzeTfPlanSchema = z.object({
  plan: z.string().describe('Terraform plan JSON as a string'),
});

// Schema for execute_tf_apply tool
const ExecuteTfApplySchema = z.object({
  planId: z.string().optional().describe('Optional plan ID for tracking'),
  autoApprove: z.boolean().optional().default(false).describe('Auto-approve the apply'),
});

class CloudDiffServer {
  private server: Server;
  private lastAnalyzedPlan: TerraformPlan | null = null;

  constructor() {
    this.server = new Server(
      {
        name: 'cloud-diff-mcp',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupHandlers();
    this.setupErrorHandling();
  }

  private setupErrorHandling(): void {
    this.server.onerror = (error) => {
      console.error('[MCP Error]', error);
    };

    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupHandlers(): void {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'analyze_tf_plan',
            description: 'Analyze a Terraform plan JSON and generate a visual Mermaid diagram',
            inputSchema: {
              type: 'object',
              properties: {
                plan: {
                  type: 'string',
                  description: 'Terraform plan JSON as a string',
                },
              },
              required: ['plan'],
            },
          },
          {
            name: 'execute_tf_apply',
            description: 'Execute terraform apply command (simulated for safety)',
            inputSchema: {
              type: 'object',
              properties: {
                planId: {
                  type: 'string',
                  description: 'Optional plan ID for tracking',
                },
                autoApprove: {
                  type: 'boolean',
                  description: 'Auto-approve the apply',
                  default: false,
                },
              },
            },
          },
        ] as Tool[],
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      try {
        if (request.params.name === 'analyze_tf_plan') {
          return await this.handleAnalyzeTfPlan(request.params.arguments);
        } else if (request.params.name === 'execute_tf_apply') {
          return await this.handleExecuteTfApply(request.params.arguments);
        } else {
          throw new Error(`Unknown tool: ${request.params.name}`);
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${errorMessage}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  private async handleAnalyzeTfPlan(args: unknown) {
    const parsed = AnalyzeTfPlanSchema.parse(args);
    
    // Parse the Terraform plan JSON
    let plan: TerraformPlan;
    try {
      plan = JSON.parse(parsed.plan);
    } catch (error) {
      throw new Error('Invalid JSON format for Terraform plan');
    }

    // Store the plan for later use
    this.lastAnalyzedPlan = plan;

    // Generate Mermaid diagram
    const mermaidDiagram = generateMermaidDiagram(plan);
    
    // Get action counts
    const actionCounts = getActionCounts(plan);

    // Create the UI content with the diagram and action button
    const uiContent = this.generateUIContent(mermaidDiagram, actionCounts);

    return {
      content: [
        {
          type: 'text',
          text: `# Terraform Plan Analysis\n\n${uiContent}`,
        },
      ],
    };
  }

  private generateUIContent(
    mermaidDiagram: string,
    actionCounts: Record<string, number>
  ): string {
    const lines: string[] = [];

    // Action summary
    lines.push('## Change Summary');
    lines.push('');
    lines.push(`- ✨ Create: ${actionCounts.create}`);
    lines.push(`- 📝 Update: ${actionCounts.update}`);
    lines.push(`- 🗑️ Delete: ${actionCounts.delete}`);
    lines.push(`- 🔄 Replace: ${actionCounts.replace}`);
    lines.push('');

    // Mermaid diagram
    lines.push('## Infrastructure Change Visualization');
    lines.push('');
    lines.push('```mermaid');
    lines.push(mermaidDiagram);
    lines.push('```');
    lines.push('');

    // Action buttons (formatted as instructions)
    lines.push('---');
    lines.push('');
    lines.push('## Next Steps');
    lines.push('');
    lines.push('To apply these changes, use the `execute_tf_apply` tool.');
    lines.push('');
    lines.push('**⚠️ Note:** This is a simulation. In production, this would execute `terraform apply`.');

    return lines.join('\n');
  }

  private async handleExecuteTfApply(args: unknown) {
    const parsed = ExecuteTfApplySchema.parse(args);

    if (!this.lastAnalyzedPlan) {
      throw new Error('No plan has been analyzed yet. Please run analyze_tf_plan first.');
    }

    // Simulate terraform apply
    // In a real implementation, this would execute the actual terraform apply command
    const planId = parsed.planId || 'plan-' + Date.now();
    const autoApprove = parsed.autoApprove ? ' --auto-approve' : '';

    const result = [
      '# Terraform Apply Simulation',
      '',
      `**Plan ID:** ${planId}`,
      `**Command:** terraform apply${autoApprove}`,
      '',
      '## Status',
      '',
      '✅ **Simulation successful**',
      '',
      '⚠️ **Note:** This is a simulated execution. In a production environment, this would:',
      '1. Validate the plan',
      '2. Execute terraform apply with the provided options',
      '3. Stream the output in real-time',
      '4. Report the final status',
      '',
      '## Safety Considerations',
      '',
      'For production use, implement:',
      '- Authentication and authorization',
      '- Approval workflows',
      '- State locking',
      '- Rollback mechanisms',
      '- Audit logging',
    ].join('\n');

    return {
      content: [
        {
          type: 'text',
          text: result,
        },
      ],
    };
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Cloud Diff MCP Server running on stdio');
  }
}

// Start the server
const server = new CloudDiffServer();
server.run().catch((error) => {
  console.error('Fatal error running server:', error);
  process.exit(1);
});
