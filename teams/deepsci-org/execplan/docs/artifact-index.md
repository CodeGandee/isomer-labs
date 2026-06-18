# Artifact Index

## Purpose

This file indexes generated artifacts for this execplan revision.

## Contents

| Artifact | Path | Authority |
| --- | --- | --- |
| Manifest | `execplan/manifest.toml` | Package metadata, generated-source posture, stage status, artifact index, and omissions. |
| Process overview | `execplan/specs/collab/collab-overview.md` | Process-first authority for phases, events, handoffs, ticks, recovery, and terminal posture. |
| Objective contract | `execplan/specs/objective/objective-contract.md` | Domain Agent Team Template objective and topic-profile requirements. |
| Participant contract | `execplan/specs/participants/participants.toml` | Role templates, skill projections, binding placeholders, and stage routing. |
| Topology contract | `execplan/specs/collab/topology/topology.toml` | Tree-loop route contract and local-close result routing. |
| Mail registry | `execplan/specs/comms/templates.toml` | Mail template names, schema ids, schema paths, renderer paths, and reply expectations. |
| Mail schemas | `execplan/specs/comms/schemas/*.schema.json` | Payload validation for generated mail families. |
| Mail renderers | `execplan/specs/comms/renderers/*.md.j2` | Human-readable Markdown mail with parseable metadata headers. |
| State overview | `execplan/specs/state/state-overview.md` | Loop-local bookkeeping authority and boundaries. |
| SQLite schema | `execplan/specs/state/schema.sql` | Loop-local state DDL. |
| State seed | `execplan/specs/state/seed.toml` | Deterministic defaults and participant seed facts. |
| State invariants | `execplan/specs/state/invariants.toml` | Named generated validation expectations. |
| Workspace contract | `execplan/specs/workspace/workspace.toml` | Placeholder-backed Topic Workspace and Agent Workspace expectations. |
| Run contract | `execplan/specs/run/run-contract.md` | Required Run inputs, expected outputs, Gates, parking, and completion. |
| Harness registry | `execplan/harness/commands.toml` | Loop-local command index. |
| Harness entrypoint | `execplan/harness/bin/deepsci-org` | Validation, query, mail schema, control, and placeholder commands. |
| Instantiation refs | `execplan/harness/refs/instantiation-parameters.toml` | Placeholder catalog for Topic Agent Team Profile creation. |
| Generated skills | `execplan/skills/*/SKILL.md` | Shared, event, tick, and operator-control behavior. |
| Agent bindings | `execplan/agents/bindings.toml` | Generated Houmao-facing binding contract with placeholders. |
| Profile placeholders | `execplan/agents/profiles/*.toml` | Role-scoped Agent Profile, Capability Binding, Skill Binding projection, and workspace slots. |
| Notifier prompts | `execplan/agents/notifier-prompts/*.md` | Per-role notifier prompt instructions. |
