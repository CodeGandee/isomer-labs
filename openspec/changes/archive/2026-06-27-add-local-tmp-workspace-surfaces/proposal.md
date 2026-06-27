## Why

The current implementation has already landed the manifest-backed semantic path model, Topic Main Repository terminology, `isomer-managed/` sharing layout, topic-env `.gitignore` handling for literal `tmp/`, documentation validation that rejects fixed-path-only tmp wording, and canonical domain language for **Local Tmp Surface**. What remains is to promote the planned tmp labels from documentation posture into first-class semantic workspace surfaces that code, CLI output, runtime validation, and operator/service skills can resolve consistently.

This change no longer depends on an active `add-topic-workspace-manifest-path-resolution` change. That work has been archived into main specs and code. The revised scope is the remaining implementation slice for `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp`.

## What Changes

- Add `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` to the Topic Workspace Manifest semantic surface catalog and the built-in `isomer-default.v1` layout profile. Under the default profile, they bind to `<topic-workspace>/tmp/`, `<resolved topic.main_repo>/tmp/`, and `<resolved agent.workspace>/tmp/`.
- Expose those labels through Workspace Path Resolution and path CLI/API output while classifying them as local, ignored, disposable, non-shared, and not durable evidence.
- Ensure explicit setup/materialization flows prepare or validate the relevant tmp directory and nearest Git ignore policy: Topic Workspace root `.gitignore` for `topic.tmp`, and Topic Main Repository root `.gitignore` for `topic.main_repo.tmp` plus Git-worktree `agent.tmp`.
- Keep `tmp/` out of durable runtime dependency semantics. Runtime records, handoffs, Evidence Items, Decision Records, Provenance Records, profile material, readiness evidence, and Peer Read Access must not depend on tmp material unless selected content has first been promoted to an approved durable path.
- Update docs and skill guidance from "planned/downstream labels" wording to implemented first-class label wording, while preserving the distinction from `agent.scratch`.
- Extend validation and tests so stale shared/durable tmp wording, missing or ineffective tmp ignore policy, tracked tmp contents, and durable references to tmp material are reported without deleting or promoting user files.

## Current Implementation Baseline

Already present before this change is applied:

- Canonical domain language defines **Local Tmp Surface** and names `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp`.
- Documentation currently frames tmp labels as planned/downstream semantic labels, not as fixed mandatory directories.
- Documentation validation rejects bare `tmp/` wording unless it also states semantic-label, local, disposable, and not-durable semantics.
- `isomer-srv-topic-env-setup` currently adds literal `tmp/` to the Topic Workspace `.gitignore` during dependency installation and warns that this is downstream `topic.tmp` posture.
- `isomer-srv-agent-env-setup` currently treats `topic.main_repo.tmp` and `agent.tmp` as optional local ignored disposable posture when those labels are available.

## Capabilities

### New Capabilities

- `local-tmp-workspace-surfaces`: Defines standard local tmp labels, ignore requirements, non-sharing semantics, and promotion boundaries for disposable workspace material.

### Modified Capabilities

- `topic-workspace-manifest`: Register tmp labels as semantic surfaces in the manifest/default-profile model with disposable, non-shared classification.
- `workspace-path-resolution`: Resolve and report `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` without treating them as durable runtime truth.
- `workspace-runtime-persistence`: Prepare or validate tmp posture where setup owns the relevant root, and reject durable runtime dependencies on tmp material.
- `topic-workspace-manager-skill`: Prepare and validate `topic.main_repo.tmp`, `agent.tmp`, and related `.gitignore` rules for resolved Topic Main Repository and Agent Workspace roots.
- `topic-team-specialization-module-skill`: Require delegated Agent Workspace setup evidence to include the tmp-label ignore contract when Git-backed worktrees are prepared.
- `isomer-service-env-setup-skill`: Resolve `topic.tmp` when available and keep Topic Workspace setup output from treating tmp material as durable evidence.
- `isomer-documentation-system-guide`: Document the implemented tmp labels, their default bindings, and the rule that tmp material is local, ignored, disposable, and not shared.

## Impact

This affects `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`, `docs/topic-workspace-definition.md`, selected system docs, `src/isomer_labs/topic_workspace_manifest.py`, `src/isomer_labs/paths.py`, runtime setup and validation code, unit tests for tmp labels and validation diagnostics, `skillset/operator/isomer-admin-topic-workspace-mgr`, `skillset/operator/isomer-admin-topic-team-specialize`, and `skillset/service/isomer-srv-topic-env-setup`. It does not add external dependencies, create a new sharing channel, require per-agent Pixi environments, or make fixed default directory names authoritative when a safe Topic Workspace Manifest binding says otherwise.
