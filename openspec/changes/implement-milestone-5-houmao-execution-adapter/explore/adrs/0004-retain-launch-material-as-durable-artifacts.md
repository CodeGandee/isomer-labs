# Retain Adapter Launch Material as Durable Artifacts

Milestone 5 launch material is part of the reproducible record for why and how a Houmao-backed Agent Team Instance was started. Isomer will not classify adapter launch material as cache-like; generated project profiles, rendered launch files, notifier prompts, communication templates, mailbox and gateway metadata, command JSON, checksums, and launch logs must be retained as durable file-backed Artifacts or adapter payload refs with Provenance Records.

## Status

accepted, implemented as existing adapter foundation

## Considered Options

- Retain all launch material durably.
- Keep a durable manifest but mark nonessential generated material cache-like.
- Treat most launch material as cache after successful launch.

## Consequences

Workspace Runtime storage grows with each launch attempt, but debugging, audit, and replay evidence do not depend on rebuildable cache directories. The revised Milestone 5 change treats durable launch material retention as foundation and extends the same durable-evidence rule to handoff payloads, observations, normalization artifacts, and adapter logs.
