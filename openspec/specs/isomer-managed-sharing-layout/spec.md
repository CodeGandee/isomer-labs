# isomer-managed-sharing-layout Specification

## Purpose
TBD - created by archiving change refine-isomer-managed-sharing-layout. Update Purpose after archive.
## Requirements
### Requirement: Canonical Isomer-Managed Worker Namespace
The system SHALL define `isomer-managed/` under the Topic Main Repository as the only standard Isomer-specific worker-facing namespace inside `topic-main`.

#### Scenario: Standard namespace exists
- **WHEN** a Topic Workspace prepares the standard Topic Main Repository layout
- **THEN** the worker-facing Isomer namespace is `<topic-workspace>/repos/topic-main/isomer-managed/`

#### Scenario: Agent worktree namespace matches
- **WHEN** an Agent Workspace worktree is prepared for agent name `alice`
- **THEN** the worker-facing Isomer namespace visible to that agent is `<topic-workspace>/agents/alice/isomer-managed/`

#### Scenario: Repository top level stays native
- **WHEN** Isomer creates worker-facing collaboration surfaces for a Topic Main Repository
- **THEN** it places those surfaces under `isomer-managed/` instead of creating top-level `shared/`, `artifacts/`, `tasks/`, `runs/`, `views/`, `logs/`, or `tools/` directories in `topic-main`

#### Scenario: Old support root is legacy
- **WHEN** validation sees `.isomer-agent/` inside an Agent Workspace
- **THEN** it reports the path as legacy support material and points migration guidance to `isomer-managed/`

### Requirement: Isomer-Managed Regime Layout
The system SHALL separate tracked Isomer-injected material, untracked agent-owned material, untracked topic-owned material, and generated links under `isomer-managed/`.

#### Scenario: Tracked regime is explicit
- **WHEN** Isomer-specific material is intended to be shared through normal Git operations
- **THEN** the standard path is under `isomer-managed/tracked/`

#### Scenario: Agent-owned regime is explicit
- **WHEN** material is owned by the current agent worktree and is not intended to be tracked by `topic-main`
- **THEN** the standard path is under `isomer-managed/agent-owned/`

#### Scenario: Topic-owned regime is explicit
- **WHEN** non-Git material is owned by the topic and intentionally projected into an Agent Workspace
- **THEN** the standard path visible to the agent is under `isomer-managed/topic-owned/`

#### Scenario: Generated links are explicit
- **WHEN** Isomer creates advisory symlinks or generated path shortcuts for peer or topic-owned material
- **THEN** those links are placed under `isomer-managed/links/`

#### Scenario: Ignore policy is local to namespace
- **WHEN** the topic workspace manager prepares `isomer-managed/`
- **THEN** it creates or validates an `isomer-managed/.gitignore` policy that ignores `agent-owned/`, `topic-owned/`, and `links/` while keeping `.gitignore` and `tracked/` eligible for Git tracking

### Requirement: Tracked Isomer Material
The system SHALL use `isomer-managed/tracked/` for Isomer-specific material that is intentionally shared among agents through Git.

#### Scenario: Tracked subdirectories are standard
- **WHEN** a standard `isomer-managed/tracked/` layout is prepared
- **THEN** it may contain `shared/`, `artifacts/`, `tasks/`, `runs/`, `views/`, `tools/`, `boundaries/`, and `manifests/` as Isomer-specific tracked collaboration surfaces

#### Scenario: Tracked material is shared by Git
- **WHEN** an agent needs durable small coordination material to be visible to peers
- **THEN** the primary sharing path is to write it under `isomer-managed/tracked/` and share it through normal Git branch operations

#### Scenario: Conflict-prone tracked files are detected
- **WHEN** validation sees unresolved conflict markers, conflicting branch edits to known tracked Isomer files when detectable, or broad multi-agent write guidance without boundary policy
- **THEN** it reports a tracked Isomer material conflict diagnostic instead of treating the workspace as clean

#### Scenario: Per-agent tracked files reduce conflicts
- **WHEN** a tracked Isomer surface is expected to accept writes from multiple agents
- **THEN** boundary guidance prefers per-agent filenames, owner prefixes, append-only conventions, or topic-owned update tasks before shared-path editing

### Requirement: Agent-Owned Untracked Share Contract
The system SHALL define `isomer-managed/agent-owned/` as the current agent worktree's untracked owner area and SHALL distinguish peer-readable material from owner-private support material.

#### Scenario: Agent-owned support paths replace old support root
- **WHEN** an agent needs local runtime, scratch, logs, or unpromoted artifact support inside its worktree
- **THEN** the standard paths are `isomer-managed/agent-owned/runtime/`, `isomer-managed/agent-owned/scratch/`, `isomer-managed/agent-owned/logs/`, and `isomer-managed/agent-owned/artifacts/`

#### Scenario: Public share is peer-readable
- **WHEN** an agent produces a large or temporary file that peer agents may inspect before a Git commit or promotion
- **THEN** the standard owner path is `isomer-managed/agent-owned/public/`

