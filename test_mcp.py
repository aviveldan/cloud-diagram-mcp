"""Test MCP server end-to-end using FastMCP in-memory Client."""
import asyncio
import json
import time

from fastmcp import Client
from cloud_diff_mcp.server import mcp


async def main():
    for plan_file in ["examples/sample-plan.json", "examples/complex-aws-plan.json"]:
        with open(plan_file) as f:
            plan = json.load(f)
        print(f"\n{'='*60}", flush=True)
        print(f"Testing with {plan_file}", flush=True)
        print(f"  Resources: {len(plan.get('resource_changes', []))}", flush=True)

        async with Client(mcp) as client:
            # 1. List tools
            tools = await client.list_tools()
            print(f"  Tools: {[t.name for t in tools]}", flush=True)

            # 2. Call tool
            print("  Calling visualize_tf_diff...", flush=True)
            start = time.time()
            try:
                result = await asyncio.wait_for(
                    client.call_tool(
                        "visualize_tf_diff", {"plan": json.dumps(plan)}
                    ),
                    timeout=60,
                )
                elapsed = time.time() - start
                print(f"  Result received in {elapsed:.1f}s", flush=True)

                for item in result.content:
                    data = json.loads(item.text)
                    has_svg = "_server_svg" in data
                    print(f"  Has SVG: {has_svg}", flush=True)
                    print(f"  Result size: {len(item.text) // 1024} KB", flush=True)

            except asyncio.TimeoutError:
                elapsed = time.time() - start
                print(f"  TIMED OUT after {elapsed:.1f}s!", flush=True)
            except Exception as e:
                elapsed = time.time() - start
                print(f"  ERROR after {elapsed:.1f}s: {type(e).__name__}: {e}", flush=True)

    print("\nDone", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
