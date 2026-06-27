## Context

Isomer Labs now has three overlapping Topic Workspace stories. The accepted path-resolution and runtime specs still default to root `artifacts/`, `tasks/`, `runs/`, `views/`, and `logs/` directories, runtime code records those surfaces through `RUNTIME_DIRECTORIES`, and team-instance creation still treats `agent_workspace_ref` or `agents/<agent-instance-id>` as the Agent Workspace path source. Recent docs and operator skills moved toward `repos/topic-main` plus `agents/<agent-name>` Git worktrees, but they still use mixed terms such as agent key and still describe root shared surfaces in places.

The user-facing design we want is simpler: a worker agent starts with cwd set to its own Git worktree at `agents/<agent-name>`. That worktree is the agent's normal world. The topic owner, operator, service agents, and runtime code may work from the Topic Workspace root, but worker agents should receive shared information through Git, approved symlinks inside their worktree, or topic-owned Pixi tasks rather than by browsing Topic Workspace root state.

## Goals / Non-Goals

**Goals:**

- Define one canonical Topic Workspace layout with clear worker-visible, owner-preserved, and runtime-internal surfaces.
- Make `repos/topic-main` the shared Git repository and `agents/<agent-name>` the standard per-agent Git worktree path.
- Keep Agent Instance ids globally unique runtime ids while introducing a stable topic-local agent name for directory, branch, and operator-facing workspace planning.
- Make root `records/*` the topic-owner preserved record area and stop presenting root collaboration directories to worker agents.
- Update path resolution, runtime persistence, skills, docs, fixtures, and tests from the same layout contract.
- Preserve compatibility diagnostics for existing workspaces instead of deleting or silently moving old root directories.

**Non-Goals:**

- This change does not add filesystem-grade sandboxing. Workspace boundaries remain advisory.
- This change does not define a scheduler, task queue, mailbox, or new inter-agent protocol beyond the directory and Git conventions.
- This change does not require rewriting Git history or automatically migrating existing user data.
- This change does not make worker agents responsible for reading or mutating `state.sqlite`, root `records/`, root `runtime/`, or Project config.

## Decisions

### Canonical Topic Workspace Layout

Use this standard layout for a prepared Topic Workspace:

```text
<topic-workspace>/
  pixi.toml
  pixi.lock
  .pixi/
  state.sqlite
  team-profile/
  repos/
    topic-main/
  agents/
    <agent-name>/
  records/
    artifacts/
    tasks/
    runs/
    views/
    logs/
  runtime/
    adapters/
      houmao/
```

`repos/topic-main` is the owner-managed checkout of the shared topic repository. Worker-visible collaboration directories such as `shared/`, `artifacts/`, `tasks/`, `runs/`, `views/`, `logs/`, and `tools/` live inside that repository when the topic needs them. Root `records/*` contains owner-preserved extracts, snapshots, normalized outputs, and durable references that should not be treated as normal worker input. Root `runtime/` contains machine/runtime internals, adapter payloads, and repair state; `state.sqlite` remains at the Topic Workspace root for compatibility with current runtime code.

Alternative considered: keep root `artifacts/`, `tasks/`, `runs/`, `views/`, and `logs/` as shared surfaces. This keeps old path defaults simple, but it invites worker agents to read root topic-owner state and makes it unclear which files should travel through Git. The new layout trades a migration cost for clearer ownership.

### Agent Name Versus Agent Instance Id

Use `agent-name` for the topic-local worktree identity and branch namespace. Agent Instance ids remain globally unique runtime records, but they are not the normal directory name. Runtime records should link Agent Instance id, topic-local agent name, Agent Workspace path plan, and branch refs.

Alternative considered: continue deriving worktree paths from Agent Instance ids. That keeps runtime identity and filesystem identity aligned, but it produces unstable, opaque paths and works poorly for pre-created worktrees that operators want to launch into.

### Worktrees and Branches

Each `agents/<agent-name>` directory is a Git worktree of `repos/topic-main`. The owner checkout normally uses `topic-owner/main`. A worker's default branch is `per-agent/<agent-name>/main`, and future worker branches stay under `per-agent/<agent-name>/`.

Agents exchange substantial information through ordinary Git operations across those branches. The workspace manager skill validates that an agent worktree is attached to `repos/topic-main`, checked out on the expected branch, and not duplicated elsewhere.

Alternative considered: keep per-agent directories as plain folders with optional Git inside them. That is easier to create, but it loses the single-repo branch model that the rest of the collaboration design assumes.

### Agent-Local Runtime Area

Because the Agent Workspace root is also a topic-main worktree, agent-local runtime and scratch files should live under an ignored `.isomer-agent/` area inside the worktree rather than as top-level `runtime/`, `artifacts/`, `scratch/`, or `logs/` directories. Collaborative outputs that should be visible to other agents belong in tracked or intentionally ignored topic-main paths, then move through Git or topic-owned tools.

