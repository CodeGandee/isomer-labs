# Ensure Main Repo

Use this subcommand for inspection, validation, or an explicitly requested manual topology operation. Canonical Topic Main Development Repository creation, configuration, and projection materialization belong to `isomer-srv-topic-env-setup`.

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require successful `storage-resolve` output:
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
6. Inspect root-level topic-main agent guidance files when the repository is usable:
   - Run or route to `isomer-cli --print-json project topic-main-guidance inspect --topic <topic>` or the equivalent CLI-backed API.
   - Report the returned target statuses for root `AGENTS.md` and `CLAUDE.md`, the CLI guidance version, blockers, and next action.
   - Treat `src/isomer_labs/assets/topic_main_guidance/isomer-labs-topic-main-guidance.v1.md.j2` as the canonical large-text template asset.
   - Do not copy the full rendered guidance body into this skill.
7. If topic-main agent guidance is missing or stale and the operator did not explicitly request guidance repair, report the condition and recommend an explicit `storage-inspect-main` guidance repair request or canonical repair through `isomer-srv-topic-env-setup`.
8. If the operator explicitly requested topic-main agent guidance repair or refresh, mutate only after mutation confirmation:
   - Run or route to `isomer-cli --print-json project topic-main-guidance ensure --topic <topic> --yes` or the equivalent CLI-backed API.
   - Preserve existing content outside the CLI-managed marked block.
   - Report changed files, target statuses, guidance block version, blockers, and next action from the CLI output.
9. Do not delete, replace, pull, reset, reinitialize, or repair the existing path silently.
10. Report the repository path, detected owner branch, current status summary, predecessor evidence, agent guidance posture, blockers, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to separate read-only repository inspection from any requested mutation, then execute only the safe portion.

## Repo Rules

The Topic Main Development Repository is the resolved `topic.repos.main` path. Under `isomer-default.v1`, that path is `<topic-workspace-dir>/repos/topic-main`. It is the Git anchor for every prepared Agent Workspace worktree in this Topic Workspace.

The repository should be normal and non-bare because operators and topic-local agents need to inspect it directly. The owner-managed checkout normally uses `topic-owner/main`; worker branches stay under `per-agent/<agent-name>/`.

The only standard Isomer-specific worker-facing namespace at the repository top level is the resolved `topic.repos.main.isomer_managed` path. Under `isomer-default.v1`, its tracked regime is `isomer-managed/tracked/`, and external repo projections use `isomer-managed/topic-owned/{readonly,writable}/extern/` plus `isomer-managed/tracked/manifests/extern-projections.toml`; do not create top-level Isomer collaboration directories in `topic-main`.

Root-level `AGENTS.md` and `CLAUDE.md` are normal topic-main files used by external agents and actors as worker-facing rule files. They are eligible for Git tracking and are not stored under `topic.repos.main.isomer_managed`, tmp paths, runtime paths, or projection roots. Their Isomer-specific content must be rendered, inspected, and updated by `isomer-cli project topic-main-guidance` from the packaged `.j2` template asset; existing user-authored content outside that CLI-managed block is owner content and must be preserved.

`topic.repos.main.tmp` is local, ignored, disposable, not shared, and not durable evidence. Under `isomer-default.v1`, it resolves to `<resolved topic.repos.main>/tmp/`. Prepare or validate the directory and the Topic Main Development Repository root `.gitignore` entry, but do not add `.gitkeep`, do not track tmp contents, and do not report tmp contents as Peer Read Access, handoff material, or Git-shared Isomer material.

## Blockers

Report a blocker for an existing non-Git path, a bare repository, a repository with missing object metadata, a base branch that cannot be determined, duplicate worktree metadata that Git reports as invalid, missing or ineffective `topic.repos.main.tmp` ignore policy, tracked files under `topic.repos.main.tmp`, missing or stale `AGENTS.md` or `CLAUDE.md` Isomer topic-main guidance without explicit repair authorization, malformed or duplicated `isomer-labs-topic-main-guidance` blocks, unknown guidance block versions, or any command failure that would make later worktree creation ambiguous.

## Agent Guidance Repair Content

When explicit repair is authorized, use `isomer-cli --print-json project topic-main-guidance ensure --topic <topic> --yes`. The CLI renders the canonical Isomer topic-main guidance block from `src/isomer_labs/assets/topic_main_guidance/isomer-labs-topic-main-guidance.v1.md.j2`; this skill must not carry a duplicate full copy of that rendered prose.

Use `isomer-cli --print-json project topic-main-guidance inspect --topic <topic>` for read-only posture. Do not substitute concrete Research Topic ids, topic statements, Topic Workspace paths, Topic Actor names, Agent Names, runtime file paths, credentials, external repository paths, resolved `manifest_path`, or resolved `pixi_environment` into Topic Manager guidance instructions.
