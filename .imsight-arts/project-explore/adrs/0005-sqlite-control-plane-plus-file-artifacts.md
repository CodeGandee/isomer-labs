# SQLite Control Plane Plus File Artifacts

Isomer Labs will use a SQLite control plane plus file artifacts for durable execution state and provenance. The `.isomer-labs/manifest.toml` file discovers project-local workspaces, while each workspace can store compact state, transitions, refs, gates, and provenance in SQLite and keep rich artifacts as Markdown, JSON, logs, figures, reports, and source files.

## Status

accepted

## Considered Options

- Store all state and artifacts as files only.
- Use SQLite for compact control-plane state and files for rich artifacts.
- Use an event-log-first model and derive current state from projections.

## Consequences

- Recovery, scheduling, gate queries, and consistency validation can use SQL instead of ad hoc file scans.
- Human-readable research outputs remain inspectable as ordinary project files.
- The implementation needs schema migrations, validation commands, and a clear split between database refs and artifact paths.
