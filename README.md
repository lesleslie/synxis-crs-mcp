# SynXis CRS MCP Server

[![Code style: crackerjack](https://img.shields.io/badge/code%20style-crackerjack-000042)](https://github.com/lesleslie/crackerjack)
[![Runtime: oneiric](https://img.shields.io/badge/runtime-oneiric-6e5494)](https://github.com/lesleslie/oneiric)
[![Framework: FastMCP](https://img.shields.io/badge/framework-FastMCP-0ea5e9)](https://github.com/jlowin/fastmcp)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Python: 3.14+](https://img.shields.io/badge/python-3.14%2B-green)](https://www.python.org/downloads/)

MCP server for SynXis CRS (Central Reservation System) integration.

**Version:** 0.2.0
**Status:** Internal Bodai integration component

## Quick Links

- [Overview](#overview)
- [Capabilities](#capabilities)
- [Quick Start](#quick-start)
- [MCP Server Configuration](#mcp-server-configuration)
- [Tool Reference](#tool-reference)
- [Configuration](#configuration)
- [Development](#development)
- [Installation via Bodai Marketplace](#installation-via-bodai-marketplace)

## Installation via Bodai Marketplace

This repo is packaged as a Bodai Claude Code plugin. Add the `bodai-plugins` marketplace, then install the `synxis-crs` plugin to expose the slash commands (`/synxis-crs-lookup`, `/synxis-crs-availability`, `/synxis-crs-reservation`) and connect to the running MCP server at `http://localhost:3046/mcp`. The plugin self-references its colocated `.mcp.json`, so no additional client configuration is required. Use the marketplace to keep the plugin versioned alongside the underlying server and to receive the same update flow as the rest of the Bodai fleet.

## Quality & CI

Crackerjack is the standard quality-control and CI/CD gate for SynXis CRS MCP changes. Local verification should mirror the Crackerjack workflow used across the Bodai ecosystem.

______________________________________________________________________

## Overview

SynXis CRS MCP exposes central-reservations workflows through a FastMCP server. It is designed for agent-facing hotel search, availability, rate lookup, and reservation creation while keeping provider credentials, request validation, and transport concerns in a narrow integration boundary.

The server is intentionally separate from `synxis-pms-mcp`. CRS owns shopping and booking workflows that belong to the central reservation system; PMS owns property operations such as guest, room, check-in, check-out, and folio workflows.

## Capabilities

Tools (4 MCP tools):

- **Property search** (`search_properties`): find hotels by city, state, region, or other location text
- **Availability lookup** (`get_availability`): check available room types for a property and date range
- **Rate lookup** (`get_rates`): retrieve rate plans, totals, currency, and cancellation policy details
- **Reservation creation** (`create_reservation`): create a booking from property, room type, rate plan, dates, and guest details

Plus runtime features:

- **Mock mode**: exercise the MCP tool surface without live SynXis credentials
- **HTTP health routes**: `/health` and `/healthz` for MCP client and process supervision checks

## Quick Start

### Prerequisites

- Python 3.13+
- UV package manager
- SynXis CRS OAuth2 credentials for live API access

### Local Setup

```bash
git clone https://github.com/lesleslie/synxis-crs-mcp.git
cd synxis-crs-mcp
uv sync --group dev
```

### Run In Mock Mode

Mock mode is the safest way to validate client wiring and tool behavior before using live credentials.

```bash
export SYNXIS_CRS_MOCK_MODE=true
uv run synxis-crs-mcp start
uv run synxis-crs-mcp health
```

### Run With Live Credentials

```bash
export SYNXIS_CRS_CLIENT_ID="your-client-id"
export SYNXIS_CRS_CLIENT_SECRET="your-client-secret"
export SYNXIS_CRS_HOTEL_ID="your-hotel-or-chain-id"
uv run synxis-crs-mcp start
```

The default HTTP bind is `127.0.0.1:3046`.

## CLI Commands

The CLI is built with `mcp-common` and provides the standard lifecycle command surface used by Bodai MCP servers.

```bash
uv run synxis-crs-mcp start      # Start the HTTP MCP server
uv run synxis-crs-mcp stop       # Stop the managed server process
uv run synxis-crs-mcp restart    # Restart the managed server process
uv run synxis-crs-mcp status     # Show process status
uv run synxis-crs-mcp health     # Run the local health probe
```

## MCP Server Configuration

### Claude / Codex Style Configuration

Add the server to an MCP client configuration:

```json
{
  "mcpServers": {
    "synxis-crs": {
      "command": "uv",
      "args": ["run", "synxis-crs-mcp", "start"],
      "cwd": "/Users/les/Projects/synxis-crs-mcp",
      "env": {
        "SYNXIS_CRS_MOCK_MODE": "true"
      }
    }
  }
}
```

For live access, replace mock mode with credential environment variables supplied by your secret manager.

### Health Checks

```bash
curl http://127.0.0.1:3046/health
curl http://127.0.0.1:3046/healthz
```

## Tool Reference

| Tool | Purpose | Required Inputs |
|------|---------|-----------------|
| `search_properties` | Search hotels by location | `location` |
| `get_availability` | Check room availability for a property | `property_id`, `start_date`, `end_date` |
| `get_rates` | Retrieve rates for a property and date range | `property_id`, `start_date`, `end_date` (optional: `room_type`) |
| `create_reservation` | Create a hotel reservation | `property_id`, `room_type`, `rate_plan_id`, `start_date`, `end_date`, guest fields |

Dates use `YYYY-MM-DD`. Tool responses follow a consistent `ToolResponse` shape:

```json
{
  "success": true,
  "message": "Found 2 properties in Miami Beach",
  "data": {},
  "error": null,
  "next_steps": []
}
```

## Configuration

Committed defaults live in `settings/synxis-crs.yaml`. Runtime overrides should come from environment variables or a local `.env` file that is not committed.

| Setting | Environment Variable | Default |
|---------|----------------------|---------|
| Client ID | `SYNXIS_CRS_CLIENT_ID` | empty |
| Client secret | `SYNXIS_CRS_CLIENT_SECRET` | empty |
| Base URL | `SYNXIS_CRS_BASE_URL` | `https://api.synxis.com/crs/v1` |
| Hotel or chain ID | `SYNXIS_CRS_HOTEL_ID` | empty |
| Mock mode | `SYNXIS_CRS_MOCK_MODE` | `false` |
| Timeout | `SYNXIS_CRS_TIMEOUT` | `30.0` |
| Max retries | `SYNXIS_CRS_MAX_RETRIES` | `3` |
| HTTP host | `SYNXIS_CRS_HTTP_HOST` | `127.0.0.1` |
| HTTP port | `SYNXIS_CRS_HTTP_PORT` | `3046` |
| Log level | `SYNXIS_CRS_LOG_LEVEL` | `INFO` |
| JSON logs | `SYNXIS_CRS_LOG_JSON` | `true` |

## Project Structure

```text
synxis_crs_mcp/
  cli.py              # mcp-common lifecycle CLI
  client.py           # SynXis CRS client boundary
  config.py           # Pydantic settings and logging
  models.py           # Typed CRS domain models
  server.py           # FastMCP application factory
  tools/crs_tools.py  # Registered MCP tools
settings/
  synxis-crs.yaml     # Committed defaults
tests/
  test_schema_validation.py
```

## Development

```bash
uv sync --group dev
uv run pytest
uv run ruff check synxis_crs_mcp tests
uv run ruff format synxis_crs_mcp tests
```

Use direct `pytest` commands for targeted debugging:

```bash
uv run pytest tests/test_schema_validation.py -v
```

## Security Notes

- Do not commit SynXis credentials, bearer tokens, tenant identifiers, or guest payment data.
- Keep examples and tests on mock mode or scrubbed fixtures.
- Treat reservation payloads and guest contact fields as sensitive operational data.
- Keep SynXis URLs, ports, and tenant settings configurable rather than hard-coded in new code.
