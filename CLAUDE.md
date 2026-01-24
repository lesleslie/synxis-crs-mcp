# Claude Code Guidelines for synxis-crs-mcp

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
uv run pytest tests/test_specific.py

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
2. Run linter: `uv run ruff check .`
3. Run tests: `uv run pytest`
4. Check coverage: Review `htmlcov/index.html`

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
