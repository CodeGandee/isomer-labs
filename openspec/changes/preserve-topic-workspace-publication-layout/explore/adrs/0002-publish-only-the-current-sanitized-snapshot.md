# Publish Only the Current Sanitized Snapshot

The publication remote will expose the current sanitized Topic Workspace state on canonical branch `main`; it will not preserve publication history or retain `topic-workspace/main` as a compatibility branch. Publication may replace prior publication commits and remove obsolete publication refs because the Source Topic Workspace and its durable records remain canonical.

## Status

accepted

## Considered Options

- Use `main` for the current snapshot and remove the legacy superproject branch.
- Use `main` for the current snapshot while retaining `topic-workspace/main` as an identical alias.
- Keep `topic-workspace/main` canonical and make `main` secondary.

## Consequences

- A normal clone of the remote opens the current Topic Workspace projection.
- Commit ancestry, rollback through remote history, and compatibility with the old superproject branch are not publication guarantees.
- Topic-owned component refs may use fresh sanitized commits when required by the chosen submodule topology.
- Synchronization must verify the complete replacement snapshot rather than infer correctness from ancestry.
