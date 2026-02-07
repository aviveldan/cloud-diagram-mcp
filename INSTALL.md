# Installation and Setup Guide

## Prerequisites

1. **Python 3.10 or higher**
   ```bash
   python3 --version
   ```

2. **Graphviz** (required by the Diagrams library)
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install graphviz
   ```
   
   **macOS:**
   ```bash
   brew install graphviz
   ```
   
   **Windows:**
   - Download from [graphviz.org](https://graphviz.org/download/)
   - Add to PATH

3. **Verify Graphviz installation:**
   ```bash
   dot -V
   ```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aviveldan/cloud-diff-mcp.git
   cd cloud-diff-mcp
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or with a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Running the Server

### As an MCP Server

Add to your MCP client configuration (e.g., Claude Desktop `config.json`):

```json
{
  "mcpServers": {
    "cloud-diff": {
      "command": "python3",
      "args": ["-m", "cloud_diff_mcp.server"],
      "cwd": "/absolute/path/to/cloud-diff-mcp"
    }
  }
}
```

**Important:** Use absolute paths for the `cwd` parameter.

### Testing the Implementation

1. **Test diagram generation:**
   ```bash
   python3 test_visualization.py
   ```
   
   This generates a diagram from the sample AWS Terraform plan.

2. **Test MCP tool integration:**
   ```bash
   python3 test_mcp_server.py
   ```
   
   This tests the visualize_tf_diff tool.

3. **Generate example diagrams:**
   ```bash
   python3 generate_examples.py
   ```
   
   This creates diagrams for both AWS and Azure examples.

## Usage

### 1. Create a Terraform Plan

```bash
# Initialize and plan
terraform init
terraform plan -out=tfplan

# Convert to JSON
terraform show -json tfplan > plan.json
```

### 2. Use the visualize_tf_diff Tool

Through your MCP client (e.g., Claude Desktop), call the `visualize_tf_diff` tool with the plan JSON:

```
Please analyze this Terraform plan and create a visual diagram:
[paste plan.json content]
```

### 3. View the Output

The tool will generate a PNG diagram in the `terraform-diffs` directory and return:
- Path to the generated image
- Summary of changes (create/update/delete/replace counts)

## Example Output

```
# Terraform Plan Visualization

## Change Summary
- ✨ **Create**: 3 resources
- 📝 **Update**: 1 resources
- 🗑️ **Delete**: 1 resources
- 🔄 **Replace**: 1 resources

**Total changes**: 6 resources

## Diagram Generated
The visual diff diagram has been saved to: `terraform-diffs/terraform_plan_diff.png`
```

## Troubleshooting

### "ImportError: cannot import name 'X' from 'diagrams.Y'"

- The Diagrams library may have version differences
- Check the installed version: `pip show diagrams`
- Ensure you have the latest version: `pip install --upgrade diagrams`

### "graphviz.backend.execute.ExecutableNotFound: failed to execute ['dot', ...]"

- Graphviz is not installed or not in PATH
- Install Graphviz using the instructions above
- Verify with `dot -V`

### Server doesn't start

- Check Python version: `python3 --version` (must be 3.10+)
- Verify all dependencies are installed: `pip list | grep -E "(fastmcp|diagrams)"`
- Check for port conflicts or permission issues

## Supported Resource Types

The tool includes icon mappings for 50+ resource types:

**AWS:** EC2, VPC, RDS, S3, ELB, Lambda, IAM, Security Groups, Route53, CloudFront, Secrets Manager, WAF, etc.

**Azure:** Virtual Machines, Virtual Networks, SQL Database, Storage Accounts, Managed Identities, Container Instances, App Services, etc.

**GCP:** Compute Engine, VPC, Cloud SQL, Cloud Storage, GKE, App Engine, etc.

Unknown resource types will default to a generic compute icon (EC2).

## Development

### Project Structure

```
cloud-diff-mcp/
├── cloud_diff_mcp/          # Python package
│   ├── __init__.py
│   ├── server.py            # FastMCP server
│   └── visualizer.py        # Diagram generation
├── examples/                 # Sample Terraform plans
│   ├── sample-plan.json     # AWS example
│   └── azure-plan.json      # Azure example
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project metadata
├── test_visualization.py   # Visualization tests
├── test_mcp_server.py      # MCP integration tests
└── generate_examples.py    # Example generator
```

### Running Tests

```bash
# All tests
python3 test_visualization.py && python3 test_mcp_server.py

# Generate examples
python3 generate_examples.py
```

## License

MIT License - See LICENSE file for details.
