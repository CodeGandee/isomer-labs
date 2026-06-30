## Context

Current Topic Workspace docs and skills already define `repos/topic-main` and the `isomer-managed/` namespace, but they still place too much topic-main creation and configuration responsibility in Agent Workspace setup. That makes the main development repository appear only when a team or agent plan exists, even though users may need a topic-owned development repository and a working Topic Workspace environment before team specialization or per-agent worktree creation.

The new design treats `repos/topic-main` as the Topic Main Development Repository. It is topic-owned, branch-based, and suitable for humans and agents. When a user wants `topic-main` to be an existing repository, Isomer should minimize impact on that repository by keeping Isomer-injected material under `isomer-managed/` instead of adding top-level external repo directories or coordination paths.

The Topic Workspace still keeps the shared Pixi environment at the Topic Workspace root through the existing Pixi binding model. Canonical third-party/support repositories still live under `repos/extern/...` as semantic `topic.repos.<group...>.<repo-name>` surfaces. Developer-facing access to those external repos inside topic-main is through Isomer-managed projections.

## Goals / Non-Goals

**Goals:**

- Make Topic Main Development Repository readiness a topic env responsibility, not an agent env responsibility.
- Keep canonical external repos under `repos/extern/...` while exposing them inside topic-main through `isomer-managed/topic-owned/{readonly,writable}/extern/...`.
- Distinguish read-only external projections from agent-writable projections with explicit policy and metadata.
- Keep ordinary user repo roots clean when `topic.repos.main` points at an existing repository.
- Keep derived gate creation owned by `isomer-admin-topic-team-specialize` in the normal operator flow, while allowing service skills to accept explicit target specs during manual invocation.
- Preserve semantic path resolution as the source of truth for every path surface.
- Treat this as a breaking Topic Workspace layout revision and allow generated `isomer-content/` internals to be recreated.

**Non-Goals:**

- Do not make projections filesystem-enforced security boundaries.
- Do not replace `repos/extern/...` as the canonical storage location for third-party repos.
- Do not require Git submodules or subtrees for external repo projections.
- Do not create Agent Instances, Workspace Runtime records, Houmao launch material, or Execution Adapter state.
- Do not create per-agent Pixi manifests or per-agent `.pixi/` environments by default.
- Do not migrate or preserve old generated Topic Workspace internals.

## Decisions

### Topic-Main Readiness Belongs to Topic Env Setup

`isomer-srv-topic-env-setup` will create, configure, and verify the Topic Main Development Repository as part of `setup-topic-env`. The service consumes `topic.env.topic_setup_target_spec` and prepares `topic.repos.main`, `topic.repos.main.isomer_managed`, tracked Isomer directories, local tmp posture, external repo projections, and topic-root or repo-specific verification commands.

Alternative considered: keep topic-main creation in `isomer-srv-agent-env-setup`. That preserves the current split but keeps topic env setup dependent on agent count, Agent Names, and worktree creation. The new design removes that dependency.

### External Repos Stay Canonical Under `repos/extern/...`

Canonical external repo storage remains registered through `topic.repos.<group...>.<repo-name>` labels, defaulting to `repos/extern/<repo-label-path>`. These locations are where the topic stores or inspects downloaded third-party repos.

Alternative considered: clone or copy third-party repos directly under topic-main. That is convenient for developers, but it pollutes existing user repositories and makes it harder to distinguish source-of-truth external material from projections.

### Topic-Main External Access Uses Isomer-Managed Projections

Topic-main exposes external repos under these fixed projection roots:

```text
repos/topic-main/
  isomer-managed/
    tracked/
      manifests/
        extern-projections.toml
    topic-owned/
      readonly/
        extern/
          <repo-label-path>/
      writable/
        extern/
          <repo-label-path>/
```

Read-only projections normally symlink to the canonical `repos/extern/...` path when symlinks are supported and safe. Writable projections must not be symlinks to the canonical external repo by default; they should be copies, dedicated clones, or dedicated worktrees recorded in projection metadata. This avoids accidental mutation of canonical third-party source material.

Alternative considered: add `repos/topic-main/extern/...`. That keeps paths shorter but adds a top-level directory to user-owned topic-main repositories and weakens the existing `isomer-managed/` boundary.

### Projection Metadata Is Tracked, Bulk Projection Content Is Ignored

The small projection manifest is tracked under `isomer-managed/tracked/manifests/extern-projections.toml`. It records source semantic label, source path, projection path, intended access, projection mode, mutability policy, creation command evidence, status, blockers, and review notes. Projection content under `isomer-managed/topic-owned/...` remains ignored by the `isomer-managed/.gitignore` policy unless a later explicit contract marks a small generated file as tracked.

