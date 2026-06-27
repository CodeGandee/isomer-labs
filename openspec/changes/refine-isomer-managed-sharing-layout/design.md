## Context

The current standard Topic Workspace layout gives worker agents a clean cwd at `<topic-workspace>/agents/<agent-name>`, but it still injects Isomer-specific collaboration directories directly at the root of `repos/topic-main` and uses `.isomer-agent/` as a separate ignored support area inside each worktree. That design solves basic visibility, but it pollutes existing repositories and makes large peer-readable artifacts depend on Git commits or ad hoc paths.

The revised design keeps the existing Topic Workspace and Agent Workspace concepts: `repos/topic-main` remains the shared normal Git repository, each `agents/<agent-name>` directory remains a Git worktree on an agent-owned branch, and the agent is still launched with that worktree as cwd. The change is where Isomer puts its worker-facing support material: every Isomer-specific path inside the worker worktree moves under `isomer-managed/`.

## Goals / Non-Goals

**Goals:**

- Keep the native repository top level as untouched as possible by using one `isomer-managed/` namespace inside `topic-main`.
- Provide a non-Git sharing lane for large or temporary peer-readable artifacts before they are committed or promoted.
- Preserve the conceptual owner/reader split for agent-owned material even though filesystem permissions do not enforce it.
- Let topic-owned material be projected into agent worktrees through `isomer-managed/` without making workers browse root `records/`, `runtime/`, or `state.sqlite`.
- Make tracked Isomer-specific material easy to validate for conflicts and easy to share through normal Git operations.
- Replace `.isomer-agent/` path surfaces, docs, skill guidance, runtime records, and validation messages with `isomer-managed/` equivalents.

**Non-Goals:**

- This change does not add filesystem-grade isolation between agents.
- This change does not make untracked large artifacts durable research records by default.
- This change does not replace Git branch exchange as the primary collaboration channel.
- This change does not define a full artifact storage backend, quota system, or garbage collection policy.
- This change does not change the rule that Execution Adapters launch worker agents from `agents/<agent-name>`.

## Decisions

### Decision: Use One Isomer Namespace Inside topic-main

Every Isomer-specific worker-facing path inside the Topic Main Repository SHALL live under `isomer-managed/`. The standard shape is:

```text
<topic-workspace>/repos/topic-main/
  isomer-managed/
    .gitignore
    tracked/
      shared/
      artifacts/
      tasks/
      runs/
      views/
      tools/
      boundaries/
      manifests/
    agent-owned/
      runtime/
      scratch/
      logs/
      artifacts/
      public/
      inbox/
    topic-owned/
      readonly/
      writable/
    links/
      peers/
      topic/
```

Agent worktrees under `agents/<agent-name>` see the same tracked `isomer-managed/tracked/*` material through Git, while their ignored `isomer-managed/agent-owned/*`, `isomer-managed/topic-owned/*`, and `isomer-managed/links/*` contents are local to that worktree or generated projections. The tracked `.gitignore` under `isomer-managed/` ignores `agent-owned/`, `topic-owned/`, and `links/`, but leaves `tracked/` and `.gitignore` trackable.

Alternatives considered: keeping `shared/`, `tasks/`, and `tools/` at the repository root would be shorter, but it makes pre-existing repositories look Isomer-shaped. Keeping `.isomer-agent/` for local support would avoid a migration, but it splits Isomer-managed material across two namespaces and weakens the new owner/category model.

### Decision: Separate Tracked, Agent-Owned, and Topic-Owned Regimes

`isomer-managed/tracked/` contains Isomer-specific files that are intended to be versioned by `topic-main` and shared through Git. This includes small coordination files, task notes, tool wrappers, boundary material, manifests, indexes, and small artifacts that agents intentionally commit.

`isomer-managed/agent-owned/` contains untracked material owned by the current agent worktree. `runtime/`, `scratch/`, `logs/`, and `artifacts/` replace the old `.isomer-agent/` support paths. `public/` is the normal peer-readable area for large or temporary files that other agents may inspect before a commit. `inbox/` is optional and MUST be treated as writable by peers only when boundary material explicitly grants that policy.

`isomer-managed/topic-owned/` contains generated or symlinked views of topic-owned non-Git material. `readonly/` is exposed for worker reads only, and `writable/` is exposed when the topic owner explicitly permits agents to drop shared material through a topic-owned surface. The physical source for topic-owned material may remain under a topic-owner-controlled path, but worker agents access it through the projected `isomer-managed/topic-owned/*` paths.

Alternatives considered: a single `untracked/` directory would be shorter, but it would hide whether an agent or the topic owns a path. Putting peer shares outside the worktree would reduce symlink complexity, but it would make workers leave their launch cwd for normal collaboration.

