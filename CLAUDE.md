# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

For a shorter, tool-neutral bootstrap document, start with `AGENTS.md`.

## Project Overview

This is an MCP server project for synxis-crs-mcp integration.

## Development Guidelines

### Quality Tools

This project uses crackerjack for quality assurance:

- **Ruff**: Code formatting and linting
- **Pytest**: Testing with parallel execution support
- **Bandit**: Security scanning
- **Creosote**: Unused dependency detection

### Running Tests

```bash
# Run all tests with coverage
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_schema_validation.py

# Run with pytest-xdist (parallel)
uv run pytest -n auto
```

### Code Quality Checks

```bash
# Format code with ruff
uv run ruff format .

# Lint with ruff
uv run ruff check .

# Security scan with bandit
uv run bandit -r synxis_crs_mcp

# Check for unused dependencies
uv run creosote
```

### Pre-Commit Workflow

1. Format code: `uv run ruff format .`
1. Run linter: `uv run ruff check .`
1. Run tests: `uv run pytest`
1. Check coverage: Review `htmlcov/index.html`

<!-- CRACKERJACK_START -->

## Crackerjack Integration

This project is configured with crackerjack best practices:

### Available Commands

- `/crackerjack:run` - Run all quality checks with AI-powered auto-fix
- `/crackerjack:status` - Check crackerjack server status

### Quality Standards

- **Test Coverage**: Target 80%+ (currently tracked by session-buddy)
- **Complexity Limit**: Max 15 per function (McCabe complexity)
- **Line Length**: 88 characters
- **Type Hints**: Required for all public functions
- **Docstrings**: Google-style for all modules and public APIs

### AI Agent Skills

Crackerjack provides AI agent skills via MCP:

- RefactoringAgent - Code complexity issues
- SecurityAgent - Security vulnerabilities
- PerformanceAgent - Performance optimization
- TestAgent - Test generation and improvement

Access these skills through the crackerjack MCP server (port 8676).

<!-- CRACKERJACK_END -->

## Tool Profile System

synxis-crs-mcp follows the Bodai ecosystem-wide convention of gating tool
registration via a `*_TOOL_PROFILE` environment variable (mcp-common
0.18.0+). The dispatch surface is in `synxis_crs_mcp/tools/profiles.py`;
the server wires it from `synxis_crs_mcp/server.py::create_app` via
`await apply_synxis_crs_tool_profile(app)`.

| Profile | Env var | Registered groups | Tool count |
|---------|-----------------------------------------|-------------------|------------|
| FULL | `SYNXIS_CRS_TOOL_PROFILE=full` (default) | `crs_tools` | 4 + `discover_tools` = 5 |
| MINIMAL | `SYNXIS_CRS_TOOL_PROFILE=minimal` | (none) | 0 + `discover_tools` = 1 |

`STANDARD` is intentionally omitted (Tier-B 2-tier mapping per the W3
brief). Unset / empty / unknown env var → FULL.

The rationale and design decisions live at
[`docs/architecture/tool-profile-rationale.md`](./docs/architecture/tool-profile-rationale.md).
