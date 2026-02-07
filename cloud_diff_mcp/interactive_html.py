"""
Interactive HTML generator for Terraform plan visualizations.
Orchestrates the full pipeline: SVG generation → icon embedding → HTML wrapping.
"""

import json
from typing import Any, Dict

from cloud_diff_mcp.visualizer_hierarchical import generate_svg
from cloud_diff_mcp.svg_embedder import embed_icons_in_svg_content


def generate_interactive_html(plan_data: Dict[str, Any]) -> str:
    """
    Generate a self-contained interactive HTML visualization from a Terraform plan.

    Orchestrates the full pipeline:
    1. Generate SVG diagram via the Diagrams library
    2. Embed cloud provider icons as base64 data URIs
    3. Wrap in interactive HTML with clickable resources

    Args:
        plan_data: Parsed Terraform plan JSON

    Returns:
        Complete HTML string
    """
    # Step 1: Generate SVG diagram
    svg_content = generate_svg(plan_data)

    # Step 2: Embed icons as base64 data URIs
    svg_content = embed_icons_in_svg_content(svg_content)

    # Step 3: Build resource lookup for the interactive sidebar
    resource_changes = plan_data.get("resource_changes", [])
    resources_by_address = {}

    for resource in resource_changes:
        address = resource["address"]
        change = resource["change"]
        actions = change.get("actions", [])

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

        resources_by_address[address] = {
            "type": resource["type"],
            "name": resource["name"],
            "action": action,
            "before": change.get("before", {}),
            "after": change.get("after", {}),
            "actions": actions,
        }

    resources_json = json.dumps(resources_by_address, indent=2, default=str)

    # Step 4: Wrap in interactive HTML
    return _build_html(svg_content, resources_json)


