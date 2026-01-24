"""Pytest configuration for synxis-crs-mcp tests."""
import pytest


@pytest.fixture
def sample_config():
    """Sample configuration fixture for tests."""
    return {
        "test": "value",
    }
