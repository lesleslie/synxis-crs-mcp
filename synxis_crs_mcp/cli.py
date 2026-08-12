"""Unified CLI for SynXis CRS MCP server using mcp-common.

Provides standard lifecycle commands (start, stop, restart, status, health).
"""

from __future__ import annotations

import os
import warnings
from pathlib import Path

os.environ["TRANSFORMERS_VERBOSITY"] = "error"
warnings.filterwarnings("ignore", message=".*PyTorch.*TensorFlow.*Flax.*")

import uvicorn
from mcp_common import MCPServerCLIFactory
from mcp_common.cli.health import RuntimeHealthSnapshot
from oneiric.core.config import OneiricMCPConfig, load_settings

from synxis_crs_mcp import __version__


class SynXisCRSSettings(OneiricMCPConfig):
    """SynXis CRS MCP server settings extending OneiricMCPConfig.

    The legacy ``MCPServerSettings`` exposed a flat YAML schema with keys
    like ``server_name``, ``cache_root``, ``health_ttl_seconds`` and
    ``log_level``. We keep the same surface (tests, factory code, and
    operator-facing YAML all reference these names) but back it with
    :class:`oneiric.core.config.OneiricMCPConfig` so the ecosystem
    deprecation of ``MCPBaseSettings`` / ``MCPServerSettings`` does not
    leak into SynXis CRS MCP.
    """

    server_name: str = "synxis-crs-mcp"
    http_port: int = 3046
    http_host: str = "127.0.0.1"
    enable_http_transport: bool = False
    cache_root: Path = Path(".oneiric_cache")
    health_ttl_seconds: float = 60.0
    log_level: str = "INFO"
    startup_timeout: int = 10
    shutdown_timeout: int = 10
    force_kill_timeout: int = 5

    def pid_path(self) -> Path:
        """Get PID file path."""
        return self.cache_root / "mcp_server.pid"

    def health_snapshot_path(self) -> Path:
        """Get runtime health snapshot path."""
        return self.cache_root / "runtime_health.json"

    def telemetry_snapshot_path(self) -> Path:
        """Get runtime telemetry snapshot path."""
        return self.cache_root / "runtime_telemetry.json"

    @classmethod
    def load(
        cls,
        server_name: str = "synxis-crs-mcp",
        config_path: str | os.PathLike[str] | None = None,
    ) -> SynXisCRSSettings:
        """Backwards-compatible loader preserving the ``MCPServerSettings.load`` API."""
        loaded = load_settings(
            path=str(config_path) if config_path else None,
            project_name=server_name,
        )
        name = getattr(loaded.app, "name", server_name) or server_name
        return cls(server_name=name)


def start_server_handler() -> None:
    """Start handler that launches the SynXis CRS MCP server in HTTP mode."""
    settings = SynXisCRSSettings()
    print(f"Starting SynXis CRS MCP server on port {settings.http_port}...")
    uvicorn.run(
        "synxis_crs_mcp.server:http_app",
        host="127.0.0.1",
        port=settings.http_port,
        log_level="info",
    )


def health_probe_handler() -> RuntimeHealthSnapshot:
    """Health probe handler for SynXis CRS MCP server."""
    from synxis_crs_mcp.config import get_settings

    settings = get_settings()
    return RuntimeHealthSnapshot(
        orchestrator_pid=os.getpid(),
        watchers_running=False,
        remote_enabled=False,
        lifecycle_state={
            "server_name": "synxis-crs-mcp",
            "status": "healthy",
            "version": __version__,
        },
        activity_state={
            "credentials_configured": settings.has_credentials(),
            "mock_mode": settings.mock_mode,
        },
    )


factory = MCPServerCLIFactory(
    server_name="synxis-crs-mcp",
    settings=None,
    start_handler=start_server_handler,
    health_probe_handler=health_probe_handler,
)

app = factory.create_app()


def main() -> None:
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
