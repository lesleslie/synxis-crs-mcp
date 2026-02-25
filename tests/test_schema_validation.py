"""Schema validation tests for Synxis CRS MCP Pydantic models.

This module provides comprehensive tests to ensure all Pydantic models in the
synxis-crs-mcp project properly handle extra fields from API responses.

Test Categories:
    - test_extra_fields_ignored: Verify models accept/ignore extra fields
    - test_model_has_extra_ignore: Verify model_config has extra="ignore" or "allow"

Status:
    CURRENTLY: No Pydantic models exist in synxis_crs_mcp/
    This file serves as a template and documentation for when models are added.

Usage:
    When models are added to the project:
    1. Import them in the MODEL_IMPORTS section below
    2. Add them to the MODEL_CLASSES list
    3. Create model-specific test classes if needed
"""

from __future__ import annotations

import pytest

# =============================================================================
# MODEL IMPORTS
# =============================================================================
# TODO: Import models when they are created
# from synxis_crs_mcp.models import (
#     Hotel,
#     Room,
#     Reservation,
#     Guest,
#     Rate,
#     Availability,
# )

# Current state: No models exist yet
MODEL_CLASSES: list[type] = []

# =============================================================================
# SAMPLE API RESPONSE FIXTURES
# =============================================================================
# These fixtures contain sample Synxis CRS API response data with realistic
# structures and extra fields that models should handle gracefully.


@pytest.fixture
def sample_hotel_response() -> dict:
    """Sample hotel response from Synxis CRS API.

    Includes common fields plus extra fields that may be added by the API.
    """
    return {
        "HotelCode": "HOTEL001",
        "HotelName": "Grand Plaza Hotel",
        "ChainCode": "CHAIN01",
        "BrandCode": "BRAND01",
        "City": "New York",
        "State": "NY",
        "Country": "US",
        "PostalCode": "10001",
        "AddressLine1": "123 Main Street",
        "AddressLine2": "Suite 100",
        "PhoneNumber": "+1-555-123-4567",
        "EmailAddress": "info@grandplaza.com",
        "TimeZone": "America/New_York",
        "CurrencyCode": "USD",
        # Extra fields that may be present but not in model
        "InternalCode": "INT-12345",
        "PropertyType": "Full Service",
        "StarRating": 4.5,
        "LastUpdated": "2024-01-15T10:30:00Z",
        "ExternalSystemId": "EXT-98765",
    }


@pytest.fixture
def sample_room_response() -> dict:
    """Sample room response from Synxis CRS API."""
    return {
        "RoomCode": "KING01",
        "RoomName": "King Deluxe Room",
        "RoomType": "King",
        "BedType": "King",
        "MaxOccupancy": 2,
        "RoomSize": 350,
        "RoomSizeUnit": "sqft",
        "ViewType": "City View",
        "SmokingIndicator": False,
        "AccessibleIndicator": True,
        # Extra fields
        "InternalRoomCode": "INT-KING-01",
        "FloorRange": "10-25",
        "RenovationYear": 2023,
        "RoomFeatures": ["MiniBar", "Safe", "Robes"],
    }


@pytest.fixture
def sample_reservation_response() -> dict:
    """Sample reservation response from Synxis CRS API."""
    return {
        "ReservationID": "RES-12345678",
        "ConfirmationNumber": "CNF-87654321",
        "HotelCode": "HOTEL001",
        "RoomCode": "KING01",
        "CheckInDate": "2024-03-15",
        "CheckOutDate": "2024-03-18",
        "NumberOfNights": 3,
        "NumberOfRooms": 1,
        "AdultCount": 2,
        "ChildCount": 0,
        "RatePlanCode": "RACK",
        "RoomRate": 199.99,
        "CurrencyCode": "USD",
        "TotalAmount": 599.97,
        "ReservationStatus": "Confirmed",
        "CreateDate": "2024-02-01T14:30:00Z",
        # Extra fields
        "GroupCode": None,
        "CorporateID": "CORP-123",
        "SpecialRequests": "High floor, away from elevator",
        "LoyaltyNumber": "LOY-987654",
        "ChannelSource": "DirectWeb",
        "ModificationHistory": [
            {"Date": "2024-02-02T09:00:00Z", "Change": "Extended stay by 1 night"}
        ],
    }


