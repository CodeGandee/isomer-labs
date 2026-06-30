## Why

The Topic Workspace design still treats `repos/topic-main` as mostly agent-workspace topology, which makes topic environment setup depend too much on later team and agent decisions. The new design makes the Topic Main Development Repository the topic-owned development substrate first, so humans and agents can work in one Git repository while Isomer keeps external repo projections inside its own managed namespace.

## What Changes

- Define `repos/topic-main` as the **Topic Main Development Repository**: a normal topic-owned Git repository created, configured, and verified before Agent Workspaces exist.
- Keep canonical third-party repositories under `repos/extern/...`, but expose them inside `topic-main` only through Isomer-managed projections under `isomer-managed/topic-owned/{readonly,writable}/extern/...`.
- Record external projections with small tracked Isomer metadata, including source semantic label, source path, projection path, access intent, projection mode, and blocker state.
- Move Topic Main Development Repository creation and projection materialization into `isomer-srv-topic-env-setup`, driven by `topic.env.topic_setup_target_spec`.
- Narrow `isomer-srv-agent-env-setup` so it consumes prepared Topic Main Development Repository evidence and creates/verifies Agent Workspace worktrees, instead of owning topic-main creation or topic-level projection setup.
- Keep `isomer-admin-topic-team-specialize` as the orchestrator that owns normal operator-flow derived gate creation before invoking setup services.
- Reduce `isomer-admin-topic-workspace-mgr` to optional/manual Git topology inspection, branch helpers, boundary summaries, and legacy compatibility guidance when the canonical service path has already prepared topic-main.
- Update domain language, docs, skills, call graph, semantic surfaces, path-resolution output, validators, fixtures, and tests to reflect the new ownership split.
- **BREAKING**: old Topic Workspace internal paths, old `isomer-content/` contents, and skill guidance that says agent-env setup creates or configures `topic.repos.main` by default may stop working without compatibility migration.

## Capabilities

### New Capabilities

- `topic-main-development-repository`: Defines Topic Main Development Repository ownership, readiness, external repo projections under `isomer-managed/`, and the boundary between canonical external repo storage and developer-facing projections.

### Modified Capabilities

- `topic-workspace-manifest`: Add or refine semantic labels and storage-profile rules for Topic Main Development Repository support paths and external repo projection metadata.
- `workspace-path-resolution`: Resolve and report Topic Main Development Repository and external projection labels without treating projection paths as independent grouped topic repositories.
- `isomer-managed-sharing-layout`: Extend `isomer-managed/topic-owned/{readonly,writable}/` to cover external repo projections and tracked projection manifests.
- `isomer-service-env-setup-skill`: Make topic env setup create/configure/verify the Topic Main Development Repository and external repo projections from the derived topic env target spec.
- `isomer-agent-env-setup-service-skill`: Require prepared topic-main and projection predecessor evidence before Agent Workspace worktree setup and per-agent cwd verification.
- `topic-team-specialization-module-skill`: Keep derived gate creation with the orchestrator in the normal operator flow, then delegate materialization to services in the revised order.
- `topic-workspace-manager-skill`: Re-scope the workspace manager around optional/manual topology inspection, branch helpers, boundaries, and compatibility instead of canonical topic-main creation.
- `isomer-documentation-system-guide`: Update user-facing Topic Workspace documentation, runtime/file docs, concepts, and breaking-layout diagnostics for the revised layout.

## Impact

Affected areas include `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`, `docs/topic-workspace-definition.md`, `docs/concepts.md`, `docs/runtime-and-files.md`, `docs/getting-started.md`, `context/design/skill-process/team-specialization.md`, `skillset/operator/isomer-admin-topic-team-specialize`, `skillset/operator/isomer-admin-topic-workspace-mgr`, `skillset/service/isomer-srv-topic-env-setup`, `skillset/service/isomer-srv-agent-env-setup`, `skillset/callgraph.md`, semantic surface definitions in `src/isomer_labs/semantic_surfaces.py`, path and manifest validation helpers, CLI output/tests for semantic paths and repository creation, skill validators, documentation validators, and OpenSpec specs. Existing generated `isomer-content/` internals are not preserved by this change; projects can recreate topic content under the new layout.
