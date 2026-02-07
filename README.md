# Cloud Diff MCP

A Model Context Protocol (MCP) server for analyzing Terraform plans and visualizing infrastructure changes with high-fidelity cloud architecture diagrams using the Python Diagrams library.

## Features

- 🎨 **Offline Visual Diffing**: Generate beautiful cloud architecture diagrams from Terraform plan JSON
- 🔒 **No Cloud Credentials Required**: Operates entirely offline, processing plan output locally
- ☁️ **Multi-Cloud Support**: Icons for AWS, Azure, and GCP resources
- 🏗️ **Hierarchical Architecture Views**: Complex infrastructures organized by architectural layers
- 🔗 **Dependency Connections**: Visual arrows showing relationships between resources
- 🖱️ **Interactive HTML**: Clickable resources with configuration details
- 🎯 **Visual State Representation**:
  - 🟢 **Green**: New resources (create)
  - 🔴 **Red**: Deleted resources (delete)
  - 🟠 **Orange**: Modified resources (update)
  - 🟣 **Purple**: Replaced resources (create + delete)

## Screenshots

### Simple AWS Infrastructure Changes
![AWS Simple Example](https://github.com/user-attachments/assets/b338b884-1ce6-4c86-b160-eab7ce3f5152)

### Simple Azure Infrastructure Changes
![Azure Simple Example](https://github.com/user-attachments/assets/a421dc13-4893-40fa-87c3-217154fd7894)

### Complex Multi-Tier AWS Architecture with Connections
![Complex AWS with Connections](https://github.com/user-attachments/assets/e63ee02d-7a6f-49d3-854c-8d6b05bd88e0)

**Features visible:**
- **Dependency Arrows**: Gray dashed arrows show relationships between resources
- **Hierarchical Layers**: Resources organized by function (Internet, Network, Compute, Data, Storage, Security)
- **Official Cloud Icons**: AWS service icons (Route53, CloudFront, VPC, ELB, EC2, RDS, ElastiCache, S3, IAM)

The complex example shows a production-grade multi-tier architecture with 15 resources organized across 7 layers: Internet (CDN, DNS), Network Infrastructure (VPC, Subnets, NAT Gateways), Load Balancing, Compute (Multi-AZ), Data Layer (RDS, ElastiCache), Storage (S3), and Security (IAM, Security Groups).

## Interactive HTML Visualization

The tool generates an interactive HTML page where users can explore infrastructure changes by clicking on resources. **Cloud provider icons are embedded as base64 data URIs** ensuring they display correctly in any browser without external dependencies.

### Initial View - Interactive Dashboard
![Interactive HTML - Initial State](https://github.com/user-attachments/assets/6d843f8d-59fb-4346-84de-50245a393671)

**Features:**
- **Official AWS Icons**: Route53 (purple), CloudFront (purple), VPC (blue), Subnets (network icons), NAT Gateways, ELB (orange), EC2 (orange), RDS (blue database), ElastiCache (database), S3 (green), IAM (red)
- **Dependency Arrows**: Gray lines showing resource relationships
- **Hierarchical Layers**: Clear organization by architectural tiers
- **Professional UI**: Gradient header, legend, clean layout
- **Placeholder**: Prompts user to click resources

### Clicking a Resource Being Created
![Interactive HTML - Create Action](https://github.com/user-attachments/assets/00595897-d9ee-4274-acbd-5ddd5377832d)

**Clicking web_az2 (EC2 instance):**
- **Green border card** appears in sidebar
- **CREATING badge** with green background
- **AWS EC2 icon** properly rendered in diagram
- **Full configuration** displayed:
  - AMI: `ami-0c55b159cbfafe1f0`
  - Instance type: `t3.small`
  - Subnet: `subnet-private-az2`

### Clicking a Resource Being Updated
![Interactive HTML - Update Action](https://github.com/user-attachments/assets/cf921edb-c8e6-4850-8908-3c5d6db1a3d6)

**Clicking primary (RDS database):**
- **Orange border card** appears in sidebar
- **UPDATING badge** with orange background
- **AWS RDS icon** properly rendered in diagram
- **Before/After comparison**:
  - `engine_version`: `"13.7"` → `"14.5"`
  - `multi_az`: `false` → `true`
- Red strikethrough for old values, green for new

### Clicking a Resource Being Replaced
![Interactive HTML - Replace Action](https://github.com/user-attachments/assets/0816edbf-6b3a-4048-86b8-3f3caaecd53d)

**Clicking www (Route53 DNS record):**
- **Purple border card** appears in sidebar
- **REPLACING badge** with purple background
- **AWS Route53 icon** properly rendered in diagram
- **Change details**:
  - `alias.name`: `old-alb.amazonaws.com` → `production-cdn.cloudfront.net`
  - Shows DNS routing evolution from ALB to CloudFront CDN

### Key Interactive Features
- ✅ **Official Cloud Provider Icons**: All AWS, Azure, GCP icons render correctly
- ✅ **Base64 Embedded**: Icons embedded in SVG as data URIs (no external file dependencies)
- ✅ **Click any resource** to view full configuration and changes
- ✅ **Before/after comparison** with color-coded highlighting
- ✅ **Professional UI** with gradient header and clean layout
- ✅ **Works offline** - self-contained HTML file
- ✅ **Responsive design** - works on different screen sizes

## Prerequisites

- Python 3.10+
- Graphviz (for diagram rendering)

### Install Graphviz

**Ubuntu/Debian:**
```bash
sudo apt-get install graphviz
```

**macOS:**
```bash
brew install graphviz
```

**Windows:**
Download from [graphviz.org](https://graphviz.org/download/)

## Installation

```bash
# Clone the repository
git clone https://github.com/aviveldan/cloud-diff-mcp.git
cd cloud-diff-mcp

# Install Python dependencies
pip install -r requirements.txt
```

## Usage

### As an MCP Server

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

### Command Line Testing

```bash
# Run the visualization test
python3 test_visualization.py

# Run the MCP server test
python3 test_mcp_server.py

# Generate interactive visualization with connections
python3 generate_interactive.py
```

Outputs:
- PNG with dependency arrows and cloud icons (265KB)
- SVG with embedded icons (self-contained)
- Interactive HTML page with clickable resources

**Open in browser:**
```bash
open terraform-diffs/terraform_plan_interactive.html
```

## Tools

### `visualize_tf_diff`

Visualizes Terraform plan changes using cloud architecture diagrams.

**Input:**
```json
{
  "plan": "<terraform-plan-json-string>"
}
```

Generate the plan JSON with:
```bash
terraform plan -out=tfplan
terraform show -json tfplan > plan.json
```

**Output:**
- High-quality PNG/SVG diagram saved to `terraform-diffs/terraform_plan_diff.png`
- Summary of changes with counts by action type
- Visual grouping by action (create/delete/update/replace)

**New Features:**
- **Dependency Connections**: Gray dashed arrows show relationships between resources (enabled by default in hierarchical view)
- **Interactive HTML**: Click resources to view configuration and changes (`generate_interactive.py`)
- **SVG Output**: Use `format='svg'` for scalable vector graphics with embedded metadata

### Interactive Features

The interactive HTML visualization provides:
- **Clickable Resources**: Click any resource icon to view details
- **Configuration Viewer**: See before/after values for updates
- **Change Highlighting**: Color-coded changes (green for additions, red for deletions)
- **Resource Metadata**: Full Terraform resource type and action information
- **Official Cloud Icons**: AWS, Azure, and GCP icons embedded as base64 data URIs
- **Offline Capable**: Self-contained HTML file with no external dependencies
- **Browser-Based**: No special tools required, just open in any modern browser
- **MCP App Compatible**: Tested with Playwright MCP browser automation

### Supported Resource Types

The tool includes icon mappings for common resources across cloud providers:

**AWS**: EC2, VPC, RDS, S3, ELB, Lambda, IAM, Security Groups, ElastiCache, Route53, CloudFront, NAT Gateway, and more  
**Azure**: Virtual Machines, Virtual Networks, SQL Database, Storage Accounts, Managed Identities, and more  
**GCP**: Compute Engine, VPC, Cloud SQL, Cloud Storage, GKE, and more

Unknown resource types default to a generic compute icon.

## Examples

The repository includes three example Terraform plans:

1. **simple-aws-plan.json**: 6 resource changes demonstrating basic AWS infrastructure
2. **azure-plan.json**: 7 resource changes showing Azure resources
3. **complex-aws-plan.json**: 15 resource changes in a multi-tier production architecture with:
   - Multi-AZ deployment across 2 availability zones
   - Load balancing with ALB
   - Database with multi-AZ failover
   - Caching layer with ElastiCache
   - CDN with CloudFront
   - DNS with Route53

Generate diagrams for all examples:
```bash
python3 generate_examples.py
```

## Development

### Project Structure

```
cloud-diff-mcp/
├── cloud_diff_mcp/
│   ├── __init__.py
│   ├── server.py                     # FastMCP server implementation
│   ├── visualizer.py                 # Standard diagram generation
│   ├── visualizer_hierarchical.py   # Hierarchical layout for complex architectures
│   ├── interactive_html.py           # Interactive HTML generator
│   └── svg_embedder.py               # Icon embedding utility
├── examples/
│   ├── simple-aws-plan.json          # Simple AWS example (6 resources)
│   ├── azure-plan.json               # Azure example (7 resources)
│   └── complex-aws-plan.json         # Complex multi-tier architecture (15 resources)
├── generate_examples.py              # Generate diagrams for all examples
├── generate_interactive.py           # Generate interactive HTML visualization
├── requirements.txt                  # Python dependencies
├── pyproject.toml                    # Project metadata
└── README.md
```

### Running Tests

```bash
# Test visualization generation
python3 test_visualization.py

# Test MCP tool integration
python3 test_mcp_server.py
```

## Technical Details

### Architecture

- **FastMCP**: Python MCP server framework for tool registration
- **Diagrams**: Python library for generating cloud architecture diagrams
- **Graphviz**: Rendering engine for diagram layout

### Icon Embedding Solution

**Problem**: SVG diagrams generated by the Diagrams library reference external PNG files using `xlink:href`, which don't display in browsers when opened directly.

**Solution**: Created `svg_embedder.py` module that:
- Parses SVG files and finds all external image references
- Converts PNG file paths to base64-encoded data URIs
- Embeds 12+ unique cloud provider icons directly in the SVG
- Makes HTML fully self-contained and portable
- Ensures no external file dependencies or broken image links

**Technical Implementation:**
1. `cloud_diff_mcp/server.py`: FastMCP server with `visualize_tf_diff` tool
2. `cloud_diff_mcp/visualizer_hierarchical.py`: Hierarchical layout with dependency connections
3. `cloud_diff_mcp/interactive_html.py`: Interactive HTML generator
4. `cloud_diff_mcp/svg_embedder.py`: Icon embedding utility

### Security & Privacy

- ✅ **Offline Operation**: No cloud API calls or network requests
- ✅ **Stateless**: No persistent storage of Terraform plans
- ✅ **Credential-Free**: Does not require cloud credentials

## Legacy TypeScript Implementation

The original TypeScript implementation using Mermaid diagrams is preserved in the `src/` directory for reference. The Python implementation provides higher-quality diagrams with official cloud provider icons.

## License

MIT