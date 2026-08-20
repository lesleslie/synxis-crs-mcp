---
description: Search for SynXis CRS properties by city, state, or region.
argument-hint: <location>
allowed-tools: mcp__synxis-crs__search_properties, mcp__synxis-crs__get_availability, mcp__synxis-crs__get_rates
---

# /synxis-crs-lookup

Search SynXis CRS for hotels by location.

## Usage

`/synxis-crs-lookup <location>`

Arguments:

- `<location>`: city, state, or region (e.g., `New York`, `Miami Beach`, `CA`).

## Workflow

1. Call `mcp__synxis-crs__search_properties` with `location` set to the supplied argument.
2. Surface the returned `property_id`, `name`, `brand`, `location`, and `star_rating` for each property.
3. If the caller wants to drill in, follow up with `mcp__synxis-crs__get_availability` or `mcp__synxis-crs__get_rates` for a chosen `property_id`.

## Example

`/synxis-crs-lookup Miami Beach`

Returns the properties list and points to the next-step tools (`get_availability`, `get_rates`, `create_reservation`).
