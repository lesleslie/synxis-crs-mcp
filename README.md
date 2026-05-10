# SynXis CRS MCP Server

[![Code style: crackerjack](https://img.shields.io/badge/code%20style-crackerjack-000042)](https://github.com/lesleslie/crackerjack)
[![Runtime: oneiric](https://img.shields.io/badge/runtime-oneiric-6e5494)](https://github.com/lesleslie/oneiric)
[![Framework: FastMCP](https://img.shields.io/badge/framework-FastMCP-0ea5e9)](https://github.com/jlowin/fastmcp)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Python: 3.13+](https://img.shields.io/badge/python-3.13%2B-green)](https://www.python.org/downloads/)

MCP server for SynXis CRS (Central Reservation System) integrations.

## Overview

This repository provides a FastMCP interface over SynXis CRS APIs, aimed at reservation, availability, and related central-reservations workflows. The repo is structured for typed request validation, clear provider boundaries, and mockable tests.

## Installation

```bash
uv sync --group dev
```

## Usage

### Stdio Mode

```bash
uv run synxis-crs-mcp
```

### HTTP Mode

```bash
uv run synxis-crs-mcp serve --http --port 3046
```

## Development

```bash
uv run pytest
uv run ruff check synxis_crs_mcp tests
uv run ruff format synxis_crs_mcp tests
```

## Project Structure

- `synxis_crs_mcp/`: MCP server package, API clients, tools, and config helpers
- `tests/`: reservation, availability, and provider error-path coverage
- `settings/`: environment-specific configuration defaults

## Security Notes

- Keep hotel credentials, tenant identifiers, and reservation data out of version control.
- Use mocks or scrubbed fixtures for test and documentation examples.
