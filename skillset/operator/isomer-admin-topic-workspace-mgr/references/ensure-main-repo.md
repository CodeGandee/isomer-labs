# Ensure Main Repo

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require successful `resolve-workspace` output, including selected Topic Workspace path and resolved `topic.main_repo`, `topic.main_repo.tmp`, and `topic.main_repo.isomer_managed` labels with sources.
2. Inspect whether the resolved `topic.main_repo` path exists. If it exists, validate that it is a usable normal non-bare Git repository for worktree creation.
3. If the path is missing and the operator requested creation, create the resolved parent directory, initialize the repository, make the owner-managed branch `topic-owner/main` available, prepare or validate `topic.main_repo.tmp` with the Topic Main Repository root ignore rule, and prepare or validate `topic.main_repo.isomer_managed` plus tracked sublabels without hiding command failures.
4. If the path exists but is not a Git repository, is bare, has missing metadata, lacks a usable base branch, or has unsafe state for worktree creation, report a blocker.
5. Do not delete, replace, pull, reset, reinitialize, or repair the existing path silently.
6. Report the repository path, detected owner branch, current status summary, blockers, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to separate read-only repository inspection from any requested mutation, then execute only the safe portion.

## Repo Rules

The shared topic repository is the resolved `topic.main_repo` path. Under `isomer-default.v1`, that path is `<topic-workspace-dir>/repos/topic-main`. It is the Git anchor for every prepared Agent Workspace worktree in this Topic Workspace.

The repository should be normal and non-bare because operators and topic-local agents need to inspect it directly. The owner-managed checkout normally uses `topic-owner/main`; worker branches stay under `per-agent/<agent-name>/`.

The only standard Isomer-specific worker-facing namespace at the repository top level is the resolved `topic.main_repo.isomer_managed` path. Under `isomer-default.v1`, its tracked regime is `isomer-managed/tracked/`; do not create top-level Isomer collaboration directories in `topic-main`.

`topic.main_repo.tmp` is local, ignored, disposable, not shared, and not durable evidence. Under `isomer-default.v1`, it resolves to `<resolved topic.main_repo>/tmp/`. Prepare or validate the directory and the Topic Main Repository root `.gitignore` entry, but do not add `.gitkeep`, do not track tmp contents, and do not report tmp contents as Peer Read Access, handoff material, or Git-shared Isomer material.

## Blockers

Report a blocker for an existing non-Git path, a bare repository, a repository with missing object metadata, a base branch that cannot be determined, duplicate worktree metadata that Git reports as invalid, missing or ineffective `topic.main_repo.tmp` ignore policy, tracked files under `topic.main_repo.tmp`, or any command failure that would make later worktree creation ambiguous.
