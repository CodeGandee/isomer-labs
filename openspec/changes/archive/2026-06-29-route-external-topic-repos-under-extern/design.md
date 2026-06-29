## Context

The current storage contract distinguishes the Topic Main Repository (`topic.repos.main`) from dynamic grouped topic repository labels (`topic.repos.<group...>.<repo-name>`), but `project repos create` still defaults non-main repositories to `repos/<group>/<repo-name>`. That physical layout makes supporting repositories look like peers of `repos/topic-main`, even though only `topic-main` is the primary collaboration repository and Agent Workspace worktree source.

The storage-layer design already says callers should resolve semantic labels instead of remembering physical paths. This change keeps that contract and only changes the default physical placement for non-main topic repositories.

## Goals / Non-Goals

**Goals:**

- Keep `topic.repos.main` defaulting to `repos/topic-main`.
- Route non-main topic repositories created by `project repos create` to `repos/extern/<repo-label-path>`.
- Preserve `topic.repos.<group...>.<repo-name>` labels so storage semantics do not depend on the `extern` directory name.
- Update service and operator skills so topic environment setup acquires supporting repositories under resolved semantic paths, with `repos/extern/...` as the default non-main layout.
- Update docs and tests to describe the role split between primary development repository and external/supporting repositories.

**Non-Goals:**

- Do not add a new storage profile for external repositories.
- Do not move existing filesystem content automatically.
- Do not make non-main repositories read-only. They remain modifiable when the gate or user authorizes modification.
- Do not use non-main repositories as Agent Workspace worktree sources.

## Decisions

1. **Keep semantic labels unchanged.**

   Non-main repositories continue to use labels such as `topic.repos.tools.benchmarks`. The default path changes to `repos/extern/tools/benchmarks`, but callers still query the label. This avoids turning physical layout into API.

2. **Keep `topic_repo` as the storage profile.**

   The existing `topic_repo` profile already captures topic-local durable repository semantics. A new `topic_external_repo` profile would create more schema and docs churn without changing the path safety, lifecycle, or Git semantics needed for this change.

3. **Make `project repos create` the default-path boundary.**

   Dynamic grouped repository labels only become resolvable after registration. The helper command is the right place to pick the default target path. Explicit `project paths register ... --path ... --storage-profile topic_repo` remains available for custom locations.

4. **Protect the built-in main repository label.**

   `project repos create main` should not create or rebind `topic.repos.main` at `repos/main`. Users should materialize or override the built-in label through the path commands that already know `repos/topic-main`.

5. **Treat `repos/extern/...` as topic-local support material, not an external root outside the Topic Workspace.**

   The word `extern` means "not the primary development target" here. It does not move repositories outside the selected Topic Workspace, and it does not bypass path safety validation.

## Risks / Trade-offs

- Existing docs or tests may still encode `repos/<repo-name>` for independent repositories. Mitigation: update the CLI examples, Topic Workspace documentation, skill references, and validation fixtures together.
- Existing user workspaces may already have repos under `repos/<name>`. Mitigation: do not migrate or delete them; existing manifest bindings and explicit paths remain valid.
- `repos/extern/...` could be mistaken as read-only. Mitigation: document that these repositories are still modifiable when explicitly required by the gate or user, but are not the primary Agent Workspace worktree source.

## Migration Plan

New helper-created repositories use `repos/extern/...`. Existing manifest bindings keep resolving to their recorded paths. Users who want to move existing repositories can register or update bindings explicitly, then move content under operator-controlled migration steps outside this change.

Rollback is limited to restoring the old helper default and docs. Existing bindings created during this change would remain explicit manifest entries and would not be deleted by rollback.

## Open Questions

None.
