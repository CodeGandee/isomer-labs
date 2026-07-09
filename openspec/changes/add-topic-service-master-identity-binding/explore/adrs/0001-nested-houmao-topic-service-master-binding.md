# Nested Houmao Topic Service Master Binding

Status: accepted

The Topic Workspace Manifest will store Topic Service Master service metadata in `[topic_service_master]` and Houmao-specific names or refs in `[topic_service_master.houmao]`. This keeps the Topic Service Master binding first-class in Isomer while preventing Houmao specialist, launch profile, and managed-agent fields from becoming top-level Topic Workspace Manifest concepts.

## Considered Options

- Flat `[topic_service_master]` table with provider, status, and all Houmao fields.
- Generic `[[service_agents]]` collection with a Topic Service Master entry.
- Isomer-level `[topic_service_master]` table plus nested `[topic_service_master.houmao]` provider details.

## Consequences

Manifest parsing and write helpers need a nested provider-details object. Future providers can add their own nested table without changing the Isomer-level Topic Service Master status shape.
