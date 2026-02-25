"""SynXis CRS MCP - MCP server for SynXis Central Reservation System."""

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

__version__ = "0.1.1"

__all__ = [
    "SynXisCRSClient",
    "SynXisCRSSettings",
    "get_settings",
    "setup_logging",
    "Availability",
    "BookingRequest",
    "DateRange",
    "GuestInfo",
    "Property",
    "Rate",
    "Reservation",
    "SynXisError",
    "__version__",
]