@pytest.fixture
def sample_guest_response() -> dict:
    """Sample guest response from Synxis CRS API."""
    return {
        "GuestID": "GUEST-12345",
        "FirstName": "John",
        "LastName": "Doe",
        "EmailAddress": "john.doe@email.com",
        "PhoneNumber": "+1-555-987-6543",
        "CountryCode": "US",
        "AddressLine1": "456 Oak Avenue",
        "City": "Los Angeles",
        "State": "CA",
        "PostalCode": "90001",
        "Country": "US",
        "Preferences": ["Non-smoking", "High floor"],
        # Extra fields
        "MiddleName": "Robert",
        "Title": "Mr.",
        "CompanyName": "Acme Corp",
        "VIPStatus": "Gold",
        "StayHistoryCount": 15,
        "LastStayDate": "2024-01-10",
        "LoyaltyTier": "Platinum",
    }


@pytest.fixture
def sample_rate_response() -> dict:
    """Sample rate response from Synxis CRS API."""
    return {
        "RatePlanCode": "RACK",
        "RatePlanName": "Standard Rack Rate",
        "RoomCode": "KING01",
        "StartDate": "2024-03-15",
        "EndDate": "2024-03-18",
        "DailyRate": 199.99,
        "CurrencyCode": "USD",
        "TaxInclusive": False,
        "TaxAmount": 29.99,
        "TotalRate": 229.98,
        "Available": True,
        # Extra fields
        "PromotionCode": "SPRING24",
        "DiscountPercentage": 10.0,
        "RateType": "Public",
        "CancellationPolicy": "24 hours before arrival",
        "DepositRequired": True,
        "DepositAmount": 99.99,
        "Commissionable": True,
    }


@pytest.fixture
def sample_availability_response() -> dict:
    """Sample availability response from Synxis CRS API."""
    return {
        "HotelCode": "HOTEL001",
        "CheckInDate": "2024-03-15",
        "CheckOutDate": "2024-03-18",
        "RoomCode": "KING01",
        "Available": True,
        "AvailableRooms": 15,
        "TotalRooms": 20,
        "RatePlanCode": "RACK",
        "MinimumRate": 199.99,
        "MaximumRate": 299.99,
        "CurrencyCode": "USD",
        # Extra fields
        "RestrictionType": None,
        "MinimumStay": 1,
        "MaximumStay": 30,
        "ReleaseDays": 3,
        "IsPackagesAvailable": True,
        "LastUpdated": "2024-02-20T12:00:00Z",
    }


# =============================================================================
# GENERIC MODEL TESTS
# =============================================================================


class TestModelSchemaValidation:
    """Generic tests applicable to all Pydantic models.

    These tests will automatically run for any model added to MODEL_CLASSES.
    When models are created, uncomment the parametrize decorator below.
    """

    # @pytest.mark.parametrize("model_class", MODEL_CLASSES)
    # def test_extra_fields_ignored(self, model_class: type, request: pytest.FixtureRequest) -> None:
    #     """Test that models accept extra fields without raising validation errors.
    #
    #     API responses often include additional fields not in our models.
    #     Models should accept these gracefully rather than failing.
    #
    #     Args:
    #         model_class: The Pydantic model class to test
    #         request: pytest fixture request object for dynamic fixture access
    #     """
    #     # Get the appropriate sample fixture for this model
    #     fixture_name = f"sample_{model_class.__name__.lower()}_response"
    #     try:
    #         sample_data = request.getfixturevalue(fixture_name)
    #     except pytest.FixtureLookupError:
    #         # Generate generic test data if no specific fixture exists
    #         sample_data = {"test_field": "test_value", "extra_field": "extra_value"}
    #
    #     # Add extra field to ensure it's tested
    #     data_with_extras = {**sample_data, "_unexpected_field_": "should_not_cause_error"}
    #
    #     # Model should accept extra fields without raising ValidationError
    #     instance = model_class(**data_with_extras)
    #     assert instance is not None
    #
    # @pytest.mark.parametrize("model_class", MODEL_CLASSES)
    # def test_model_has_extra_ignore(self, model_class: type) -> None:
    #     """Test that model_config has extra='ignore' or extra='allow'.
    #
    #     This ensures forward compatibility with API changes that may add
    #     new fields to responses.
    #
    #     Args:
    #         model_class: The Pydantic model class to test
    #     """
    #     from pydantic import ConfigDict
    #
    #     # Check model_config
    #     if hasattr(model_class, "model_config"):
    #         config = model_class.model_config
    #         extra_value = config.get("extra", None)
    #         assert extra_value in ("ignore", "allow"), (
    #             f"{model_class.__name__}.model_config['extra'] should be 'ignore' or 'allow', "
    #             f"got {extra_value!r}"
    #         )
    #     else:
    #         pytest.fail(f"{model_class.__name__} has no model_config defined")
    pass


