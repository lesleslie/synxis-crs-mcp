"""Regression test for Plan 7 Phase 5 — FastMCP 3.4+ baseline.

Asserts that the installed ``fastmcp`` package is on the 3.4+ baseline as
required by Plan 7 (FastMCP 3.x Ecosystem Upgrade). A downgrade below 3.4
should fail this test so the CI guard catches it.
"""

from __future__ import annotations

import fastmcp


def test_fastmcp_version_meets_plan7_baseline() -> None:
    """fastmcp.__version__ must be >= 3.4 (Plan 7 baseline)."""
    parsed = fastmcp.__version__.split(".")
    major = int(parsed[0])
    minor = int(parsed[1]) if len(parsed) > 1 else 0
    assert (major, minor) >= (3, 4), (
        f"fastmcp.__version__ is {fastmcp.__version__!r}; "
        "Plan 7 requires >= 3.4.0,<4."
    )


def test_fastmcp_version_is_below_4() -> None:
    """fastmcp must stay below the 4.x major to avoid surprise breakages."""
    parsed = fastmcp.__version__.split(".")
    major = int(parsed[0])
    assert major < 4, (
        f"fastmcp.__version__ is {fastmcp.__version__!r}; "
        "Plan 7 pins <4 to avoid surprise major-version breakages."
    )


def test_fastmcp_exposes_fastmcp_class() -> None:
    """The fastmcp top-level package must expose the FastMCP class."""
    from fastmcp import FastMCP

    assert FastMCP is not None


def test_fastmcp_exposes_context_class() -> None:
    """The fastmcp top-level package must expose the Context class."""
    from fastmcp import Context

    assert Context is not None
