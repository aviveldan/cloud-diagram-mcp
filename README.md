# Cloud Diff MCP

An MCP server that visualizes Terraform plan changes as interactive cloud architecture diagrams, delivered as [MCP Apps](http://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/) — rich, embedded UI directly in your AI assistant.

## Features

- 🎨 **Interactive MCP App**: Returns a self-contained HTML visualization as an embedded UI — no file paths, no browser tabs
- 🔒 **Fully Offline**: No cloud credentials or network access required
- ☁️ **Multi-Cloud Icons**: Official AWS, Azure, and GCP resource icons
- 🏗️ **Hierarchical Layout**: Resources organized by architectural layers (DNS, Network, Compute, Data, Storage, Security)
- 🔗 **Dependency Arrows**: Visual connections showing resource relationships
- 🖱️ **Clickable Resources**: Click any resource to see its configuration and before/after changes
- 🎯 **Color-Coded Actions**:
  - 🟢 Green: Creating
  - 🔴 Red: Deleting
  - 🟠 Orange: Updating
  - 🟣 Purple: Replacing

## Screenshots

### Interactive Visualization (MCP App)
![Interactive HTML - Initial State](https://github.com/user-attachments/assets/6d843f8d-59fb-4346-84de-50245a393671)

### Clicking a Resource Shows Details
![Interactive HTML - Create Action](https://github.com/user-attachments/assets/00595897-d9ee-4274-acbd-5ddd5377832d)

### Before/After Change Comparison
![Interactive HTML - Update Action](https://github.com/user-attachments/assets/cf921edb-c8e6-4850-8908-3c5d6db1a3d6)

## Prerequisites

- Python 3.10+
- [Graphviz](https://graphviz.org/download/) (for diagram rendering)

```bash
# Ubuntu/Debian
sudo apt-get install graphviz

# macOS
brew install graphviz

# Windows
winget install --id Graphviz.Graphviz
# Ensure Graphviz bin directory is on your PATH
```

## Installation

```bash
git clone https://github.com/aviveldan/cloud-diff-mcp.git
cd cloud-diff-mcp
pip install -r requirements.txt
```

## Usage

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "cloud-diff": {
      "command": "python3",
      "args": ["-m", "cloud_diff_mcp.server"],
      "cwd": "/path/to/cloud-diff-mcp"
    }
  }
}
```

Then ask your AI assistant to visualize a Terraform plan:

```
Please visualize this Terraform plan:
<paste output of `terraform show -json tfplan`>
```

The tool returns an interactive MCP App directly in the conversation — no files to open.

## Tool: `visualize_tf_diff`

**Input:** Terraform plan JSON string (from `terraform show -json tfplan`)

**Output:** An MCP App with an interactive architecture diagram featuring:
- Clickable resources with configuration details
- Before/after comparisons for updates
- Color-coded change indicators
- Embedded cloud provider icons (base64, no external dependencies)

## Project Structure

```
cloud-diff-mcp/
├── cloud_diff_mcp/
│   ├── __init__.py
│   ├── server.py                  # FastMCP server — returns HTML as MCP App
│   ├── interactive_html.py        # Orchestrates pipeline, builds interactive HTML
│   ├── visualizer_hierarchical.py # Generates SVG via Diagrams library
│   └── svg_embedder.py            # Embeds icons as base64 data URIs
├── examples/                      # Sample Terraform plans
├── requirements.txt
├── pyproject.toml
└── README.md
```

## How It Works

1. **SVG Generation**: The Diagrams library + Graphviz renders a hierarchical architecture diagram as SVG
2. **Icon Embedding**: External PNG icon references are converted to base64 data URIs for portability
3. **HTML Wrapping**: The SVG is wrapped in an interactive HTML page with JavaScript for click-to-inspect functionality
4. **MCP App Delivery**: The complete HTML is returned as an MCP App UI resource, rendered inline by the client

## Supported Resources

**AWS**: EC2, VPC, RDS, S3, ELB, Route53, CloudFront, IAM, ElastiCache, NAT Gateway, and more
**Azure**: Virtual Machines, Virtual Networks, SQL Database, Storage Accounts, Managed Identities, and more
**GCP**: Compute Engine, VPC, Cloud SQL, Cloud Storage, GKE, App Engine, and more

Unknown resource types default to a generic compute icon.

## Examples

The `examples/` directory contains sample Terraform plans:
- `sample-plan.json` — Simple AWS infrastructure (6 resources)
- `azure-plan.json` — Azure resources (7 resources)
- `complex-aws-plan.json` — Multi-tier production AWS architecture (15 resources)

## License

MIT