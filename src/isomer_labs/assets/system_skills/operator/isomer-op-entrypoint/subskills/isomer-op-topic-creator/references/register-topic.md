# Register Topic

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require a concrete topic statement or topic id from `resolve-topic-input`.
2. Check Project Manifest-backed Research Topic and Topic Workspace registration through `isomer-cli project topics list`, `isomer-cli project topics show`, or equivalent Isomer API surfaces.
3. If registration is missing and mutation is approved, select the supported command shape from the Topic Workspace candidate source:
   - When the user did not explicitly supply a custom Topic Workspace directory, run `isomer-cli project topics create <topic-id> --statement "<research topic>"` without `--workspace-dir`. The CLI must resolve the Project Manifest `topic_workspace_base_dir`, or the built-in `isomer-content/topic-ws/` base when that manifest value is absent, and create `isomer-content/topic-ws/<topic-id>` under the built-in default.
   - When the user explicitly supplied a custom Topic Workspace directory, run `isomer-cli project topics create <topic-id> --statement "<research topic>" --workspace-dir <topic-workspace-dir>` after path-safety and collision checks.
4. Validate the resulting Topic Workspace ref, Topic Workspace path, effective Topic Workspace Pixi binding, and semantic path preview. When no custom directory was supplied, require the resulting path to equal `<topic_workspace_base_dir>/<topic-id>` and treat a different path as a blocker.
5. Report registration status, Project Manifest refs, Topic Workspace path, Topic Workspace candidate source, command shape, blockers, and readiness state.

If the user's task does not map cleanly to these steps, report the missing topic statement, topic id, Project root, workspace dir, or mutation approval.

## Operational Notes

- Use supported CLI/API surfaces.

## Guardrails

- DO NOT hand-edit Project Manifest or `topic-workspace.toml`.
- DO NOT pass `--workspace-dir <topic-workspace-dir>` for ordinary topic creation when the user did not explicitly supply a custom Topic Workspace directory.
- DO NOT substitute a bare `<topic-id>` for `<topic-workspace-dir>`; the normal default is `isomer-content/topic-ws/<topic-id>` when the Project Manifest uses the built-in Topic Workspace base.
