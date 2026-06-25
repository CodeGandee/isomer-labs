# Create Worktrees

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require successful `resolve-workspace`, usable `ensure-main-repo` output, and a `plan-agents` result with role ids, agent keys, paths, and branches.
2. For each planned agent key, inspect existing Git worktrees for `<topic-workspace-dir>/repos/topic-main`.
3. If `<topic-workspace-dir>/agents/<agent-key>` already exists as a worktree of `topic-main` on `per-agent/<agent-key>/main`, report it as ready.
4. If the Agent Workspace path exists but is not the expected worktree, report a blocker and do not overwrite it.
5. If `per-agent/<agent-key>/main` is already checked out in another worktree, report a blocker and do not create a second worktree for the same branch.
6. Create missing branches and worktrees only for safe planned entries, using `topic-main` as the Git anchor and `<topic-workspace-dir>/agents/<agent-key>` as the Agent Workspace path.
7. Report ready worktrees, created worktrees, skipped entries, blockers, and validation refs.

If the user's task does not map cleanly to these steps, use your native planning tool to inspect first, separate ready entries from blocked entries, and mutate only entries that are safe.

## Safety Rules

Use idempotent Git worktree operations. Do not delete, clean, reset, or reuse an existing nonmatching path.

Do not create a worktree outside the selected Topic Workspace. Do not create a worktree for a branch that Git already marks as checked out elsewhere.
