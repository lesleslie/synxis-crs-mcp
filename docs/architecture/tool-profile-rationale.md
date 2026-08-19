# synxis-crs-mcp Tool Profile System

## Context

synxis-crs-mcp is a small FastMCP server (1 register group, 4 tools) that
needs to follow the Bodai ecosystem-wide convention of gating tool
registration via a `*_TOOL_PROFILE` environment variable. The convention
originates in mcp-common 0.18.0 (`mcp_common.tools.dispatch`) and has been
adopted across W1.1-W1.4 + W2a + W2b.1 + W2b.2 + W2b.3 + W3.1 + W3.2 of
the mcp-tool-profile rollout.

Pre-refactor, `synxis_crs_mcp/server.py::create_app` called the single
register function directly at startup:

```python
client = SynXisCRSClient(settings)
register_crs_tools(app, client)
```

This worked, but had no env-var gating — operators could not reduce the
tool surface for memory-constrained clients or health-probe deployments.

## Decision

synxis-crs-mcp adopts the W0 tool profile dispatch (`_apply_tool_profile`
from `mcp_common.tools.dispatch`) with a **2-tier mapping** (Tier-B per
the W3 brief). The mapping lives in `synxis_crs_mcp/tools/profiles.py`:

| Profile | Registered groups | Total tools |
|---------|-------------------|-------------|
| MINIMAL | (none)            | 0 + `discover_tools` = 1 |
| FULL    | `crs_tools`       | 4 + `discover_tools` = 5 |

`STANDARD` is intentionally **omitted** — synxis-crs-mcp has only 1
register group and 4 tools; a 3-tier split adds no operational value.
Operators who want fewer tools use `MINIMAL`; operators who want the
full surface use `FULL` (the default). No `STANDARD` middle ground
needed.

The env var is `SYNXIS_CRS_TOOL_PROFILE`. Unset / empty / unknown → FULL
(match `mcp_common.tools.ToolProfile.from_env` behavior).

## Wiring

`synxis_crs_mcp/server.py::create_app` is now `async def` and ends with:

```python
await apply_synxis_crs_tool_profile(app)
```

`apply_synxis_crs_tool_profile` (in `synxis_crs_mcp/tools/profiles.py`)
is the async wrapper around `mcp_common.tools.dispatch._apply_tool_profile`.
The sync `apply_tool_profile()` wrapper raises `RuntimeError` inside a
running event loop, so the async path is the only correct entry point
for any async startup context (and for tests that exercise `create_app`
under `asyncio`).

Sync callers (`get_app`, CLI startup) bridge via `asyncio.run(create_app())`.

## Client instantiation

`register_crs_tools` takes a 2-arg `(app, client)` signature; the W0
helper expects single-arg callables. `_build_registration_map` and
`register_all_tool_groups` both instantiate a single `SynXisCRSClient`
and bind it via a shared helper (`_register_crs_with_app`) which also
stores the client on `app._synxis_client` so the server lifespan can
close the same client the tools use. This avoids the orphan-client
leak that would result from instantiating two clients per startup.

The client init is lazy (no network call until first request), so a
single instance is safe to share across the registration phase and
the lifespan cleanup phase.

## MANDATORY_TOOLS invariant

No tools are mandatory at any profile level for synxis-crs-mcp —
every tool group (including any future health-related tools) is
opt-in per profile. The `/healthz` HTTP route lives outside the W0
dispatch (registered via `mcp_common.health.register_http_health_route`)
so it is always available regardless of profile. We pass empty sets
explicitly to opt out of the MANDATORY_GROUPS / MANDATORY_TOOLS
subset check.

`tests/unit/test_tool_profile.py::test_mandatory_tools_invariant` pins
this opt-out via `inspect.getsource` so the relationship cannot drift
silently.

## Behavioral parity

| Profile | Pre-refactor (inline) | Post-refactor (W0 helper) | Match? |
|---------|----------------------|---------------------------|--------|
| (unset) | 4 tools at startup   | 4 + `discover_tools` = 5 | YES (extra discover_tools is by design) |
| MINIMAL | (not supported)      | 0 + `discover_tools` = 1 | NEW behavior |
| FULL    | (always-on)          | 4 + `discover_tools` = 5 | YES |

The 4 CRS tool names are identical at FULL profile to the pre-refactor
inline mode (verified by
`tests/unit/test_tool_profile.py::test_full_registers_all_4_crs_tools`).
The W0 helper additionally registers the `discover_tools` meta-tool,
which is the ecosystem-wide convention (matches W1.1-W1.4 + W2a + W2b.1
+ W2b.2 + W2b.3 + W3.1 + W3.2 behavior).

The `/healthz` custom HTTP route is unchanged (registered via
`register_http_health_route(app, ...)`) — it does NOT register an MCP
tool, so it doesn't appear in `list_tools()` (intentional, per W1.4
convention).

## MANDATORY_TOOLS ⊆ REGISTRATION_MAP.keys()

Always true because mcp-common's default `MANDATORY_TOOLS` is empty.
Verified by `test_mandatory_tools_invariant`.

## Files

- `synxis_crs_mcp/tools/profiles.py` (NEW) — `PROFILE_REGISTRATIONS`,
  `_build_registration_map`, `_register_crs_with_app`,
  `register_all_tool_groups`, `apply_synxis_crs_tool_profile`
- `synxis_crs_mcp/server.py` (MODIFIED) — `create_app` now `async def`,
  ends with `await apply_synxis_crs_tool_profile(app)`; `get_app`
  bridges via `asyncio.run`
- `synxis_crs_mcp/tools/__init__.py` (MODIFIED) — exports
  `apply_synxis_crs_tool_profile` alongside `register_crs_tools`
- `tests/unit/test_tool_profile.py` (NEW) — wiring tests (AST + runtime,
  including 2 real production-path tests via `await create_app()`)
- `pyproject.toml` (MODIFIED) — `mcp-common>=0.18.0` pin (was `>=0.17.0`)
- `CLAUDE.md` (MODIFIED) — added "Tool Profile System" subsection

## Notes for downstream consumers

`create_app` is now `async`. Any existing caller that did
`from synxis_crs_mcp.server import create_app; app = create_app()` must
wrap with `asyncio.run`. The `get_app()` singleton bridge handles
the standard `app` / `http_app` access pattern unchanged.

Adding a new tool group requires editing both `FULL_REGISTRATIONS` and
`register_all_tool_groups` (intentional redundancy, matches W2a
Crackerjack / W3.1 graphics-mcp pattern).
