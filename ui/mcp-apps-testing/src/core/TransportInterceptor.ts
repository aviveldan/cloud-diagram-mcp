import {
  JSONRPCRequest,
  JSONRPCResponse,
  JSONRPCNotification,
  MessageHandler,
  RequestInterceptor,
  ResponseInterceptor,
} from '../types';

/**
 * TransportInterceptor - Intercepts and mocks JSON-RPC messages
 * 
 * This class allows you to:
 * - Intercept outgoing requests and modify them
 * - Intercept incoming responses and modify them
 * - Mock responses to specific requests
 * - Record all messages for testing assertions
 */
export class TransportInterceptor {
  private requestInterceptors: RequestInterceptor[] = [];
  private responseInterceptors: ResponseInterceptor[] = [];
  private messageHandlers: MessageHandler[] = [];
  private requestMocks: Map<string, (request: JSONRPCRequest) => JSONRPCResponse | Promise<JSONRPCResponse>> = new Map();
  private recordedMessages: Array<JSONRPCRequest | JSONRPCResponse | JSONRPCNotification> = [];
  private debug: boolean;

  constructor(debug = false) {
    this.debug = debug;
  }

  /**
   * Add a request interceptor
   */
  onRequest(interceptor: RequestInterceptor): void {
    this.requestInterceptors.push(interceptor);
  }

  /**
   * Add a response interceptor
   */
  onResponse(interceptor: ResponseInterceptor): void {
    this.responseInterceptors.push(interceptor);
  }

  /**
   * Add a message handler (for all messages)
   */
  onMessage(handler: MessageHandler): void {
    this.messageHandlers.push(handler);
  }

  /**
   * Mock a response for a specific method
   */
  mockResponse(method: string, handler: (request: JSONRPCRequest) => JSONRPCResponse | Promise<JSONRPCResponse>): void {
    this.requestMocks.set(method, handler);
  }

  /**
   * Process an outgoing request
   */
  async interceptRequest(request: JSONRPCRequest): Promise<JSONRPCRequest> {
    if (this.debug) {
      console.log('[TransportInterceptor] Outgoing request:', JSON.stringify(request, null, 2));
    }

    this.recordedMessages.push(request);

    let modifiedRequest = request;
    for (const interceptor of this.requestInterceptors) {
      modifiedRequest = await interceptor(modifiedRequest);
    }

    for (const handler of this.messageHandlers) {
      await handler(modifiedRequest);
    }

    return modifiedRequest;
  }

  /**
   * Process an incoming response
   */
  async interceptResponse(response: JSONRPCResponse): Promise<JSONRPCResponse> {
    if (this.debug) {
      console.log('[TransportInterceptor] Incoming response:', JSON.stringify(response, null, 2));
    }

    this.recordedMessages.push(response);

    let modifiedResponse = response;
    for (const interceptor of this.responseInterceptors) {
      modifiedResponse = await interceptor(modifiedResponse);
    }

    for (const handler of this.messageHandlers) {
      await handler(modifiedResponse);
    }

    return modifiedResponse;
  }

  /**
   * Check if a request should be mocked
   */
  async shouldMock(request: JSONRPCRequest): Promise<JSONRPCResponse | null> {
    const mockHandler = this.requestMocks.get(request.method);
    if (mockHandler) {
      if (this.debug) {
        console.log(`[TransportInterceptor] Mocking response for method: ${request.method}`);
      }
      return await mockHandler(request);
    }
    return null;
  }

  /**
   * Get all recorded messages
   */
  getRecordedMessages(): Array<JSONRPCRequest | JSONRPCResponse | JSONRPCNotification> {
    return [...this.recordedMessages];
  }

  /**
   * Get recorded requests only
   */
  getRecordedRequests(): JSONRPCRequest[] {
    return this.recordedMessages.filter(msg => 'method' in msg && 'id' in msg) as JSONRPCRequest[];
  }

  /**
   * Get recorded responses only
   */
  getRecordedResponses(): JSONRPCResponse[] {
    return this.recordedMessages.filter(msg => 'id' in msg && !('method' in msg)) as JSONRPCResponse[];
  }

  /**
   * Find requests by method name
   */
  findRequestsByMethod(method: string): JSONRPCRequest[] {
    return this.getRecordedRequests().filter(req => req.method === method);
  }

  /**
   * Clear all recorded messages
   */
  clearRecordedMessages(): void {
    this.recordedMessages = [];
  }

  /**
   * Clear all interceptors and mocks
   */
  reset(): void {
    this.requestInterceptors = [];
    this.responseInterceptors = [];
    this.messageHandlers = [];
    this.requestMocks.clear();
    this.recordedMessages = [];
  }
}
