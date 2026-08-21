# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-08-21

### Added

- synxis-crs-mcp: Adopt apply_tool_profile with SYNXIS_CRS_TOOL_PROFILE (W3.3 Tier-B 2-tier)
- synxis-crs: Bodai plugin conversion (manifest, mcp.json, slash commands)

### Documentation

- synxis-crs-mcp: Tool-profile rationale update before dep refresh

### Internal

- gitignore: Untrack .pyscn/ (bodai 2026-08-20)
- synxis-crs-mcp: Add [tool.creosote] block for dep hygiene
- synxis-crs-mcp: Bootstrap [tool.crackerjack] section + uv sync upgrade
- synxis-crs-mcp: Gitignore .lycheecache (file, not just dir)
- synxis-crs-mcp: Gitignore .lycheecache + .hypothesis
- synxis-crs-mcp: Untrack .lycheecache (final)
- synxis-crs-mcp: Upgrade crackerjack 0.73.5->0.74.0, oneiric 0.16.3->0.16.5

## [0.2.1] - 2026-08-16

### Documentation

- Align README/CLAUDE with 0.2.0 release and actual tool surface

### Internal

- Untrack backup files (.backup, .backup.json, .bak)

## [0.2.0] - 2026-08-12

### Added

- synxis-crs-mcp: Plan 7 Phase 5 — FastMCP 3.4 migration

### Internal

- Adopt register_http_health_route from mcp-common
- Bump oneiric dep to >=0.16.0
- Restore LICENSE and normalize attribution
- synxis-crs-mcp: Migrate # type: ignore stragglers to ty syntax or fix
- synxis-crs-mcp: Migrate MCPBaseSettings → OneiricMCPConfig

## [0.1.5] - 2026-06-20

### Fixed

- Track .cache dir via .gitkeep for gitleaks support

### Internal

- Add mypy.ini and track .cache dir for quality tooling

## [0.1.4] - 2026-05-10

### Added

- Complete SynXis CRS MCP server implementation
- Implement real SynXis CRS API integration with OAuth2
- Initial commit - synxis-crs-mcp MCP server

### Changed

- Update config, core

### Internal

- Add Unofficial prefix to description
- Bump version to 0.1.1
- Bump version to 0.1.2
- Update LICENSE copyright to 2026

## [0.1.3] - 2026-05-10

### Added

- Implement real SynXis CRS API integration with OAuth2
