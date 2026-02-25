"""SynXis CRS API client with mock mode support.

This module provides an async HTTP client for interacting with the SynXis CRS API.
It supports mock mode for testing without real API access.

API Documentation: https://developer.synxis.com/
"""

from __future__ import annotations

import asyncio
import random
from datetime import date, timedelta
from typing import Any

import httpx

from .config import SynXisCRSSettings, get_logger_instance, get_settings
from .models import (
    Availability,
    BookingRequest,
    DateRange,
    Property,
    Rate,
    Reservation,
    ReservationStatus,
    Room,
    SynXisError,
)

logger = get_logger_instance("synxis-crs-mcp.client")

# =============================================================================
# Mock Data for Testing
# =============================================================================

MOCK_PROPERTIES: list[dict[str, Any]] = [
    {
        "property_id": "HOTEL001",
        "name": "Grand Plaza Hotel",
        "brand": "Grand Hotels",
        "location": "New York, NY, USA",
        "address": "123 Main Street, New York, NY 10001",
        "phone": "+1-212-555-0100",
        "email": "reservations@grandplaza.com",
        "star_rating": 5,
        "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Gym", "Valet"],
    },
    {
        "property_id": "HOTEL002",
        "name": "Seaside Resort",
        "brand": "Coastal Inns",
        "location": "Miami Beach, FL, USA",
        "address": "456 Ocean Drive, Miami Beach, FL 33139",
        "phone": "+1-305-555-0200",
        "email": "bookings@seasideresort.com",
        "star_rating": 4,
        "amenities": ["WiFi", "Beach Access", "Pool", "Restaurant", "Water Sports"],
    },
    {
        "property_id": "HOTEL003",
        "name": "Mountain Lodge",
        "brand": "Alpine Retreats",
        "location": "Aspen, CO, USA",
        "address": "789 Summit Road, Aspen, CO 81611",
        "phone": "+1-970-555-0300",
        "email": "stay@mountainlodge.com",
        "star_rating": 4,
        "amenities": ["WiFi", "Ski Access", "Spa", "Restaurant", "Fireplace"],
    },
]

MOCK_ROOM_TYPES: list[dict[str, Any]] = [
    {"room_type": "STD", "room_type_name": "Standard Room", "max_occupancy": 2, "bed_type": "Queen"},
    {"room_type": "DLX", "room_type_name": "Deluxe Room", "max_occupancy": 2, "bed_type": "King"},
    {"room_type": "SUI", "room_type_name": "Suite", "max_occupancy": 4, "bed_type": "King + Sofa"},
    {"room_type": "EXE", "room_type_name": "Executive Suite", "max_occupancy": 4, "bed_type": "King + Twin"},
]


