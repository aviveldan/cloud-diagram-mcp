#!/usr/bin/env python3
"""
Test script for Cloud Diff MCP Server (Python implementation)
Tests the visualize_tf_diff tool with the sample Terraform plan
"""

import json
import sys
from pathlib import Path

# Add parent directory to path to import our module
sys.path.insert(0, str(Path(__file__).parent))

from cloud_diff_mcp.visualizer import visualize_terraform_plan


def test_visualization():
    """Test the Terraform plan visualization."""
    print("🧪 Testing Terraform Plan Visualization\n")
    
    # Load the sample plan
    sample_plan_path = Path(__file__).parent / "examples" / "sample-plan.json"
    
    if not sample_plan_path.exists():
        print(f"❌ Sample plan not found at {sample_plan_path}")
        return False
    
    with open(sample_plan_path, "r") as f:
        plan_data = json.load(f)
    
    print("📋 Loaded Terraform plan with resource changes:")
    for resource in plan_data.get("resource_changes", []):
        actions = resource["change"]["actions"]
        print(f"  - {resource['address']}: {actions}")
    print()
    
    try:
        # Generate the visualization
        print("🎨 Generating visualization...")
        output_path, summary = visualize_terraform_plan(plan_data)
        
        print("✅ Visualization generated successfully!\n")
        print("📊 Summary:")
        print(summary)
        print()
        print(f"📁 Output file: {output_path}")
        
        # Check if file exists
        if Path(output_path).exists():
            file_size = Path(output_path).stat().st_size
            print(f"✅ File created successfully ({file_size} bytes)")
            return True
        else:
            print(f"❌ Output file not found at {output_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error during visualization: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_visualization()
    sys.exit(0 if success else 1)
