# Tasks: Enforce Globally Unique Agent Instance ids

## 1. Identifier Generation

- [x] 1.1 Add a helper in `src/isomer_labs/runtime/identifiers.py` that generates a globally unique Agent Instance id containing topic workspace, team counter, role slug, and a short random suffix.
- [x] 1.2 Update `WorkspaceRuntimeStore.next_agent_team_instance_id` if the counter logic needs to account for globally scoped uniqueness. (No change needed: Agent Instance ids use a UUID suffix for global uniqueness.)

## 2. Agent Instance and Workspace Creation

- [x] 2.1 Replace the team-scoped id generation in `src/isomer_labs/runtime/store.py` (`agent_id = f"{team_id}-{_slug(binding.role_id)}"`) with the new global id helper.
- [x] 2.2 Ensure `record_path_plan` is called with surface `agent_workspace:<agent-instance-id>` before the Agent Workspace directory is created.
- [x] 2.3 Add a creation-time uniqueness check that queries `agent_instances` for the generated id and rejects duplicates with a diagnostic.

## 3. Runtime Validation

- [x] 3.1 Add a validation check in `src/isomer_labs/runtime/validation*.py` that scans all Topic Workspaces in the Project for duplicate Agent Instance ids.
- [x] 3.2 Report duplicate ids as `Diagnostic` entries with severity `error` and concept `Agent Instance Identity`. (`ValidationIssueRecord` is not currently used by the validation framework; the existing `Diagnostic` format is used for consistency.)

## 4. Tests and Fixtures

- [x] 4.1 Update `tests/unit/test_isomer_cli.py` profile fixtures to remove or replace stale `agent_workspace_ref = "topic-workspaces/{workspace_topic}/agent-workspaces/{profile_id}/{role_id}"` references.
- [x] 4.2 Update test assertions that depend on the old `{team_id}-{role}` Agent Instance id shape.
- [x] 4.3 Add unit tests that verify two Agent Team Instances cannot produce the same Agent Instance id and that `runtime validate` reports duplicates.

## 5. Verification

- [x] 5.1 Run `pixi run lint` and fix style issues.
- [x] 5.2 Run `pixi run typecheck` and fix type errors.
- [x] 5.3 Run `pixi run test` and ensure all unit tests pass.