class SynXisCRSClient:
    """Async HTTP client for SynXis CRS API with mock mode support."""

    def __init__(self, settings: SynXisCRSSettings | None = None) -> None:
        """Initialize the SynXis CRS client."""
        self.settings = settings or get_settings()
        self._client: httpx.AsyncClient | None = None
        self._access_token: str | None = None

    async def __aenter__(self) -> "SynXisCRSClient":
        """Async context manager entry."""
        if not self.settings.mock_mode:
            await self._ensure_client()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self.close()

    async def _ensure_client(self) -> httpx.AsyncClient:
        """Ensure HTTP client is initialized."""
        if self._client is None:
            config = self.settings.http_client_config()
            self._client = httpx.AsyncClient(**config)
            logger.debug(
                "HTTP client initialized",
                base_url=config["base_url"],
                mock_mode=self.settings.mock_mode,
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
            logger.debug("HTTP client closed")

    async def _get_access_token(self) -> str:
        """Get OAuth2 access token."""
        if self._access_token:
            return self._access_token

        # In real implementation, this would call the OAuth2 token endpoint
        # For now, return a mock token
        self._access_token = "mock_access_token_12345"
        return self._access_token

    # =========================================================================
    # Mock Implementations
    # =========================================================================

    def _mock_search_properties(self, location: str) -> list[Property]:
        """Generate mock property search results."""
        results = []
        for prop_data in MOCK_PROPERTIES:
            if location.lower() in prop_data["location"].lower():
                results.append(Property(**prop_data))
        return results or [Property(**MOCK_PROPERTIES[0])]

    def _mock_get_availability(
        self,
        property_id: str,
        date_range: DateRange,
    ) -> Availability:
        """Generate mock availability data."""
        # Generate random available rooms and rates
        rooms = []
        rates = []
        min_rate = float("inf")
        max_rate = 0.0

        for room_data in MOCK_ROOM_TYPES:
            available = random.random() > 0.2  # 80% chance of availability
            room = Room(
                room_type=room_data["room_type"],
                room_type_name=room_data["room_type_name"],
                max_occupancy=room_data["max_occupancy"],
                bed_type=room_data["bed_type"],
                available=available,
                available_count=random.randint(1, 10) if available else 0,
            )
            rooms.append(room)

            if available:
                # Generate rates for this room
                base_rate = random.uniform(99.0, 499.0)
                rate = Rate(
                    rate_plan_id=f"RATE_{room_data['room_type']}_BAR",
                    rate_plan_name="Best Available Rate",
                    rate_plan_type="BAR",
                    room_type=room_data["room_type"],
                    base_rate=round(base_rate, 2),
                    currency="USD",
                    taxes=round(base_rate * 0.12, 2),
                    total_rate=round(base_rate * 1.12, 2),
                    cancellation_policy="Free cancellation up to 24 hours before check-in",
                    deposit_required=False,
                )
                rates.append(rate)
                min_rate = min(min_rate, rate.total_rate or base_rate)
                max_rate = max(max_rate, rate.total_rate or base_rate)

        return Availability(
            property_id=property_id,
            date_range=date_range,
            rooms=rooms,
            rates=rates,
            min_rate=round(min_rate, 2) if min_rate != float("inf") else None,
            max_rate=round(max_rate, 2) if max_rate > 0 else None,
        )

    def _mock_create_reservation(self, booking: BookingRequest) -> Reservation:
        """Generate mock reservation confirmation."""
        import uuid

        reservation_id = str(uuid.uuid4())[:8].upper()
        confirmation_number = f"SYN{random.randint(100000, 999999)}"

        # Calculate total
        nightly_rate = random.uniform(150.0, 400.0)
        total_amount = nightly_rate * booking.date_range.nights

        return Reservation(
            reservation_id=reservation_id,
            confirmation_number=confirmation_number,
            property_id=booking.property_id,
            property_name="Grand Plaza Hotel",
            room_type=booking.room_type,
            room_type_name="Deluxe Room",
            rate_plan_id=booking.rate_plan_id,
            rate_plan_name="Best Available Rate",
            status=ReservationStatus.CONFIRMED,
            date_range=booking.date_range,
            guest=booking.guest,
            adults=booking.adults,
            children=booking.children,
            nightly_rate=round(nightly_rate, 2),
            total_amount=round(total_amount, 2),
            currency="USD",
            special_requests=booking.special_requests,
            cancellation_deadline=booking.date_range.start_date - timedelta(days=1),
            created_at=date.today().isoformat(),
        )

    # =========================================================================
    # Public API Methods
    # =========================================================================

    async def search_properties(self, location: str) -> list[Property]:
        """Search for properties by location.

        Args:
            location: City, state, or region to search

        Returns:
            List of matching properties
        """
        logger.info("Searching properties", location=location, mock_mode=self.settings.mock_mode)

        if self.settings.mock_mode:
            return self._mock_search_properties(location)

        # Real API implementation would go here
        raise SynXisError(
            message="Real API not implemented. Use mock_mode=True for testing.",
            status=501,
        )

    async def get_availability(
        self,
        property_id: str,
        date_range: DateRange,
    ) -> Availability:
        """Get room availability for a property.

        Args:
            property_id: Property identifier
            date_range: Date range to check

        Returns:
            Availability information
        """
        logger.info(
            "Getting availability",
            property_id=property_id,
            dates=f"{date_range.start_date} to {date_range.end_date}",
            mock_mode=self.settings.mock_mode,
        )

        if self.settings.mock_mode:
            return self._mock_get_availability(property_id, date_range)

        raise SynXisError(
            message="Real API not implemented. Use mock_mode=True for testing.",
            status=501,
        )

    async def get_rates(
        self,
        property_id: str,
        date_range: DateRange,
        room_type: str | None = None,
    ) -> list[Rate]:
        """Get available rates for a property.

        Args:
            property_id: Property identifier
            date_range: Date range to check
            room_type: Optional room type filter

        Returns:
            List of available rates
        """
        logger.info("Getting rates", property_id=property_id, mock_mode=self.settings.mock_mode)

        if self.settings.mock_mode:
            availability = self._mock_get_availability(property_id, date_range)
            rates = availability.rates
            if room_type:
                rates = [r for r in rates if r.room_type == room_type]
            return rates

        raise SynXisError(
            message="Real API not implemented. Use mock_mode=True for testing.",
            status=501,
        )

    async def create_reservation(self, booking: BookingRequest) -> Reservation:
        """Create a new reservation.

        Args:
            booking: Booking request details

        Returns:
            Confirmed reservation
        """
        logger.info(
            "Creating reservation",
            property_id=booking.property_id,
            guest=booking.guest.first_name,
            mock_mode=self.settings.mock_mode,
        )

        if self.settings.mock_mode:
            return self._mock_create_reservation(booking)

        raise SynXisError(
            message="Real API not implemented. Use mock_mode=True for testing.",
            status=501,
        )

    async def get_reservation(self, reservation_id: str) -> Reservation | None:
        """Get reservation details.

        Args:
            reservation_id: Reservation identifier

        Returns:
            Reservation details or None if not found
        """
        logger.info("Getting reservation", reservation_id=reservation_id)

        if self.settings.mock_mode:
            # Return a mock reservation
            return Reservation(
                reservation_id=reservation_id,
                confirmation_number="SYN123456",
                property_id="HOTEL001",
                property_name="Grand Plaza Hotel",
                room_type="DLX",
                room_type_name="Deluxe Room",
                rate_plan_id="RATE_DLX_BAR",
                rate_plan_name="Best Available Rate",
                status=ReservationStatus.CONFIRMED,
                date_range=DateRange(
                    start_date=date.today() + timedelta(days=7),
                    end_date=date.today() + timedelta(days=10),
                ),
                guest={
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john.doe@example.com",
                },
                adults=2,
                children=0,
                nightly_rate=199.99,
                total_amount=599.97,
                currency="USD",
            )

        raise SynXisError(
            message="Real API not implemented. Use mock_mode=True for testing.",
            status=501,
        )


__all__ = ["SynXisCRSClient"]
