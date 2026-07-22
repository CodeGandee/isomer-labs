## Why

Topic Workspaces currently lack an operator-owned way to opt into local root-level Git tracking or to publish a privacy-reviewed representation to a user-selected remote. These are different needs: local tracking manages history in the canonical Topic Workspace without remote operations, while remote publication builds and synchronizes a separate sanitized copy without depending on local tracking.

## What Changes

- Add protected operator subskill `isomer-op-topic-workspace-git`, exposed as `isomer-op-entrypoint->topic-git`, with an overall `status` operation and independent `local` and `publish` operation groups. These are skill operations, not an Isomer CLI command family.
- Define Source Topic Workspace as a contextual role of the canonical Topic Workspace when contrasted with a Topic Publication Copy. Define Topic Publication Copy as a derived projection, not a fourth managed workspace type or canonical source.
- Use `isomer-cli --print-json` only for read-only Project, Research Topic, semantic-path, Topic Actor, Agent, and Workspace Runtime queries. After pinning and validating those query results, teach the agent to invoke Git directly with explicit `git -C <resolved-path> ...` commands.
- Keep both in-workspace tracking and remote publication disabled by default. Topic creation, environment setup, actor setup, and agent setup do not enable or require either layer.
- Add opt-in in-workspace tracking that initializes a Git repository at the Source Topic Workspace root only after every ancestor Git repository reports that root as untracked and effectively ignored, plans exact local tracking and ignore changes, and creates local commits without configuring, contacting, or pushing to a remote. Topic Git reports ancestor prerequisites but never mutates an ancestor repository.
- Preserve the existing Topic Main, Topic Actor Workspace, and Agent Workspace Git topology during local tracking. The root repository excludes those nested Git workspaces and may record their branch, commit, and dirty-state summary without reparenting them.
- Add independent opt-in remote publication that accepts a credential-safe remote, creates a disposable ignored Topic Publication Copy under the Project temporary directory, sanitizes source material, and never requires a Source Topic Workspace root repository or local commit.
- Allow remote publication as soon as the Research Topic and Topic Workspace are registered, even before Workspace Runtime, intent, environment, Topic Main, actor, agent, or finalization stages are ready. Missing later-stage components are reported and skipped or blocked according to the approved publication plan.
- Resolve the default publication-copy parent by inspecting Project-root `tmp/` and `temp/` directories and effective Git ignore policy. Prefer an existing ignored temporary directory; when none exists, plan creation of ignored Project-root `tmp/`.
- By default, select every currently available Topic Main, registered Topic Actor Workspace, and selected-team Agent Workspace resolved through read-only Isomer queries, unless the user explicitly excludes a component in the current publication plan. Materialize selected components as sanitized submodules in the Topic Publication Copy and store the superproject and component histories on deterministic branches of the same user-provided remote.
- Never copy source `.git` directories, worktree metadata, remote configuration, or source repository history into the Topic Publication Copy.
- Add privacy dispositions, placeholder generation, publication manifests, source-copy comparison, conflict detection, missing-copy reconstruction, fetch-first remote checks, component-first pushes, and superproject-last publication.
- Treat the supplied remote as dedicated to one Research Topic publication and initially empty. Use normal pushes for absent or compatible publication branches; when a deterministic publication branch is incompatible, require a fresh destructive-change plan and explicit force-push permission before using plain `--force` for only the named branch and replacement commit.
- Make `publish sync` compare the Source Topic Workspace filesystem, the last projection manifest, the current Topic Publication Copy, and fetched remote state before applying necessary mutations and pushing again.
- Persist local-tracking and remote-publication state independently so either layer may be enabled, disabled, missing, stale, or blocked without changing the other.
- Require an existing valid Workspace Runtime for local Git mutations. Before Workspace Runtime exists, keep publication plans, bindings, projection state, and outcomes only in an ignored local support root inside the Topic Publication Copy; after runtime becomes available, the next approved publication mutation records the credential-safe binding and current state under `<topic.runtime>/topic-git/` without editing `state.sqlite` or using Isomer CLI mutation commands.

## Capabilities

### New Capabilities

- `topic-workspace-git-management`: Defines the protected `topic-git` skill, independent opt-in state model, overall status, operation grouping, read-only Isomer query boundary, direct Git execution contract, routing, and shared safety boundaries.
- `topic-workspace-local-git-tracking`: Defines local-only Topic Workspace root repository initialization, exact tracking plans, ignore maintenance, nested workspace preservation, and commits with no remote dependency or operation.
- `topic-workspace-git-publication`: Defines Topic Publication Copy placement, privacy projection, sanitized component repositories and submodules, same-remote branch layout, synchronization comparison, and guarded remote push.

### Modified Capabilities

- `isomer-op-entrypoint-skill`: Route local Topic Workspace tracking and remote publication requests to the protected `topic-git` member while preserving their independence.
- `topic-manager-skill`: Delegate explicit Git tracking or publication requests instead of embedding those workflows in general initialized-topic management.
- `isomer-documentation-system-guide`: Document the two opt-in layers, Source Topic Workspace and Topic Publication Copy boundary, operation effects, query and execution boundary, temporary placement, sanitization, submodules, and synchronization behavior.

## Impact

The change affects packaged operator skills, the core protected-member manifest and routing indexes, low-freedom direct Git guidance, schema-validated Topic Git support files under `topic.runtime` and inside pre-runtime Topic Publication Copies, Project-root ignore inspection and bounded managed-block updates, non-Git privacy and projection helpers, temporary publication copies, Git submodule and remote synchronization behavior, documentation, and validation fixtures. It may add a read-only Isomer query only if existing query families cannot expose required topology, but it adds no Topic Git mutation CLI, Git-wrapping service, or Git-wrapping helper script. It does not change the default Topic Workspace filesystem layout, Topic Main ownership, Topic Actor or Agent worktree construction, Topic Creator readiness, or environment setup prerequisites.
