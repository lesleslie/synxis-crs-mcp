"""FastMCP server for SynXis CRS management."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

from fastmcp import FastMCP

from synxis_crs_mcp import __version__
from synxis_crs_mcp.client import SynXisCRSClient
from synxis_crs_mcp.config import get_logger_instance, get_settings, setup_logging
from synxis_crs_mcp.tools import register_crs_tools

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

logger = get_logger_instance("synxis-crs-mcp.server")

APP_NAME = "synxis-crs-mcp"
APP_VERSION = __version__


def create_app() -> FastMCP:
    """Create and configure the FastMCP application."""
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

    client = SynXisCRSClient(settings)
    register_crs_tools(app, client)

    original_lifespan = app._mcp_server.lifespan

    @asynccontextmanager
    async def lifespan(server: Any) -> AsyncGenerator[dict[str, Any]]:
        async with original_lifespan(server) as state:
            try:
                yield state
            finally:
                await client.close()
                logger.info("SynXis CRS client closed")

    app._mcp_server.lifespan = lifespan
    app._synxis_client = client  # type: ignore[attr-defined]

    logger.info("SynXis CRS MCP server initialized")
    return app


_app: FastMCP | None = None


def get_app() -> FastMCP:
    """Get or create the FastMCP application."""
    global _app
    if _app is None:
        _app = create_app()
    return _app


def __getattr__(name: str) -> Any:
    """Lazy attribute access."""
    if name == "app":
        return get_app()
    if name == "http_app":
        return get_app().http_app
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = ["create_app", "get_app", "APP_NAME", "APP_VERSION"]
