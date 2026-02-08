# Test Suite Documentation

This repository contains comprehensive tests for all MCP server tools.

## Test Coverage

The cloud-diagram-mcp server provides 3 tools:

1. **visualize_tf_diff** - Visualizes Terraform plan changes as interactive diagrams
2. **visualize_architecture** - Visualizes cloud architecture as interactive diagrams
3. **export_architecture_svg** - Exports architecture diagrams as SVG files

### Python Tests (test_mcp.py)

Located at the repository root, these tests validate all three tools using the FastMCP in-memory client:

- Tests `visualize_tf_diff` with multiple example plans (sample-plan.json, complex-aws-plan.json)
- Tests `visualize_architecture` with Azure architecture examples
- Tests `export_architecture_svg` to verify SVG file generation and content

**Requirements:**
- Python 3.10+
- Graphviz system package
- Python dependencies from requirements.txt

**Running Python tests:**
```bash
# Install dependencies
pip install -r requirements.txt
sudo apt-get install graphviz  # or brew install graphviz on macOS

# Run tests
python test_mcp.py
```

### Playwright UI Tests (ui/*.spec.ts)

Located in the `ui/` directory, these tests validate the interactive UI behavior for visualization tools:

#### ui.spec.ts (14 tests)
Tests for the **visualize_tf_diff** tool UI:
- SVG rendering and node display
- Sidebar open/close behavior
- Node selection and navigation
- Visual highlights on selected nodes
- Zoom functionality preservation
- Address-based node matching
- Toggle behavior for repeated clicks

#### architecture.spec.ts (17 tests)
Tests for the **visualize_architecture** tool UI:
- Architecture diagram rendering
- Resource node interactions
- Connection/edge rendering
- Azure resource type display
- Sidebar navigation between architecture nodes
- Zoom and pan functionality
- Visual structure validation
- Node clickability
- State preservation during interactions

**Requirements:**
- Node.js 18+
- npm
- Playwright with Chromium browser

**Running Playwright tests:**
```bash
cd ui

# Install dependencies
npm install
npx playwright install chromium

# Build the UI (required before testing)
npm run build

# Generate test harnesses
python create-test-harness.py
python create-test-harness-architecture.py

# Run all tests
npm test

# Run specific test suite
npx playwright test ui.spec.ts
npx playwright test architecture.spec.ts

# Run with UI mode for debugging
npm run test:ui
```

## Test Architecture

### Python Tests
The Python tests use FastMCP's in-memory Client to:
1. Load sample JSON data from the `examples/` directory
2. Call each tool directly
3. Validate the response structure
4. Verify SVG generation and embedding

### Playwright Tests
The Playwright tests:
1. Use pre-built HTML from `npm run build`
2. Inject test data using helper scripts (create-test-harness*.py)
3. Load the HTML in a headless browser
4. Simulate user interactions (clicks, hovers, scrolling)
5. Validate UI state and behavior

## CI/CD Integration

To integrate these tests into CI/CD:

```yaml
# Example GitHub Actions workflow
- name: Setup Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.10'

- name: Install dependencies
  run: |
    pip install -r requirements.txt
    sudo apt-get install -y graphviz

- name: Run Python tests
  run: python test_mcp.py

- name: Setup Node
  uses: actions/setup-node@v4
  with:
    node-version: '18'

- name: Install UI dependencies
  run: |
    cd ui
    npm ci
    npx playwright install chromium --with-deps

- name: Build UI
  run: cd ui && npm run build

- name: Generate test harnesses
  run: |
    cd ui
    python create-test-harness.py
    python create-test-harness-architecture.py

- name: Run Playwright tests
  run: cd ui && npm test
```

## Test Data

Example files in `examples/`:
- `sample-plan.json` - Small Terraform plan with AWS resources
- `complex-aws-plan.json` - Larger Terraform plan with 23 resources
- `architecture-azure.json` - Azure architecture with 6 resources and 6 connections
- `azure-plan.json` - Azure Terraform plan

## Coverage Summary

- ✅ **100% tool coverage** - All 3 MCP tools have tests
- ✅ **31 UI tests** - Comprehensive Playwright tests for interactive behavior
- ✅ **Multiple scenarios** - Tests cover simple and complex plans, different cloud providers
- ✅ **Integration tests** - Python tests validate end-to-end tool functionality
- ✅ **UI interaction tests** - Playwright tests validate user interactions and visual behavior

## Note on export_architecture_svg

The `export_architecture_svg` tool is tested in Python but does not have dedicated Playwright UI tests because:
1. It doesn't use the MCP App UI - it directly exports to a file
2. The Python tests adequately verify file creation, content, and SVG structure
3. UI testing is not applicable as there's no interactive interface for this tool
