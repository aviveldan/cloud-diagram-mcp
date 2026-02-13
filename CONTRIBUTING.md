# Contributing to Cloud Diagram MCP

Thank you for your interest in contributing to Cloud Diagram MCP! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/0/code_of_conduct/). By participating, you are expected to uphold this code. Please report unacceptable behavior to the repository maintainers.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/cloud-diagram-mcp.git
   cd cloud-diagram-mcp
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/aviveldan/cloud-diagram-mcp.git
   ```
4. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Graphviz (required for diagram generation)

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
```bash
winget install --id Graphviz.Graphviz
```
Add Graphviz `bin` directory to your PATH.

### Install Python Dependencies

```bash
pip install -r requirements.txt
pip install -e ".[dev]"  # Install with dev dependencies
```

### Install UI Dependencies

```bash
cd ui
npm install
cd ..
```

### Build UI

```bash
cd ui
npm run build
cd ..
```

## Making Changes

### Before You Start

1. **Check existing issues** to see if someone is already working on it
2. **Create an issue** if one doesn't exist to discuss your proposed changes
3. **Keep changes focused** - one feature or fix per pull request
4. **Write tests** for new functionality

### Commit Guidelines

- Use clear and descriptive commit messages
- Follow the format: `<type>: <description>`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Examples:
  - `feat: Add support for GCP Cloud Run`
  - `fix: Correct color mapping for replaced resources`
  - `docs: Update installation instructions`

## Testing

### Python Tests

Run the MCP server tests:
```bash
python test_mcp.py
```

### UI Tests

Build the UI and run Playwright tests:
```bash
cd ui
npm run build
python create-test-harness.py
python create-test-harness-architecture.py
npm test
cd ..
```

### Run All Tests

The complete test suite (matches CI):
```bash
# Python tests
python test_mcp.py

# UI tests
cd ui
npm run build
python create-test-harness.py
python create-test-harness-architecture.py
npm test
cd ..
```

See [TESTING.md](TESTING.md) for detailed testing documentation.

## Submitting Changes

### Before Submitting

1. **Update tests** to cover your changes
2. **Run all tests** locally and ensure they pass
3. **Update documentation** if you've changed functionality
4. **Check code formatting**:
   ```bash
   black --check --line-length 100 cloud_diagram_mcp/ test_mcp.py
   ```
5. **Run type checking** (optional but recommended):
   ```bash
   mypy cloud_diagram_mcp/ --config-file pyproject.toml
   ```

### Create Pull Request

1. **Push your changes** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub from your fork to the main repository

3. **Fill out the PR template** with:
   - Description of changes
   - Type of change (bug fix, feature, etc.)
   - Testing performed
   - Screenshots (if UI changes)

4. **Wait for CI** to complete and fix any failures

5. **Respond to review feedback** promptly

### Pull Request Guidelines

- Keep PRs focused and reasonably sized
- Include tests for new functionality
- Update documentation as needed
- Ensure CI passes before requesting review
- Be responsive to feedback and questions

## Release Process

Releases are managed by maintainers. The process is:

1. Update version in `cloud_diagram_mcp/__init__.py` and `pyproject.toml`
2. Update `CHANGELOG.md` with release notes
3. Commit changes and push to main
4. Create and push a version tag (e.g., `v2.1.0`)
5. GitHub Actions automatically:
   - Builds the package
   - Creates a GitHub release
   - Publishes to PyPI

See [CI_CD.md](CI_CD.md) for detailed release documentation.

## Style Guidelines

### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://black.readthedocs.io/) for formatting (line length: 100)
- Use type hints where possible
- Write docstrings for public functions and classes
- Keep functions focused and reasonably sized

### TypeScript/JavaScript

- Use TypeScript for type safety
- Follow React best practices
- Use functional components with hooks
- Keep components focused and reusable

### Documentation

- Use Markdown for documentation
- Keep language clear and concise
- Include code examples where helpful
- Update README.md for user-facing changes

### Git

- Write descriptive commit messages
- Keep commits atomic (one logical change per commit)
- Rebase on main before submitting PR
- Squash commits if requested during review

## Questions?

- **General questions**: Open a [discussion](https://github.com/aviveldan/cloud-diagram-mcp/discussions)
- **Bug reports**: Open an [issue](https://github.com/aviveldan/cloud-diagram-mcp/issues/new?template=bug_report.yml)
- **Feature requests**: Open an [issue](https://github.com/aviveldan/cloud-diagram-mcp/issues/new?template=feature_request.yml)

## License

By contributing to Cloud Diagram MCP, you agree that your contributions will be licensed under the [MIT License](LICENSE).

## Thank You!

Your contributions help make Cloud Diagram MCP better for everyone. We appreciate your time and effort! 🎉
