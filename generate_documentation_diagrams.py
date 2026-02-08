#!/usr/bin/env python3
"""
Generate example diagrams for documentation purposes.
This script creates diagrams from the example Terraform plans
and saves them to the examples/diagrams/ directory.
"""

import asyncio
import json
import os
from pathlib import Path

from fastmcp import Client
from cloud_diagram_mcp.server import mcp


async def generate_diagram(plan_file: str, output_name: str):
    """Generate a diagram from a Terraform plan file."""
    print(f"\nGenerating diagram for {plan_file}...")
    
    with open(plan_file) as f:
        plan = json.load(f)
    
    async with Client(mcp) as client:
        result = await client.call_tool(
            "visualize_tf_diff", 
            {"plan": json.dumps(plan)}
        )
        
        # The SVG is embedded in the response
        for item in result.content:
            data = json.loads(item.text)
            if "_server_svg" in data:
                svg_content = data["_server_svg"]
                
                # Save SVG to examples/diagrams directory
                output_dir = Path("examples/diagrams")
                output_dir.mkdir(parents=True, exist_ok=True)
                
                output_file = output_dir / f"{output_name}.svg"
                with open(output_file, "w") as f:
                    f.write(svg_content)
                
                print(f"  Saved to {output_file}")
                print(f"  Size: {len(svg_content) // 1024} KB")
                return True
    
    return False


async def main():
    """Generate all example diagrams."""
    examples = [
        ("examples/sample-plan.json", "simple-aws"),
        ("examples/azure-plan.json", "simple-azure"),
        ("examples/complex-aws-plan.json", "complex-aws"),
    ]
    
    print("=" * 60)
    print("Generating Documentation Diagrams")
    print("=" * 60)
    
    for plan_file, output_name in examples:
        if os.path.exists(plan_file):
            await generate_diagram(plan_file, output_name)
        else:
            print(f"\nSkipping {plan_file} (not found)")
    
    print("\n" + "=" * 60)
    print("Done! Diagrams saved to examples/diagrams/")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
