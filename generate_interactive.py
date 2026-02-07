#!/usr/bin/env python3
"""
Generate interactive Terraform plan visualization with connections.
Creates PNG with dependency arrows and HTML with clickable resources.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cloud_diff_mcp.visualizer_hierarchical import visualize_terraform_plan_hierarchical
from cloud_diff_mcp.interactive_html import generate_interactive_html


def generate_interactive_example():
    """Generate interactive visualization for complex AWS example."""
    
    # Load complex plan
    plan_path = Path(__file__).parent / "examples" / "complex-aws-plan.json"
    
    with open(plan_path, 'r') as f:
        plan_data = json.load(f)
    
    print("🎨 Generating visualizations for Complex AWS Architecture\n")
    
    # 1. Generate PNG with connections
    print("📊 Step 1: Generating PNG diagram with dependency connections...")
    png_path, summary = visualize_terraform_plan_hierarchical(
        plan_data, 
        format='png', 
        show_connections=True
    )
    print(f"   ✅ PNG saved: {png_path}")
    print(f"   📦 File size: {Path(png_path).stat().st_size:,} bytes\n")
    
    # 2. Generate SVG for HTML embedding
    print("📊 Step 2: Generating SVG diagram for interactive HTML...")
    svg_path, _ = visualize_terraform_plan_hierarchical(
        plan_data, 
        format='svg', 
        show_connections=True
    )
    print(f"   ✅ SVG saved: {svg_path}\n")
    
    # 3. Generate interactive HTML
    print("🌐 Step 3: Generating interactive HTML page...")
    output_dir = Path.cwd() / "terraform-diffs"
    html_path = output_dir / "terraform_plan_interactive.html"
    
    generate_interactive_html(plan_data, svg_path, str(html_path))
    print(f"   ✅ Interactive HTML saved: {html_path}\n")
    
    # Print summary
    print("=" * 80)
    print("✨ Interactive Visualization Complete!")
    print("=" * 80)
    print(f"\n📊 Summary:")
    for line in summary.split('\n'):
        print(f"   {line}")
    
    print(f"\n📁 Generated Files:")
    print(f"   • PNG with connections: {png_path}")
    print(f"   • SVG diagram: {svg_path}")
    print(f"   • Interactive HTML: {html_path}")
    
    print(f"\n💡 To view the interactive visualization:")
    print(f"   Open {html_path} in your web browser")
    print(f"   Click on any resource to see its configuration and changes")
    print()


if __name__ == "__main__":
    generate_interactive_example()
