"""SynXis CRS MCP - MCP server for SynXis Central Reservation System."""

from importlib.metadata import version as _importlib_version

from synxis_crs_mcp.client import SynXisCRSClient
from synxis_crs_mcp.config import SynXisCRSSettings, get_settings, setup_logging
from synxis_crs_mcp.models import (
    Availability,
    BookingRequest,
    DateRange,
    GuestInfo,
    Property,
    Rate,
    Reservation,
    SynXisError,
)

__version__ = _importlib_version("synxis-crs-mcp")

__all__ = [
    "Availability",
    "BookingRequest",
    "DateRange",
    "GuestInfo",
    "Property",
    "Rate",
    "Reservation",
    "SynXisCRSClient",
    "SynXisCRSSettings",
    "SynXisError",
    "__version__",
    "get_settings",
    "setup_logging",
]
