## Why

Topic Workspace tooling already needs predictable local disposable surfaces, but the path contract is moving from fixed directory names to Topic Workspace Manifest-backed semantic labels. The downstream `tmp/` change must therefore define disposable surfaces as labels such as `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` instead of making callers rely on specific directory shapes.

This change depends on `add-topic-workspace-manifest-path-resolution`. It should be implemented only after semantic path resolution, Effective Agent Context, and default-layout materialization are available.

## What Changes

- Define `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` as standard local disposable semantic surfaces. Under `isomer-default.v1`, their bindings use `tmp/` directories at the Topic Workspace root, resolved Topic Main Repository root, and resolved Agent Workspace root. In every binding, tmp material is local, ignored, disposable, not shared, and not durable evidence.
- Require each resolved tmp surface to be ignored by the nearest relevant Git ignore policy and excluded from Git sharing, Peer Read Access, Workspace Runtime records, Provenance Records, handoffs, and downstream research evidence.
- Distinguish `tmp/` from `isomer-managed/agent-owned/scratch/`: `scratch/` may hold agent-local drafts that need later promotion, while `tmp/` is sweepable throwaway material that must not be referenced as durable state.
- Update path resolution, runtime initialization, validation diagnostics, topic workspace manager guidance, service environment setup guidance, and documentation to prepare or validate the standard tmp labels.
- Keep `isomer-managed/agent-owned/public/`, `isomer-managed/topic-owned/`, Git-tracked material, and owner-preserved records as the only supported ways to share or preserve material.

## Capabilities

### New Capabilities

- `local-tmp-workspace-surfaces`: Defines standard local tmp labels, ignore requirements, non-sharing semantics, and promotion boundaries for disposable workspace material.

### Modified Capabilities

- `workspace-path-resolution`: Resolve and report `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` through the manifest/default-profile path model without treating them as durable runtime truth.
- `workspace-runtime-persistence`: Prepare or validate resolved tmp directories and ignore policies without storing dependencies on tmp material as durable runtime records.
- `topic-workspace-manager-skill`: Prepare and validate `topic.main_repo.tmp`, `agent.tmp`, and related `.gitignore` rules for resolved Topic Main Repository and Agent Workspace roots.
- `topic-team-specialization-module-skill`: Require delegated Agent Workspace setup evidence to include the tmp-label ignore contract when Git-backed worktrees are prepared.
- `isomer-service-env-setup-skill`: Keep `topic.tmp` in the baseline environment setup ignore posture and align wording with the non-sharing contract.
- `isomer-documentation-system-guide`: Document the standard tmp labels, their default bindings, and the rule that tmp material is local, ignored, disposable, and not shared.

## Impact

This affects `docs/topic-workspace-definition.md`, selected system docs, the canonical domain-language notes, `src/isomer_labs/topic_workspace_manifest.py`, `src/isomer_labs/paths.py`, runtime setup and validation code, unit tests for tmp labels and validation diagnostics, `skillset/operator/isomer-admin-topic-workspace-mgr`, `skillset/operator/isomer-admin-topic-team-specialize`, and `skillset/service/isomer-srv-topic-env-setup`. It does not add external dependencies, create a new sharing channel, or require fixed default directory names when a Topic Workspace Manifest safely binds the labels elsewhere.
