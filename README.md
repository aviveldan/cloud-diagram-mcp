# Cloud Diagram MCP

A Model Context Protocol (MCP) server that visualizes cloud infrastructure and Terraform plan changes using high-fidelity architecture diagrams with official cloud provider icons.

## Features

- **Offline Visual Diffing** — Generate cloud architecture diagrams from Terraform plan JSON without cloud credentials
- **Multi-Cloud Support** — Official icons for AWS, Azure, and GCP resources
- **Hierarchical Architecture Views** — Complex infrastructures organized by architectural layers
- **Dependency Visualization** — Visual arrows showing relationships between resources
- **Interactive HTML Output** — Clickable resources with detailed configuration views
- **Color-Coded Change Tracking**:
  - Green: New resources (create)
  - Red: Deleted resources (delete)
  - Orange: Modified resources (update)
  - Purple: Replaced resources (create + delete)

## Screenshots

### Simple AWS Infrastructure Changes
![AWS Simple Example](https://github.com/user-attachments/assets/b338b884-1ce6-4c86-b160-eab7ce3f5152)

### Simple Azure Infrastructure Changes
![Azure Simple Example](https://github.com/user-attachments/assets/a421dc13-4893-40fa-87c3-217154fd7894)

### Complex Multi-Tier AWS Architecture with Connections
![Complex AWS with Connections](https://github.com/user-attachments/assets/e63ee02d-7a6f-49d3-854c-8d6b05bd88e0)

This example demonstrates a production-grade multi-tier architecture with 15 resources organized across 7 architectural layers: Internet (CDN, DNS), Network Infrastructure (VPC, Subnets, NAT Gateways), Load Balancing, Compute (Multi-AZ), Data Layer (RDS, ElastiCache), Storage (S3), and Security (IAM, Security Groups). The diagram includes dependency arrows showing resource relationships, hierarchical layer organization, and official AWS service icons.

## Interactive HTML Visualization

The tool generates an interactive HTML page for exploring infrastructure changes. Cloud provider icons are embedded as base64 data URIs, ensuring correct display in any browser without external dependencies.

### Initial View - Interactive Dashboard
![Interactive HTML - Initial State](https://github.com/user-attachments/assets/6d843f8d-59fb-4346-84de-50245a393671)

The interactive dashboard features official AWS service icons (Route53, CloudFront, VPC, Subnets, NAT Gateways, ELB, EC2, RDS, ElastiCache, S3, IAM), dependency arrows showing resource relationships, hierarchical layer organization, and a clean UI with gradient header and legend.

### Clicking a Resource Being Created
![Interactive HTML - Create Action](https://github.com/user-attachments/assets/00595897-d9ee-4274-acbd-5ddd5377832d)

Clicking on a resource displays detailed information in the sidebar. This example shows an EC2 instance being created with a green border card, "CREATING" badge, and full configuration details including AMI, instance type, and subnet information.

### Clicking a Resource Being Updated
![Interactive HTML - Update Action](https://github.com/user-attachments/assets/cf921edb-c8e6-4850-8908-3c5d6db1a3d6)

For updated resources, the sidebar displays a before/after comparison with color-coded highlighting. This RDS database example shows engine version upgrade from 13.7 to 14.5 and multi-AZ enablement, with red strikethrough for old values and green for new values.

### Clicking a Resource Being Replaced
![Interactive HTML - Replace Action](https://github.com/user-attachments/assets/0816edbf-6b3a-4048-86b8-3f3caaecd53d)

Replaced resources show with a purple border and "REPLACING" badge. This Route53 DNS record example demonstrates DNS routing evolution from ALB to CloudFront CDN.

### Key Interactive Features

- Official cloud provider icons for AWS, Azure, and GCP
- Base64 embedded icons in SVG (no external file dependencies)
- Click any resource to view full configuration and changes
- Before/after comparison with color-coded highlighting
- Professional UI with gradient header and clean layout
- Fully offline-capable, self-contained HTML file
- Responsive design for different screen sizes

## Prerequisites

- Python 3.10 or higher
- Graphviz (required for diagram rendering)
- Node.js 18 or higher (for building the React UI)

### Installing Graphviz

**Ubuntu/Debian:**
```bash
sudo apt-get install graphviz
```

**macOS:**
```bash
brew install graphviz
```

**Windows:**
```powershell
winget install --id Graphviz.Graphviz
```

> **Note:** On Windows, ensure the Graphviz `bin` directory (typically `C:\Program Files\Graphviz\bin`) is added to your system PATH. You may need to restart your terminal after installation.

## Installation

```bash
# Clone the repository
git clone https://github.com/aviveldan/cloud-diagram-mcp.git
cd cloud-diagram-mcp

# Install Python dependencies
pip install -r requirements.txt

# Build the React UI (required once, for interactive visualizations)
cd ui && npm install && npm run build && cd ..
```

## Usage

### MCP Server Integration

Configure your MCP client (such as Claude Desktop) to use the server:

```json
{
  "mcpServers": {
    "cloud-diagram": {
      "command": "python3",
      "args": ["-m", "cloud_diagram_mcp.server"],
      "cwd": "/path/to/cloud-diagram-mcp"
    }
  }
}
```

### Command Line Usage

```bash
# Run visualization tests
python3 test_visualization.py

# Run MCP server tests
python3 test_mcp_server.py

# Generate interactive visualization with dependency connections
python3 generate_interactive.py
```

**Output Files:**
- PNG with dependency arrows and official cloud icons (~265KB)
- SVG with embedded icons (self-contained, scalable)
- Interactive HTML page with clickable resources

**View in Browser:**
```bash
open terraform-diffs/terraform_plan_interactive.html
```

## Tools

### visualize_tf_diff

Visualizes Terraform plan changes as cloud architecture diagrams.

**Input:**
```json
{
  "plan": "<terraform-plan-json-string>"
}
```

**Generating Terraform Plan JSON:**
```bash
terraform plan -out=tfplan
terraform show -json tfplan > plan.json
```

**Output:**
- High-quality PNG/SVG diagram saved to `terraform-diffs/terraform_plan_diff.png`
- Summary of changes with counts by action type
- Visual grouping by action (create/delete/update/replace)

**Features:**
- Dependency connections via gray dashed arrows (enabled by default in hierarchical view)
- Interactive HTML with clickable resources (`generate_interactive.py`)
- SVG output with `format='svg'` for scalable vector graphics with embedded metadata

### Interactive Features

The interactive HTML visualization provides:

- Clickable resource icons for viewing detailed information
- Configuration viewer showing before/after values for updates
- Color-coded change highlighting (green for additions, red for deletions)
- Complete resource metadata including Terraform resource type and action
- Official AWS, Azure, and GCP icons embedded as base64 data URIs
- Self-contained HTML file with no external dependencies
- Browser-based viewing with no special tools required
- Compatible with MCP App and Playwright browser automation

### Supported Resource Types

The tool includes icon mappings for common cloud resources:

- **AWS**: EC2, VPC, RDS, S3, ELB, Lambda, IAM, Security Groups, ElastiCache, Route53, CloudFront, NAT Gateway, and more
- **Azure**: Virtual Machines, Virtual Networks, SQL Database, Storage Accounts, Managed Identities, and more
- **GCP**: Compute Engine, VPC, Cloud SQL, Cloud Storage, GKE, and more

Unknown resource types use a generic compute icon as fallback.

## Examples

The repository includes example Terraform plans demonstrating various scenarios:

1. **simple-aws-plan.json** — 6 resource changes showcasing basic AWS infrastructure
2. **azure-plan.json** — 7 resource changes demonstrating Azure resources
3. **complex-aws-plan.json** — 15 resource changes in a multi-tier production architecture including:
   - Multi-AZ deployment across 2 availability zones
   - Application Load Balancer (ALB)
   - Multi-AZ database with failover capability
   - Caching layer with ElastiCache
   - Content delivery with CloudFront CDN
   - DNS management with Route53

**Generate diagrams for all examples:**
```bash
python3 generate_examples.py
```

## Development

### Project Structure

```
cloud-diagram-mcp/
├── cloud_diagram_mcp/
│   ├── __init__.py
│   ├── server.py                     # FastMCP server (reads built UI from dist/)
│   ├── visualizer_hierarchical.py    # Hierarchical layout + SVG generation
│   ├── interactive_html.py           # Standalone interactive HTML generator
│   ├── svg_embedder.py               # Icon embedding utility
│   └── dist/
│       └── mcp-app.html              # Built React UI (generated by Vite)
├── ui/                                # React frontend source
│   ├── package.json                   # Dependencies: React, React Flow, ext-apps SDK
│   ├── vite.config.ts                 # Vite + singlefile plugin → builds to dist/
│   ├── tsconfig.json
│   ├── mcp-app.html                   # Entry HTML
│   └── src/
│       ├── main.tsx                    # React root + ext-apps SDK integration
│       ├── types.ts                    # TypeScript types for plan data
│       ├── components/
│       │   ├── App.tsx                 # Main app: routes between SVG/diagram modes
│       │   ├── Header.tsx              # Header bar with summary badges
│       │   ├── Legend.tsx              # Bottom legend bar
│       │   ├── DetailPanel.tsx         # Sidebar: resource details + diff view
│       │   ├── SvgViewer.tsx           # Server SVG viewer with zoom/pan
│       │   ├── DiagramView.tsx         # React Flow diagram (fallback mode)
│       │   └── ResourceNode.tsx        # Custom React Flow node
│       ├── icons/
│       │   ├── aws.tsx                 # AWS SVG icon components (~18 icons)
│       │   ├── azure.tsx               # Azure SVG icon components (~14 icons)
│       │   ├── gcp.tsx                 # GCP SVG icon components (~8 icons)
│       │   └── index.tsx               # Icon registry + categorization
│       └── styles/
│           └── global.css              # Dark theme styles
├── examples/
├── requirements.txt
├── pyproject.toml
└── README.md
```

### Building the React UI

The MCP App UI is built using React, TypeScript, and Vite. The build process produces a single self-contained HTML file at `cloud_diagram_mcp/dist/mcp-app.html`.

```bash
cd ui
npm install        # Install dependencies (first time only)
npm run build      # Build production bundle
```

During development, use `npm run dev` for hot-reload functionality.

### Running Tests

```bash
# Test visualization generation
python3 test_visualization.py

# Test MCP tool integration
python3 test_mcp_server.py
```

## Technical Details

### Architecture

- **FastMCP** — Python MCP server framework for tool registration
- **React + TypeScript** — Interactive UI with React Flow for diagram visualization
- **Vite + singlefile plugin** — Bundles the React app into a single HTML file
- **@modelcontextprotocol/ext-apps** — SDK for MCP App to host communication
- **@xyflow/react (React Flow)** — Node-based diagrams with zoom/pan/minimap capabilities
- **Diagrams** — Python library for generating cloud architecture SVGs using Graphviz backend

### Icon Embedding Solution

**Problem:** SVG diagrams generated by the Diagrams library reference external PNG files using `xlink:href`, which don't display correctly in browsers when opened directly.

**Solution:** The `svg_embedder.py` module addresses this by:
- Parsing SVG files to find all external image references
- Converting PNG file paths to base64-encoded data URIs
- Embedding 12+ unique cloud provider icons directly in the SVG
- Creating fully self-contained and portable HTML files
- Eliminating external file dependencies and broken image links

**Implementation:**
1. `cloud_diagram_mcp/server.py` — FastMCP server with `visualize_tf_diff` tool
2. `cloud_diagram_mcp/visualizer_hierarchical.py` — Hierarchical layout with dependency connections
3. `cloud_diagram_mcp/interactive_html.py` — Interactive HTML generator
4. `cloud_diagram_mcp/svg_embedder.py` — Icon embedding utility

### Security & Privacy

- **Offline Operation** — No cloud API calls or network requests required
- **Stateless Processing** — No persistent storage of Terraform plans
- **Credential-Free** — Does not require cloud provider credentials

## Legacy TypeScript Implementation

The original TypeScript implementation using Mermaid diagrams is preserved in the `src/` directory for reference. The Python implementation provides higher-quality diagrams with official cloud provider icons.

## License

MIT