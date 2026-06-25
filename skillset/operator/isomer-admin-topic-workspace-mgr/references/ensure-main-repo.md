# Ensure Main Repo

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require successful `resolve-workspace` output, including selected Topic Workspace path and expected `<topic-workspace-dir>/repos/topic-main`.
2. Inspect whether `repos/topic-main` exists. If it exists, validate that it is a usable normal non-bare Git repository for worktree creation.
3. If the path is missing and the operator requested creation, create parent `repos/`, initialize `topic-main`, and make the initial base branch available without hiding command failures.
4. If the path exists but is not a Git repository, is bare, has missing metadata, lacks a usable base branch, or has unsafe state for worktree creation, report a blocker.
5. Do not delete, replace, pull, reset, reinitialize, or repair the existing path silently.
6. Report the repository path, detected base branch, current status summary, blockers, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to separate read-only repository inspection from any requested mutation, then execute only the safe portion.

## Repo Rules

The shared topic repository is `<topic-workspace-dir>/repos/topic-main`. It is the Git anchor for every prepared Agent Workspace worktree in this Topic Workspace.

The repository should be normal and non-bare because operators and topic-local agents need to inspect it directly.

## Blockers

Report a blocker for an existing non-Git path, a bare repository, a repository with missing object metadata, a base branch that cannot be determined, duplicate worktree metadata that Git reports as invalid, or any command failure that would make later worktree creation ambiguous.
