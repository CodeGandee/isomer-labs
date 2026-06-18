# Run Context Recording

The accepted first-version design stores validated refs plus resolution source metadata when a Run, Run plan, or future Execution Adapter command request consumes Effective Topic Context.

## Accepted Choice

Option A: Durable records store selected refs, resolution sources, and consumed config or default versions. They do not store the full Effective Topic Context snapshot.

## Rationale

Effective Topic Context is a resolved process envelope, not a lifecycle object. Refs plus source metadata explain which Project, Research Topic, Topic Workspace, Research Task, config, defaults, and overrides influenced the action without copying the whole context blob into every Run.

## Consequences

- Run records stay compact and use durable refs instead of stale duplicated config.
- Audits can still explain whether a value came from a CLI selector, current directory, environment variable, `.isomer-labs/local.toml`, Project Manifest default, Research Topic Config, profile/template default, built-in default, or Workspace Runtime record.
- Forensic replay may need referenced records and consumed config/default versions.
- Process-local Effective Topic Context values do not become durable state by default.

## Rejected Alternatives

- Store the full Effective Topic Context snapshot on every Run. This is easy to inspect but duplicates config and can preserve stale or secret-adjacent values.
- Store refs only and reconstruct context later. This is compact but weakens auditability when config or defaults change.
