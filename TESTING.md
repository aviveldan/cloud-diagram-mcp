# Test Suite Documentation

This repository contains comprehensive tests for all MCP server tools using both traditional methods and the new mcp-apps-testing framework.

## Test Coverage

The cloud-diagram-mcp server provides 3 tools:

1. **visualize_tf_diff** - Visualizes Terraform plan changes as interactive diagrams
2. **visualize_architecture** - Visualizes cloud architecture as interactive diagrams
3. **export_architecture_svg** - Exports architecture diagrams as SVG files

### MCP Apps Testing (mcp-apps.spec.ts)

Located in the `ui/` directory, this new test suite uses the [mcp-apps-testing framework](https://github.com/aviveldan/mcp-apps-testing) to validate MCP protocol interactions:

- Tests MCP host initialization and capabilities
- Tests tool listing with proper schema validation
- Tests `visualize_tf_diff` with sample Terraform plans
- Tests `visualize_architecture` with Azure architecture examples
- Tests `export_architecture_svg` for SVG file generation
- Tests error handling for invalid JSON inputs
- Tests protocol logging and message flow recording
- Uses MockMCPHost with Claude profile simulation

**Requirements:**
- Node.js 18+
- npm
- Playwright with Chromium browser
- mcp-apps-testing framework (installed via npm)

**Running MCP Apps tests:**
```bash
cd ui

# Install dependencies (includes mcp-apps-testing)
npm install

# Run MCP Apps tests
npm run test:mcp

# Run with UI mode for debugging
npx playwright test mcp-apps.spec.ts --ui
```

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

### MCP Apps Testing
The MCP Apps tests use the mcp-apps-testing framework to:
1. Create a MockMCPHost simulating an IDE environment (Claude, VS Code, etc.)
2. Mock MCP protocol JSON-RPC messages and responses
3. Test tool calls with proper parameter validation
4. Verify protocol message flows and capabilities
5. Test error handling and edge cases

Key features:
- **Zero-config setup**: MockMCPHost handles protocol details automatically
- **Fluent DSL**: Human-readable methods like `callTool()`, `listTools()`
- **Auto-retry**: Configurable retry logic with timeout support
- **Host profiles**: Pre-configured profiles for Claude, VS Code
- **Protocol logging**: Detailed JSON-RPC message logging for debugging
- **Message recording**: Assert on complete message flows

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

This repository includes a GitHub Actions workflow (`.github/workflows/test.yml`) that automatically runs all tests on every pull request and push to main.

The workflow:
1. Sets up Python 3.10 and installs Graphviz
2. Installs Python dependencies and runs `test_mcp.py`
3. Sets up Node.js 18 and installs UI dependencies (including mcp-apps-testing)
4. Builds the React UI with `npm run build`
5. Installs Playwright browsers
6. Generates test harnesses for UI tests
7. Runs all 31 Playwright UI tests
8. Runs 10 MCP Apps protocol tests
9. Uploads test reports on failure for debugging

The workflow ensures that all tests pass before code can be merged, maintaining high code quality and preventing regressions.

## Test Data

Example files in `examples/`:
- `sample-plan.json` - Small Terraform plan with AWS resources
- `complex-aws-plan.json` - Larger Terraform plan with 23 resources
- `architecture-azure.json` - Azure architecture with 6 resources and 6 connections
- `azure-plan.json` - Azure Terraform plan

## Coverage Summary

- ✅ **100% tool coverage** - All 3 MCP tools have tests
- ✅ **10 MCP protocol tests** - Comprehensive protocol interaction validation using mcp-apps-testing
- ✅ **31 UI tests** - Comprehensive Playwright tests for interactive behavior
- ✅ **Multiple scenarios** - Tests cover simple and complex plans, different cloud providers
- ✅ **Integration tests** - Python tests validate end-to-end tool functionality
- ✅ **Protocol tests** - MCP Apps tests validate JSON-RPC message flows and tool schemas
- ✅ **UI interaction tests** - Playwright tests validate user interactions and visual behavior

## Note on export_architecture_svg

The `export_architecture_svg` tool is tested in Python but does not have dedicated Playwright UI tests because:
1. It doesn't use the MCP App UI - it directly exports to a file
2. The Python tests adequately verify file creation, content, and SVG structure
3. UI testing is not applicable as there's no interactive interface for this tool
