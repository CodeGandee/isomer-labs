# Ensure Main Repo

Use this subcommand for inspection, validation, or an explicitly requested manual topology operation. Canonical Topic Main Development Repository creation, configuration, and projection materialization belong to `isomer-srv-topic-env-setup`.

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require successful `resolve-workspace` output:
   - Include selected Topic Workspace path.
   - Include resolved `topic.repos.main`, `topic.repos.main.tmp`, `topic.repos.main.isomer_managed`, projection root labels, and `topic.repos.main.projections.manifest` with sources.
2. Inspect whether the resolved `topic.repos.main` path exists. If it exists, validate that it is a usable normal non-bare Git repository for worktree inspection and report predecessor evidence.
3. If the path is missing and the operator did not explicitly request a manual topology operation, report a blocker and route canonical repair to `isomer-srv-topic-env-setup`.
4. If the path is missing and the operator explicitly requested a manual topology operation, prepare the repository only after mutation confirmation, risk notes, and predecessor evidence or explicit manual acceptance:
   - Create the resolved parent directory.
   - Initialize the repository.
   - Make the owner-managed branch `topic-owner/main` available.
   - Prepare or validate `topic.repos.main.tmp` with the Topic Main Development Repository root ignore rule.
   - Prepare or validate `topic.repos.main.isomer_managed` plus tracked sublabels without hiding command failures.
5. If the path exists but is not a Git repository, is bare, has missing metadata, lacks a usable base branch, or has unsafe state for worktree inspection, report a blocker.
6. Do not delete, replace, pull, reset, reinitialize, or repair the existing path silently.
7. Report the repository path, detected owner branch, current status summary, predecessor evidence, blockers, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to separate read-only repository inspection from any requested mutation, then execute only the safe portion.

## Repo Rules

The Topic Main Development Repository is the resolved `topic.repos.main` path. Under `isomer-default.v1`, that path is `<topic-workspace-dir>/repos/topic-main`. It is the Git anchor for every prepared Agent Workspace worktree in this Topic Workspace.

The repository should be normal and non-bare because operators and topic-local agents need to inspect it directly. The owner-managed checkout normally uses `topic-owner/main`; worker branches stay under `per-agent/<agent-name>/`.

The only standard Isomer-specific worker-facing namespace at the repository top level is the resolved `topic.repos.main.isomer_managed` path. Under `isomer-default.v1`, its tracked regime is `isomer-managed/tracked/`, and external repo projections use `isomer-managed/topic-owned/{readonly,writable}/extern/` plus `isomer-managed/tracked/manifests/extern-projections.toml`; do not create top-level Isomer collaboration directories in `topic-main`.

`topic.repos.main.tmp` is local, ignored, disposable, not shared, and not durable evidence. Under `isomer-default.v1`, it resolves to `<resolved topic.repos.main>/tmp/`. Prepare or validate the directory and the Topic Main Development Repository root `.gitignore` entry, but do not add `.gitkeep`, do not track tmp contents, and do not report tmp contents as Peer Read Access, handoff material, or Git-shared Isomer material.

## Blockers

Report a blocker for an existing non-Git path, a bare repository, a repository with missing object metadata, a base branch that cannot be determined, duplicate worktree metadata that Git reports as invalid, missing or ineffective `topic.repos.main.tmp` ignore policy, tracked files under `topic.repos.main.tmp`, or any command failure that would make later worktree creation ambiguous.
