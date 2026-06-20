## Context

The repository currently has accepted contracts for CLI topic-context resolution and Workspace Path Resolution, plus architecture notes for the manifested workspace engine, but there is no platform-level `isomer-cli` implementation. `src/isomer_labs/` only contains a placeholder package module, while OpenSpec files and `.imsight-arts/project-explore/` describe the intended Project, Project Config Directory, Project Manifest, Research Topic Config, Topic Workspace, Effective Topic Context, and Workspace Path Resolver behavior.

Milestone 1 should convert that design into a narrow runnable core. The CLI should make Project discovery, manifest validation, topic selection, and path preview observable before later milestones add Workspace Runtime SQLite state, durable research records, agent execution, manual handoffs, or GUI serving.

## Goals / Non-Goals

**Goals:**

- Provide an installed `isomer-cli` command through the Python package.
- Create the minimal file-backed Project configuration needed for one Research Topic and one Topic Workspace.
- Validate `.isomer-labs/manifest.toml`, registered Research Topic Config TOML files, optional `.isomer-labs/local.toml`, and supported selector or environment inputs.
- Resolve and display Effective Topic Context for topic-scoped commands.
- Preview Workspace Path Resolution outputs without creating Workspace Runtime state.
- Return deterministic human-readable diagnostics and JSON output suitable for tests and future Operator Agent use.

**Non-Goals:**

- Do not create `state.sqlite` or implement Workspace Runtime schema migrations.
- Do not create Research Inquiries, Research Tasks, Runs, Artifacts, Gates, Decision Records, Evidence Items, Findings, Research Claims, or Provenance Records.
- Do not launch Agent Team Instances, Service Agent Instances, Execution Adapter operations, or Houmao workflows.
- Do not start the GUI Backend or implement GUI Component Registry behavior.
- Do not treat Research Topic Config or `.isomer-labs/local.toml` as runtime truth or credential storage.

## Decisions

### Decision 1: Keep `isomer-cli` Thin and Use Click at the Command Boundary

Implement the first command surface with `click`, `tomllib`, dataclasses or `attrs`, and explicit validation functions. Click should own command grouping, option parsing, help text, and test invocation while Project discovery, validation, Effective Topic Context resolution, Workspace Path Resolution, diagnostics, and rendering remain in dedicated modules.

Alternative considered: keep the original `argparse` parser tree. Rejected after the first implementation pass because nested command groups are already present and Click is already available in the project dependencies.

### Decision 2: Separate Loading, Resolution, Validation, and Rendering

Use distinct internal modules for Project discovery, Project Manifest parsing, Research Topic Config parsing, Effective Topic Context resolution, Workspace Path Resolution, diagnostics, and CLI rendering. The CLI layer should orchestrate these modules but should not own domain rules.

Alternative considered: implement all Milestone 1 logic in one `cli.py`. Rejected because selector precedence, path validation, and diagnostics will be reused by the Operator Agent, tests, and future Execution Adapter preparation.

### Decision 3: Treat Effective Topic Context as a Process Object

Represent Effective Topic Context as an in-memory value carrying validated refs and source metadata. `context show` can serialize it as JSON, but the implementation should not write it as durable lifecycle state.

Alternative considered: persist the full context snapshot during validation. Rejected because accepted specs say durable records should later store bounded refs, source metadata, and consumed config/default versions rather than a full context blob.

### Decision 4: Initialize Files, Not Runtime State

`isomer-cli init` should create `.isomer-labs/manifest.toml`, a registered Research Topic Config, and a Topic Workspace directory for user clarity. It should not create `state.sqlite`; that belongs to Workspace Runtime work in Milestone 2.

Alternative considered: create the full default Topic Workspace layout during `init`. This is tempting, but it blurs the boundary between project discovery and runtime creation. Milestone 1 can preview the default layout and create only the directory anchor.

### Decision 5: Make Path Preview Side-Effect Free

`paths preview` should resolve and print semantic paths with sources such as `explicit`, `env`, `manifest`, or `default`, but it should not create directories by default. Side-effect-free preview makes tests deterministic and lets users inspect external-path rejection before files appear.

Alternative considered: eagerly create all previewed directories. Rejected because path resolution is a validation and planning operation; Workspace Runtime and Run creation should own durable directory creation later.

### Decision 6: Use Structured Diagnostics Internally

