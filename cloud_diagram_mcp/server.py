#!/usr/bin/env python3
"""
Cloud Diagram MCP Server
FastMCP server that visualizes Terraform plan changes as an interactive MCP App.

Uses the MCP Apps pattern:
- Tool linked to a ui:// resource via ToolUI
- HTML resource with the @modelcontextprotocol/ext-apps JS SDK
- Tool returns structured plan data; the UI renders it client-side
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from fastmcp import FastMCP
from fastmcp.server.apps import AppConfig

mcp = FastMCP("cloud-diagram-mcp")

VIEW_URI = "ui://cloud-diagram/visualization"


# ---------------------------------------------------------------------------
# UI HTML — built from ui/ React app via `npm run build` (Vite + singlefile)
# ---------------------------------------------------------------------------

_UI_HTML_PATH = Path(__file__).parent / "dist" / "mcp-app.html"


def _load_ui_html() -> str:
    """Load the pre-built React UI HTML file."""
    if _UI_HTML_PATH.exists():
        return _UI_HTML_PATH.read_text(encoding="utf-8")
    raise FileNotFoundError(
        f"UI not built. Run: cd ui && npm run build\n" f"Expected at: {_UI_HTML_PATH}"
    )


# ---------------------------------------------------------------------------
# Tool — returns structured plan data; the UI resource renders it
# ---------------------------------------------------------------------------


@mcp.tool(app=AppConfig(resourceUri=VIEW_URI))
def visualize_tf_diff(plan: str) -> str:
    """
    Visualize Terraform plan changes as an interactive cloud architecture diagram.

    Generates an MCP App with clickable resources showing configuration details
    and before/after comparisons. Connections are color-coded: green for new
    dependencies, red for removed, grey for unchanged.

    Args:
        plan: Terraform plan JSON as a string (from `terraform show -json tfplan`)

    Returns:
        The parsed plan data as JSON for the MCP App UI to render
    """
    try:
        plan_data = json.loads(plan)
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {e}"})

    if "resource_changes" not in plan_data:
        return json.dumps({"error": "Invalid Terraform plan — missing 'resource_changes'."})

    # Try to generate SVG server-side with official cloud provider icons
    try:
        from cloud_diagram_mcp.visualizer_hierarchical import generate_svg
        from cloud_diagram_mcp.svg_embedder import embed_icons_in_svg_content

        svg = generate_svg(plan_data)
        svg = embed_icons_in_svg_content(svg)
        # Remove surrogate characters that break UTF-8 JSON serialisation
        # Use 'ignore' to strip surrogates completely
        svg = svg.encode("utf-8", errors="ignore").decode("utf-8")
        plan_data["_server_svg"] = svg
    except Exception:
        pass  # Fall back to client-side icon rendering

    # Use ensure_ascii=True to prevent any Unicode issues in JSON
    result = json.dumps(plan_data, ensure_ascii=True)
    return result


@mcp.tool(app=AppConfig(resourceUri=VIEW_URI))
def visualize_architecture(architecture: str) -> str:
    """
    Visualize a cloud architecture as an interactive diagram.

    Use this to show the architecture of existing infrastructure or to propose
    a new architecture for user approval. Connections can be color-coded to
    highlight new (green) or removed (red) relationships.

    Args:
        architecture: JSON string with the architecture description:
            {
                "title": "My Architecture",
                "resources": [
                    {"address": "aws_vpc.main", "type": "aws_vpc", "name": "main-vpc"},
                    {"address": "aws_instance.web", "type": "aws_instance", "name": "web-server"}
                ],
                "connections": [
                    {"from": "aws_instance.web", "to": "aws_vpc.main", "label": "runs in"},
                    {"from": "aws_instance.web", "to": "aws_s3_bucket.data",
                     "label": "reads from", "action": "create"}
                ]
            }
            Resource types use Terraform naming (aws_*, azurerm_*, google_*).
            Connection action: "create" (green), "delete" (red), or omit for grey.

    Returns:
        The architecture data as JSON for the MCP App UI to render
    """
    try:
        arch_data = json.loads(architecture)
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {e}"})

    if "resources" not in arch_data:
        return json.dumps({"error": "Missing 'resources' array."})

    # Try to generate SVG server-side
    try:
        from cloud_diagram_mcp.visualizer_hierarchical import generate_architecture_svg
        from cloud_diagram_mcp.svg_embedder import embed_icons_in_svg_content

        svg = generate_architecture_svg(arch_data)
        svg = embed_icons_in_svg_content(svg)
        svg = svg.encode("utf-8", errors="ignore").decode("utf-8")
        arch_data["_server_svg"] = svg
    except Exception:
        pass

    # Build a compatible structure for the UI
    arch_data["_mode"] = "architecture"
    result = json.dumps(arch_data, ensure_ascii=True, default=str)
    return result


@mcp.tool()
def export_architecture_svg(architecture: str, output_path: str = "") -> str:
    """
    Export a cloud architecture diagram as an SVG file.

    Generates the diagram and writes it to a file so it can be embedded in
    READMEs or documentation. The SVG is NOT returned as a string to avoid
    wasting LLM tokens — only the file path is returned.

    Args:
        architecture: JSON string with the architecture description (same
            format as visualize_architecture).
        output_path: Optional file path for the SVG. If empty, a temp file
            is created. Use a path like "docs/architecture.svg" to place
            it in your repo.

    Returns:
        The absolute path to the generated SVG file.
    """
    try:
        arch_data = json.loads(architecture)
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {e}"})

    if "resources" not in arch_data:
        return json.dumps({"error": "Missing 'resources' array."})

    from cloud_diagram_mcp.visualizer_hierarchical import generate_architecture_svg
    from cloud_diagram_mcp.svg_embedder import embed_icons_in_svg_content

    svg = generate_architecture_svg(arch_data)
    svg = embed_icons_in_svg_content(svg)
    svg = svg.encode("utf-8", errors="ignore").decode("utf-8")

    if output_path:
        target = Path(output_path).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
    else:
        import tempfile as _tmp

        fd, tmp = _tmp.mkstemp(suffix=".svg", prefix="architecture_")
        os.close(fd)
        target = Path(tmp)

    target.write_text(svg, encoding="utf-8")
    return json.dumps({"path": str(target), "size_kb": round(len(svg) / 1024, 1)})


# ---------------------------------------------------------------------------
# UI Resource — serves the interactive HTML viewer
# ---------------------------------------------------------------------------


@mcp.resource(
    VIEW_URI,
    app=AppConfig(),
)
def visualization_view() -> str:
    """Interactive Terraform plan viewer — renders tool results as architecture diagrams."""
    return _load_ui_html()


def main() -> None:
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
