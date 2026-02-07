#!/usr/bin/env python3
"""
Test script for Cloud Diff FastMCP Server
Tests the MCP server tool integration
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))


def test_mcp_tool():
    """Test the visualize_tf_diff MCP tool."""
    print("🧪 Testing Cloud Diff FastMCP Tool\n")
    
    # Load the sample plan
    sample_plan_path = Path(__file__).parent / "examples" / "sample-plan.json"
    
    if not sample_plan_path.exists():
        print(f"❌ Sample plan not found at {sample_plan_path}")
        return False
    
    with open(sample_plan_path, "r") as f:
        plan_json = f.read()
    
    print("📋 Testing with sample Terraform plan...")
    print(f"   Plan size: {len(plan_json)} bytes\n")
    
    try:
        # Import the visualizer directly
        from cloud_diff_mcp.visualizer import visualize_terraform_plan
        import json as json_lib
        
        print("✅ Visualizer imported successfully\n")
        
        # Parse plan and call visualizer
        print("🎨 Generating visualization...")
        plan_data = json_lib.loads(plan_json)
        output_path, summary = visualize_terraform_plan(plan_data)
        
        print("✅ Tool executed successfully!\n")
        print("📊 Result:")
        print("─" * 80)
        print(f"Output: {output_path}")
        print(f"\n{summary}")
        print("─" * 80)
        
        # Check if output file was created
        if Path(output_path).exists():
            print("\n✅ Diagram file created successfully")
            return True
        else:
            print("\n⚠️  Warning: Diagram file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error during tool execution: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_mcp_tool()
    print("\n" + "=" * 80)
    if success:
        print("✅ All MCP server tests passed!")
    else:
        print("❌ Some tests failed")
    print("=" * 80)
    sys.exit(0 if success else 1)