Alternative considered: preserve the old Agent Workspace subpaths at worktree root. That keeps the old resolver shape but collides with repository content and makes it easier to mistake private runtime traces for collaborative Artifacts.

### Shared Symlinks

The primary communication channel is Git. Optional symlinks inside `agents/<agent-name>/.isomer-agent/links/` may point to owner-managed paths under `repos/topic-main`, such as `shared`, `tasks`, or `tools`, when the operator wants read-mostly convenience links without requiring an immediate merge. These symlinks are advisory and should be reported by the workspace manager; they are not a substitute for Git synchronization or path-plan validation.

Alternative considered: create root-level `shared/` and link each agent to it. That conflicts with the rule that worker-visible shared content belongs in `repos/topic-main`.

### Topic-Owned Pixi Tasks

Topic-owned Pixi tasks are the principled way for worker agents to use topic-owned tools, scripts, or APIs without hand-browsing root state. A task may run from the Topic Workspace Pixi manifest through an explicit wrapper, environment binding, or `pixi --manifest-path` style invocation. The task contract decides what root records it can read and what worker-visible output it returns or publishes into `repos/topic-main`.

Alternative considered: ask worker agents to run commands from the Topic Workspace root when they need topic tooling. That weakens the cwd convention and makes the root layout part of normal worker context.

### Path Resolution and Runtime Persistence

Path Resolution should expose explicit surfaces for `topic_main_repo`, `agents`, `records`, `records_artifacts`, `records_tasks`, `records_runs`, `records_views`, `records_logs`, `runtime`, and adapter internals. Existing `ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR` style environment variables should either become compatibility aliases for owner-preserved `records/*` surfaces or be deprecated with diagnostics; they must not be reinterpreted as worker-visible Git surfaces without a new accepted contract.

Runtime initialization should create `state.sqlite`, `repos/`, `agents/`, `records/*`, and `runtime/`, but it should not silently create root worker collaboration directories. Agent Team Instance creation should prefer validated agent-name workspace plans from profile or packet material. If no workspace plan exists for a launch-facing role, creation should report a blocker or use a clearly generated topic-local agent name, not a bare `agents/<agent-instance-id>` fallback.

Alternative considered: keep `agent_workspace_ref` as the primary authored profile field and only validate that it points to `agents/<name>`. That preserves existing fixtures but keeps the profile language path-first instead of agent-first.

## Risks / Trade-offs

- Existing fixtures and tests may fail broadly because they assert old path surfaces and source labels. Mitigation: migrate tests in small groups, preserve explicit compatibility diagnostics, and keep old-path assertions only where they prove migration behavior.
- Users may already have root `artifacts/`, `tasks/`, `runs/`, `views/`, or `logs/` directories. Mitigation: never delete or move them automatically; report them as legacy root collaboration surfaces and provide migration guidance to move worker-visible content into `repos/topic-main` or owner records into `records/*`.
- Symlinks inside worktrees can blur the “agent stays in cwd” convention. Mitigation: place them under `.isomer-agent/links/`, label them read-mostly convenience links, and make Git operations the authoritative sharing mechanism.
- Topic-owned Pixi tasks may need to access root records while worker agents should not browse root state directly. Mitigation: treat Pixi tasks as explicit tool/API boundaries with narrow inputs and recorded outputs.
- Agent names can collide or become unsafe path segments. Mitigation: normalize and validate agent names before worktree creation, reject collisions, and require deterministic branch namespaces.

## Migration Plan

1. Update specs and domain docs first so every implementation task has one contract to follow.
2. Update path-resolution code and runtime constants to produce the new surfaces while reporting legacy root surfaces without deleting them.
3. Update Agent Workspace planning, profile/packet validation, and team-instance creation to use topic-local agent names and derived workspace path plans.
4. Update the topic workspace manager skill to create `repos/topic-main`, owner branches, per-agent worktrees, `.isomer-agent/` support dirs, and optional symlinks.
5. Update Houmao adapter launch/materialization to set cwd to each recorded Agent Workspace worktree and keep adapter payloads under root `runtime/adapters/houmao/` or `records/*` unless deliberately published into Git.
6. Update docs, skill references, fixtures, and tests; keep migration diagnostics for old `agent_workspace_ref`, `agent-workspaces/`, `agents/<agent-instance-id>`, and root collaboration directory examples.

Rollback is documentation/spec-level until implementation starts. During implementation, rollback should keep any user-created directories intact and can restore old resolver behavior behind compatibility diagnostics if new validation blocks a legitimate existing workspace.

## Open Questions

- Should launch-facing profile material keep a compatibility `agent_workspace_ref` field indefinitely, or should it migrate to explicit `agent_name` plus derived workspace path refs in a later schema version?
- Which exact Pixi wrapper command should worker agents use from inside a worktree when invoking topic-owned tasks?
- Should compatibility aliases for `ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR` and related variables warn immediately, or remain silent for one release while resolving to `records/*`?
