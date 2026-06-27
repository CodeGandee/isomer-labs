## Why

Isomer already describes Topic Workspace paths as semantic surfaces, but the effective storage contract is still partly encoded in `isomer-cli` helpers, default directory names, compatibility surface ids, and workflow prose. This coupling makes custom Topic Workspace layouts hard, prevents user-defined semantic paths, and encourages agents and skills to remember physical paths instead of querying Workspace Path Resolution.

## What Changes

- Define Workspace Path Resolution as the storage-layer contract for Topic Workspace and Agent Workspace file surfaces.
- Treat `isomer-default.v1` paths as default bindings, not as the public contract.
- Allow the Topic Workspace Manifest to declare semantic path bindings with only `label`, `path`, and `storage_profile`; storage profile definitions own required context, kind, lifecycle, visibility, safety policy, and Git semantics.
- Add reserved semantic namespace semantics so Isomer-owned roots such as `topic.*`, `agent.*`, and future `project.*` cannot be used for arbitrary user-defined labels, while grouped storage labels such as `topic.repos.main` and `topic.repos.inner_group.some_repo_name` remain valid under Isomer-owned rules.
- Add parent-derived default binding semantics so child surfaces such as `topic.repos.main.tmp` and `topic.repos.main.isomer_managed` resolve under the resolved parent `topic.repos.main` instead of hard-coded default path strings.
- Add CLI support to query the default-layout path for a reserved semantic label, materialize a reserved label's default filesystem path, and register a label/path/storage_profile binding with optional path creation.
- Define semantic path binding lifecycle operations so create, update, unregister, reset, and materialize behavior is explicit for built-in labels, accepted grouped label families, and `custom.*` labels.
- Add a deterministic 12-factor environment override convention for semantic labels while preserving existing `ISOMER_*` compatibility variables.
- Clarify when callers should use stored Path Plans versus current configured resolution, including diagnostics for drift.
- Require agents, skills, services, and docs to query `isomer-cli project paths get/list/preview` or the equivalent resolver API rather than constructing known default paths.
- No breaking change: existing compatibility surface ids and existing path environment variables remain supported.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `workspace-path-resolution`: strengthen semantic labels as the public storage API; support reserved namespace validation, manifest-declared `custom.*` labels, parent-derived defaults, default-path queries, default materialization, universal semantic env overrides, and explainable configured-versus-path-plan resolution.
- `topic-workspace-manifest`: extend binding schema and validation for grouped reserved labels, user-defined `custom.*` labels, compact `label`/`path`/`storage_profile` binding declarations, and CLI-backed binding lifecycle operations.
- `workspace-runtime-persistence`: clarify Path Plan snapshot semantics, drift behavior, and semantic path evidence stored before durable runtime records depend on files.
- `research-recording-contracts`: require project-local Artifact and Provenance locators to preserve semantic surface evidence rather than relying only on absolute paths.
- `isomer-documentation-system-guide`: document the storage-layer contract, default layout profile posture, custom binding examples, and the rule that agents query semantic paths.
- `topic-workspace-manager-skill`: require manager workflows to honor custom semantic bindings and report path sources before repository or worktree mutation.
- `isomer-service-env-setup-skill`: require topic environment setup to consume semantic surfaces, including custom user-defined labels when setup material names them.
- `isomer-agent-env-setup-service-skill`: require Agent Workspace setup to resolve every target through semantic labels and avoid default-path assembly.

## Impact

- Affected code: `src/isomer_labs/semantic_surfaces.py`, `src/isomer_labs/topic_workspace_manifest.py`, `src/isomer_labs/paths.py`, `src/isomer_labs/runtime/store.py`, `src/isomer_labs/runtime/validation*.py`, CLI path commands, and related models/tests.
- Affected docs and skills: Topic Workspace, runtime/file, CLI, system-design docs, operator/service skill references, and validation scripts that detect stale default-path guidance.
- Affected behavior: read-only path queries remain side-effect-free; default-path queries ignore manifest/env/path-plan overrides; mutating commands must resolve semantic labels before writing; custom safe project-local bindings are accepted when they name an accepted storage profile; users can create, update, unregister, reset, and materialize bindings through `isomer-cli` instead of editing `topic-workspace.toml` directly; binding removal leaves filesystem targets and historical Path Plans intact; unknown arbitrary labels remain rejected unless the manifest declares them under the accepted custom-label rules.
