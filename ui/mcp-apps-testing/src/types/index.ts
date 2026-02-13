/**
 * Types for MCP Apps Testing Framework
 */

/**
 * JSON-RPC 2.0 message types
 */
export interface JSONRPCRequest {
  jsonrpc: '2.0';
  id: string | number;
  method: string;
  params?: unknown;
}

export interface JSONRPCResponse {
  jsonrpc: '2.0';
  id: string | number;
  result?: unknown;
  error?: JSONRPCError;
}

export interface JSONRPCNotification {
  jsonrpc: '2.0';
  method: string;
  params?: unknown;
}

export interface JSONRPCError {
  code: number;
  message: string;
  data?: unknown;
}

/**
 * Transport interceptor handler types
 */
export type MessageHandler = (message: JSONRPCRequest | JSONRPCResponse | JSONRPCNotification) => void | Promise<void>;

export type RequestInterceptor = (request: JSONRPCRequest) => JSONRPCRequest | Promise<JSONRPCRequest>;

export type ResponseInterceptor = (response: JSONRPCResponse) => JSONRPCResponse | Promise<JSONRPCResponse>;

/**
 * Transport interface for MCP communication
 */
export interface MCPTransport {
  // Basic transport interface - can be extended as needed
  send?: (message: unknown) => void | Promise<void>;
  close?: () => void | Promise<void>;
}

/**
 * Mock MCP Host configuration
 */
export interface MockMCPHostConfig {
  /**
   * Whether to automatically respond to common MCP protocol messages
   */
  autoRespond?: boolean;
  
  /**
   * Custom transport implementation
   */
  transport?: MCPTransport;
  
  /**
   * Enable verbose logging
   */
  debug?: boolean;

  /**
   * Host profile to simulate (e.g., 'Claude', 'VSCode', 'Generic')
   */
  hostProfile?: string;
}

/**
 * MCP capabilities that can be simulated
 */
export interface MCPCapabilities {
  tools?: {
    listChanged?: boolean;
  };
  resources?: {
    subscribe?: boolean;
    listChanged?: boolean;
  };
  prompts?: {
    listChanged?: boolean;
  };
}

/**
 * Test context for MCP applications
 */
export interface MCPTestContext {
  /**
   * Mock host instance
   */
  host: import('../core/MockMCPHost').MockMCPHost;
  
  /**
   * Transport interceptor
   */
  interceptor: import('../core/TransportInterceptor').TransportInterceptor;
  
  /**
   * Cleanup function
   */
  cleanup: () => Promise<void>;
}
