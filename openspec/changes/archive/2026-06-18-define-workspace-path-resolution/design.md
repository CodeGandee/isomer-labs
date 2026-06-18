## Context

The manifested workspace design already defines `.isomer-labs/manifest.toml` as the Project Manifest and discovery authority for project-local Topic Workspaces. It also defines a Workspace Runtime plus file Artifacts under each Topic Workspace and per-agent Agent Workspaces under the active Topic Workspace during Agent Team Instance execution.

The research-paradigm skills currently preserve safety by marking many concrete paths as `[[tbd-surface:path-*]]`. That was correct while the workspace layout was unsettled, but it now creates friction: skills cannot tell an Agent Team Instance where ordinary research outputs belong, and each skill repeats a local copy of the same uncertainty. The better boundary is a single workspace path resolution contract that skills can consume.

## Goals / Non-Goals

**Goals:**

- Define default Project, Topic Workspace, Workspace Runtime, Run, Artifact, View Manifest, log, and Agent Workspace paths.
- Let the Operator Agent or Execution Adapter override those defaults at launch time with `ISOMER_*` environment variables.
- Preserve workspace planning authority by resolving paths from recorded task, Run, and Agent Instance context before relying on environment variables.
- Require canonicalization, Project-boundary validation, and durable recording of resolved paths before agents depend on them.
- Update research-paradigm skills so ordinary workspace and Artifact paths are resolved surfaces, not path TBD placeholders.

**Non-Goals:**

- Define the final SQLite schema for Artifact, Evidence Item, Gate, Finding, or Decision Record APIs.
- Define literature provider, command execution, scheduler, or GUI component contracts.
- Add OS-level isolation to Agent Workspaces. Workspace Boundaries remain advisory collaboration contracts.
- Require all Topic Workspaces to use the default root. The Project Manifest and workspace plan can choose different project-local paths.

## Decisions

### Decision 1: Add a Workspace Path Resolver contract

The implementation should centralize path computation in a Workspace Path Resolver. Research skills should request semantic targets such as `artifact:analysis-output`, `artifact:paper-draft`, `run-log`, or `agent-scratch`; they should not assemble paths directly.

Resolution precedence:

1. Recorded workspace plan for the Research Task, Run, handoff, Agent Team Instance, or Agent Instance.
2. `ISOMER_*` environment variables exported by the Execution Adapter for the current process.
3. Project Manifest defaults.
4. Built-in defaults.

Rationale: the recorded plan preserves Operator Agent authority and recovery. Environment variables support adapter-specific launch details without becoming durable truth. Manifest defaults let a Project customize layout once. Built-in defaults make the first workspace usable.

Alternative considered: each skill documents its own preferred path. Rejected because it repeats policy, makes validation inconsistent, and makes Agent Team Instance execution depend on which skill happened to run first.

### Decision 2: Use visible project-local defaults

The built-in workspace root should default to `<project>/topic-workspaces/`, not `.isomer-labs/workspaces/`. The Project Config Directory stays configuration and discovery state, while research Artifacts stay visible ordinary files.

Default layout:

```text
<project>/
  .isomer-labs/
    manifest.toml
  topic-workspaces/
    <topic-id>/
      state.sqlite
      artifacts/
      agents/
      tasks/
      runs/
      views/
      logs/
```

Agent Workspace layout:

```text
<topic-workspace>/
  agents/
    <agent-instance-id>/
      README.md
      boundary.toml
      runtime/
      artifacts/
      scratch/
      logs/
```

Run layout:

```text
<topic-workspace>/
  runs/
    <run-id>/
      run.toml
      prompts/
      tool-calls/
      logs/
      outputs/
```

Rationale: this follows the current design's split between Project Config Directory, Topic Workspace, Workspace Runtime, and Agent Workspace. It also keeps file Artifacts inspectable by the user and by agents.

Alternative considered: place all workspaces under `.isomer-labs/`. Rejected because `.isomer-labs/` is already defined as configuration and discovery state, not a workspace root.

### Decision 3: Keep environment variables small and root-oriented

The resolver should support a small set of root environment variables:

```text
ISOMER_PROJECT_ROOT
ISOMER_PROJECT_CONFIG_DIR
ISOMER_TOPIC_WORKSPACE_BASE_DIR
ISOMER_CURRENT_TOPIC_WORKSPACE_DIR
ISOMER_TOPIC_WORKSPACE_RUNTIME_DB
ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR
ISOMER_TOPIC_WORKSPACE_TASKS_DIR
ISOMER_TOPIC_WORKSPACE_RUNS_DIR
ISOMER_TOPIC_WORKSPACE_VIEWS_DIR
ISOMER_TOPIC_WORKSPACE_LOGS_DIR
ISOMER_AGENT_WORKSPACE_DIR
ISOMER_AGENT_WORKSPACE_RUNTIME_DIR
ISOMER_AGENT_WORKSPACE_ARTIFACTS_DIR
ISOMER_AGENT_WORKSPACE_SCRATCH_DIR
ISOMER_AGENT_WORKSPACE_LOGS_DIR
```