Alternative considered: use per-repo semantic labels such as `topic.repos.main.extern.foo`. That collides conceptually with grouped `topic.repos.*` labels and risks treating projections as independent topic repositories. Fixed projection-root labels plus manifest entries avoid that namespace problem.

### Agent Env Setup Consumes Prepared Topic-Main Evidence

`isomer-srv-agent-env-setup` will require Topic Workspace predecessor evidence from topic env setup, including `topic.env.topic_setup_target_spec`, selected Pixi binding, ready Topic Main Development Repository state, and projection readiness relevant to the agent gate. It then creates or validates Agent Workspace worktrees and verifies commands from each `agent.workspace` cwd. It does not create topic-main or set up external projections in the normal flow.

Alternative considered: allow agent-env setup to repair topic-main opportunistically. That creates two writers for the same repository setup contract. The safer route is a repair next action back to `isomer-srv-topic-env-setup`.

### Orchestrator Owns Normal Derived Gate Creation

`isomer-admin-topic-team-specialize` remains the normal user interaction point. It creates or updates source intent files under `topic.intent.*`, creates or updates derived target specs under `topic.env.*`, and then invokes service skills for materialization. Service skills may still accept explicit manual target spec files, prompts, or context when invoked directly, but the canonical operator path should not ask services to decide user-facing derived gates on their own.

Alternative considered: let each service derive its own target spec from source intent during the normal operator flow. That is simpler for direct service use but moves too much user-facing interpretation into lower-level services.

### Workspace Manager Becomes Optional Topology Support

`isomer-admin-topic-workspace-mgr` remains useful for manual inspection, branch helper operations, boundary summaries, compatibility validation, and legacy repair guidance. It should not be the canonical creator of the Topic Main Development Repository when topic env setup has a derived target spec and mutation authorization.

Alternative considered: keep the workspace manager as the creator of topic-main and call it from topic env setup. That adds another cross-skill hop and leaves ownership split across operator and service layers.

## Risks / Trade-offs

- Existing docs and tests expect agent-env setup to own `ensure-topic-main-repository` → Break that contract and replace it with predecessor checks that route repair back to topic env setup.
- Writable external projections can diverge from canonical external repos → Record projection mode and source in `extern-projections.toml`, and make promotion or sync explicit.
- Symlinks can behave differently across platforms → Treat symlink as a preferred read-only mode, but allow copy mode with recorded reason and portability warning.
- Existing user topic-main repositories may already contain `isomer-managed/` or conflicting paths → Validate non-destructively and report blockers rather than moving or deleting user content.
- `topic.repos.main.*` labels can overlap mentally with grouped `topic.repos.*` labels → Add fixed built-in labels for projection roots and reject unknown reserved sublabels unless explicitly supported.
- Services could drift back toward deriving gates from source intent in the operator flow → Update skill guardrails and validators to require orchestrator-owned derived gates for normal team specialization.
- Existing `isomer-content/` internals may fail validation after this change → Accept this break and recreate generated topic content under the revised layout.

## Recreate Plan

1. Update domain language and docs to introduce Topic Main Development Repository and external repo projections.
2. Add semantic labels and storage profiles for projection roots and the projection manifest.
3. Update Topic Workspace Manifest and Workspace Path Resolution validation so projection-root labels are built-in and safe.
4. Update `isomer-srv-topic-env-setup` workflows, output contract, and reference pages to create/configure/verify topic-main and projections.
5. Update `isomer-srv-agent-env-setup` workflows to require prepared topic-main/projection predecessor evidence and remove topic-main creation from its normal setup chain.
6. Update `isomer-admin-topic-team-specialize` process, call graph, and subcommands so derived gates are orchestrator-owned before services materialize.
7. Re-scope `isomer-admin-topic-workspace-mgr` docs and validators toward optional topology support.
8. Replace fixtures that encode old generated `isomer-content/` internals instead of migrating them.
9. Update tests, then run `pixi run test`, `pixi run typecheck`, `pixi run lint`, and `openspec validate --all`.

There is no compatibility migration for old generated Topic Workspace contents. Existing `isomer-content/` can be recreated under the revised layout, and old internal paths may break.

## Open Questions

- Should writable projections default to plain copies or dedicated Git worktrees when the canonical `repos/extern/...` path is itself a Git repository?
- Should the projection manifest be TOML only, or should Markdown summaries also be generated for humans?
- Do we need a CLI command such as `project repos project-into-main`, or should projection materialization remain service-owned until a user-facing command is requested?
