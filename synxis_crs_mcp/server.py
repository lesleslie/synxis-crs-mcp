"""FastMCP server for SynXis CRS management."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

from mcp_common.fastmcp import FastMCP
from mcp_common.health import register_http_health_route

from synxis_crs_mcp import __version__
from synxis_crs_mcp.config import get_logger_instance, get_settings, setup_logging
from synxis_crs_mcp.tools.profiles import apply_synxis_crs_tool_profile

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

logger = get_logger_instance("synxis-crs-mcp.server")

APP_NAME = "synxis-crs-mcp"
APP_VERSION = __version__


async def create_app() -> FastMCP:
    """Create and configure the FastMCP application (async).

    Tool profile dispatch is async because the W0 helper from
    mcp-common 0.18.0 (``_apply_tool_profile``) is async. Per the
    W2b.3 lesson, the sync ``apply_tool_profile`` wrapper raises
    ``RuntimeError`` when called from inside a running event loop, so
    the async path is the only correct entry point for any async
    startup context (and for tests that exercise ``create_app`` under
    ``asyncio``).

    Callers from sync contexts (CLI startup, ``get_app``) wrap with
    ``asyncio.run(create_app())``.
    """
    settings = get_settings()
    setup_logging(settings)

    logger.info(
        "Initializing SynXis CRS MCP server",
        version=APP_VERSION,
        mock_mode=settings.mock_mode,
        http_transport=settings.enable_http_transport,
    )

    if not settings.has_credentials() and not settings.mock_mode:
        logger.warning(
            "OAuth2 credentials not configured. Set SYNXIS_CRS_CLIENT_ID and "
            "SYNXIS_CRS_CLIENT_SECRET, or use mock_mode=True for testing."
        )

    app = FastMCP(
        name=APP_NAME,
        version=APP_VERSION,
    )

    # HTTP health endpoint for Claude Code compatibility
    register_http_health_route(
        app,
        service_name="synxis-crs",
        version=APP_VERSION,
    )

    @app.custom_route("/healthz", methods=["GET"])
    async def healthz_check(request: Any) -> Any:
        """Kubernetes-style health check endpoint."""
        from starlette.responses import JSONResponse

        return JSONResponse({"status": "ok"})

    original_lifespan = app._mcp_server.lifespan

    @asynccontextmanager
    async def lifespan(server: Any) -> AsyncGenerator[dict[str, Any]]:
        async with original_lifespan(server) as state:
            try:
                yield state
            finally:
                client = getattr(app, "_synxis_client", None)
                if client is not None:
                    await client.close()
                logger.info("SynXis CRS client closed")

    app._mcp_server.lifespan = lifespan

    # Apply tool profile dispatch (SYNXIS_CRS_TOOL_PROFILE env var).
    #
    # Replaces the previous direct CRS tool registration call.
    # The W0 helper from mcp-common 0.18.0+ dispatches by group name and
    # always registers the ``discover_tools`` meta-tool. The default
    # (no env var) remains FULL = all 4 CRS tools — the previous behavior
    # is preserved.
    await apply_synxis_crs_tool_profile(app)

    logger.info("SynXis CRS MCP server initialized")
    return app


_app: FastMCP | None = None


def get_app() -> FastMCP:
    """Get the singleton FastMCP application (sync wrapper).

    Bridges to the async ``create_app`` via ``asyncio.run``. This works
    because the FastMCP app-building phase does not require a running
    event loop — only the tool profile dispatch needs an async context.
    """
    global _app
    if _app is None:
        _app = asyncio.run(create_app())
    return _app


def __getattr__(name: str) -> Any:
    """Lazy attribute access."""
    if name == "app":
        return get_app()
    if name == "http_app":
        return get_app().http_app
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = ["APP_NAME", "APP_VERSION", "create_app", "get_app"]