# =============================================================================
# MODEL-SPECIFIC TEST CLASSES (Templates)
# =============================================================================
# When models are created, copy these template classes and customize them.


class TestHotelSchema:  # noqa: D101
    """
    Template for Hotel model tests.

    When Hotel model is created:
    1. Uncomment this class
    2. Import Hotel from synxis_crs_mcp.models
    3. Customize fixtures and tests as needed
    """

    # @pytest.fixture
    # def hotel_model(self) -> type:
    #     """Return the Hotel model class."""
    #     from synxis_crs_mcp.models import Hotel
    #     return Hotel
    #
    # def test_extra_fields_ignored(self, hotel_model: type, sample_hotel_response: dict) -> None:
    #     """Test Hotel accepts extra fields."""
    #     data = {**sample_hotel_response, "future_field": "value"}
    #     hotel = hotel_model(**data)
    #     assert hotel.HotelCode == sample_hotel_response["HotelCode"]
    #
    # def test_model_has_extra_ignore(self, hotel_model: type) -> None:
    #     """Test Hotel has extra='ignore' or extra='allow'."""
    #     config = hotel_model.model_config
    #     assert config.get("extra") in ("ignore", "allow")
    pass


class TestRoomSchema:  # noqa: D101
    """
    Template for Room model tests.

    When Room model is created, uncomment and customize.
    """

    pass


class TestReservationSchema:  # noqa: D101
    """
    Template for Reservation model tests.

    When Reservation model is created, uncomment and customize.
    """

    pass


class TestGuestSchema:  # noqa: D101
    """
    Template for Guest model tests.

    When Guest model is created, uncomment and customize.
    """

    pass


class TestRateSchema:  # noqa: D101
    """
    Template for Rate model tests.

    When Rate model is created, uncomment and customize.
    """

    pass


class TestAvailabilitySchema:  # noqa: D101
    """
    Template for Availability model tests.

    When Availability model is created, uncomment and customize.
    """

    pass


# =============================================================================
# INTEGRATION TESTS
# =============================================================================


class TestSchemaIntegration:
    """Integration tests for schema validation across multiple models."""

    @pytest.mark.skip(reason="No models exist yet - enable when models are created")
    def test_all_models_have_extra_configured(self) -> None:
        """Verify all models in the models module have extra field handling."""
        pytest.skip("No models exist yet")

    @pytest.mark.skip(reason="No models exist yet - enable when models are created")
    def test_nested_model_extra_fields(self) -> None:
        """Test that nested models also handle extra fields correctly."""
        pytest.skip("No models exist yet")


# =============================================================================
# CURRENT STATE DOCUMENTATION
# =============================================================================


def test_no_models_exist_currently() -> None:
    """Document the current state: no Pydantic models exist yet.

    This test serves as documentation and will fail when models are added,
    reminding developers to update the schema validation tests.
    """
    # This assertion documents the current state
    # When models are added, this test should be updated or removed
    assert len(MODEL_CLASSES) == 0, (
        "Models have been added to MODEL_CLASSES. "
        "Please update the schema validation tests to test them properly."
    )


def test_pydantic_available() -> None:
    """Verify Pydantic is available for when models are created."""
    try:
        import pydantic  # noqa: F401

        available = True
    except ImportError:
        available = False

    # This should pass - Pydantic is typically available
    # If it fails, add pydantic to dependencies
    if not available:
        pytest.skip("Pydantic not installed - required for schema validation tests")