Validation should produce diagnostic objects with code, path, optional line when available, severity, neutral Isomer concept, and message. The CLI can render concise text by default and JSON when requested.

Alternative considered: print ad hoc strings at validation sites. Rejected because diagnostics need stable tests and future Operator Agent consumption.

### Decision 7: Default `init` to a `default` Research Topic

When no topic id is provided, `isomer-cli init` should create a Research Topic with id `default`, a Research Topic Config at `.isomer-labs/research-topics/default.toml`, and a Topic Workspace directory at `topic-workspaces/default/`. The command may accept explicit topic id, topic statement, and workspace path options, but the no-argument path should work for a first-time user.

Alternative considered: require an explicit topic id for every initialization. Rejected because Milestone 1 needs a low-friction smoke path, and users can rename or create a more specific Project later when richer migration behavior exists.

### Decision 8: Treat JSON Output as Versioned Milestone 1 Developer Contract

JSON output should be deterministic and include an output schema version, but it is not yet a durable public research-record API. Tests and future Operator Agent experiments may consume it during Milestone 1; a later Workspace Runtime or API-stability change can promote selected response shapes into stable contracts.

Alternative considered: declare JSON output fully stable immediately. Rejected because command scope, Workspace Runtime integration, and Operator Agent consumption are still evolving.

### Decision 9: Keep `schemas list` to Isomer Built-Ins

`schemas list` should expose only Isomer built-in schema and contract names known to the package. It should not inspect OpenSpec capability names or change artifacts by default, because `isomer-cli` is a user-facing platform command while OpenSpec is a development planning tool.

Alternative considered: include OpenSpec capability names for developer convenience. Rejected for Milestone 1 because it blurs runtime platform behavior with repository planning metadata.

### Decision 10: Reject External Paths Without an Allowlist

Milestone 1 should reject Project Manifest, Research Topic Config, Topic Workspace, and previewed workspace paths outside the Project root. It should not implement an external-root allowlist or force policy yet.

Alternative considered: support explicit external roots in the first manifest schema. Rejected because external storage has security, provenance, and export implications that deserve a dedicated design.

### Decision 11: Do Not Support Manifest Overwrite in `init`

`isomer-cli init` should refuse to overwrite an existing `.isomer-labs/manifest.toml`. There should be no `--force` flag in Milestone 1.

Alternative considered: add `--force` immediately. Rejected because migration, backup, and user data preservation semantics are not designed yet.

## Risks / Trade-offs

- [Risk] Milestone 1 overlaps with existing `cli-topic-context-resolution` and `workspace-path-resolution` specs. → Mitigation: keep this change focused on the concrete command surface and implementation subset, and leave existing specs as the deeper source contracts.
- [Risk] `init` may create project files that later schema revisions need to migrate. → Mitigation: include schema version fields from the start and keep generated files minimal.
- [Risk] rejecting external paths may frustrate users with out-of-tree research data. → Mitigation: allow the error to name the rejected path and defer explicit external-root policy to a later change.
- [Risk] source metadata can become noisy. → Mitigation: expose it in JSON and concise preview output, but keep default human output focused on selected Project, Research Topic, Topic Workspace, and errors.
- [Risk] avoiding a CLI framework may make nested commands slightly manual. → Mitigation: keep command parsing boring and local; revisit only after command count or help text becomes painful.

## Migration Plan

1. Add package modules and tests without changing existing design artifacts.
2. Add `[project.scripts]` entry for `isomer-cli` once the CLI module exists.
3. Add fixture Projects in tests to exercise valid and invalid manifests, topic configs, local active context, and environment selectors.
4. Run `pixi run lint`, `pixi run typecheck`, `pixi run test`, and `pixi run validate-research-skills`.
5. Mark Milestone 1 checklist items in `ROADMAP.md` only when the corresponding implementation and tests land.

Rollback is straightforward because Milestone 1 adds a new command surface and new package modules. Removing the script entry and package modules returns the repository to the current design-only posture without migrating user data.

## Resolved Questions

- `isomer-cli init` defaults to topic id `default` when no explicit topic id is provided.
- JSON output is deterministic and versioned for Milestone 1, but it is not yet a durable public research-record API.
- `schemas list` exposes Isomer built-in schema and contract names only.
- `init` does not support force-overwriting an existing Project Manifest.
- External project, topic config, Topic Workspace, and preview paths are rejected in Milestone 1 when they resolve outside the Project root.
