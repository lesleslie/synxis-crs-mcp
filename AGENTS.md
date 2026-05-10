# Repository Guidelines

## Project Structure & Module Organization

- `synxis_crs_mcp/` contains the MCP server package, API clients, tool implementations, and config helpers for CRS integrations.
- `settings/` holds environment-specific defaults, while `docs/` and root docs should carry operator-facing guidance.
- Tests should mirror the package structure for reservation, availability, and API error-path coverage.

## Build, Test, and Development Commands

- `uv sync --group dev` installs development dependencies.
- Use the documented local server commands for smoke tests.
- `uv run pytest` runs the full suite.
- `uv run ruff check synxis_crs_mcp tests` and `uv run ruff format synxis_crs_mcp tests` cover linting and formatting.
- Run project quality checks through Crackerjack before landing changes.

## Coding Style & Naming Conventions

- Use explicit type hints, validated schemas, and small transport/client helpers around SynXis API calls.
- Keep modules snake_case and tool responses structured and consistent.

## Testing Guidelines

- Add tests for reservation flows, availability checks, and provider error handling.
- Prefer mocks or fixtures over live-network tests unless the case explicitly requires end-to-end verification.

## Commit & Pull Request Guidelines

- Use focused commits such as `fix(availability): handle empty room inventory payloads`.
- PRs should describe affected tools, commands run, and any auth or API behavior changes.

## Security & Configuration Tips

- Never commit hotel credentials, API keys, or customer data.
- Scrub guest or reservation details from shared logs and fixtures.
