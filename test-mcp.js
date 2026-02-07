#!/usr/bin/env node

/**
 * MCP Client Test
 * This simulates an MCP client connecting to the Cloud Diff server
 */

import { spawn } from 'child_process';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function testMCPServer() {
  console.log('🧪 Testing MCP Server Integration\n');

  // Load sample plan
  const samplePlanPath = join(__dirname, 'examples', 'sample-plan.json');
  const planContent = readFileSync(samplePlanPath, 'utf-8');

  // Start the MCP server
  const serverProcess = spawn('node', [join(__dirname, 'dist', 'index.js')], {
    stdio: ['pipe', 'pipe', 'pipe']
  });

  let responses = [];
  let errorOutput = '';

  serverProcess.stdout.on('data', (data) => {
    const text = data.toString();
    responses.push(text);
  });

  serverProcess.stderr.on('data', (data) => {
    errorOutput += data.toString();
  });

  // Wait for server to start
  await new Promise(resolve => setTimeout(resolve, 1000));

  console.log('📡 Server started:', errorOutput.trim());
  console.log();

  // Send initialize request
  const initRequest = {
    jsonrpc: '2.0',
    id: 1,
    method: 'initialize',
    params: {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: {
        name: 'test-client',
        version: '1.0.0'
      }
    }
  };

  console.log('📤 Sending initialize request...');
  serverProcess.stdin.write(JSON.stringify(initRequest) + '\n');

  await new Promise(resolve => setTimeout(resolve, 500));

  // Send tools/list request
  const listToolsRequest = {
    jsonrpc: '2.0',
    id: 2,
    method: 'tools/list',
    params: {}
  };

  console.log('📤 Requesting tools list...');
  serverProcess.stdin.write(JSON.stringify(listToolsRequest) + '\n');

  await new Promise(resolve => setTimeout(resolve, 500));

  // Send analyze_tf_plan request
  const analyzeRequest = {
    jsonrpc: '2.0',
    id: 3,
    method: 'tools/call',
    params: {
      name: 'analyze_tf_plan',
      arguments: {
        plan: planContent
      }
    }
  };

  console.log('📤 Sending analyze_tf_plan request...');
  serverProcess.stdin.write(JSON.stringify(analyzeRequest) + '\n');

  // Wait for responses
  await new Promise(resolve => setTimeout(resolve, 2000));

  console.log();
  console.log('📥 Received responses:');
  console.log('─'.repeat(80));
  
  if (responses.length > 0) {
    for (let i = 0; i < responses.length; i++) {
      console.log(`Response ${i + 1}:`);
      try {
        const jsonData = responses[i].trim().split('\n').filter(line => line.startsWith('{')).map(line => JSON.parse(line));
        jsonData.forEach(data => {
          console.log(JSON.stringify(data, null, 2));
        });
      } catch (e) {
        console.log(responses[i]);
      }
      console.log();
    }
    console.log('✅ Server responded successfully!');
  } else {
    console.log('⚠️ No responses received yet (server may still be processing)');
  }
  
  console.log('─'.repeat(80));

  // Cleanup
  serverProcess.kill();
  console.log('\n✅ MCP integration test completed!');
}

testMCPServer().catch((error) => {
  console.error('❌ Test failed:', error);
  process.exit(1);
});
