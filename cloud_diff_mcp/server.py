#!/usr/bin/env python3
"""
Cloud Diff MCP Server
FastMCP server for analyzing Terraform plans and visualizing infrastructure changes
with cloud architecture diagrams using the Diagrams library.
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

from .visualizer import visualize_terraform_plan

# Initialize FastMCP server
mcp = FastMCP("cloud-diff-mcp")


@mcp.tool()
def visualize_tf_diff(plan: str) -> str:
    """
    Visualize Terraform plan changes using cloud architecture diagrams.
    
    This tool generates a visual diagram showing infrastructure changes from a
    Terraform plan. It operates entirely offline, processing the plan output
    without requiring cloud credentials or connectivity.
    
    Args:
        plan: Terraform plan JSON as a string (from `terraform show -json tfplan`)
    
    Returns:
        Path to the generated diagram image file with a summary of changes
    """
    try:
        # Parse the Terraform plan JSON
        try:
            plan_data = json.loads(plan)
        except json.JSONDecodeError as e:
            return f"Error: Invalid JSON format in Terraform plan: {str(e)}"
        
        # Validate the plan structure
        if "resource_changes" not in plan_data:
            return "Error: Invalid Terraform plan format. Missing 'resource_changes' field."
        
        # Generate the visualization
        output_path, summary = visualize_terraform_plan(plan_data)
        
        # Return the result with summary
        result = f"""# Terraform Plan Visualization

## Change Summary
{summary}

## Diagram Generated
The visual diff diagram has been saved to: `{output_path}`

The diagram shows:
- 🟢 **Green borders**: New resources (create)
- 🔴 **Red borders**: Deleted resources (delete)
- 🟠 **Orange borders**: Modified resources (update)
- 🟣 **Purple borders**: Replaced resources (create + delete)
- ⚪ **Gray/Standard**: Unchanged resources (context)

**Note:** This is an offline analysis. No cloud API calls were made.
"""
        return result
        
    except Exception as e:
        return f"Error generating visualization: {str(e)}"


def main() -> None:
    """Main entry point for the MCP server."""
    # Run the FastMCP server
    mcp.run()


if __name__ == "__main__":
    main()
