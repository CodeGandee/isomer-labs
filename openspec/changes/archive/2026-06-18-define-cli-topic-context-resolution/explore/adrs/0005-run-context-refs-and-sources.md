# Run Context Refs and Sources

Runs, Run plans, and future Execution Adapter command requests store validated refs, resolution source metadata, and consumed config or default versions when they consume Effective Topic Context. They do not store the full Effective Topic Context snapshot.

## Status

accepted

## Considered Options

- Store refs plus resolution source metadata and consumed config or default versions.
- Store the full Effective Topic Context snapshot on every Run.
- Store refs only and reconstruct context later.

## Consequences

Run records stay compact while preserving an audit trail for topic, workspace, task, config, defaults, and override sources. Reconstructing a full context later may need referenced records and the consumed config/default versions.
