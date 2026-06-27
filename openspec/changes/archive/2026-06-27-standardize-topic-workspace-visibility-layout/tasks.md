## 1. Canonical Language and Documentation

- [x] 1.1 Update `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` to define Topic Main Repository, topic-local Agent Name, Agent Workspace Worktree, root `records/*`, root `runtime/`, and the worker visibility boundary.
- [x] 1.2 Revise `docs/topic-workspace-definition.md` so the standard layout uses `repos/topic-main`, `agents/<agent-name>`, `records/*`, `runtime/`, `.isomer-agent/`, and approved symlink links consistently.
- [x] 1.3 Update `docs/concepts.md`, `docs/system-design.md`, `docs/runtime-and-files.md`, `docs/workflows.md`, `docs/isomer-cli.md`, `docs/getting-started.md`, and `docs/troubleshooting.md` to remove root worker-visible `shared/artifacts/tasks/runs/views/logs` guidance.
- [x] 1.4 Add migration guidance for legacy root collaboration directories, `agent-workspaces/`, `agents/<agent-instance-id>`, `agent-key`, and primary authored `agent_workspace_ref` usage.

## 2. Workspace Path Resolution and Runtime Layout

- [x] 2.1 Update `src/isomer_labs/paths.py` to expose path surfaces for `repos`, `topic_main_repo`, `agents`, `records`, `records_artifacts`, `records_tasks`, `records_runs`, `records_views`, `records_logs`, `runtime`, and Agent Workspace `.isomer-agent/` support paths.
- [x] 2.2 Treat existing `ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR`, `ISOMER_TOPIC_WORKSPACE_TASKS_DIR`, `ISOMER_TOPIC_WORKSPACE_RUNS_DIR`, `ISOMER_TOPIC_WORKSPACE_VIEWS_DIR`, and `ISOMER_TOPIC_WORKSPACE_LOGS_DIR` as compatibility aliases for owner-preserved `records/*` surfaces with source-detail diagnostics.
- [x] 2.3 Update `src/isomer_labs/runtime/models.py` and `src/isomer_labs/runtime/schema.py` so runtime initialization creates and validates the new directory set and stops creating old root collaboration directories.
- [x] 2.4 Update runtime path-plan persistence in `src/isomer_labs/runtime/store.py` so initialization records the new surfaces before dependent records use them.
- [x] 2.5 Add non-destructive validation diagnostics for existing legacy root collaboration directories and missing standard visibility directories.

## 3. Agent Workspace Planning and Runtime Records

- [x] 3.1 Extend profile and packet models to carry topic-local `agent_name` and branch planning fields while preserving `agent_workspace_ref` as derived compatibility material where existing schemas need it.
- [x] 3.2 Update `src/isomer_labs/workspace_refs.py`, `src/isomer_labs/team_profiles.py`, `src/isomer_labs/topic_team_instantiation.py`, `src/isomer_labs/profile_bundle_validation.py`, and `src/isomer_labs/topic_team_packet_validation.py` to validate agent-name worktree plans and derive compatibility refs.
- [x] 3.3 Update Agent Team Instance creation in `src/isomer_labs/runtime/store.py` so active role bindings require validated agent-name workspace plans and no longer silently fall back to `agents/<agent-instance-id>`.
- [x] 3.4 Extend Agent Workspace runtime records or linked metadata to include topic-local agent name, expected repo ref, expected branch namespace, and `.isomer-agent/` boundary refs.
- [x] 3.5 Update runtime validation to distinguish globally unique Agent Instance ids from topic-local agent names and to allow the same agent name in different Topic Workspaces.

## 4. Operator Skill Revisions

- [x] 4.1 Revise `skillset/operator/isomer-admin-topic-workspace-mgr` entrypoint and references to use `agent-name`, `topic-owner/main`, `per-agent/<agent-name>/...`, `records/*`, `.isomer-agent/`, and derived compatibility refs consistently.
- [x] 4.2 Update `isomer-admin-topic-workspace-mgr` workflows to create or validate `repos/topic-main`, owner branch, per-agent worktrees, ignored `.isomer-agent/` support dirs, optional `.isomer-agent/links/*` symlinks, and visibility diagnostics.
- [x] 4.3 Revise `skillset/operator/isomer-admin-topic-team-specialize/references/setup-agent-workspace.md` and related finalize/validate pages to delegate standard worktree setup and report agent-name workspace evidence.
- [x] 4.4 Update `skillset/operator/isomer-admin-project-mgr` runtime-boundary and help references to explain the new Topic Workspace visibility layout and hand off worktree setup to the topic workspace manager.
- [x] 4.5 Update skill validation tests and fixtures so they reject stale `agent-key` public wording where the new contract requires `agent-name`.

## 5. Houmao Adapter and Launch Behavior

- [x] 5.1 Update Houmao adapter materialization and launch code to consume topic-local agent names and recorded Agent Workspace path plans.
- [x] 5.2 Ensure each mapped Houmao managed agent is prepared or launched with cwd set to `<topic-workspace>/agents/<agent-name>`.
- [x] 5.3 Move or keep generated adapter payloads, manifests, logs, inspection snapshots, and reconciliation material under `runtime/adapters/houmao/` or `records/*` path plans by default.
- [x] 5.4 Add explicit publication behavior for any adapter output that must become worker-visible through `repos/topic-main`.

## 6. Fixtures, Tests, and Compatibility Coverage

- [x] 6.1 Migrate fixture profile and packet material from `agent-workspaces/` or `agent_workspace_ref`-first planning to agent-name worktree plans under `agents/<agent-name>`.
- [x] 6.2 Update `tests/unit/test_isomer_cli.py` assertions for runtime init directories, path plan surfaces, Agent Workspace path sources, missing workspace-plan blockers, and legacy layout diagnostics.
- [x] 6.3 Update `tests/unit/test_validate_skillsets.py` and skill fixture writers for the revised operator skill language and expected output fields.
- [x] 6.4 Update documentation validation tests to require the Topic Workspace visibility page and reject stale root collaboration layout examples.
- [x] 6.5 Add regression tests that legacy root directories and legacy workspace refs produce diagnostics without deleting or moving files.

## 7. Verification

- [x] 7.1 Run `openspec validate standardize-topic-workspace-visibility-layout --strict`.
- [x] 7.2 Run `pixi run lint`.
- [x] 7.3 Run `pixi run typecheck`.
- [x] 7.4 Run `pixi run test`.
- [x] 7.5 Run `pixi run validate-operator-skills` and any repo-local docs validation command updated by this change.
