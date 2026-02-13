# MCP Apps Testing Framework

This directory contains the [mcp-apps-testing framework](https://github.com/aviveldan/mcp-apps-testing), a professional testing framework for Model Context Protocol (MCP) UI applications.

## About

The mcp-apps-testing framework is embedded in this repository to test MCP protocol interactions for the cloud-diagram-mcp server. It provides:

- **MockMCPHost**: Simulates IDE environments (Claude, VS Code, etc.)
- **TransportInterceptor**: Mocks JSON-RPC 2.0 messages
- **Host Profiles**: Pre-configured environments with capabilities
- **Protocol Logging**: Detailed message flow debugging

## Usage

The framework is used in `../mcp-apps.spec.ts` to test all three cloud-diagram-mcp tools:
1. `visualize_tf_diff` - Terraform plan visualization
2. `visualize_architecture` - Cloud architecture visualization
3. `export_architecture_svg` - SVG export functionality

## Building

The framework is written in TypeScript and must be compiled before use:

```bash
cd ui/mcp-apps-testing
npx tsc
```

This generates the compiled JavaScript in the `dist/` directory (ignored by git).

## CI/CD

The GitHub Actions workflow automatically builds the framework during testing:

```yaml
- name: Build mcp-apps-testing framework
  run: |
    cd ui/mcp-apps-testing
    npx tsc
```

## Source

This is a copy of the mcp-apps-testing framework from:
https://github.com/aviveldan/mcp-apps-testing

Version: 0.1.0

## License

MIT License - see the original repository for details.
