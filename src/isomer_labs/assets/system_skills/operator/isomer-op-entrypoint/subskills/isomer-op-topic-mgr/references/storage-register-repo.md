# Storage Register Repo

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, and current Topic Workspace Manifest through `storage-resolve`.
2. Extract the requested repository label, path, purpose, and whether the operator wants an empty support directory or needs to register an existing externally acquired repository.
3. Require a grouped non-main `topic.repos.*` semantic label; reject labels that collide with `topic.repos.main`, `topic.actors.*`, `agent.*`, `topic.records.*`, or `topic.runtime`.
4. For an existing repository, require caller evidence that external acquisition and source-identity verification succeeded, then plan `project repos register <label> --path <existing-path>`. Do not execute or accept repository commands through this subcommand.
5. For an explicitly requested empty support directory, plan `project repos create <label>` and state that it only creates and registers a directory; it does not initialize or acquire a repository.
6. Mutate only after explicit operator intent, then verify the new binding with `project paths get` and `project paths explain`.
7. Report the registered label, path, fixed `storage_profile = "topic_repo"`, path source, command evidence, blockers, and next action.

If the user's task does not map cleanly to these steps, ask for the missing repository label, storage profile, path, or helper-created default intent before mutation.

## Output

Report the registration outcome and selected Research Topic, then name the registered label and path, storage profile and path source, commands run, blockers, and the next action.

## Operational Contract

- Treat additional topic repositories as support surfaces.
- Keep repository source-control commands outside Isomer and register only after external verification.
- Use `project paths default <label>` only for a read-only candidate when an external repository still needs acquisition.

## Guardrails

- DO NOT describe non-main repositories as Topic Actor Workspace or Agent Workspace worktree sources.
- DO NOT use `project repos create` as a pre-acquisition target reservation.
