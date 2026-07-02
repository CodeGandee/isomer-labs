# Project Extern Repos

Use this subcommand to expose each canonical external repository as an external repo projection inside the Topic Main Development Repository only through Isomer-managed projection roots.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Workspace context | Require `topic.repos.main`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, path sources, and blockers from `resolve-status`. |
| Topic Main Development Repository evidence | Require `ensure-topic-main-repository` output showing a usable topic-main repository and Isomer-managed namespace. |
| Canonical external repo evidence | Require `ensure-topic-repos` output for each non-main `topic.repos.*` repository named by the target spec. |
| Topic env target spec | Require projection access intent from `topic.env.topic_setup_target_spec` or an explicit validated target spec. |
| Mutation confirmation | Require direct Project Operator Session mutation confirmation or equivalent service authorization before creating projection paths or writing the manifest. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**:
   - Require topic-main evidence, canonical external repo evidence, target spec projection requirements, and mutation confirmation.
2. **Classify projection access intent**:
   - For each external repository, classify the projection as read-only, writable, or not projected.
   - Treat missing projection intent as read-only only when the target spec clearly says agents need to inspect the repo from topic-main.
3. **Prepare read-only projections**:
   - Place read-only projections under `topic.repos.main.projections.readonly`.
   - Use a symlink, copy, or other target-spec-approved projection mode.
   - When using a symlink, resolve the canonical source repository with `realpath -e` first and create the symlink to that absolute real path. Treat the symlink as host-local regenerated setup material, not as portable metadata.
   - Record that the policy is read-only even when the filesystem cannot enforce read-only access.
4. **Prepare writable projections**:
   - Place writable projections under `topic.repos.main.projections.writable`.
   - Use a copy, dedicated clone, dedicated worktree, or another isolated writable materialization unless the user explicitly authorizes writes to the canonical external repository.
5. **Validate projection targets**:
   - For symlink projections, resolve the canonical `topic.repos.*` source path from `ensure-topic-repos` to an absolute real path with `realpath -e`, then confirm `readlink -f <projection-path>` equals that source real path.
   - Do not create relative symlink targets for these projections. Relative targets are easy to miscalculate from the nested `isomer-managed/topic-owned/{readonly,writable}/extern/` roots and can silently point outside `repos/`.
   - Treat a missing target, broken symlink, path that resolves outside the Topic Workspace, or path that resolves to a different repository than the canonical source as a projection blocker or repair action.
   - For copy, dedicated clone, or worktree projections, confirm the projected path exists and record how it was derived from the canonical source.
6. **Write or validate projection metadata**:
   - Write small tracked metadata to `topic.repos.main.projections.manifest`.
   - For each projection, record intended access, projection mode, canonical source label, canonical source path, projected path, mutation policy, status, blockers, and source evidence.
7. **Report projection readiness**:
   - Include projection paths, changed files, commands run, blockers, and repair next actions.

If the user's task does not map cleanly to these steps, use your native planning tool to inspect the canonical repo evidence and target spec first, then materialize only projections whose access intent is clear.

## Guardrails

- Do not create `extern/` at the topic-main repository root.
- Do not treat projections as canonical source repositories; the canonical source remains the resolved non-main `topic.repos.*` path.
- Do not report a symlink projection as ready until `readlink -f <projection-path>` equals `realpath -e <canonical-source-path>`.
- Do not store absolute symlink targets as durable metadata. Projection metadata should keep semantic labels and project- or topic-relative paths; absolute symlink targets are local materialization details that may need repair after relocation.
- Do not mutate an existing canonical external repository unless the target spec explicitly authorizes source mutation.
- Do not hide projection blockers behind generic readiness language.
- Do not create Agent Workspace-local substitute projections; missing or stale projection evidence must be repaired through topic env setup.
