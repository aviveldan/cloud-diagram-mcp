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

### Simple Infrastructure Changes
![AWS Simple Example](https://github.com/user-attachments/assets/b338b884-1ce6-4c86-b160-eab7ce3f5152)

### Complex Multi-Tier Architecture with Connections
![Complex AWS Architecture with Connections](https://github.com/user-attachments/assets/e63ee02d-7a6f-49d3-854c-8d6b05bd88e0)

The complex example shows a production-grade multi-tier architecture with 15 resources organized across 7 layers: Internet (CDN, DNS), Network Infrastructure (VPC, Subnets, NAT Gateways), Load Balancing, Compute (Multi-AZ), Data Layer (RDS, ElastiCache), Storage (S3), and Security (IAM, Security Groups). **Gray dashed arrows** show dependency relationships between resources (e.g., instances depend on subnets, subnets depend on VPC).

### Interactive Visualization
The tool also generates an interactive HTML page where you can **click on any resource** to view its full configuration and what changed. Perfect for understanding complex infrastructure changes in detail.

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

The interactive visualization creates:
- **PNG with connections**: Static diagram showing dependency arrows
- **SVG diagram**: Scalable vector format
- **Interactive HTML**: Click any resource to see its configuration and changes

Open `terraform-diffs/terraform_plan_interactive.html` in a web browser to explore resources interactively.

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
- **Browser-Based**: No special tools required, just open in any modern browser

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
│   ├── server.py                    # FastMCP server implementation
│   ├── visualizer.py                # Standard diagram generation
│   └── visualizer_hierarchical.py  # Hierarchical layout for complex architectures
├── examples/
│   ├── sample-plan.json             # Simple AWS example
│   ├── azure-plan.json              # Azure example
│   └── complex-aws-plan.json        # Complex multi-tier architecture
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Project metadata
└── README.md
```
│   └── sample-plan.json   # Sample Terraform plan
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project metadata
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

### Security & Privacy

- ✅ **Offline Operation**: No cloud API calls or network requests
- ✅ **Stateless**: No persistent storage of Terraform plans
- ✅ **Credential-Free**: Does not require cloud credentials

## Legacy TypeScript Implementation

The original TypeScript implementation using Mermaid diagrams is preserved in the `src/` directory for reference. The Python implementation provides higher-quality diagrams with official cloud provider icons.

## License

MIT