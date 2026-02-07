#!/usr/bin/env python3
"""Generate diagrams for both AWS and Azure examples."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cloud_diff_mcp.visualizer import visualize_terraform_plan
from cloud_diff_mcp.visualizer_hierarchical import visualize_terraform_plan_hierarchical


def generate_example_diagrams():
    """Generate diagrams for all example plans."""
    examples_dir = Path(__file__).parent / "examples"
    
    examples = [
        ("sample-plan.json", "AWS Example", False),
        ("azure-plan.json", "Azure Example", False),
        ("complex-aws-plan.json", "Complex AWS Architecture", True),
    ]
    
    for example_file, description, use_hierarchical in examples:
        example_path = examples_dir / example_file
        
        if not example_path.exists():
            print(f"⚠️  Skipping {description}: file not found")
            continue
        
        print(f"\n{'=' * 80}")
        print(f"🎨 Generating diagram for {description}")
        print(f"{'=' * 80}\n")
        
        with open(example_path, "r") as f:
            plan_data = json.load(f)
        
        try:
            if use_hierarchical:
                # Use hierarchical layout for complex architectures
                output_path, summary = visualize_terraform_plan_hierarchical(plan_data)
            else:
                # Use standard visualization
                # Modify the visualizer temporarily for custom output
                from diagrams import Cluster, Diagram
                from cloud_diff_mcp.visualizer import (
                    get_icon_class,
                    get_primary_action,
                )
                
                resource_changes = plan_data.get("resource_changes", [])
                
                # Count actions
                action_counts = {
                    "create": 0,
                    "delete": 0,
                    "update": 0,
                    "replace": 0,
                }
                
                resources_by_action = {
                    "create": [],
                    "delete": [],
                    "update": [],
                    "replace": [],
                }
                
                for resource in resource_changes:
                    action = get_primary_action(resource["change"]["actions"])
                    if action != "no-op":
                        resources_by_action[action].append(resource)
                        action_counts[action] += 1
                
                # Create custom output name
                output_name = example_file.replace(".json", "_diagram")
                output_dir = Path.cwd() / "examples" / "diagrams"
                output_dir.mkdir(exist_ok=True, parents=True)
                output_file = output_dir / output_name
                
                graph_attr = {
                    "fontsize": "14",
                    "bgcolor": "white",
                    "pad": "0.5",
                }
                
                with Diagram(
                    f"Terraform Plan - {description}",
                    filename=str(output_file),
                    show=False,
                    direction="TB",
                    graph_attr=graph_attr,
                    outformat="png",
                ):
                    for action in ["create", "delete", "update", "replace"]:
                        resources = resources_by_action[action]
                        if not resources:
                            continue
                        
                        action_label = {
                            "create": "🟢 Creating",
                            "delete": "🔴 Deleting",
                            "update": "🟠 Updating",
                            "replace": "🟣 Replacing",
                        }[action]
                        
                        with Cluster(action_label):
                            for resource in resources:
                                resource_type = resource["type"]
                                resource_name = resource["name"]
                                icon_class = get_icon_class(resource_type)
                                label = f"{resource_name}\n({resource_type})"
                                icon_class(label)
                
                output_path = f"{output_file}.png"
                
                # Generate summary
                summary_lines = []
                summary_lines.append(f"- ✨ Create: {action_counts['create']} resources")
                summary_lines.append(f"- 📝 Update: {action_counts['update']} resources")
                summary_lines.append(f"- 🗑️ Delete: {action_counts['delete']} resources")
                summary_lines.append(f"- 🔄 Replace: {action_counts['replace']} resources")
                summary_lines.append(f"- **Total**: {sum(action_counts.values())} changes")
                summary = "\n".join(summary_lines)
            
            print("✅ Diagram generated successfully!")
            print(f"📁 Output: {output_path}")
            print("\n📊 Summary:")
            for line in summary.split('\n'):
                print(f"   {line}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    generate_example_diagrams()
    print(f"\n{'=' * 80}")
    print("✅ All example diagrams generated!")
    print(f"{'=' * 80}\n")
