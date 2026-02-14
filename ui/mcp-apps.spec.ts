import { test, expect } from '@playwright/test';
import { MockMCPHost } from 'mcp-apps-testing';
import * as path from 'path';
import * as fs from 'fs';
import { fileURLToPath } from 'url';

// Get __dirname equivalent in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * MCP Apps Testing for Cloud Diagram MCP
 * 
 * This test suite validates the cloud-diagram-mcp tools using the mcp-apps-testing framework:
 * 1. visualize_tf_diff - Terraform plan visualization
 * 2. visualize_architecture - Cloud architecture visualization
 * 3. export_architecture_svg - SVG export functionality
 */

test.describe('Cloud Diagram MCP Tools', () => {
  let host: MockMCPHost;

  test.beforeEach(async () => {
    // Setup MockMCPHost with Claude profile
    host = new MockMCPHost({ 
      debug: false,
      hostProfile: 'Claude',
      autoRespond: true
    });
  });

  test.afterEach(async () => {
    await host.cleanup();
  });

  test('should initialize MCP host', async () => {
    await host.initialize({ name: 'cloud-diagram-mcp', version: '2.0.0' });
    expect(host.isInitialized()).toBe(true);
  });

  test('should list cloud diagram tools', async () => {
    await host.initialize();

    // Mock the tools/list response
    const interceptor = host.getInterceptor();
    interceptor.mockResponse('tools/list', (request: any) => ({
      jsonrpc: '2.0',
      id: request.id,
      result: {
        tools: [
          {
            name: 'visualize_tf_diff',
            description: 'Visualize Terraform plan changes as an interactive cloud architecture diagram',
            inputSchema: {
              type: 'object',
              properties: {
                plan: { type: 'string', description: 'Terraform plan JSON as a string' }
              },
              required: ['plan']
            }
          },
          {
            name: 'visualize_architecture',
            description: 'Visualize a cloud architecture as an interactive diagram',
            inputSchema: {
              type: 'object',
              properties: {
                architecture: { type: 'string', description: 'Architecture JSON string' }
              },
              required: ['architecture']
            }
          },
          {
            name: 'export_architecture_svg',
            description: 'Export a cloud architecture diagram as an SVG file',
            inputSchema: {
              type: 'object',
              properties: {
                architecture: { type: 'string', description: 'Architecture JSON string' },
                output_path: { type: 'string', description: 'Optional file path for the SVG' }
              },
              required: ['architecture']
            }
          }
        ]
      }
    }));

    const response = await host.listTools();
    expect(response.result.tools).toHaveLength(3);
    expect(response.result.tools.map((t: any) => t.name)).toContain('visualize_tf_diff');
    expect(response.result.tools.map((t: any) => t.name)).toContain('visualize_architecture');
    expect(response.result.tools.map((t: any) => t.name)).toContain('export_architecture_svg');
  });

  test('should call visualize_tf_diff tool', async () => {
    await host.initialize();

    // Load sample Terraform plan
    const samplePlanPath = path.join(__dirname, '../examples/sample-plan.json');
    const planContent = fs.readFileSync(samplePlanPath, 'utf-8');
    const planData = JSON.parse(planContent);

    // Mock the tool response
    const interceptor = host.getInterceptor();
    interceptor.mockResponse('tools/call', (request: any) => {
      if (request.params?.name === 'visualize_tf_diff') {
        // Simulate the tool returning plan data with SVG
        const result = {
          ...planData,
          _server_svg: '<svg>mock svg content</svg>'
        };
        return {
          jsonrpc: '2.0',
          id: request.id,
          result: {
            content: [{
              type: 'text',
              text: JSON.stringify(result)
            }]
          }
        };
      }
      return {
        jsonrpc: '2.0',
        id: request.id,
        error: {
          code: -32601,
          message: 'Method not found'
        }
      };
    });

    const response = await host.callTool('visualize_tf_diff', { 
      plan: planContent 
    }, { 
      timeout: 10000, 
      retries: 2 
    });

    expect(response.result).toBeDefined();
    expect(response.result.content).toHaveLength(1);
    
    const resultData = JSON.parse(response.result.content[0].text);
    expect(resultData._server_svg).toBeDefined();
    expect(resultData.resource_changes).toBeDefined();
  });

  test('should call visualize_architecture tool', async () => {
    await host.initialize();

    // Load sample architecture
    const archPath = path.join(__dirname, '../examples/architecture-azure.json');
    const archContent = fs.readFileSync(archPath, 'utf-8');
    const archData = JSON.parse(archContent);

    // Mock the tool response
    const interceptor = host.getInterceptor();
    interceptor.mockResponse('tools/call', (request: any) => {
      if (request.params?.name === 'visualize_architecture') {
        const result = {
          ...archData,
          _server_svg: '<svg>mock architecture svg</svg>',
          _mode: 'architecture'
        };
        return {
          jsonrpc: '2.0',
          id: request.id,
          result: {
            content: [{
              type: 'text',
              text: JSON.stringify(result)
            }]
          }
        };
      }
      return {
        jsonrpc: '2.0',
        id: request.id,
        error: {
          code: -32601,
          message: 'Method not found'
        }
      };
    });

    const response = await host.callTool('visualize_architecture', { 
      architecture: archContent 
    }, { 
      timeout: 10000, 
      retries: 2 
    });

    expect(response.result).toBeDefined();
    expect(response.result.content).toHaveLength(1);
    
    const resultData = JSON.parse(response.result.content[0].text);
    expect(resultData._mode).toBe('architecture');
    expect(resultData._server_svg).toBeDefined();
    expect(resultData.resources).toBeDefined();
    expect(resultData.connections).toBeDefined();
  });

  test('should call export_architecture_svg tool', async () => {
    await host.initialize();

    // Load sample architecture
    const archPath = path.join(__dirname, '../examples/architecture-azure.json');
    const archContent = fs.readFileSync(archPath, 'utf-8');

    // Mock the tool response
    const interceptor = host.getInterceptor();
    interceptor.mockResponse('tools/call', (request: any) => {
      if (request.params?.name === 'export_architecture_svg') {
        return {
          jsonrpc: '2.0',
          id: request.id,
          result: {
            content: [{
              type: 'text',
              text: JSON.stringify({
                path: '/tmp/architecture_test.svg',
                size_kb: 42.5
              })
            }]
          }
        };
      }
      return {
        jsonrpc: '2.0',
        id: request.id,
        error: {
          code: -32601,
          message: 'Method not found'
        }
      };
    });

    const response = await host.callTool('export_architecture_svg', { 
      architecture: archContent,
      output_path: ''
    }, { 
      timeout: 10000, 
      retries: 2 
    });

    expect(response.result).toBeDefined();
    expect(response.result.content).toHaveLength(1);
    
    const resultData = JSON.parse(response.result.content[0].text);
    expect(resultData.path).toBeDefined();
    expect(resultData.size_kb).toBeGreaterThan(0);
  });

  test('should verify Claude host profile capabilities', async () => {
    const profile = host.getHostProfile();
    
    expect(profile).toBeDefined();
    expect(profile?.name).toBe('Claude');
    expect(profile?.capabilities.tools?.listChanged).toBe(true);
  });

  test('should record and verify message flow', async () => {
    await host.initialize();
    
    // Mock a simple tools/list call
    const interceptor = host.getInterceptor();
    interceptor.mockResponse('tools/list', (request: any) => ({
      jsonrpc: '2.0',
      id: request.id,
      result: { tools: [] }
    }));
    
    await host.listTools();

    const requests = interceptor.getRecordedRequests();
    
    // Verify the sequence of calls
    expect(requests.some(r => r.method === 'initialize')).toBe(true);
    expect(requests.some(r => r.method === 'tools/list')).toBe(true);
  });

  test('should handle invalid JSON in tool arguments', async () => {
    await host.initialize();

    const interceptor = host.getInterceptor();
    interceptor.mockResponse('tools/call', (request: any) => {
      if (request.params?.name === 'visualize_tf_diff') {
        return {
          jsonrpc: '2.0',
          id: request.id,
          result: {
            content: [{
              type: 'text',
              text: JSON.stringify({ error: 'Invalid JSON: Unexpected token' })
            }]
          }
        };
      }
      return {
        jsonrpc: '2.0',
        id: request.id,
        error: { code: -32601, message: 'Method not found' }
      };
    });

    const response = await host.callTool('visualize_tf_diff', { 
      plan: 'invalid json {' 
    });

    expect(response.result).toBeDefined();
    const resultData = JSON.parse(response.result.content[0].text);
    expect(resultData.error).toContain('Invalid JSON');
  });

  test('should handle complex AWS plan', async () => {
    await host.initialize();

    // Load complex AWS plan
    const complexPlanPath = path.join(__dirname, '../examples/complex-aws-plan.json');
    const planContent = fs.readFileSync(complexPlanPath, 'utf-8');
    const planData = JSON.parse(planContent);

    const interceptor = host.getInterceptor();
    interceptor.mockResponse('tools/call', (request: any) => {
      if (request.params?.name === 'visualize_tf_diff') {
        const result = {
          ...planData,
          _server_svg: '<svg>complex plan svg</svg>'
        };
        return {
          jsonrpc: '2.0',
          id: request.id,
          result: {
            content: [{
              type: 'text',
              text: JSON.stringify(result)
            }]
          }
        };
      }
      return {
        jsonrpc: '2.0',
        id: request.id,
        error: { code: -32601, message: 'Method not found' }
      };
    });

    const response = await host.callTool('visualize_tf_diff', { 
      plan: planContent 
    }, { 
      timeout: 15000, 
      retries: 2 
    });

    expect(response.result).toBeDefined();
    const resultData = JSON.parse(response.result.content[0].text);
    expect(resultData.resource_changes).toBeDefined();
    expect(resultData.resource_changes.length).toBeGreaterThan(10);
  });

  test('should enable protocol logging for debugging', async () => {
    const logs: string[] = [];
    const originalLog = console.log;
    console.log = (...logArgs: unknown[]) => {
      logs.push(logArgs.join(' '));
      originalLog(...logArgs);
    };

    host.enableProtocolLogging();
    await host.initialize();

    console.log = originalLog;

    // Verify protocol logs were generated
    const requestLogs = logs.filter(log => log.includes('[MCP Request]') || log.includes('initialize'));
    expect(requestLogs.length).toBeGreaterThan(0);
  });
});
