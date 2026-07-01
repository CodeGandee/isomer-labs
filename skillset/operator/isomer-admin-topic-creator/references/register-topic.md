# Register Topic

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require a concrete topic statement or topic id from `resolve-topic-input`.
2. Check Project Manifest-backed Research Topic and Topic Workspace registration through `isomer-cli project topics list`, `isomer-cli project topics show`, or equivalent Isomer API surfaces.
3. If missing and mutation is approved, create registration through `isomer-cli project topics create <topic-id> --statement "<research topic>" --workspace-dir <topic-workspace-dir>` when a custom workspace dir is required, or the supported default command shape when the default content root is acceptable.
4. Validate the resulting Topic Workspace ref, topic workspace path, effective Topic Workspace Pixi binding, and semantic path preview.
5. Report registration status, Project Manifest refs, Topic Workspace path, blockers, and next subcommand.

If the user's task does not map cleanly to these steps, report the missing topic statement, topic id, Project root, workspace dir, or mutation approval.

## Guardrails

Do not hand-edit Project Manifest or `topic-workspace.toml`. Use supported CLI/API surfaces.
