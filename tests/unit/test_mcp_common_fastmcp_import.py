"""Smoke test for Plan 7 Phase 5 — centralized FastMCP re-exports.

Verifies that ``mcp_common.fastmcp`` re-exports the FastMCP surface that
Plan 7 established as the canonical import path.
"""

from __future__ import annotations


def test_mcp_common_fastmcp_re_exports_fastmcp_class() -> None:
    """``mcp_common.fastmcp.FastMCP`` must point to the real FastMCP class."""
    from mcp_common.fastmcp import FastMCP as Reexported
    from fastmcp import FastMCP as Direct

    assert Reexported is Direct


def test_mcp_common_fastmcp_re_exports_context() -> None:
    """``mcp_common.fastmcp.Context`` must point to the real Context class."""
    from mcp_common.fastmcp import Context as Reexported
    from fastmcp import Context as Direct

    assert Reexported is Direct


def test_mcp_common_fastmcp_re_exports_middleware() -> None:
    """``mcp_common.fastmcp.Middleware`` must point to the real middleware."""
    from mcp_common.fastmcp import Middleware as Reexported
    from fastmcp.server.middleware import Middleware as Direct

    assert Reexported is Direct


def test_synxis_crs_server_imports_from_mcp_common() -> None:
    """The synxis_crs_mcp server module must import FastMCP via mcp_common.

    This is the Plan 7 Phase 5 import-path migration: every consumer
    switches from ``from fastmcp import ...`` to
    ``from mcp_common.fastmcp import ...`` so the foundation package
    becomes the single place to swap versions.
    """
    import synxis_crs_mcp.server as server_module

    module_source = getattr(server_module, "__file__", "")
    assert module_source, "synxis_crs_mcp.server must have a __file__"

    from pathlib import Path

    source_text = Path(module_source).read_text(encoding="utf-8")
    assert "from mcp_common.fastmcp import" in source_text, (
        "synxis_crs_mcp.server.py must import FastMCP via mcp_common.fastmcp "
        "(Plan 7 Phase 5 import-path migration)."
    )
    # Block the bare fastmcp top-level import in production code.
    assert "from fastmcp import" not in source_text, (
        "synxis_crs_mcp.server.py must NOT import directly from fastmcp; "
        "use mcp_common.fastmcp instead."
    )


def test_synxis_crs_tools_imports_from_mcp_common() -> None:
    """The crs_tools module's TYPE_CHECKING block must use mcp_common."""
    import synxis_crs_mcp.tools.crs_tools as tools_module

    from pathlib import Path

    module_source = getattr(tools_module, "__file__", "")
    source_text = Path(module_source).read_text(encoding="utf-8")
    assert "from mcp_common.fastmcp import FastMCP" in source_text, (
        "synxis_crs_mcp/tools/crs_tools.py must import FastMCP from "
        "mcp_common.fastmcp (Plan 7 Phase 5 import-path migration)."
    )