def _build_html(svg_content: str, resources_json: str) -> str:
    """Build the interactive HTML page with responsive layout, zoom/pan, and dark theme."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terraform Plan - Interactive Visualization</title>
    <style>
        *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ height: 100%; overflow: hidden; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #1a1a2e; color: #e0e0e0;
            display: flex; flex-direction: column;
        }}

        /* ---- Header ---- */
        .header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white; padding: 12px 20px;
            display: flex; align-items: center; gap: 16px;
            border-bottom: 1px solid #333; flex-shrink: 0;
        }}
        .header h1 {{ font-size: 18px; font-weight: 700; }}
        .header p {{ opacity: 0.7; font-size: 12px; }}
        .summary-badges {{ margin-left: auto; display: flex; gap: 10px; }}
        .summary-badges .badge {{
            font-size: 11px; font-weight: 600;
            padding: 3px 10px; border-radius: 10px;
        }}
        .badge.create {{ background: #1b5e20; color: #a5d6a7; }}
        .badge.update {{ background: #e65100; color: #ffcc80; }}
        .badge.delete {{ background: #b71c1c; color: #ef9a9a; }}
        .badge.replace {{ background: #4a148c; color: #ce93d8; }}

        /* ---- Main layout ---- */
        .content {{ flex: 1; display: flex; overflow: hidden; min-height: 0; }}

        /* ---- Diagram area ---- */
        .diagram-container {{
            flex: 1; min-width: 0; overflow: hidden; position: relative;
            background: #111 radial-gradient(circle at 1px 1px, rgba(255,255,255,.03) 1px, transparent 0);
            background-size: 20px 20px;
        }}
        .diagram-viewport {{
            width: 100%; height: 100%; overflow: hidden;
            cursor: grab; position: relative;
        }}
        .diagram-viewport:active {{ cursor: grabbing; }}
        .diagram-viewport svg {{ display: block; transform-origin: 0 0; }}

        /* ---- Zoom controls ---- */
        .zoom-controls {{
            position: absolute; bottom: 16px; right: 16px;
            display: flex; flex-direction: column; gap: 4px; z-index: 10;
        }}
        .zoom-btn {{
            width: 36px; height: 36px; border: 1px solid #444; border-radius: 6px;
            background: rgba(30,30,40,0.9); color: #ccc; font-size: 18px;
            cursor: pointer; display: flex; align-items: center; justify-content: center;
            transition: all 0.15s;
        }}
        .zoom-btn:hover {{
            background: rgba(60,60,80,0.95); color: #fff; border-color: #667eea;
        }}
        .zoom-level {{ text-align: center; font-size: 10px; color: #888; padding: 2px 0; }}

        /* ---- Sidebar ---- */
        .sidebar {{
            width: 320px; flex-shrink: 0; background: #161616;
            border-left: 1px solid #2a2a2a; padding: 16px;
            overflow-y: auto; display: flex; flex-direction: column;
        }}
        .placeholder {{ text-align: center; padding: 40px 10px; color: #444; }}
        .placeholder-icon {{ font-size: 36px; margin-bottom: 12px; opacity: 0.4; }}
        .placeholder p {{ font-size: 12px; }}

        /* ---- Resource detail card ---- */
        .resource-details {{ display: none; }}
        .resource-details.active {{ display: block; }}
        .resource-card {{
            background: #1e1e1e; border-radius: 8px; padding: 16px;
            margin-bottom: 16px; border-left: 3px solid #667eea;
        }}
        .resource-card.create {{ border-left-color: #4caf50; }}
        .resource-card.delete {{ border-left-color: #f44336; }}
        .resource-card.update {{ border-left-color: #ff9800; }}
        .resource-card.replace {{ border-left-color: #9c27b0; }}
        .resource-title {{ font-size: 16px; font-weight: 600; margin-bottom: 4px; color: #eee; }}
        .resource-type {{ font-size: 11px; color: #666; margin-bottom: 12px; font-family: 'Courier New', monospace; }}
        .action-badge {{
            display: inline-block; padding: 3px 10px; border-radius: 10px;
            font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 12px;
        }}
        .action-badge.create {{ background: #1b5e20; color: #a5d6a7; }}
        .action-badge.delete {{ background: #b71c1c; color: #ef9a9a; }}
        .action-badge.update {{ background: #e65100; color: #ffcc80; }}
        .action-badge.replace {{ background: #4a148c; color: #ce93d8; }}
        .changes-section {{ margin-top: 12px; }}
        .changes-section h3 {{
            font-size: 11px; font-weight: 700; color: #888;
            text-transform: uppercase; letter-spacing: 0.4px; margin-bottom: 8px;
        }}
        .change-item {{
            background: #151515; padding: 8px 10px; border-radius: 5px;
            margin-bottom: 6px; font-size: 12px;
        }}
        .change-key {{ font-weight: 600; color: #bbb; margin-bottom: 3px; }}
        .change-value {{ font-family: 'Courier New', monospace; font-size: 11px; word-break: break-all; }}
        .change-value.old {{ color: #ef5350; text-decoration: line-through; }}
        .change-value.new {{ color: #66bb6a; }}

        /* ---- Legend bar ---- */
        .legend {{
            display: flex; gap: 14px; padding: 8px 20px;
            background: #111; border-top: 1px solid #2a2a2a;
            font-size: 11px; flex-shrink: 0; color: #777;
        }}
        .legend-item {{ display: flex; align-items: center; gap: 5px; }}
        .legend-dot {{ width: 8px; height: 8px; border-radius: 50%; }}
        .legend-dot.create {{ background: #4caf50; }}
        .legend-dot.delete {{ background: #f44336; }}
        .legend-dot.update {{ background: #ff9800; }}
        .legend-dot.replace {{ background: #9c27b0; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>&#x1f3d7;&#xfe0f; Terraform Plan Visualization</h1>
            <p>Click any resource to view details &bull; Scroll to zoom &bull; Drag to pan</p>
        </div>
        <div class="summary-badges" id="summary"></div>
    </div>

    <div class="content">
        <div class="diagram-container">
            <div class="diagram-viewport" id="viewport">
                {svg_content}
            </div>
            <div class="zoom-controls">
                <button class="zoom-btn" onclick="zoomIn()" title="Zoom in">+</button>
                <div class="zoom-level" id="zoom-level">100%</div>
                <button class="zoom-btn" onclick="zoomOut()" title="Zoom out">&minus;</button>
                <button class="zoom-btn" onclick="zoomFit()" title="Fit to view" style="font-size:13px">&#x229e;</button>
            </div>
        </div>

        <div class="sidebar">
            <div class="resource-details" id="details-view">
                <div class="placeholder">
                    <div class="placeholder-icon">&#x1f446;</div>
                    <p>Click on a resource in the diagram<br>to view its details</p>
                </div>
            </div>
        </div>
    </div>

    <div class="legend">
        <div class="legend-item"><div class="legend-dot create"></div>Create</div>
        <div class="legend-item"><div class="legend-dot update"></div>Update</div>
        <div class="legend-item"><div class="legend-dot delete"></div>Destroy</div>
        <div class="legend-item"><div class="legend-dot replace"></div>Replace</div>
        <div class="legend-item" style="margin-left:auto;opacity:0.5">&#x21e2; connections = dependencies</div>
    </div>

    <script>
        var resources = {resources_json};

        /* ====== SVG responsive fix: strip fixed pt dimensions, use viewBox ====== */
        (function fixSvgSizing() {{
            var svg = document.querySelector('#viewport svg');
            if (!svg) return;
            var vb = svg.getAttribute('viewBox');
            if (!vb) {{
                var w = parseFloat(svg.getAttribute('width')) || 800;
                var h = parseFloat(svg.getAttribute('height')) || 600;
                svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
            }}
            svg.removeAttribute('width');
            svg.removeAttribute('height');
            svg.style.width = '100%';
            svg.style.height = '100%';
        }})();

        /* ====== Zoom & Pan ====== */
        var scale = 1, panX = 0, panY = 0;
        var isPanning = false, startX = 0, startY = 0;
        var viewport = document.getElementById('viewport');
        var svgEl = viewport ? viewport.querySelector('svg') : null;

        function applyTransform() {{
            if (!svgEl) return;
            svgEl.style.transform = 'translate(' + panX + 'px,' + panY + 'px) scale(' + scale + ')';
            var el = document.getElementById('zoom-level');
            if (el) el.textContent = Math.round(scale * 100) + '%';
        }}

        function zoomIn() {{ scale = Math.min(scale * 1.25, 5); applyTransform(); }}
        function zoomOut() {{ scale = Math.max(scale / 1.25, 0.2); applyTransform(); }}

        function zoomFit() {{
            if (!svgEl) return;
            var vb = svgEl.getAttribute('viewBox');
            if (!vb) return;
            var parts = vb.split(/[\\s,]+/).map(Number);
            var svgW = parts[2], svgH = parts[3];
            var cRect = viewport.getBoundingClientRect();
            var scaleX = cRect.width / svgW;
            var scaleY = cRect.height / svgH;
            scale = Math.min(scaleX, scaleY) * 0.92;
            panX = (cRect.width - svgW * scale) / 2;
            panY = (cRect.height - svgH * scale) / 2;
            applyTransform();
        }}

        if (viewport) {{
            viewport.addEventListener('wheel', function(e) {{
                e.preventDefault();
                var rect = viewport.getBoundingClientRect();
                var mx = e.clientX - rect.left;
                var my = e.clientY - rect.top;
                var oldScale = scale;
                scale = e.deltaY < 0
                    ? Math.min(scale * 1.1, 5)
                    : Math.max(scale / 1.1, 0.2);
                panX = mx - (mx - panX) * (scale / oldScale);
                panY = my - (my - panY) * (scale / oldScale);
                applyTransform();
            }}, {{ passive: false }});

            viewport.addEventListener('mousedown', function(e) {{
                if (e.target.closest('.node')) return;
                isPanning = true;
                startX = e.clientX - panX;
                startY = e.clientY - panY;
            }});
        }}

        window.addEventListener('mousemove', function(e) {{
            if (!isPanning) return;
            panX = e.clientX - startX;
            panY = e.clientY - startY;
            applyTransform();
        }});
        window.addEventListener('mouseup', function() {{ isPanning = false; }});

        setTimeout(zoomFit, 100);
        window.addEventListener('resize', function() {{ setTimeout(zoomFit, 100); }});

        /* ====== Resource lookup ====== */
        function findResourceByName(name) {{
            for (var address in resources) {{
                var r = resources[address];
                if (r.name === name || address.indexOf(name) !== -1) {{
                    return {{ address: address, type: r.type, name: r.name,
                             action: r.action, before: r.before, after: r.after }};
                }}
            }}
            return null;
        }}

        /* ====== Summary badges ====== */
        (function() {{
            var counts = {{}};
            for (var addr in resources) {{ var a = resources[addr].action; counts[a] = (counts[a]||0)+1; }}
            var el = document.getElementById('summary');
            if (!el) return;
            var labels = [['create','create'],['update','update'],['delete','destroy'],['replace','replace']];
            labels.forEach(function(pair) {{
                if (counts[pair[0]]) {{
                    var span = document.createElement('span');
                    span.className = 'badge ' + pair[0];
                    span.textContent = counts[pair[0]] + ' ' + pair[1];
                    el.appendChild(span);
                }}
            }});
        }})();

        /* ====== Detail panel ====== */
        function esc(s) {{ var d = document.createElement('div'); d.textContent = String(s); return d.innerHTML; }}

        function showResourceDetails(resource) {{
            if (!resource) return;
            var dv = document.getElementById('details-view');
            var html = '';

            if (resource.action === 'create') {{
                html = '<div class="changes-section"><h3>New Configuration</h3>';
                if (resource.after && typeof resource.after === 'object') {{
                    Object.keys(resource.after).forEach(function(key) {{
                        var v = resource.after[key];
                        if (key !== 'tags' && v !== null)
                            html += '<div class="change-item"><div class="change-key">' + esc(key) + '</div>' +
                                    '<div class="change-value new">' + esc(JSON.stringify(v, null, 2)) + '</div></div>';
                    }});
                }}
                html += '</div>';
            }} else if (resource.action === 'delete') {{
                html = '<div class="changes-section"><h3>Resource will be destroyed</h3>';
                if (resource.before && typeof resource.before === 'object') {{
                    Object.keys(resource.before).forEach(function(key) {{
                        var v = resource.before[key];
                        if (v !== null)
                            html += '<div class="change-item"><div class="change-key">' + esc(key) + '</div>' +
                                    '<div class="change-value old">' + esc(JSON.stringify(v, null, 2)) + '</div></div>';
                    }});
                }}
                html += '</div>';
            }} else if (resource.action === 'update' || resource.action === 'replace') {{
                html = '<div class="changes-section"><h3>Changes</h3>';
                var before = resource.before || {{}};
                var after = resource.after || {{}};
                var allKeys = new Set([].concat(Object.keys(before), Object.keys(after)));
                allKeys.forEach(function(key) {{
                    var bv = JSON.stringify(before[key], null, 2);
                    var av = JSON.stringify(after[key], null, 2);
                    if (bv !== av)
                        html += '<div class="change-item"><div class="change-key">' + esc(key) + '</div>' +
                                '<div class="change-value old">&minus; ' + esc(bv) + '</div>' +
                                '<div class="change-value new">+ ' + esc(av) + '</div></div>';
                }});
                html += '</div>';
            }}

            var emojis = {{ create:'&#x2728;', delete:'&#x1f5d1;&#xfe0f;', update:'&#x1f4dd;', replace:'&#x1f504;' }};
            var names = {{ create:'Creating', delete:'Deleting', update:'Updating', replace:'Replacing' }};
            var emoji = emojis[resource.action] || '';
            var actionName = names[resource.action] || resource.action;

            dv.innerHTML = '<div class="resource-card ' + resource.action + '">' +
                '<div class="resource-title">' + emoji + ' ' + esc(resource.name) + '</div>' +
                '<div class="resource-type">' + esc(resource.type) + '</div>' +
                '<span class="action-badge ' + resource.action + '">' + actionName.toUpperCase() + '</span>' +
                html + '</div>';
            dv.classList.add('active');
        }}

        /* ====== Make SVG nodes clickable ====== */
        document.addEventListener('DOMContentLoaded', function() {{
            var svg = document.querySelector('#viewport svg');
            if (!svg) return;

            var nodeGroups = svg.querySelectorAll('.node');
            nodeGroups.forEach(function(group) {{
                var texts = group.querySelectorAll('text');
                var matched = null;
                texts.forEach(function(text) {{
                    var raw = text.textContent.trim().replace(/[\\u2728\\ud83d\\uddd1\\ufe0f\\ud83d\\udcdd\\ud83d\\udd04]/g, '').trim();
                    if (!matched) matched = findResourceByName(raw);
                }});

                if (matched) {{
                    group.style.cursor = 'pointer';
                    group.addEventListener('click', function(e) {{
                        e.stopPropagation();
                        svg.querySelectorAll('.node').forEach(function(n) {{ n.style.filter = ''; }});
                        group.style.filter = 'brightness(1.3) drop-shadow(0 0 8px rgba(102,126,234,.6))';
                        showResourceDetails(matched);
                    }});
                    group.addEventListener('mouseenter', function() {{
                        if (!group.style.filter || group.style.filter === '')
                            group.style.filter = 'brightness(1.15)';
                    }});
                    group.addEventListener('mouseleave', function() {{
                        if (group.style.filter === 'brightness(1.15)')
                            group.style.filter = '';
                    }});
                }}
            }});

            // Fallback: text-only targets
            if (nodeGroups.length === 0) {{
                svg.querySelectorAll('text').forEach(function(text) {{
                    var raw = text.textContent.trim().replace(/[\\u2728\\ud83d\\uddd1\\ufe0f\\ud83d\\udcdd\\ud83d\\udd04]/g, '').trim();
                    var res = findResourceByName(raw);
                    if (res) {{
                        text.style.cursor = 'pointer';
                        text.addEventListener('click', function(e) {{
                            e.stopPropagation();
                            showResourceDetails(res);
                        }});
                    }}
                }});
            }}
        }});
    </script>
</body>
</html>
"""
