#!/usr/bin/env node

/**
 * Test script for Cloud Diff MCP Server
 * This script tests the analyze_tf_plan tool with the sample plan
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function testMermaidGeneration() {
  console.log('🧪 Testing Mermaid Generation and Risk Analysis\n');

  // Import the utilities
  const { generateMermaidDiagram, getActionCounts } = await import('./dist/utils/mermaid-generator.js');
  const { generateRiskSummary } = await import('./dist/utils/risk-summary.js');

  // Load sample plan
  const samplePlanPath = join(__dirname, 'examples', 'sample-plan.json');
  const planContent = readFileSync(samplePlanPath, 'utf-8');
  const plan = JSON.parse(planContent);

  console.log('📋 Analyzing Terraform Plan...\n');

  // Test Mermaid generation
  const mermaidDiagram = generateMermaidDiagram(plan);
  console.log('📊 Mermaid Diagram:');
  console.log('─'.repeat(80));
  console.log(mermaidDiagram);
  console.log('─'.repeat(80));
  console.log();

  // Test action counts
  const actionCounts = getActionCounts(plan);
  console.log('📈 Action Counts:');
  console.log(`  ✨ Create: ${actionCounts.create}`);
  console.log(`  📝 Update: ${actionCounts.update}`);
  console.log(`  🗑️ Delete: ${actionCounts.delete}`);
  console.log(`  🔄 Replace: ${actionCounts.replace}`);
  console.log();

  // Test risk summary
  const riskSummary = generateRiskSummary(plan);
  console.log('⚠️ Risk Summary:');
  console.log('─'.repeat(80));
  console.log(riskSummary);
  console.log('─'.repeat(80));
  console.log();

  console.log('✅ All tests completed successfully!');
}

testMermaidGeneration().catch((error) => {
  console.error('❌ Test failed:', error);
  process.exit(1);
});
