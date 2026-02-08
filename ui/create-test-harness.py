"""Create a test harness HTML that loads the built app with injected test data."""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cloud_diagram_mcp.visualizer_hierarchical import generate_svg
from cloud_diagram_mcp.svg_embedder import embed_icons_in_svg_content

# Generate plan data with SVG
with open(os.path.join(os.path.dirname(__file__), "..", "examples", "sample-plan.json")) as f:
    plan = json.load(f)

svg = generate_svg(plan)
svg = embed_icons_in_svg_content(svg)
svg = svg.encode("utf-8", errors="ignore").decode("utf-8")
plan["_server_svg"] = svg

plan_json = json.dumps(plan, ensure_ascii=True)

# Read the built HTML
dist_path = os.path.join(os.path.dirname(__file__), "..", "cloud_diagram_mcp", "dist", "mcp-app.html")
with open(dist_path, "r", encoding="utf-8") as f:
    html = f.read()

# Inject test data before the module script
inject = f'<script>window.__TEST_PLAN_DATA__ = {plan_json};</script>\n'
html = html.replace('<script type="module"', inject + '<script type="module"', 1)

out_path = os.path.join(os.path.dirname(__file__), "test-harness.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Test harness: {len(html)} chars, {len(plan['resource_changes'])} resources")
