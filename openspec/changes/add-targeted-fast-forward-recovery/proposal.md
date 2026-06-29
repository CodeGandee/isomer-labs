## Why

Operators often enter Topic Team Specialization through a specific subcommand, then discover that predecessor artifacts such as topic intent, registration evidence, or environment gates are missing. The current skill text tells the operator to run earlier commands manually, which makes the already complicated specialization process harder to recover from.

## What Changes

- Add targeted fast-forward recovery for blocked subcommands in `isomer-admin-topic-team-specialize`.
- When a subcommand has unmet prerequisites, require the skill to offer a bounded fast-forward path to that subcommand instead of only refusing.
- Support two recovery modes: inclusive by default, which runs missing predecessor stages and then the requested subcommand, and exclusive, which runs predecessor stages and stops before the requested subcommand.
- Keep mutation explicit by requiring user confirmation before targeted fast-forward recovery starts, unless the user has already given clear permission to proceed.
- Clarify that targeted fast-forward is bounded by the requested subcommand, while the existing full `fast-forward` path still runs through final topic-team summary output.

## Capabilities

### New Capabilities

### Modified Capabilities
- `topic-team-specialization-module-skill`: Add prerequisite recovery behavior for blocked subcommands through targeted fast-forward.

## Impact

- Affects the `isomer-admin-topic-team-specialize` skill entrypoint and relevant subcommand reference pages.
- Affects only operator skill behavior and documentation; no Python APIs, storage schema, or runtime adapter behavior change.
