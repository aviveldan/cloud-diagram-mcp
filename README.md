# Cloud Diff MCP

A Model Context Protocol (MCP) server for analyzing Terraform plans and visualizing infrastructure changes with high-fidelity cloud architecture diagrams using the Python Diagrams library.

## Features

- 🎨 **Offline Visual Diffing**: Generate beautiful cloud architecture diagrams from Terraform plan JSON
- 🔒 **No Cloud Credentials Required**: Operates entirely offline, processing plan output locally
- ☁️ **Multi-Cloud Support**: Icons for AWS, Azure, and GCP resources
- 🏗️ **Hierarchical Architecture Views**: Complex infrastructures organized by architectural layers
- 🎯 **Visual State Representation**:
  - 🟢 **Green**: New resources (create)
  - 🔴 **Red**: Deleted resources (delete)
  - 🟠 **Orange**: Modified resources (update)
  - 🟣 **Purple**: Replaced resources (create + delete)

## Screenshots

### Simple Infrastructure Changes
![AWS Simple Example](https://github.com/user-attachments/assets/b338b884-1ce6-4c86-b160-eab7ce3f5152)

### Complex Multi-Tier Architecture
![Complex AWS Architecture](https://github.com/user-attachments/assets/522ad236-d273-41f8-8007-c189093d7731)

The complex example shows a production-grade multi-tier architecture with 15 resources organized across 7 layers: Internet (CDN, DNS), Network Infrastructure (VPC, Subnets, NAT Gateways), Load Balancing, Compute (Multi-AZ), Data Layer (RDS, ElastiCache), Storage (S3), and Security (IAM, Security Groups).

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
- High-quality PNG diagram saved to `terraform-diffs/terraform_plan_diff.png`
- Summary of changes with counts by action type
- Visual grouping by action (create/delete/update/replace)

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