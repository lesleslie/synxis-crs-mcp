"""CRS management MCP tools.

Tools for SynXis Central Reservation System:
- search_properties: Find hotels by location
- get_availability: Check room availability
- get_rates: Get rate information
- create_reservation: Make a booking
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

from synxis_crs_mcp.client import SynXisCRSClient
from synxis_crs_mcp.config import get_logger_instance
from synxis_crs_mcp.models import (
    Availability,
    BookingRequest,
    DateRange,
    GuestInfo,
    Property,
    Rate,
    Reservation,
)

if TYPE_CHECKING:
    from fastmcp import FastMCP

logger = get_logger_instance("synxis-crs-mcp.tools")


class ToolResponse(BaseModel):
    """Standardized LLM-friendly tool response."""

    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Human-readable result message")
    data: dict[str, Any] | None = Field(
        default=None,
        description="Structured output data",
    )
    error: str | None = Field(
        default=None,
        description="Error details if operation failed",
    )
    next_steps: list[str] | None = Field(
        default=None,
        description="Suggested follow-up actions",
    )


def _property_to_dict(prop: Property) -> dict[str, Any]:
    """Convert Property to dictionary."""
    return {
        "property_id": prop.property_id,
        "name": prop.name,
        "brand": prop.brand,
        "location": prop.location,
        "address": prop.address,
        "phone": prop.phone,
        "email": prop.email,
        "star_rating": prop.star_rating,
        "amenities": prop.amenities,
    }


def _availability_to_dict(avail: Availability) -> dict[str, Any]:
    """Convert Availability to dictionary."""
    return {
        "property_id": avail.property_id,
        "date_range": {
            "start_date": str(avail.date_range.start_date),
            "end_date": str(avail.date_range.end_date),
            "nights": avail.date_range.nights,
        },
        "rooms": [
            {
                "room_type": r.room_type,
                "room_type_name": r.room_type_name,
                "max_occupancy": r.max_occupancy,
                "bed_type": r.bed_type,
                "available": r.available,
                "available_count": r.available_count,
            }
            for r in avail.rooms
        ],
        "rates:": [
            {
                "rate_plan_id": r.rate_plan_id,
                "rate_plan_name": r.rate_plan_name,
                "room_type": r.room_type,
                "base_rate": r.base_rate,
                "total_rate": r.total_rate,
                "currency": r.currency,
            }
            for r in avail.rates
        ],
        "min_rate": avail.min_rate,
        "max_rate": avail.max_rate,
    }


def _reservation_to_dict(res: Reservation) -> dict[str, Any]:
    """Convert Reservation to dictionary."""
    return {
        "reservation_id": res.reservation_id,
        "confirmation_number": res.confirmation_number,
        "property_id": res.property_id,
        "property_name": res.property_name,
        "room_type": res.room_type,
        "room_type_name": res.room_type_name,
        "status": res.status.value,
        "date_range": {
            "start_date": str(res.date_range.start_date),
            "end_date": str(res.date_range.end_date),
            "nights": res.date_range.nights,
        },
        "guest": {
            "first_name": res.guest.first_name,
            "last_name": res.guest.last_name,
            "email": res.guest.email,
        },
        "adults": res.adults,
        "children": res.children,
        "nightly_rate": res.nightly_rate,
        "total_amount": res.total_amount,
        "currency": res.currency,
        "cancellation_deadline": str(res.cancellation_deadline) if res.cancellation_deadline else None,
    }


def register_crs_tools(app: "FastMCP", client: SynXisCRSClient) -> None:
    """Register CRS management tools with the FastMCP app."""

    @app.tool()
    async def search_properties(location: str) -> ToolResponse:
        """Search for hotels by location.

        Find properties in a specific city, state, or region.

        Args:
            location: City, state, or region (e.g., 'New York', 'Miami Beach')

        Returns:
            ToolResponse with list of matching properties
        """
        logger.info("Searching properties", location=location)

        try:
            properties = await client.search_properties(location)

            return ToolResponse(
                success=True,
                message=f"Found {len(properties)} properties in {location}",
                data={
                    "location": location,
                    "properties": [_property_to_dict(p) for p in properties],
                    "count": len(properties),
                },
                next_steps=[
                    "Use get_availability to check room availability",
                    "Use get_rates to see pricing",
                    "Use create_reservation to book a room",
                ],
            )

        except Exception as e:
            logger.error("Failed to search properties", location=location, error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to search properties in {location}",
                error=str(e),
                next_steps=[
                    "Try a different location search term",
                    "Check if mock mode is enabled for testing",
                ],
            )

    @app.tool()
    async def get_availability(
        property_id: str,
        start_date: str,
        end_date: str,
    ) -> ToolResponse:
        """Check room availability for a property.

        Args:
            property_id: Property identifier (e.g., 'HOTEL001')
            start_date: Check-in date (YYYY-MM-DD)
            end_date: Check-out date (YYYY-MM-DD)

        Returns:
            ToolResponse with availability information
        """
        logger.info("Getting availability", property_id=property_id)

        try:
            date_range = DateRange(
                start_date=date.fromisoformat(start_date),
                end_date=date.fromisoformat(end_date),
            )

            availability = await client.get_availability(property_id, date_range)

            return ToolResponse(
                success=True,
                message=f"Found {len(availability.rooms)} room types for {property_id}",
                data={
                    "availability": _availability_to_dict(availability),
                },
                next_steps=[
                    "Review available room types and rates",
                    "Use get_rates for detailed pricing",
                    "Use create_reservation to book",
                ],
            )

        except Exception as e:
            logger.error("Failed to get availability", property_id=property_id, error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to check availability for {property_id}",
                error=str(e),
                next_steps=[
                    "Verify the property_id is correct",
                    "Check date format is YYYY-MM-DD",
                    "Ensure end_date is after start_date",
                ],
            )

    @app.tool()
    async def get_rates(
        property_id: str,
        start_date: str,
        end_date: str,
        room_type: str | None = None,
    ) -> ToolResponse:
        """Get rate information for a property.

        Args:
            property_id: Property identifier (e.g., 'HOTEL001')
            start_date: Check-in date (YYYY-MM-DD)
            end_date: Check-out date (YYYY-MM-DD)
            room_type: Optional room type filter (e.g., 'STD', 'DLX', 'SUI')

        Returns:
            ToolResponse with rate information
        """
        logger.info("Getting rates", property_id=property_id, room_type=room_type)

        try:
            date_range = DateRange(
                start_date=date.fromisoformat(start_date),
                end_date=date.fromisoformat(end_date),
            )

            rates = await client.get_rates(property_id, date_range, room_type)

            return ToolResponse(
                success=True,
                message=f"Found {len(rates)} rates for {property_id}",
                data={
                    "property_id": property_id,
                    "date_range": {
                        "start_date": start_date,
                        "end_date": end_date,
                        "nights": date_range.nights,
                    },
                    "rates": [
                        {
                            "rate_plan_id": r.rate_plan_id,
                            "rate_plan_name": r.rate_plan_name,
                            "room_type": r.room_type,
                            "base_rate": r.base_rate,
                            "total_rate": r.total_rate,
                            "currency": r.currency,
                            "cancellation_policy": r.cancellation_policy,
                        }
                        for r in rates
                    ],
                },
                next_steps=[
                    "Compare rates to find the best option",
                    "Use create_reservation to book a room",
                ],
            )

        except Exception as e:
            logger.error("Failed to get rates", property_id=property_id, error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to get rates for {property_id}",
                error=str(e),
                next_steps=[
                    "Verify the property_id is correct",
                    "Check date format is YYYY-MM-DD",
                ],
            )

    @app.tool()
    async def create_reservation(
        property_id: str,
        room_type: str,
        rate_plan_id: str,
        start_date: str,
        end_date: str,
        guest_first_name: str,
        guest_last_name: str,
        guest_email: str,
        adults: int = 1,
        children: int = 0,
        special_requests: str | None = None,
    ) -> ToolResponse:
        """Create a hotel reservation.

        Args:
            property_id: Property identifier (e.g., 'HOTEL001')
            room_type: Room type code (e.g., 'STD', 'DLX', 'SUI')
            rate_plan_id: Rate plan identifier
            start_date: Check-in date (YYYY-MM-DD)
            end_date: Check-out date (YYYY-MM-DD)
            guest_first_name: Guest first name
            guest_last_name: Guest last name
            guest_email: Guest email address
            adults: Number of adults (default: 1)
            children: Number of children (default: 0)
            special_requests: Optional special requests

        Returns:
            ToolResponse with reservation confirmation
        """
        logger.info("Creating reservation", property_id=property_id, guest=guest_first_name)

        try:
            booking = BookingRequest(
                property_id=property_id,
                room_type=room_type,
                rate_plan_id=rate_plan_id,
                date_range=DateRange(
                    start_date=date.fromisoformat(start_date),
                    end_date=date.fromisoformat(end_date),
                ),
                guest=GuestInfo(
                    first_name=guest_first_name,
                    last_name=guest_last_name,
                    email=guest_email,
                ),
                adults=adults,
                children=children,
                special_requests=special_requests,
            )

            reservation = await client.create_reservation(booking)

            return ToolResponse(
                success=True,
                message=f"Reservation confirmed! Confirmation #{reservation.confirmation_number}",
                data={
                    "reservation": _reservation_to_dict(reservation),
                },
                next_steps=[
                    f"Save your confirmation number: {reservation.confirmation_number}",
                    f"Free cancellation until: {reservation.cancellation_deadline}",
                    "Contact the hotel for any changes",
                ],
            )

        except Exception as e:
            logger.error("Failed to create reservation", property_id=property_id, error=str(e))
            return ToolResponse(
                success=False,
                message="Failed to create reservation",
                error=str(e),
                next_steps=[
                    "Verify all required fields are provided",
                    "Check dates are valid and available",
                    "Ensure room type and rate plan exist",
                ],
            )

    logger.info("Registered 4 CRS management tools")
