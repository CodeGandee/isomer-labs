## Context

Isomer Topic Workspaces already own `repos/`, `agents/`, Workspace Runtime state, Topic Agent Team Profile Bundle material, and topic-scoped Pixi environment files. Topic Team Specialization can carry `agent_workspace_ref` values through role bindings in profiles and Topic Team Instantiation Packets, but current Agent Team Instance creation derives Agent Workspace paths from generated Agent Instance ids and does not use those refs as the path source.

The requested layout introduces one shared topic repository at `<topic-workspace-dir>/repos/topic-main` and one Git worktree per topic-local agent at `<topic-workspace-dir>/agents/<agent-key>`. The branch namespace is intentionally per-agent: `per-agent/<agent-key>/main` is the agent's default branch, and future branches live under `per-agent/<agent-key>/<branch-name>`.

## Goals / Non-Goals

**Goals:**

- Add an operator skill that can plan, create, validate, and summarize the Git-backed Topic Workspace layout.
- Keep Isomer domain language intact: the shared repo is a topic repository, and each worktree path is an Agent Workspace inside the Topic Workspace.
- Preserve Workspace Runtime as the authority for Agent Instance and Agent Workspace records by making runtime creation consume approved `agent_workspace_ref` values.
- Make branch and worktree safety explicit, including idempotent creation, collision checks, and per-agent branch namespace validation.
- Keep static preparation separate from live launch, Houmao adapter operation, Agent Instance creation, and Workspace Runtime mutation.

**Non-Goals:**

- Do not launch Houmao agents or create Agent Team Instances from the new skill.
- Do not make Git branch names into Research Inquiry or Research Task identifiers.
- Do not create a second active Topic Agent Team Profile or a workspace-local `teams/` directory.
- Do not use filesystem boundaries as security isolation; Workspace Boundary and Peer Read Access remain advisory.
- Do not replace `isomer-srv-env-setup`, which still owns gate-driven Topic Workspace Pixi environment setup and independent repo acquisition for environment checks.

## Decisions

### Decision: Add a Separate Operator Skill

Create `skillset/operator/isomer-admin-topic-workspace-mgr` instead of expanding `isomer-admin-topic-team-specialize` further.

Rationale: Topic Team Specialization should remain focused on copied template material, profile or packet inputs, static setup evidence, validation, and summary. Git worktree setup is a concrete workspace preparation operation with its own idempotence, branch, and validation rules. A separate skill keeps the operator surface small enough to use directly and lets `setup-agent-workspace` delegate when Git-backed Agent Workspaces are requested.

Alternative considered: add many Git subcommands to `isomer-admin-topic-team-specialize`. This would blur static specialization with mutable workspace topology and make the already-large skill harder to validate.

### Decision: Use a Command-Style Skill Shape

Use the same shape as `isomer-srv-env-setup`: a lean `SKILL.md` router, grouped subcommands, and one-level `references/*.md` pages.

Initial public subcommands should be `resolve-workspace`, `ensure-main-repo`, `plan-agents`, `create-worktrees`, `write-boundaries`, `create-agent-branch`, `validate-worktrees`, `summarize`, `help`, and `topic-workspace`. The `topic-workspace` subcommand should orchestrate the normal full flow.

Alternative considered: one long workflow page. The workflow has several directly useful stages, and operators will often need to run only validation or branch creation after initial setup.

### Decision: Keep `agent-key` Separate from Agent Instance id

The skill should normalize a path-safe `agent-key` such as `alice` for branch and worktree planning. Runtime Agent Instance ids remain globally unique generated ids unless a future capability explicitly changes Agent Instance identity rules.

The bridge is `agent_workspace_ref`: the skill writes or validates `role_bindings.<role>.agent_workspace_ref = "<topic-workspace>/agents/<agent-key>"` in packet or profile material. When runtime creation creates the concrete Agent Instance for that role binding, it records the Agent Workspace path plan from that ref.

Alternative considered: force Agent Instance ids to equal `alice`. That conflicts with the existing global uniqueness requirement and would turn a friendly operator alias into a durable runtime id.

