"""Configuration for SynXis CRS MCP server.

Uses Oneiric for layered configuration and structured logging.

Configuration loading order:
1. Default values in field definitions
2. settings/synxis-crs.yaml
3. settings/local.yaml
4. Environment variables SYNXIS_CRS_{FIELD}
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import httpx
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Oneiric logging imports
try:
    from oneiric.core.logging import LoggingConfig, configure_logging, get_logger

    ONEIRIC_LOGGING_AVAILABLE = True
except ImportError:
    ONEIRIC_LOGGING_AVAILABLE = False
    import logging

    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)

    def configure_logging(*args: Any, **kwargs: Any) -> None:
        logging.basicConfig(level=logging.INFO)


class SynXisCRSSettings(BaseSettings):
    """Settings for SynXis CRS MCP server.

    Attributes:
        client_id: OAuth2 client ID
        client_secret: OAuth2 client secret
        base_url: SynXis API base URL
        hotel_id: Default hotel/chain ID
        mock_mode: Use mock data instead of real API
        timeout: Request timeout in seconds
        enable_http_transport: Enable HTTP transport for MCP
        http_port: HTTP server port
    """

    model_config = SettingsConfigDict(
        env_prefix="SYNXIS_CRS_",
        env_file=(".env",),
        extra="ignore",
        case_sensitive=False,
    )

    # OAuth2 credentials
    client_id: str = Field(
        default="",
        description="SynXis OAuth2 client ID",
    )
    client_secret: str = Field(
        default="",
        description="SynXis OAuth2 client secret",
    )

    # API configuration
    base_url: str = Field(
        default="https://api.synxis.com/crs/v1",
        description="SynXis CRS API base URL",
    )
    hotel_id: str = Field(
        default="",
        description="Default hotel/chain ID",
    )
    timeout: float = Field(
        default=30.0,
        ge=1.0,
        le=120.0,
        description="Request timeout in seconds",
    )
    max_retries: int = Field(
        default=3,
        ge=0,
        le=5,
        description="Maximum retry attempts",
    )

    # Mock mode for testing
    mock_mode: bool = Field(
        default=False,
        description="Use mock data instead of real API",
    )

    # HTTP transport configuration
    enable_http_transport: bool = Field(
        default=False,
        description="Enable HTTP transport for MCP server",
    )
    http_host: str = Field(
        default="127.0.0.1",
        description="HTTP server bind address",
    )
    http_port: int = Field(
        default=3046,
        ge=1,
        le=65535,
        description="HTTP server port",
    )

    # Logging configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level",
    )
    log_json: bool = Field(
        default=True,
        description="Output logs as JSON",
    )

    @field_validator("base_url", mode="after")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        """Validate and normalize base URL."""
        if not v:
            return "https://api.synxis.com/crs/v1"
        return v.rstrip("/")

    def has_credentials(self) -> bool:
        """Check if OAuth2 credentials are configured."""
        return bool(self.client_id and self.client_secret)

    def get_masked_client_id(self) -> str:
        """Get masked client ID for safe logging."""
        if not self.client_id:
            return "***"
        if len(self.client_id) <= 4:
            return "***"
        return f"...{self.client_id[-4:]}"

    def http_client_config(self) -> dict[str, Any]:
        """Get HTTP client configuration."""
        return {
            "base_url": self.base_url,
            "timeout": httpx.Timeout(self.timeout),
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "synxis-crs-mcp/0.1.1",
            },
        }


def setup_logging(settings: SynXisCRSSettings | None = None) -> None:
    """Configure logging using Oneiric patterns."""
    if settings is None:
        settings = get_settings()

    if ONEIRIC_LOGGING_AVAILABLE:
        config = LoggingConfig(
            level=settings.log_level,
            emit_json=settings.log_json,
            service_name="synxis-crs-mcp",
        )
        configure_logging(config)
    else:
        logging.basicConfig(
            level=getattr(logging, settings.log_level.upper(), logging.INFO),
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        )


@lru_cache
def get_settings() -> SynXisCRSSettings:
    """Get cached settings instance."""
    return SynXisCRSSettings()


def get_logger_instance(name: str = "synxis-crs-mcp") -> Any:
    """Get a structured logger instance."""
    if ONEIRIC_LOGGING_AVAILABLE:
        return get_logger(name)
    return logging.getLogger(name)


__all__ = [
    "SynXisCRSSettings",
    "get_settings",
    "setup_logging",
    "get_logger_instance",
    "ONEIRIC_LOGGING_AVAILABLE",
]
