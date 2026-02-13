# Cloud Diagram MCP

[![Tests](https://github.com/aviveldan/cloud-diagram-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/aviveldan/cloud-diagram-mcp/actions/workflows/test.yml)
[![CodeQL](https://github.com/aviveldan/cloud-diagram-mcp/actions/workflows/codeql.yml/badge.svg)](https://github.com/aviveldan/cloud-diagram-mcp/actions/workflows/codeql.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

### Continuous Integration

All tests run automatically on every pull request via GitHub Actions. See `.github/workflows/test.yml` for the complete CI configuration.

For complete CI/CD documentation, including release process and workflows, see [CI_CD.md](CI_CD.md).

## CI/CD

This repository includes comprehensive CI/CD workflows:

- **Tests** (`.github/workflows/test.yml`): Runs Python and Playwright tests on all PRs and pushes to main
- **Release** (`.github/workflows/release.yml`): Automatically publishes to PyPI when a new version tag is pushed
- **Auto-merge** (`.github/workflows/auto-merge.yml`): Automatically merges PRs labeled with `auto-merge` when tests pass and approvals are met
- **Dependabot** (`.github/dependabot.yml`): Automatically updates dependencies weekly

### Creating a Release

1. Update version in `cloud_diagram_mcp/__init__.py`
2. Update `CHANGELOG.md` with the new version and changes
3. Commit the changes
4. Create and push a version tag:
   ```bash
   git tag v2.1.0
   git push origin v2.1.0
   ```
5. The release workflow will automatically:
   - Build the package
   - Create a GitHub release with release notes
   - Publish to PyPI

### Auto-merge

To enable auto-merge on a PR:
1. Add the `auto-merge` label to the PR
2. Ensure the PR has at least one approval
3. Ensure no changes are requested
4. Ensure all tests pass

The PR will be automatically merged when all conditions are met.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

MIT