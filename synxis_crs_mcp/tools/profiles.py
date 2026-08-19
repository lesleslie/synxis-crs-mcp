"""Tool profile registration groups for synxis-crs-mcp MCP server.

Maps ``ToolProfile`` levels to specific ``register_<group>_tools()`` call
lists, controlling which tools are exposed at startup based on the
``SYNXIS_CRS_TOOL_PROFILE`` environment variable.

Profile tiers (2-tier, Tier-B — synxis-crs-mcp has a single tool group
with 4 tools, so a 3-tier split adds no value):

    MINIMAL:  No tool groups registered (only ``discover_tools`` meta-tool
              + /healthz HTTP route).
    FULL:     All 4 CRS tools across 1 group (``crs_tools``).
              Default behavior — matches pre-refactor inline registration.

The dispatch surface (``PROFILE_REGISTRATIONS`` + ``_build_registration_map``
+ ``register_all_tool_groups`` + ``apply_synxis_crs_tool_profile``) is
consumed by ``synxis_crs_mcp.server.create_app`` which delegates to
``mcp_common.tools.dispatch._apply_tool_profile``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mcp_common.tools import ToolProfile
from mcp_common.tools.dispatch import ALL_TOOLS

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from fastmcp import FastMCP

    from synxis_crs_mcp.client import SynXisCRSClient

MINIMAL_REGISTRATIONS: list[str | Callable[[FastMCP], Awaitable[None] | None]] = []

FULL_REGISTRATIONS: list[str | Callable[[FastMCP], Awaitable[None] | None]] = [
    "crs_tools",
]

PROFILE_REGISTRATIONS: dict[
    ToolProfile,
    list[str | Callable[[FastMCP], Awaitable[None] | None]] | type[ALL_TOOLS],
] = {
    ToolProfile.MINIMAL: MINIMAL_REGISTRATIONS,
    ToolProfile.FULL: FULL_REGISTRATIONS,
}


def _build_registration_map() -> dict[str, Callable[[FastMCP], Awaitable[None] | None]]:
    """Build the {group_key: register_fn(app)} map.

    Local import keeps ``synxis_crs_mcp.tools.profiles`` importable without
    forcing ``synxis_crs_mcp.client`` to resolve at module import time.
    Called by ``apply_synxis_crs_tool_profile`` (not eagerly at import).

    ``register_crs_tools`` takes a 2-arg ``(app, client)`` signature; the W0
    helper expects single-arg callables, so this wrapper instantiates a
    single ``SynXisCRSClient`` at map-build time and binds it via lambda.
    The lambda also stores the client on ``app._synxis_client`` so the
    server lifespan can close the SAME client the tools use (avoids
    the orphan-httpx-client leak that a second instance would create).
    """
    from synxis_crs_mcp.client import SynXisCRSClient

    client = SynXisCRSClient()
    return {
        "crs_tools": lambda app: _register_crs_with_app(app, client),
    }


def _register_crs_with_app(app: FastMCP, client: SynXisCRSClient) -> None:
    """Bind client to app and register the CRS tools.

    Helper extracted so both ``_build_registration_map`` and
    ``register_all_tool_groups`` share the same client-binding logic.
    """
    app._synxis_client = client  # ty: ignore[unresolved-attribute]
    from synxis_crs_mcp.tools.crs_tools import register_crs_tools

    register_crs_tools(app, client)


def register_all_tool_groups(server: FastMCP) -> None:
    """Bulk register every synxis-crs-mcp tool group (called at FULL profile).

    Used as ``register_all_fn`` for the W0 helper. Instantiates a single
    ``SynXisCRSClient`` and binds it to ``server._synxis_client`` so the
    lifespan can close the same client the tools use.
    """
    from synxis_crs_mcp.client import SynXisCRSClient

    client = SynXisCRSClient()
    _register_crs_with_app(server, client)


async def apply_synxis_crs_tool_profile(server: FastMCP) -> None:
    """Apply the SYNXIS_CRS_TOOL_PROFILE dispatch to ``server`` at startup.

    Async because the W0 helper is async; called from
    ``synxis_crs_mcp.server.create_app`` via
    ``await apply_synxis_crs_tool_profile(app)``. The sync ``apply_tool_profile``
    wrapper raises RuntimeError in any async context, so this async path
    is the only correct entry point.

    No tools are mandatory at any profile level for synxis-crs-mcp —
    every tool group (including any future health-related tools) is
    opt-in per profile. The /healthz HTTP route lives outside the W0
    dispatch (registered via ``mcp_common.health.register_http_health_route``)
    so it is always available regardless of profile. We pass empty sets
    explicitly to opt out of the MANDATORY_GROUPS / MANDATORY_TOOLS
    subset check.
    """
    from mcp_common.tools.dispatch import _apply_tool_profile

    await _apply_tool_profile(
        server,
        profile_env_var="SYNXIS_CRS_TOOL_PROFILE",
        registrations=PROFILE_REGISTRATIONS,
        registration_map=_build_registration_map(),
        register_all_fn=register_all_tool_groups,
        mandatory_groups=set(),
        essential_tool_names=set(),
    )


__all__ = [
    "FULL_REGISTRATIONS",
    "MINIMAL_REGISTRATIONS",
    "PROFILE_REGISTRATIONS",
    "_build_registration_map",
    "apply_synxis_crs_tool_profile",
    "register_all_tool_groups",
]
