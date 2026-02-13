/**
 * MCP Apps Testing Framework
 * 
 * A professional framework for testing Model Context Protocol (MCP) UI applications
 * with Playwright. Bridge the gap between MCP protocol testing and UI rendering/iframe sandboxing.
 */

export { MockMCPHost } from './core/MockMCPHost';
export { TransportInterceptor } from './core/TransportInterceptor';
export { HostProfiles, ClaudeProfile, VSCodeProfile, GenericProfile, applyTheme } from './core/HostProfiles';
export type { HostProfile } from './core/HostProfiles';

export type {
  JSONRPCRequest,
  JSONRPCResponse,
  JSONRPCNotification,
  JSONRPCError,
  MessageHandler,
  RequestInterceptor,
  ResponseInterceptor,
  MockMCPHostConfig,
  MCPCapabilities,
  MCPTestContext,
  MCPTransport,
} from './types';

import type { MockMCPHostConfig, MCPTestContext } from './types';

/**
 * Create a test context with a mock MCP host
 */
export async function createMCPTestContext(config?: MockMCPHostConfig): Promise<MCPTestContext> {
  const { MockMCPHost } = await import('./core/MockMCPHost');
  const host = new MockMCPHost(config);
  const interceptor = host.getInterceptor();

  return {
    host,
    interceptor,
    cleanup: async () => {
      await host.cleanup();
    },
  };
}
