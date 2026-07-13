# Storage Register Repo

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, and current Topic Workspace Manifest through `storage-resolve`.
2. Extract the requested repository label, path, purpose, storage profile, and whether the operator wants a helper-created default path under `repos/extern/...`.
3. Require a grouped non-main `topic.repos.*` semantic label and explicit `storage_profile`; reject labels that collide with `topic.repos.main`, `topic.actors.*`, `agent.*`, `topic.records.*`, or `topic.runtime`.
4. Plan the `project repos create` or `project paths register` command and show the resolved path source before mutation.
5. Mutate only after explicit operator intent, then verify the new binding with `project paths get` and `project paths explain`.
6. Report the registered label, path, storage profile, command evidence, blockers, and next action.

If the user's task does not map cleanly to these steps, ask for the missing repository label, storage profile, path, or helper-created default intent before mutation.

## Output

Report the registration outcome and selected Research Topic, then name the registered label and path, storage profile and path source, commands run, blockers, and the next action.

## Guardrails

Additional topic repositories are support surfaces. Do not describe non-main repositories as Topic Actor Workspace or Agent Workspace worktree sources.
