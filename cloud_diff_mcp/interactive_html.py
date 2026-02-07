"""
Interactive HTML generator for Terraform plan visualizations.
Creates an HTML page with clickable resource icons showing change details.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

from cloud_diff_mcp.svg_embedder import embed_icons_in_svg


def generate_interactive_html(
    plan_data: Dict[str, Any],
    svg_path: str,
    output_path: str
) -> str:
    """
    Generate an interactive HTML page with the SVG diagram and clickable resources.
    
    Args:
        plan_data: Parsed Terraform plan JSON
        svg_path: Path to the generated SVG file
        output_path: Path where HTML file should be saved
    
    Returns:
        Path to the generated HTML file
    """
    # First, embed the icons in the SVG as base64 data URIs
    print("   🖼️  Embedding cloud provider icons in SVG...")
    embed_icons_in_svg(svg_path)
    
    resource_changes = plan_data.get("resource_changes", [])
    
    # Build resource lookup
    resources_by_address = {}
    for resource in resource_changes:
        address = resource["address"]
        change = resource["change"]
        actions = change.get("actions", [])
        
        # Determine action
        if "create" in actions and "delete" in actions:
            action = "replace"
        elif "delete" in actions:
            action = "delete"
        elif "create" in actions:
            action = "create"
        elif "update" in actions:
            action = "update"
        else:
            action = "no-op"
        
        # Get changes
        before = change.get("before", {})
        after = change.get("after", {})
        
        resources_by_address[address] = {
            "type": resource["type"],
            "name": resource["name"],
            "action": action,
            "before": before,
            "after": after,
            "actions": actions,
        }
    
    # Read SVG content
    with open(svg_path, 'r') as f:
        svg_content = f.read()
    
    # Generate resource details JSON for JavaScript
    resources_json = json.dumps(resources_by_address, indent=2, default=str)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terraform Plan - Interactive Visualization</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
        }}
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        
        .header p {{
            opacity: 0.9;
            font-size: 16px;
        }}
        
        .content {{
            display: grid;
            grid-template-columns: 1fr 400px;
            gap: 0;
        }}
        
        .diagram-container {{
            padding: 30px;
            overflow: auto;
            border-right: 1px solid #e0e0e0;
        }}
        
        .diagram-container svg {{
            max-width: 100%;
            height: auto;
            cursor: pointer;
        }}
        
        .sidebar {{
            background: #fafafa;
            padding: 30px;
            overflow-y: auto;
            max-height: calc(100vh - 200px);
        }}
        
        .sidebar h2 {{
            font-size: 20px;
            margin-bottom: 20px;
            color: #333;
        }}
        
        .resource-details {{
            display: none;
        }}
        
        .resource-details.active {{
            display: block;
        }}
        
        .resource-card {{
            background: white;
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }}
        
        .resource-card.create {{
            border-left-color: #2E7D32;
        }}
        
        .resource-card.delete {{
            border-left-color: #C62828;
        }}
        
        .resource-card.update {{
            border-left-color: #F57F17;
        }}
        
        .resource-card.replace {{
            border-left-color: #6A1B9A;
        }}
        
        .resource-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }}
        
        .resource-type {{
            font-size: 14px;
            color: #666;
            margin-bottom: 15px;
            font-family: 'Courier New', monospace;
        }}
        
        .action-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 15px;
        }}
        
        .action-badge.create {{
            background: #C8E6C9;
            color: #2E7D32;
        }}
        
        .action-badge.delete {{
            background: #FFCDD2;
            color: #C62828;
        }}
        
        .action-badge.update {{
            background: #FFF9C4;
            color: #F57F17;
        }}
        
        .action-badge.replace {{
            background: #E1BEE7;
            color: #6A1B9A;
        }}
        
        .changes-section {{
            margin-top: 15px;
        }}
        
        .changes-section h3 {{
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 10px;
            color: #555;
        }}
        
        .change-item {{
            background: #f5f5f5;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 8px;
            font-size: 13px;
        }}
        
        .change-key {{
            font-weight: 600;
            color: #333;
            margin-bottom: 4px;
        }}
        
        .change-value {{
            font-family: 'Courier New', monospace;
            color: #666;
            word-break: break-all;
        }}
        
        .change-value.old {{
            color: #C62828;
            text-decoration: line-through;
        }}
        
        .change-value.new {{
            color: #2E7D32;
        }}
        
        .placeholder {{
            text-align: center;
            padding: 40px 20px;
            color: #999;
        }}
        
        .placeholder-icon {{
            font-size: 48px;
            margin-bottom: 15px;
        }}
        
        .legend {{
            background: white;
            border-radius: 6px;
            padding: 15px;
            margin-top: 20px;
        }}
        
        .legend h3 {{
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 10px;
            color: #333;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            font-size: 13px;
        }}
        
        .legend-icon {{
            width: 20px;
            height: 20px;
            border-radius: 3px;
            margin-right: 10px;
        }}
        
        .legend-icon.create {{
            background: #C8E6C9;
        }}
        
        .legend-icon.delete {{
            background: #FFCDD2;
        }}
        
        .legend-icon.update {{
            background: #FFF9C4;
        }}
        
        .legend-icon.replace {{
            background: #E1BEE7;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏗️ Terraform Plan Visualization</h1>
            <p>Click on any resource in the diagram to view its configuration and changes</p>
        </div>
        
        <div class="content">
            <div class="diagram-container">
                {svg_content}
            </div>
            
            <div class="sidebar">
                <div class="resource-details" id="details-view">
                    <div class="placeholder">
                        <div class="placeholder-icon">👆</div>
                        <p>Click on a resource in the diagram<br>to view its details</p>
                    </div>
                </div>
                
                <div class="legend">
                    <h3>Legend</h3>
                    <div class="legend-item">
                        <div class="legend-icon create"></div>
                        <span>✨ Creating new resource</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-icon update"></div>
                        <span>📝 Updating existing resource</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-icon delete"></div>
                        <span>🗑️ Deleting resource</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-icon replace"></div>
                        <span>🔄 Replacing resource</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Resource data
        const resources = {resources_json};
        
        // Find resource by name in the address
        function findResourceByName(name) {{
            for (const [address, resource] of Object.entries(resources)) {{
                if (resource.name === name || address.includes(name)) {{
                    return {{ address, ...resource }};
                }}
            }}
            return null;
        }}
        
        // Display resource details
        function showResourceDetails(resource) {{
            if (!resource) return;
            
            const detailsView = document.getElementById('details-view');
            
            // Build changes HTML
            let changesHTML = '';
            
            if (resource.action === 'create') {{
                changesHTML = '<div class="changes-section"><h3>New Configuration:</h3>';
                if (resource.after && typeof resource.after === 'object') {{
                    for (const [key, value] of Object.entries(resource.after)) {{
                        if (key !== 'tags' && value !== null) {{
                            changesHTML += `
                                <div class="change-item">
                                    <div class="change-key">${{key}}</div>
                                    <div class="change-value new">${{JSON.stringify(value, null, 2)}}</div>
                                </div>
                            `;
                        }}
                    }}
                }}
                changesHTML += '</div>';
            }} else if (resource.action === 'delete') {{
                changesHTML = '<div class="changes-section"><h3>Resource will be destroyed</h3></div>';
            }} else if (resource.action === 'update' || resource.action === 'replace') {{
                changesHTML = '<div class="changes-section"><h3>Changes:</h3>';
                
                const before = resource.before || {{}};
                const after = resource.after || {{}};
                const allKeys = new Set([...Object.keys(before), ...Object.keys(after)]);
                
                for (const key of allKeys) {{
                    const beforeVal = before[key];
                    const afterVal = after[key];
                    
                    if (JSON.stringify(beforeVal) !== JSON.stringify(afterVal)) {{
                        changesHTML += `
                            <div class="change-item">
                                <div class="change-key">${{key}}</div>
                                <div class="change-value old">- ${{JSON.stringify(beforeVal, null, 2)}}</div>
                                <div class="change-value new">+ ${{JSON.stringify(afterVal, null, 2)}}</div>
                            </div>
                        `;
                    }}
                }}
                changesHTML += '</div>';
            }}
            
            // Action emoji
            const actionEmoji = {{
                create: '✨',
                delete: '🗑️',
                update: '📝',
                replace: '🔄'
            }}[resource.action] || '';
            
            // Action name
            const actionName = {{
                create: 'Creating',
                delete: 'Deleting',
                update: 'Updating',
                replace: 'Replacing'
            }}[resource.action] || resource.action;
            
            detailsView.innerHTML = `
                <div class="resource-card ${{resource.action}}">
                    <div class="resource-title">${{actionEmoji}} ${{resource.name}}</div>
                    <div class="resource-type">${{resource.type}}</div>
                    <span class="action-badge ${{resource.action}}">${{actionName.toUpperCase()}}</span>
                    ${{changesHTML}}
                </div>
            `;
            
            detailsView.classList.add('active');
        }}
        
        // Add click handlers to SVG text elements
        document.addEventListener('DOMContentLoaded', () => {{
            const svg = document.querySelector('svg');
            if (!svg) return;
            
            // Find all text elements in the SVG
            const textElements = svg.querySelectorAll('text');
            
            textElements.forEach(text => {{
                const content = text.textContent.trim();
                
                // Remove emoji and extract resource name
                const resourceName = content.replace(/[✨🗑️📝🔄]/g, '').trim();
                
                // Try to find matching resource
                const resource = findResourceByName(resourceName);
                
                if (resource) {{
                    text.style.cursor = 'pointer';
                    text.style.fill = '#667eea';
                    
                    text.addEventListener('click', (e) => {{
                        e.stopPropagation();
                        showResourceDetails(resource);
                    }});
                    
                    text.addEventListener('mouseenter', () => {{
                        text.style.fill = '#764ba2';
                    }});
                    
                    text.addEventListener('mouseleave', () => {{
                        text.style.fill = '#667eea';
                    }});
                }}
            }});
        }});
    </script>
</body>
</html>
"""
    
    # Write HTML file
    with open(output_path, 'w') as f:
        f.write(html_content)
    
    return output_path
