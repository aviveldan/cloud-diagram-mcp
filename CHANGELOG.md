# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CI/CD workflows for automated testing, releases, and auto-merge
- GitHub Actions workflow for automated PyPI publishing
- Auto-merge workflow for automatic PR merging when tests pass
- Dependabot configuration for automated dependency updates
- This CHANGELOG file

## [2.0.0] - Previous

### Features
- MCP server that visualizes Terraform plan changes as interactive cloud architecture diagrams
- Multi-cloud support with official AWS, Azure, and GCP icons
- Interactive HTML with clickable resources showing configuration details
- Color-coded changes: green (create), red (delete), orange (update), purple (replace)
- Three MCP tools: visualize_tf_diff, visualize_architecture, export_architecture_svg
- Hierarchical architecture views with dependency connections
- React-based UI for interactive visualization
- Comprehensive test suite with Python and Playwright tests

[Unreleased]: https://github.com/aviveldan/cloud-diagram-mcp/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/aviveldan/cloud-diagram-mcp/releases/tag/v2.0.0