#### Scenario: Reader writes are diagnostics by default
- **WHEN** validation detects that a peer agent wrote into another agent's `isomer-managed/agent-owned/public/`
- **THEN** it reports an owner/reader contract diagnostic unless explicit boundary policy permits that write

#### Scenario: Inbox requires explicit policy
- **WHEN** an agent-owned `isomer-managed/agent-owned/inbox/` path is used for peer writes
- **THEN** boundary material MUST explicitly state the allowed writers, expected file naming, and cleanup or promotion policy

#### Scenario: Untracked material is not durable by default
- **WHEN** downstream research claims, handoffs, or records depend on files under `isomer-managed/agent-owned/`
- **THEN** the files MUST be promoted into tracked Isomer material, owner-preserved records, or Provenance Records before the dependency is treated as durable

### Requirement: Topic-Owned Untracked Projection Contract
The system SHALL define `isomer-managed/topic-owned/` as the worker-visible projection of topic-owned non-Git material.

#### Scenario: Read-only topic projection is explicit
- **WHEN** a topic-owned non-Git path is exposed to worker agents for reading
- **THEN** the worker-visible path is under `isomer-managed/topic-owned/readonly/`

#### Scenario: Writable topic projection is explicit
- **WHEN** a topic-owned non-Git path is exposed to worker agents for writes
- **THEN** the worker-visible path is under `isomer-managed/topic-owned/writable/` and boundary material states the write policy

#### Scenario: Topic roots remain owner controlled
- **WHEN** topic-owned material is sourced from root `records/`, root `runtime/`, adapter material, or another topic-owner-controlled store
- **THEN** worker agents access only the approved projection under `isomer-managed/topic-owned/` or an approved topic-owned Pixi task

#### Scenario: Writable topic projection prefers tasks
- **WHEN** a topic-owned writable projection needs structured updates, locking, validation, or aggregation
- **THEN** boundary guidance points agents to a topic-owned Pixi task or wrapper rather than unconstrained file writes

### Requirement: Generated Peer and Topic Links
The system SHALL keep generated convenience links under `isomer-managed/links/` and validate their targets.

#### Scenario: Peer public link target is standard
- **WHEN** the topic workspace manager creates a peer-readable link from Alice's worktree to Bob's public share
- **THEN** the link is under `agents/alice/isomer-managed/links/peers/bob/` and targets Bob's `isomer-managed/agent-owned/public/`

#### Scenario: Topic link target is standard
- **WHEN** the topic workspace manager creates a link for topic-owned material
- **THEN** the link is under `isomer-managed/links/topic/` and targets an approved `isomer-managed/topic-owned/readonly/` or `isomer-managed/topic-owned/writable/` projection

#### Scenario: Unsafe links are diagnostics
- **WHEN** a generated or declared link points outside the selected Topic Workspace without an accepted external-root contract
- **THEN** validation reports an unsafe link diagnostic and does not treat the link as ready

#### Scenario: Links are advisory
- **WHEN** Isomer reports generated links in summaries or boundary material
- **THEN** it identifies them as advisory conveniences rather than filesystem-grade isolation or durable path truth

### Requirement: Worker Collaboration Channel Order
The system SHALL describe Git branch exchange, untracked Isomer-managed sharing, and topic-owned Pixi tasks as distinct worker collaboration channels.

#### Scenario: Git remains primary channel
- **WHEN** worker agents share durable topic work
- **THEN** the primary channel is Git operations across `repos/topic-main` and the per-agent branches

#### Scenario: Untracked share handles large temporary material
- **WHEN** worker agents need to inspect large or temporary peer material before it is committed
- **THEN** they use the owner-approved `isomer-managed/agent-owned/public/`, `isomer-managed/topic-owned/`, or `isomer-managed/links/` surfaces

#### Scenario: Pixi tasks handle principled shared operations
- **WHEN** shared operations need topic-owned tools, scripts, APIs, structured updates, or access to owner-preserved root state
- **THEN** agents use approved topic-owned Pixi tasks or wrappers instead of browsing root topic-owner directories directly

### Requirement: Legacy Layout Diagnostics
The system SHALL report legacy worker-facing path conventions without deleting or moving user files automatically.

#### Scenario: Legacy top-level topic-main directories are reported
- **WHEN** validation finds `shared/`, `artifacts/`, `tasks/`, `runs/`, `views/`, `logs/`, or `tools/` at the root of `repos/topic-main`
- **THEN** it reports them as legacy Isomer worker-facing directories and recommends the corresponding `isomer-managed/tracked/`, `isomer-managed/agent-owned/`, or owner-preserved `records/*` destination

#### Scenario: Legacy support root is reported
- **WHEN** validation finds `.isomer-agent/` inside a worktree
- **THEN** it reports the old support root as legacy and recommends `isomer-managed/agent-owned/` and `isomer-managed/links/` destinations

#### Scenario: Diagnostics are non-destructive
- **WHEN** legacy layout diagnostics are emitted
- **THEN** the system does not delete, move, reset, rewrite, or commit the referenced files without explicit operator instruction

