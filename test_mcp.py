"""Test MCP server end-to-end using FastMCP client to debug hangs."""
import asyncio
import json
import time
import sys

from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport


async def main():
    plan = json.load(open("examples/sample-plan.json"))

    transport = PythonStdioTransport(
        "cloud_diff_mcp.server:mcp",
        python_cmd=sys.executable,
    )

    print("Connecting to server...", flush=True)
    async with Client(transport) as client:
        print("Connected! Listing tools...", flush=True)
        tools = await client.list_tools()
        print(f"Tools: {[t.name for t in tools]}", flush=True)

        print("\nCalling visualize_tf_diff...", flush=True)
        start = time.time()
        try:
            result = await asyncio.wait_for(
                client.call_tool("visualize_tf_diff", {"plan": json.dumps(plan)}),
                timeout=30,
            )
            elapsed = time.time() - start
            print(f"Result received in {elapsed:.1f}s", flush=True)
            for item in result:
                print(f"  Content type: {item.type}, size: {len(str(item.text)) if hasattr(item, 'text') else 'N/A'}", flush=True)
        except asyncio.TimeoutError:
            elapsed = time.time() - start
            print(f"TIMED OUT after {elapsed:.1f}s!", flush=True)
        except Exception as e:
            elapsed = time.time() - start
            print(f"ERROR after {elapsed:.1f}s: {type(e).__name__}: {e}", flush=True)

    print("\nDone", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
