"""Create a test harness HTML for testing the visualize_architecture tool."""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cloud_diagram_mcp.visualizer_hierarchical import generate_architecture_svg
from cloud_diagram_mcp.svg_embedder import embed_icons_in_svg_content

# Load the architecture example
with open(os.path.join(os.path.dirname(__file__), "..", "examples", "architecture-azure.json")) as f:
    arch = json.load(f)

# Generate SVG
svg = generate_architecture_svg(arch)
svg = embed_icons_in_svg_content(svg)
svg = svg.encode("utf-8", errors="ignore").decode("utf-8")
arch["_server_svg"] = svg
arch["_mode"] = "architecture"

arch_json = json.dumps(arch, ensure_ascii=True, default=str)

# Read the built HTML
dist_path = os.path.join(os.path.dirname(__file__), "..", "cloud_diagram_mcp", "dist", "mcp-app.html")
with open(dist_path, "r", encoding="utf-8") as f:
    html = f.read()

# Inject test data before the module script
inject = f'<script>window.__TEST_PLAN_DATA__ = {arch_json};</script>\n'
html = html.replace('<script type="module"', inject + '<script type="module"', 1)

out_path = os.path.join(os.path.dirname(__file__), "test-harness-architecture.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Architecture test harness: {len(html)} chars, {len(arch['resources'])} resources, {len(arch.get('connections', []))} connections")
