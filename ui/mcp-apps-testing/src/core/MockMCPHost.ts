import { TransportInterceptor } from './TransportInterceptor';
import { MockMCPHostConfig, MCPCapabilities, JSONRPCRequest, JSONRPCResponse } from '../types';
import { HostProfiles, HostProfile } from './HostProfiles';

/**
 * MockMCPHost - Simulates an IDE environment hosting an MCP server
 * 
 * This class provides:
 * - A simulated MCP host environment for testing
 * - Automatic handling of common MCP protocol messages
 * - Integration with TransportInterceptor for request/response mocking
 * - Capability simulation (tools, resources, prompts)
 * - Host profile simulation (Claude, VS Code, etc.)
 */
export class MockMCPHost {
  private interceptor: TransportInterceptor;
  private config: MockMCPHostConfig;
  private capabilities: MCPCapabilities;
  private initialized = false;
  private requestIdCounter = 0;
  private hostProfile: HostProfile | null = null;

  constructor(config: MockMCPHostConfig = {}) {
    this.config = {
      autoRespond: true,
      debug: false,
      ...config,
    };

    this.interceptor = new TransportInterceptor(this.config.debug);
    this.capabilities = {};

    // Load host profile if specified
    if (this.config.hostProfile) {
      this.loadHostProfile(this.config.hostProfile);
    }

    if (this.config.autoRespond) {
      this.setupAutoResponders();
    }
  }

  /**
   * Load a host profile
   */
  private loadHostProfile(profileName: string): void {
    const profile = HostProfiles[profileName as keyof typeof HostProfiles];
    if (profile) {
      this.hostProfile = profile;
      this.capabilities = profile.capabilities;
    }
  }

  /**
   * Get the current host profile
   */
  getHostProfile(): HostProfile | null {
    return this.hostProfile;
  }

  /**
   * Get the transport interceptor
   */
  getInterceptor(): TransportInterceptor {
    return this.interceptor;
  }

  /**
   * Set up automatic responses for common MCP protocol messages
   */
  private setupAutoResponders(): void {
    // Auto-respond to initialize requests
    this.interceptor.mockResponse('initialize', (request: JSONRPCRequest) => {
      this.initialized = true;
      return {
        jsonrpc: '2.0',
        id: request.id,
        result: {
          protocolVersion: '2024-11-05',
          capabilities: this.capabilities,
          serverInfo: {
            name: 'mock-mcp-server',
            version: '0.1.0',
          },
        },
      };
    });

    // Auto-respond to ping requests
    this.interceptor.mockResponse('ping', (request: JSONRPCRequest) => ({
      jsonrpc: '2.0',
      id: request.id,
      result: {},
    }));

    // Auto-respond to tools/list requests
    this.interceptor.mockResponse('tools/list', (request: JSONRPCRequest) => ({
      jsonrpc: '2.0',
      id: request.id,
      result: {
        tools: [],
      },
    }));

    // Auto-respond to resources/list requests
    this.interceptor.mockResponse('resources/list', (request: JSONRPCRequest) => ({
      jsonrpc: '2.0',
      id: request.id,
      result: {
        resources: [],
      },
    }));

    // Auto-respond to prompts/list requests
    this.interceptor.mockResponse('prompts/list', (request: JSONRPCRequest) => ({
      jsonrpc: '2.0',
      id: request.id,
      result: {
        prompts: [],
      },
    }));
  }

  /**
   * Set capabilities that this host supports
   */
  setCapabilities(capabilities: MCPCapabilities): void {
    this.capabilities = capabilities;
  }

  /**
   * Send a request to the server (simulate client -> server)
   */
  async sendRequest(method: string, params?: unknown): Promise<JSONRPCResponse> {
    const request: JSONRPCRequest = {
      jsonrpc: '2.0',
      id: ++this.requestIdCounter,
      method,
      params,
    };

    // Intercept the request
    const interceptedRequest = await this.interceptor.interceptRequest(request);

    // Check if we should mock the response
    const mockResponse = await this.interceptor.shouldMock(interceptedRequest);
    if (mockResponse) {
      return await this.interceptor.interceptResponse(mockResponse);
    }

    // If no mock, return an error
    const errorResponse: JSONRPCResponse = {
      jsonrpc: '2.0',
      id: interceptedRequest.id,
      error: {
        code: -32601,
        message: `Method not found: ${method}`,
      },
    };

    return await this.interceptor.interceptResponse(errorResponse);
  }

