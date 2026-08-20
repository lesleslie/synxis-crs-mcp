---
description: Create a SynXis CRS hotel reservation with guest details and dates.
argument-hint: <property-id> <room-type> <rate-plan-id> <start-date> <end-date> <guest-first-name> <guest-last-name> <guest-email> [--adults N] [--children N] [--special-requests "..."]
allowed-tools: mcp__synxis-crs__create_reservation, mcp__synxis-crs__search_properties, mcp__synxis-crs__get_availability, mcp__synxis-crs__get_rates
---

# /synxis-crs-reservation

Create a hotel reservation through SynXis CRS.

## Usage

`/synxis-crs-reservation <property-id> <room-type> <rate-plan-id> <start-date> <end-date> <guest-first-name> <guest-last-name> <guest-email> [--adults N] [--children N] [--special-requests "..."]`

Arguments:

- `<property-id>`: property identifier (e.g., `HOTEL001`).
- `<room-type>`: room type code (e.g., `STD`, `DLX`, `SUI`).
- `<rate-plan-id>`: rate plan identifier from `get_rates`.
- `<start-date>`: check-in date in `YYYY-MM-DD`.
- `<end-date>`: check-out date in `YYYY-MM-DD`.
- `<guest-first-name>`, `<guest-last-name>`, `<guest-email>`: guest contact details.
- `--adults N`: optional, defaults to `1`.
- `--children N`: optional, defaults to `0`.
- `--special-requests "..."`: optional free-form text.

## Workflow

1. If the caller does not already have a `rate_plan_id`, call `mcp__synxis-crs__get_rates` first to surface the live plans.
2. Call `mcp__synxis-crs__create_reservation` with the validated arguments.
3. Report the returned `confirmation_number`, `total_amount`, and `cancellation_deadline`.

## Example

`/synxis-crs-reservation HOTEL001 DLX RP-FLEX 2026-10-12 2026-10-15 Jane Doe jane@example.com --adults 2 --special-requests "high floor"`
