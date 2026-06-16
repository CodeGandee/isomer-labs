# SQLite Control Plane Plus File Artifacts

Isomer Labs will use a SQLite control plane plus file artifacts for durable workspace state and provenance. The Project Manifest at `.isomer-labs/manifest.toml` discovers project-local Isomer Workspaces that back Research Threads, while each Workspace Runtime can store compact state, transitions, refs, Gates, Run records, and provenance in SQLite and keep rich Artifacts as Markdown, JSON, logs, figures, reports, and source files.

## Status

accepted

## Considered Options

- Store all state and artifacts as files only.
- Use SQLite for compact control-plane state and files for rich artifacts.
- Use an event-log-first model and derive current state from projections.

## Consequences

- Recovery, scheduling, gate queries, and consistency validation can use SQL instead of ad hoc file scans.
- Human-readable research outputs remain inspectable as ordinary project files.
- Per-agent Agent Workspaces can hold Agent Runtime files and Agent Artifacts for concrete Agent Instances while SQLite records ownership, advisory Workspace Boundaries, and provenance links.
- The implementation needs schema migrations, validation commands, and a clear split between database refs and artifact paths.