  /**
   * Initialize the MCP connection
   */
  async initialize(clientInfo?: { name: string; version: string }): Promise<JSONRPCResponse> {
    return await this.sendRequest('initialize', {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: clientInfo || {
        name: 'mock-client',
        version: '0.1.0',
      },
    });
  }

  /**
   * Check if the host is initialized
   */
  isInitialized(): boolean {
    return this.initialized;
  }

  /**
   * Cleanup and reset the host
   */
  async cleanup(): Promise<void> {
    this.interceptor.reset();
    this.initialized = false;
    this.requestIdCounter = 0;
  }

  /**
   * Get all recorded messages from the interceptor
   */
  getRecordedMessages() {
    return this.interceptor.getRecordedMessages();
  }

  /**
   * Clear recorded messages
   */
  clearRecordedMessages(): void {
    this.interceptor.clearRecordedMessages();
  }

  /**
   * Fluent DSL: Call a tool with automatic response handling
   * @param name Tool name
   * @param args Tool arguments
   * @param options Optional retry and timeout settings
   */
  async callTool(
    name: string,
    args: Record<string, unknown> = {},
    options: { timeout?: number; retries?: number } = {}
  ): Promise<JSONRPCResponse> {
    const { timeout = 5000, retries = 3 } = options;
    let lastError: Error | null = null;

    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        const response = await Promise.race([
          this.sendRequest('tools/call', { name, arguments: args }),
          new Promise<never>((_, reject) =>
            setTimeout(() => reject(new Error('Tool call timeout')), timeout)
          ),
        ]);

        if (response.error) {
          throw new Error(response.error.message);
        }

        return response;
      } catch (error) {
        lastError = error as Error;
        if (attempt < retries) {
          await new Promise(resolve => setTimeout(resolve, 100 * (attempt + 1)));
        }
      }
    }

    throw new Error(`Tool call failed after ${retries + 1} attempts: ${lastError?.message}`);
  }

  /**
   * Fluent DSL: List available tools
   */
  async listTools(): Promise<JSONRPCResponse> {
    return await this.sendRequest('tools/list');
  }

  /**
   * Fluent DSL: Read a resource
   * @param uri Resource URI
   */
  async readResource(uri: string): Promise<JSONRPCResponse> {
    return await this.sendRequest('resources/read', { uri });
  }

  /**
   * Fluent DSL: List available resources
   */
  async listResources(): Promise<JSONRPCResponse> {
    return await this.sendRequest('resources/list');
  }

  /**
   * Fluent DSL: Get a prompt
   * @param name Prompt name
   * @param args Prompt arguments
   */
  async getPrompt(name: string, args: Record<string, unknown> = {}): Promise<JSONRPCResponse> {
    return await this.sendRequest('prompts/get', { name, arguments: args });
  }

  /**
   * Fluent DSL: List available prompts
   */
  async listPrompts(): Promise<JSONRPCResponse> {
    return await this.sendRequest('prompts/list');
  }

  /**
   * Enable protocol logging for debugging
   */
  private protocolLoggingEnabled = false;
  
  enableProtocolLogging(): void {
    // Prevent duplicate logging interceptors
    if (this.protocolLoggingEnabled) {
      return;
    }
    
    this.protocolLoggingEnabled = true;
    
    this.interceptor.onRequest(async (request) => {
      console.log('[MCP Request]', JSON.stringify(request, null, 2));
      return request;
    });

    this.interceptor.onResponse(async (response) => {
      console.log('[MCP Response]', JSON.stringify(response, null, 2));
      return response;
    });
  }
}
