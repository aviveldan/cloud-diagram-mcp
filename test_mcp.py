"""Test MCP server end-to-end using FastMCP in-memory Client."""

import asyncio
import json
import os
import time

from fastmcp import Client
from cloud_diagram_mcp.server import mcp


async def test_visualize_tf_diff():
    """Test the visualize_tf_diff tool with sample plans."""
    for plan_file in ["examples/sample-plan.json", "examples/complex-aws-plan.json"]:
        with open(plan_file) as f:
            plan = json.load(f)
        print(f"\n{'='*60}", flush=True)
        print(f"Testing visualize_tf_diff with {plan_file}", flush=True)
        print(f"  Resources: {len(plan.get('resource_changes', []))}", flush=True)

        async with Client(mcp) as client:
            tools = await client.list_tools()
            print(f"  Tools: {[t.name for t in tools]}", flush=True)

            print("  Calling visualize_tf_diff...", flush=True)
            start = time.time()
            result = await asyncio.wait_for(
                client.call_tool("visualize_tf_diff", {"plan": json.dumps(plan)}),
                timeout=60,
            )
            elapsed = time.time() - start
            print(f"  Result received in {elapsed:.1f}s", flush=True)

            for item in result.content:
                data = json.loads(item.text)
                has_svg = "_server_svg" in data
                print(f"  Has SVG: {has_svg}", flush=True)
                print(f"  Result size: {len(item.text) // 1024} KB", flush=True)


async def test_visualize_architecture():
    """Test the visualize_architecture tool."""
    arch_file = "examples/architecture-azure.json"
    with open(arch_file) as f:
        arch = json.load(f)
    print(f"\n{'='*60}", flush=True)
    print(f"Testing visualize_architecture with {arch_file}", flush=True)
    print(f"  Resources: {len(arch.get('resources', []))}", flush=True)
    print(f"  Connections: {len(arch.get('connections', []))}", flush=True)

    async with Client(mcp) as client:
        print("  Calling visualize_architecture...", flush=True)
        start = time.time()
        result = await asyncio.wait_for(
            client.call_tool("visualize_architecture", {"architecture": json.dumps(arch)}),
            timeout=60,
        )
        elapsed = time.time() - start
        print(f"  Result received in {elapsed:.1f}s", flush=True)

        for item in result.content:
            data = json.loads(item.text)
            has_svg = "_server_svg" in data
            is_arch = data.get("_mode") == "architecture"
            print(f"  Has SVG: {has_svg}", flush=True)
            print(f"  Architecture mode: {is_arch}", flush=True)
            print(f"  Result size: {len(item.text) // 1024} KB", flush=True)


async def test_export_architecture_svg():
    """Test the export_architecture_svg tool."""
    arch_file = "examples/architecture-azure.json"
    with open(arch_file) as f:
        arch = json.load(f)
    print(f"\n{'='*60}", flush=True)
    print(f"Testing export_architecture_svg with {arch_file}", flush=True)

    async with Client(mcp) as client:
        print("  Calling export_architecture_svg...", flush=True)
        start = time.time()
        result = await asyncio.wait_for(
            client.call_tool("export_architecture_svg", {"architecture": json.dumps(arch)}),
            timeout=60,
        )
        elapsed = time.time() - start
        print(f"  Result received in {elapsed:.1f}s", flush=True)

        for item in result.content:
            data = json.loads(item.text)
            svg_path = data.get("path", "")
            size_kb = data.get("size_kb", 0)
            exists = os.path.exists(svg_path) if svg_path else False
            print(f"  SVG path: {svg_path}", flush=True)
            print(f"  File exists: {exists}", flush=True)
            print(f"  Size: {size_kb} KB", flush=True)
            # Verify file content
            if exists:
                with open(svg_path) as f:
                    content = f.read()
                has_icons = "data:image/png;base64" in content
                has_edges = "edge" in content
                print(f"  Has embedded icons: {has_icons}", flush=True)
                print(f"  Has edges: {has_edges}", flush=True)


async def main():
    await test_visualize_tf_diff()
    await test_visualize_architecture()
    await test_export_architecture_svg()
    print("\nDone", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