`BASE` names the directory containing many Topic Workspaces. `CURRENT` names the process-bound Topic Workspace. Topic Workspace subdirectory variables include `TOPIC_WORKSPACE` in the name so they cannot be confused with Agent Workspace subdirectories.

The resolver should derive research Artifact class paths from `ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR` unless a recorded workspace plan says otherwise:

```text
artifacts/intake/
artifacts/baselines/
artifacts/experiments/<run-id>/
artifacts/analysis/<campaign-id>/
artifacts/figures/<figure-set-id>/
artifacts/paper/<paper-id-or-default>/
artifacts/decisions/
artifacts/evidence/
artifacts/findings/
artifacts/handoffs/
```

Rationale: root-oriented variables are easier for adapters to export correctly and easier for validation to audit. Per-artifact-class variables can be added later if a real adapter needs them.

Alternative considered: define an environment variable for every Artifact class. Rejected for the first implementation because it creates a larger override surface before the artifact schema is settled.

### Decision 4: Validate and record resolved paths

Every resolved path should be canonicalized before use. Paths should remain inside the Project by default. A path outside the Project root should fail validation unless the recorded workspace plan or Project Manifest explicitly permits that external root.

The resolver should record the effective path set in Workspace Runtime or a Provenance Record. Records should include source of each value, such as `plan`, `env`, `manifest`, or `default`.

Rationale: environment variables are process-local and disappear after launch. Recovery, validation, and GUI inspection need durable refs.

Alternative considered: trust process environment as the source of truth. Rejected because it breaks recovery and makes later agents guess which paths were active.

### Decision 5: Narrow path TBD usage in research skills

Once this contract is implemented, path placeholders in research skills should mean only "outside the resolved workspace contract" or "artifact class not yet mapped." Ordinary paths such as active Topic Workspace, Workspace Runtime, Agent Workspace, run logs, experiment outputs, analysis outputs, paper outputs, and figure outputs should use the resolver contract instead of `[[tbd-surface:path-*]]`.

API, schema, provider, and policy TBD placeholders should remain until their contracts are separately settled.

Rationale: this keeps the skills conservative about real unknowns while removing noise from a design area that has enough structure to standardize.

## Risks / Trade-offs

- [Risk] Environment overrides can point to the wrong Project or a stale workspace. -> Mitigation: validate canonical paths, require a matching Project root or explicit external-root allowance, and record the resolved source in Workspace Runtime.
- [Risk] Visible `topic-workspaces/` may add project-root noise. -> Mitigation: keep the root configurable through Project Manifest defaults and document it as generated workspace state.
- [Risk] Existing skill references contain copied local TBD registries. -> Mitigation: update the shared registry first, then update local copies and run a path-placeholder scan.
- [Risk] Deriving Artifact class paths may be too rigid for future adapters. -> Mitigation: treat class paths as defaults, allow recorded workspace plans to override them, and leave per-class env vars out until there is concrete demand.

## Migration Plan

1. Update the workspace-engine design notes with the Workspace Path Resolver contract, default layout, env variable list, validation rule, and durable recording rule.
2. Update `isomer-rsch-shared/references/tbd-surface-registry.md` to mark ordinary workspace path surfaces as resolved by the workspace path resolution contract or replace them with a single path-resolution contract reference.
3. Update local `isomer-research-contract.md` copies and route-specific references so skills request semantic Artifact kinds and workspace scopes instead of ordinary path TBD placeholders.
4. Preserve API, schema, provider, and policy TBD placeholders.
5. Run searches for `[[tbd-surface:path-`, `path-topic-workspace`, `path-workspace-runtime`, `path-agent-workspace`, hard-coded source paths, and local absolute paths.
6. Validate OpenSpec and review the final diff for accidental runtime API definitions.

Rollback is documentation-only for this change: revert the design and skill-reference edits, restoring the path TBD placeholders.

## Open Questions

- Should a future runtime expose per-artifact-class environment variables after Artifact schemas stabilize?
- What manifest field should explicitly allow external workspace roots outside the Project?
- Should the first `isomer-cli` implementation create `topic-workspaces/<topic-id>/` eagerly when a Research Topic starts, or only when the first Research Task or Run needs durable state?
