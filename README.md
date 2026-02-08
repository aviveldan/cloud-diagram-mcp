# Cloud Diagram MCP

MCP server that visualizes Terraform plan changes as cloud architecture diagrams with official AWS, Azure, and GCP icons.

## Features

- Generate diagrams from Terraform plan JSON (no cloud credentials required)
- Multi-cloud support with official provider icons
- Hierarchical architecture views with dependency connections
- Interactive HTML with clickable resources showing configuration details
- Color-coded changes: green (create), red (delete), orange (update), purple (replace)

## Screenshots

![AWS Infrastructure](https://github.com/user-attachments/assets/b338b884-1ce6-4c86-b160-eab7ce3f5152)
![Azure Infrastructure](https://github.com/user-attachments/assets/a421dc13-4893-40fa-87c3-217154fd7894)
![Complex AWS Architecture](https://github.com/user-attachments/assets/e63ee02d-7a6f-49d3-854c-8d6b05bd88e0)
![Interactive HTML](https://github.com/user-attachments/assets/6d843f8d-59fb-4346-84de-50245a393671)

## Installation

**Prerequisites:** Python 3.10+, Graphviz, Node.js 18+

```bash
# Install Graphviz
# Ubuntu/Debian: sudo apt-get install graphviz
# macOS: brew install graphviz
# Windows: winget install --id Graphviz.Graphviz (add bin to PATH)

# Clone and install
git clone https://github.com/aviveldan/cloud-diagram-mcp.git
cd cloud-diagram-mcp
pip install -r requirements.txt

# Build React UI
cd ui && npm install && npm run build && cd ..
```

## Usage

### MCP Server

Add to your MCP client configuration (e.g., Claude Desktop):

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

### Terraform Plan

```bash
terraform plan -out=tfplan
terraform show -json tfplan > plan.json
```

Use the MCP `visualize_tf_diff` tool with the plan JSON as input:
```json
{
  "plan": "<plan-json-content>"
}
```

### Command Line

```bash
python3 test_mcp.py                          # Test MCP tools
python3 generate_documentation_diagrams.py    # Generate example diagrams
```

## Supported Resources

**AWS:** EC2, VPC, RDS, S3, ELB, Lambda, IAM, ElastiCache, Route53, CloudFront, NAT Gateway, and more  
**Azure:** VMs, Virtual Networks, SQL Database, Storage Accounts, Managed Identities, and more  
**GCP:** Compute Engine, VPC, Cloud SQL, Cloud Storage, GKE, and more

## Development

```bash
# Build UI
cd ui && npm install && npm run build

# Run Python tests (requires Graphviz)
python3 test_mcp.py

# Run Playwright UI tests
cd ui
npm run build
python create-test-harness.py
python create-test-harness-architecture.py
npm test
```

For complete testing documentation, see [TESTING.md](TESTING.md).

## License

MIT