### Decision: Make `repos/topic-main` the Git Anchor

`<topic-workspace-dir>/repos/topic-main` should be a normal non-bare Git repository. Per-agent Agent Workspaces are Git worktrees of this repo at `<topic-workspace-dir>/agents/<agent-key>`.

The skill should initialize `topic-main` when missing and explicitly requested by the selected workflow, or validate an existing repo when present. If an existing `topic-main` is not a Git repo, has unsafe state for worktree creation, or lacks a usable base branch, the skill reports a blocker rather than repairing it silently.

Alternative considered: use a bare repo under `repos/topic-main.git`. A normal repo is easier for operators and agents to inspect, and it matches the user's requested path exactly.

### Decision: Make Branch Rules Deterministic

The default per-agent branch is `per-agent/<agent-key>/main`. Future branch creation uses `per-agent/<agent-key>/<branch-name>`.

Branch names must stay inside the owning agent prefix and must reject empty segments, `..`, names ending in `.lock`, leading slashes, trailing slashes, and names already checked out in another worktree. The skill should refuse to create two worktrees for the same branch from the same repo.

Alternative considered: derive branch names from Research Tasks or Workflow Stages. That would confuse Git branches with Isomer research lifecycle records and make simple per-agent ownership less obvious.

### Decision: Runtime Honors Approved Workspace Refs

Agent Team Instance creation should use a role binding's `agent_workspace_ref` when present, validated, and project-scoped. It records the path plan source as profile or packet material and materializes the Agent Workspace directory there. If no approved ref exists, runtime keeps the existing default of `<topic-workspace>/agents/<agent-instance-id>`.

This preserves current behavior for existing profiles while making prepared worktree paths real runtime paths.

Alternative considered: let the skill create worktrees only and rely on launch-time `ISOMER_AGENT_WORKSPACE_DIR` overrides. That would be process-local and brittle; downstream runtime records would still point at generated directories.

## Risks / Trade-offs

- Runtime and prepared worktree paths can drift if a user edits profile material after workspace creation. Mitigation: `validate-worktrees` checks profile or packet refs against Git worktrees, and runtime validation reports missing Agent Workspace paths.
- `topic-main` may contain uncommitted or conflicting work when new worktrees are requested. Mitigation: the skill validates repository state and reports blockers before mutation.
- Friendly `agent-key` values can collide after normalization. Mitigation: reject empty names and normalized collisions during `plan-agents`.
- The new skill overlaps superficially with `isomer-srv-env-setup` repo handling. Mitigation: document that `isomer-srv-env-setup` handles independent repos needed for environment gates, while this skill handles the shared topic collaboration repo and Agent Workspace worktrees.
- Prepared worktrees are advisory ownership boundaries, not hard isolation. Mitigation: Workspace Boundary docs must state write ownership, Peer Read Access, and integration expectations.

## Migration Plan

1. Add OpenSpec deltas and validate them.
2. Add the new operator skill folder, UI metadata, reference pages, and operator skill documentation.
3. Extend operator skill validation to require the new skill's command-style structure and key terms.
4. Update `isomer-admin-topic-team-specialize` so Git-backed setup delegates to the new skill and reports the resulting workspace refs.
5. Update profile and packet validation to reject cross-topic or unsafe Git-backed Agent Workspace refs.
6. Update Workspace Runtime creation to honor valid `agent_workspace_ref` values, with fallback to existing generated Agent Instance path behavior.
7. Add tests for skillset validation, worktree planning behavior, and runtime path-plan behavior.

Rollback is straightforward before implementation ships: remove the new skill and validation expectations, and runtime falls back to generated Agent Workspace paths.

## Open Questions

- Should `ensure-main-repo` initialize `topic-main` with an empty first commit, or should it require the operator to provide or seed repository content before worktree creation?
- Should the skill update packet/profile files directly, or should it write a workspace plan artifact that `materialize-profile` then consumes?
- Should per-agent Agent Workspace directories include ignored `runtime/`, `artifacts/`, `scratch/`, and `logs/` subdirectories inside the Git worktree, or should those local state paths be kept out of the worktree root by default?
