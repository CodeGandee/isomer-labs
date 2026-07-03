## Why

Manual Topic Actor research works, but generated payloads, drafts, figures, paper builds, and scratch outputs can scatter across the actor workspace root. Isomer needs a queryable worker output policy so agents and Topic Actors write plain outputs into conflict-safe locations and know whether the user prefers post-operation commits.

## What Changes

- Add a configurable worker output root for Topic Actors and Agent Workspaces, expressed as a path relative to the worker's private workspace.
- Provide default output roots under `isomer-managed/worker-output/...` when no user override is configured.
- Namespace default output paths by worker kind and worker name so branches from multiple agents or actors can merge without colliding on common output filenames.
- Keep Git tracking controlled by generated or user-edited `.gitignore` files; do not model tracked versus untracked output status as a separate Isomer policy.
- Add a per-worker `commit_after_operation` preference that agents can query and apply as a post-action step after research operations.
- Teach research-paradigm skills to use `isomer-cli` to resolve output locations and post-operation commit preference before writing plain output files.

## Capabilities

### New Capabilities
- `worker-output-root-policy`: Defines configurable worker output roots, default conflict-safe path templates, queryable post-operation commit preference, and skill guidance for plain output placement.

### Modified Capabilities
- `topic-workspace-manifest`: Adds manifest fields or bindings for Topic Actor output root and post-operation commit preference.
- `workspace-path-resolution`: Adds path-resolution support for worker output roots for Topic Actors and Agent Workspaces.
- `research-paradigm-skills`: Requires v2 research skills that write plain files to resolve output policy and apply `commit_after_operation` as a post-action step.

## Impact

- Affects semantic workspace surface definitions and path resolution for actor-scoped and agent-scoped output roots.
- Affects Topic Workspace Manifest parsing, validation, and topic actor inspection output.
- May add CLI output-policy query surfaces or extend existing path query output to expose output root and `commit_after_operation`.
- Affects Topic Actor materialization and Agent Workspace setup so default output roots and local `.gitignore` policy are materialized.
- Affects research-paradigm v2 skill instructions and validation so agents do not write plain outputs directly into actor or agent workspace roots.
