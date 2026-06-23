# One Research Topic Uses One Topic Team

Each Research Topic in Isomer Labs will be handled by one topic-level team. The owning Topic Workspace stores one authoritative Topic Agent Team Profile Bundle at `<topic-workspace>/team-profile/`, and the Project Manifest keeps a ref to that bundle for discovery. A different team strategy should be represented as a profile revision, an archived-and-replaced profile, or a new Research Topic, not as a second active Topic Agent Team Profile under the same Topic Workspace.

## Status

accepted

## Considered Options

- Allow multiple Topic Agent Team Profile variants under one Research Topic: rejected because it makes topic ownership, task routing, profile selection, and diagnostics ambiguous.
- Keep one Topic Agent Team Profile Bundle per Research Topic and fork a new Research Topic for a materially different team strategy: accepted because it keeps the topic-team boundary concrete and testable.

## Consequences

- Topic Agent Team Profile identity is derived from the Research Topic and Topic Workspace, not from a user-selected `profile-id`.
- Topic Workspaces use the fixed `team-profile/` bundle path rather than `team-profiles/<profile-id>/`.
- Agent Team Instance creation must use the Research Topic's single profile bundle and reject attempts to launch or register a second active topic team for the same Research Topic.
- Research Topic-level parallelism means multiple Research Topics run concurrently, each with one team. Inside one Research Topic, parallel execution is task-level fanout among Agent Instances in that topic's Agent Team Instance.
