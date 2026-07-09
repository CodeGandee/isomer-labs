# Topic Service Master Binding Shape

## Decision

Use `[topic_service_master]` for Isomer-level service metadata and `[topic_service_master.houmao]` for Houmao-specific specialist, launch profile, and managed-agent names or refs.

## Why

The architecture keeps Houmao concepts inside the Execution Adapter boundary unless a spec explicitly promotes them. Topic Service Master identity is an Isomer concept, but Houmao specialist and managed-agent details are provider-specific, so nesting those details preserves the boundary while still giving skills deterministic context.

## Rejected Alternatives

- A flat `[topic_service_master]` table is simpler, but it promotes provider fields into the top-level manifest.
- A generic `[[service_agents]]` table is more extensible, but it introduces abstraction before Isomer has a second Topic Workspace service-agent binding.

## Follow-up Decision

Isomer records the Topic Workspace Manifest binding only after Houmao-owned preparation reports concrete created or updated entities. `planned`, `blocked`, and `skipped` outcomes remain command or readiness outcomes rather than manifest binding statuses.
