"""MCP tools for SynXis CRS management."""

from synxis_crs_mcp.tools.crs_tools import register_crs_tools
from synxis_crs_mcp.tools.profiles import apply_synxis_crs_tool_profile

__all__ = ["apply_synxis_crs_tool_profile", "register_crs_tools"]
