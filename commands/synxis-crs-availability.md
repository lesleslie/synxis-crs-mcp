---
description: Check room availability for a SynXis CRS property and date range.
argument-hint: <property-id> <start-date> <end-date>
allowed-tools: mcp__synxis-crs__get_availability, mcp__synxis-crs__search_properties, mcp__synxis-crs__get_rates
---

# /synxis-crs-availability

Check available room types for a SynXis CRS property between two dates.

## Usage

`/synxis-crs-availability <property-id> <start-date> <end-date>`

Arguments:

- `<property-id>`: property identifier (e.g., `HOTEL001`). Use `/synxis-crs-lookup` first if you do not know it.
- `<start-date>`: check-in date in `YYYY-MM-DD`.
- `<end-date>`: check-out date in `YYYY-MM-DD` (must be after `start-date`).

## Workflow

1. Call `mcp__synxis-crs__get_availability` with `property_id`, `start_date`, and `end_date`.
2. Report the available room types and their `available_count`.
3. If the caller wants pricing, follow up with `mcp__synxis-crs__get_rates` using the same arguments.

## Example

`/synxis-crs-availability HOTEL001 2026-10-12 2026-10-15`
