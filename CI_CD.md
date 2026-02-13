# CI/CD Documentation

This document describes the continuous integration and deployment setup for the cloud-diagram-mcp project.

## Overview

The repository uses GitHub Actions for CI/CD automation. All workflows are located in `.github/workflows/`.

## Workflows

### 1. Tests (`test.yml`)

**Trigger:** On every push to `main` and on all pull requests

**Purpose:** Validates code quality and functionality

**Steps:**
- Sets up Python 3.10 and Node.js 18
- Installs system dependencies (Graphviz)
- Installs Python dependencies
- Runs Python MCP tests (`test_mcp.py`)
- Builds React UI
- Installs Playwright
- Generates test harnesses
- Runs Playwright UI tests

**Status:** Required for merge

### 2. Lint (`lint.yml`)

**Trigger:** On every push to `main` and on all pull requests

**Purpose:** Ensures code quality and formatting standards

**Steps:**
- **Python Lint:**
  - Checks code formatting with Black (line length: 100)
  - Type checking with MyPy
- **UI Type Check:**
  - TypeScript type checking

**Status:** Informational (failures don't block merge)

### 3. CodeQL Security Analysis (`codeql.yml`)

**Trigger:** 
- On every push to `main`
- On all pull requests
- Weekly on Mondays at 00:00 UTC

**Purpose:** Detects security vulnerabilities and code quality issues

**Languages:** Python, JavaScript

**Status:** Informational (findings don't block merge but should be reviewed)

### 4. Release (`release.yml`)

**Trigger:** When a version tag (e.g., `v2.1.0`) is pushed

**Purpose:** Automates the release process

**Steps:**
- Installs Graphviz (required for diagrams)
- Builds React UI
- Builds Python package (wheel and source distribution)
- Creates GitHub Release with auto-generated release notes
- Publishes package to PyPI using trusted publishing

**Requirements:**
- Tag must match pattern `v*` (e.g., `v2.1.0`)
- PyPI trusted publishing must be configured

### 5. Auto-merge (`auto-merge.yml`)

**Trigger:**
- PR labeled/unlabeled
- PR synchronized/opened/edited
- PR review submitted
- Check suite completed
- Tests workflow completed

**Purpose:** Automatically merges PRs when conditions are met

**Conditions:**
- PR must have the `auto-merge` label
- At least one approval from latest reviews
- No "changes requested" reviews
- All tests must pass (if tests exist)

**Behavior:**
- Enables auto-merge with squash merge strategy
- Comments on PR if conditions are not met

## Dependabot

**Configuration:** `.github/dependabot.yml`

**Purpose:** Automated dependency updates

**Ecosystems:**
- GitHub Actions (weekly)
- Python pip (weekly)
- npm for UI (weekly)

**Limits:** 5 open PRs per ecosystem

**Labels:** Automatically adds appropriate labels to dependency PRs

## Issue and PR Templates

### Issue Templates

Located in `.github/ISSUE_TEMPLATE/`:

1. **Bug Report** (`bug_report.yml`)
   - Structured bug reporting with required fields
   - Collects Python version, OS, steps to reproduce

2. **Feature Request** (`feature_request.yml`)
   - Structured feature suggestions
   - Problem description, proposed solution, alternatives

3. **Config** (`config.yml`)
   - Disables blank issues
   - Provides links to documentation

### Pull Request Template

Located in `.github/pull_request_template.md`

**Sections:**
- Description
- Type of change (bug fix, feature, breaking change, etc.)
- Checklist for code quality
- Testing description
- Screenshots (if applicable)

## Labels

**Configuration:** `.github/labels.yml`

**Categories:**
- Type: `bug`, `enhancement`, `documentation`
- Technology: `python`, `ui`, `github-actions`
- Workflow: `auto-merge`, `dependencies`
- Status: `good first issue`, `help wanted`, `wontfix`
- Impact: `breaking change`

## Code Owners

**Configuration:** `.github/CODEOWNERS`

**Purpose:** Automatically requests reviews from specified owners

**Owners:**
- All files: @aviveldan
- GitHub workflows: @aviveldan
- Python code: @aviveldan
- UI code: @aviveldan
- Documentation: @aviveldan

## Creating a Release

Follow these steps to create a new release:

1. **Update version number** in `cloud_diagram_mcp/__init__.py`:
   ```python
   __version__ = "X.Y.Z"  # e.g., "2.1.0"
   ```

2. **Update pyproject.toml** version:
   ```toml
   version = "X.Y.Z"  # e.g., "2.1.0"
   ```

3. **Update CHANGELOG.md**:
   - Move items from `[Unreleased]` to a new version section
   - Add release date
   - Create new `[Unreleased]` section

4. **Commit changes**:
   ```bash
   git add cloud_diagram_mcp/__init__.py pyproject.toml CHANGELOG.md
   git commit -m "Bump version to X.Y.Z"
   git push
   ```

5. **Create and push tag**:
   ```bash
   git tag vX.Y.Z  # e.g., v2.1.0
   git push origin vX.Y.Z
   ```

6. **Automated process**:
   - Release workflow triggers
   - UI is built
   - Package is built and tested
   - GitHub release is created with notes
   - Package is published to PyPI

## PyPI Publishing Setup

The release workflow uses PyPI Trusted Publishing (no API tokens needed).

**Setup instructions:**

1. Go to [PyPI](https://pypi.org/manage/account/publishing/)
2. Add a new "pending publisher"
3. Configure:
   - PyPI Project Name: `cloud-diagram-mcp`
   - Owner: `aviveldan`
   - Repository name: `cloud-diagram-mcp`
   - Workflow name: `release.yml`
   - Environment name: (leave blank)

## Development Workflow

### For Contributors

1. Fork the repository
2. Create a feature branch
3. Make changes with appropriate tests
4. Push to your fork
5. Create a Pull Request
6. Wait for tests to pass
7. Request review
8. (Optional) Add `auto-merge` label if you're a maintainer

### For Maintainers

1. Review PR
2. Approve if changes are good
3. Add `auto-merge` label if desired
4. PR will automatically merge when tests pass

## Best Practices

1. **Always wait for CI to pass** before merging
2. **Review security alerts** from CodeQL
3. **Keep dependencies updated** via Dependabot
4. **Use semantic versioning** for releases
5. **Update CHANGELOG.md** with every significant change
6. **Add tests** for new features
7. **Use descriptive commit messages**

## Troubleshooting

### Tests Failing

- Check the test logs in GitHub Actions
- Run tests locally: `python test_mcp.py` and `cd ui && npm test`
- Ensure all dependencies are installed

### Release Fails

- Verify version is bumped correctly
- Check PyPI trusted publishing is configured
- Ensure UI builds successfully
- Check GitHub Actions logs

### Auto-merge Not Working

- Verify PR has `auto-merge` label
- Check that PR has approval
- Ensure no "changes requested" reviews exist
- Confirm all tests passed

## Security

- CodeQL runs weekly and on every PR
- Security vulnerabilities are reported as GitHub Security Alerts
- Dependabot keeps dependencies up to date
- Follow security best practices in all contributions

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