### Decision: Make Links Generated and Ignored

Generated convenience links live under `isomer-managed/links/`. Peer links normally point from one agent worktree to another agent's `isomer-managed/agent-owned/public/`, for example `isomer-managed/links/peers/bob/public -> ../../../../bob/isomer-managed/agent-owned/public`. Topic links point to entries projected under `isomer-managed/topic-owned/`.

The topic workspace manager reports generated links, validates that they stay within the selected Topic Workspace unless an explicit external-root contract permits otherwise, and treats unsafe targets as diagnostics. Links are advisory conveniences; path plans and boundary docs remain the durable description of intended access.

Alternatives considered: direct absolute symlinks are simpler to generate but make workspace relocation harder. Copying large artifacts into each worktree avoids symlinks but wastes disk and breaks the owner/reader contract.

### Decision: Track Conflict-Prone Isomer Material Through Git Policy

Tracked Isomer-specific material under `isomer-managed/tracked/` is shared through normal Git operations, so conflicts are expected and must be visible. The default policy should prefer per-agent filenames, append-only logs with owner prefixes, or topic-owned update tasks for any file that multiple agents may edit. Validation should detect unresolved conflict markers, simultaneous edits to known shared files across branches when detectable, missing boundary notes, and unsafe broad-write guidance.

Alternatives considered: making tracked material read-only to workers would avoid conflicts, but it would remove the lightweight coordination channel that agents need. Requiring all shared writes through Pixi tasks would be more controlled, but too heavy for ordinary notes and small coordination files.

### Decision: Preserve Topic-Level Owner Areas Outside Worker Browsing

Root `records/`, root `runtime/`, `state.sqlite`, and adapter material remain topic-owner or runtime surfaces, not normal worker browsing surfaces. If a worker needs material derived from those roots, a topic-owned Pixi task or topic-owned projection places the intended view under `isomer-managed/topic-owned/`.

Alternatives considered: letting workers read root topic directories directly would be easy, but it would blur the Worker Visibility Boundary and make later runtime validation harder.

## Risks / Trade-offs

- Existing docs, tests, and skills may still mention `.isomer-agent/` after the change. Mitigation: add validation coverage for stale path terms and update domain-language references in the same implementation.
- Generated symlinks can cross from one worktree into another and confuse naive tooling. Mitigation: keep links under `isomer-managed/links/`, validate targets, and report them as advisory rather than durable ownership.
- Untracked large artifacts can disappear or change without Git history. Mitigation: require durable dependencies to be promoted into `records/*`, tracked `isomer-managed/tracked/*`, or Provenance Records before downstream claims depend on them.
- Topic-owned writable shares can create race-prone writes. Mitigation: require boundary policy for writable topic-owned surfaces and prefer topic-owned Pixi tasks for structured updates.
- The `tracked/` prefix adds one more path segment. Mitigation: it makes the three regimes obvious and keeps ignore policy simple.

## Migration Plan

1. Update specs and docs to define `isomer-managed/` as the canonical worker-facing Isomer namespace and mark `.isomer-agent/` plus top-level `repos/topic-main/{shared,artifacts,tasks,runs,views,logs,tools}` as legacy.
2. Update path resolution to expose `isomer_managed`, `isomer_managed_tracked`, `agent_owned`, `topic_owned`, and generated-link surfaces, while preserving legacy environment variable diagnostics where needed.
3. Update the topic workspace manager skill to create or validate `isomer-managed/.gitignore`, tracked subdirectories, untracked owner/topic directories, generated links, branch ownership, and conflict diagnostics.
4. Update Topic Team Specialization guidance to delegate workspace setup and report `isomer-managed/` evidence instead of `.isomer-agent/` evidence.
5. Update validation tests and skillset checks so stale `.isomer-agent/` guidance fails outside migration notes.
6. Leave existing user files in place during validation and emit migration guidance rather than deleting, moving, or rewriting legacy paths automatically.

Rollback is documentation and behavior rollback only before implementation lands. After implementation, rollback means restoring `.isomer-agent/` path resolution and manager behavior while keeping non-destructive diagnostics for any created `isomer-managed/` directories.

## Open Questions

- Should `isomer-managed/agent-owned/inbox/` be enabled by default as an empty ignored directory, or created only when a boundary explicitly grants peer writes?
- Should topic-owned physical share sources live under root `runtime/`, root `records/`, or a future topic-owner-controlled store that is separate from both?
- Should the first implementation only validate conflict markers and branch namespaces, or also compare known tracked Isomer paths across peer branches?
