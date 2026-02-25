"""Pydantic models for SynXis CRS API.

SynXis CRS (Central Reservation System) API models for:
- Property search and management
- Rate management
- Availability/inventory
- Booking creation and management

API Documentation: https://developer.synxis.com/
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class RoomType(str, Enum):
    """Room type categories."""

    STANDARD = "STANDARD"
    DELUXE = "DELUXE"
    SUITE = "SUITE"
    EXECUTIVE = "EXECUTIVE"
    PRESIDENTIAL = "PRESIDENTIAL"


class RatePlanType(str, Enum):
    """Rate plan categories."""

    BAR = "BAR"  # Best Available Rate
    CORPORATE = "CORPORATE"
    PACKAGE = "PACKAGE"
    PROMOTIONAL = "PROMOTIONAL"
    GROUP = "GROUP"


class ReservationStatus(str, Enum):
    """Reservation status values."""

    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"
    NO_SHOW = "NO_SHOW"


class DateRange(BaseModel):
    """Date range for searches and bookings."""

    start_date: date = Field(description="Start date (check-in)")
    end_date: date = Field(description="End date (check-out)")

    @field_validator("end_date", mode="after")
    @classmethod
    def validate_end_date(cls, v: date, info: Any) -> date:
        """Ensure end_date is after start_date."""
        if "start_date" in info.data and v <= info.data["start_date"]:
            raise ValueError("end_date must be after start_date")
        return v

    @property
    def nights(self) -> int:
        """Calculate number of nights."""
        return (self.end_date - self.start_date).days


class Property(BaseModel):
    """A hotel property from SynXis CRS."""

    property_id: str = Field(description="Unique property identifier")
    name: str = Field(description="Property name")
    brand: str | None = Field(default=None, description="Brand name")
    location: str | None = Field(default=None, description="City, State/Country")
    address: str | None = Field(default=None, description="Full address")
    phone: str | None = Field(default=None, description="Contact phone")
    email: str | None = Field(default=None, description="Contact email")
    star_rating: int | None = Field(
        default=None,
        description="Star rating (1-5)",
        ge=1,
        le=5,
    )
    amenities: list[str] = Field(
        default_factory=list,
        description="List of amenities",
    )


class Room(BaseModel):
    """A room type with availability."""

    room_type: str = Field(description="Room type code")
    room_type_name: str = Field(description="Room type display name")
    description: str | None = Field(default=None, description="Room description")
    max_occupancy: int = Field(default=2, description="Maximum occupancy")
    bed_type: str | None = Field(default=None, description="Bed configuration")
    available: bool = Field(default=True, description="Is room available")
    available_count: int | None = Field(default=None, description="Number available")


class Rate(BaseModel):
    """A rate plan for a room."""

    rate_plan_id: str = Field(description="Rate plan identifier")
    rate_plan_name: str = Field(description="Rate plan display name")
    rate_plan_type: RatePlanType = Field(description="Rate plan category")
    room_type: str = Field(description="Associated room type")
    base_rate: float = Field(description="Base nightly rate", ge=0)
    currency: str = Field(default="USD", description="Currency code")
    taxes: float | None = Field(default=None, description="Tax amount", ge=0)
    fees: float | None = Field(default=None, description="Additional fees", ge=0)
    total_rate: float | None = Field(default=None, description="Total rate per night")
    cancellation_policy: str | None = Field(
        default=None,
        description="Cancellation policy description",
    )
    deposit_required: bool = Field(default=False, description="Is deposit required")
    deposit_amount: float | None = Field(default=None, description="Deposit amount")


class Availability(BaseModel):
    """Room availability for a property."""

    property_id: str = Field(description="Property identifier")
    date_range: DateRange = Field(description="Requested date range")
    rooms: list[Room] = Field(
        default_factory=list,
        description="Available room types",
    )
    rates: list[Rate] = Field(
        default_factory=list,
        description="Available rates",
    )
    min_rate: float | None = Field(default=None, description="Minimum available rate")
    max_rate: float | None = Field(default=None, description="Maximum available rate")


class GuestInfo(BaseModel):
    """Guest information for booking."""

    first_name: str = Field(description="Guest first name")
    last_name: str = Field(description="Guest last name")
    email: str | None = Field(default=None, description="Guest email")
    phone: str | None = Field(default=None, description="Guest phone")
    address: str | None = Field(default=None, description="Guest address")
    city: str | None = Field(default=None, description="Guest city")
    country: str | None = Field(default=None, description="Guest country code")
    loyalty_number: str | None = Field(default=None, description="Loyalty program number")


class BookingRequest(BaseModel):
    """Request to create a reservation."""

    property_id: str = Field(description="Property identifier")
    room_type: str = Field(description="Room type code")
    rate_plan_id: str = Field(description="Rate plan identifier")
    date_range: DateRange = Field(description="Stay dates")
    guest: GuestInfo = Field(description="Guest information")
    adults: int = Field(default=1, description="Number of adults", ge=1)
    children: int = Field(default=0, description="Number of children", ge=0)
    special_requests: str | None = Field(default=None, description="Special requests")
    guarantee_type: str = Field(
        default="CC",
        description="Guarantee type (CC, DEPOSIT, PREPAID)",
    )
    credit_card: dict[str, str] | None = Field(
        default=None,
        description="Credit card details (tokenized)",
    )


class Reservation(BaseModel):
    """A confirmed reservation."""

    reservation_id: str = Field(description="Unique reservation identifier")
    confirmation_number: str = Field(description="Guest-facing confirmation number")
    property_id: str = Field(description="Property identifier")
    property_name: str | None = Field(default=None, description="Property name")
    room_type: str = Field(description="Room type code")
    room_type_name: str | None = Field(default=None, description="Room type name")
    rate_plan_id: str = Field(description="Rate plan identifier")
    rate_plan_name: str | None = Field(default=None, description="Rate plan name")
    status: ReservationStatus = Field(description="Reservation status")
    date_range: DateRange = Field(description="Stay dates")
    guest: GuestInfo = Field(description="Guest information")
    adults: int = Field(default=1, description="Number of adults")
    children: int = Field(default=0, description="Number of children")
    nightly_rate: float = Field(description="Rate per night")
    total_amount: float = Field(description="Total reservation amount")
    currency: str = Field(default="USD", description="Currency code")
    special_requests: str | None = Field(default=None, description="Special requests")
    cancellation_deadline: date | None = Field(
        default=None,
        description="Free cancellation deadline",
    )
    created_at: str | None = Field(default=None, description="Creation timestamp")


class SynXisError(Exception):
    """Exception raised for SynXis API errors."""

    def __init__(
        self,
        message: str,
        status: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for API responses."""
        result: dict[str, Any] = {
            "error": self.message,
            "status": self.status,
        }
        if self.details:
            result["details"] = self.details
        return result


__all__ = [
    "RoomType",
    "RatePlanType",
    "ReservationStatus",
    "DateRange",
    "Property",
    "Room",
    "Rate",
    "Availability",
    "GuestInfo",
    "BookingRequest",
    "Reservation",
    "SynXisError",
]
