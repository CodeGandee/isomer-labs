## 1. Effective Catalog and Manifest Bindings

- [x] 1.1 Add Isomer-defined storage profile definitions that expand `storage_profile` ids into required context, kind, lifecycle, visibility, safety policy, and Git semantics where applicable.
- [x] 1.2 Extend the semantic surface model to distinguish Isomer-owned reserved labels, grouped reserved label families, manifest-declared `custom.*` surfaces, and storage-profile-derived traits while preserving existing compatibility ids where still accepted.
- [x] 1.3 Rename the canonical Topic Main Repository label to `topic.repos.main` and update dependent child labels such as `topic.repos.main.tmp`, `topic.repos.main.isomer_managed`, and `topic.repos.main.tracked.*`.
- [x] 1.4 Add parent-derived default metadata for `topic.repos.main` child labels and Agent Workspace child labels so child defaults can resolve from parent semantic results.
- [x] 1.5 Add effective catalog loading that combines the built-in catalog with valid grouped reserved labels and Topic Workspace Manifest `label`/`path`/`storage_profile` bindings for the selected context.
- [x] 1.6 Extend Topic Workspace Manifest parsing to accept active bindings with `label`, `path`, and `storage_profile` only as the semantic authoring fields.
- [x] 1.7 Validate reserved namespace roots, grouped label segment syntax, custom label namespaces, accepted `storage_profile` ids, storage profile compatibility with label family, duplicate bindings, safe project-local paths, Project Config Directory exclusion, cross-topic exclusion, and Agent Workspace template placeholders.
- [x] 1.8 Update default materialization so it preserves existing custom bindings and only adds or updates selected default-layout bindings it owns.
- [x] 1.9 Add CLI-backed binding lifecycle support in the manifest layer for register, update, unregister, and reset operations on `label`/`path`/`storage_profile` bindings after validation.
- [x] 1.10 Enforce lifecycle rules that protect built-in label definitions, remove dynamic `custom.*` and grouped-label slots when unregistered, reset built-in overrides without deleting definitions, and leave filesystem targets and historical Path Plans untouched.
- [x] 1.11 Add unit tests for valid grouped repository labels, valid topic storage profile custom labels, valid agent storage profile custom labels, missing `storage_profile`, storage profile mismatch, reserved namespace rejection, unsafe custom paths, CLI registration, update validation, duplicate registration rejection, unregister/reset behavior, and materialization preservation.

## 2. Workspace Path Resolution and CLI

- [x] 2.1 Update semantic path resolution to use the effective catalog for `paths get`, `paths list`, `paths preview`, runtime initialization, and Agent Workspace planning.
- [x] 2.2 Implement required-context resolution so `project.*` requires Project context, `topic.*` requires Effective Topic Context, `agent.*` requires Effective Topic Context plus Effective Agent Context, and `custom.*` follows its declared `storage_profile`.
- [x] 2.3 Require an explicit topic selector for `topic.*`, `agent.*`, and topic-required `custom.*` labels when cwd does not unambiguously identify a Topic Workspace.
- [x] 2.4 Implement parent-derived default resolution for Topic Main Repository descendants and Agent Workspace descendants, including custom `topic.repos.main` and `agent.workspace` parent bindings.
- [x] 2.5 Add default path query mode that returns a reserved label's default-layout path without Path Plan, environment, or manifest override precedence.
- [x] 2.6 Add default path materialization for reserved labels with default path definitions, including storage-profile-aware directory, file-parent, or repository path creation behavior.
- [x] 2.7 Add effective path materialization for existing labels that creates the currently configured target according to `storage_profile` while ignoring stored Path Plans and preserving previous targets.
- [x] 2.8 Add generated semantic environment variable support such as `ISOMER_PATH__TOPIC__REPOS__MAIN` and `ISOMER_PATH__CUSTOM__DATASETS__RAW`.
- [x] 2.9 Require generated environment variables for `custom.*` labels to apply only after the label exists in the effective catalog.
- [x] 2.10 Preserve existing compatibility environment variables and report a diagnostic when a generated semantic env var conflicts with a compatibility env var for the same label.
- [x] 2.11 Add configured resolution mode that ignores stored Path Plans for callers that need current manifest or environment configuration.
- [x] 2.12 Add path explanation output that reports candidate sources, selected source, source detail, and why the selected source won.
- [x] 2.13 Update CLI commands to expose side-effect-free list/get/preview reads, default path lookup, default materialization, configured-target materialization, configured path lookup, and explanation.
- [x] 2.14 Add CLI tests for grouped repository lookup, custom label lookup, custom label listing, required-topic selection, parent-derived defaults, default path lookup, default materialization, configured-target materialization, path registration with creation, path update, unregister/reset, universal env overrides, env conflicts, configured resolution, and explanation output.

## 3. Runtime Path Evidence and Recording

- [x] 3.1 Extend Path Plan records and row conversion to preserve `storage_profile` id and storage-profile-derived trait snapshots for semantic labels when available.
- [x] 3.2 Update runtime initialization and Agent Team Instance creation to record Path Plans from effective semantic results, including custom labels used by dependent runtime records.
- [x] 3.3 Update runtime validation to compare stored Path Plans against configured semantic resolution without rewriting historical rows.
- [x] 3.4 Add drift diagnostics for custom labels that changed, disappeared from the manifest, or now fail configured resolution.
- [x] 3.5 Add a semantic file-locator helper that can express semantic label, scope ref, Path Plan id when available, relative path beneath the resolved surface, and resolved absolute path for display.
- [x] 3.6 Apply semantic file-locator evidence to new project-local Artifact-like lifecycle records and adapter payload refs where the runtime already records or can resolve a Path Plan.
- [x] 3.7 Preserve historical absolute-path records and report missing semantic evidence as compatibility diagnostics rather than deleting or rewriting those records.
- [x] 3.8 Add runtime tests for Path Plan metadata, custom-label drift, missing custom binding diagnostics, semantic locator generation, and historical compatibility.

## 4. Docs, Skills, and Validation Rules

- [x] 4.1 Update Topic Workspace, runtime/file, CLI, system-design, concepts, and roadmap docs to describe Workspace Path Resolution as the storage-layer contract.
- [x] 4.2 Document reserved roots, `topic.repos.main`, grouped repository labels, storage profiles, and CLI-backed `label`/`path`/`storage_profile` binding lifecycle commands with safe-path constraints.
- [x] 4.3 Document parent-derived defaults, read-only path queries, default path lookup, default materialization, configured-target materialization, universal semantic env vars, compatibility env vars, configured resolution, explanation output, unregister/reset data preservation, and Path Plan drift behavior.
- [x] 4.4 Update operator and service skill references so they query semantic labels and reject default-path-only guidance for repository, worktree, setup, tmp, and support surfaces.
- [x] 4.5 Update documentation and skillset validation scripts to detect default directory guidance without semantic labels, missing `storage_profile` fields, and stale path assembly instructions.
- [x] 4.6 Add or update tests for docs validation and skillset validation covering the storage contract language.

## 5. Verification

- [x] 5.1 Run `openspec validate define-storage-layer-contract --strict` and fix proposal or spec issues.
- [x] 5.2 Run `pixi run docs-validate` and fix documentation validation issues.
- [x] 5.3 Run `pixi run lint` and fix style issues.
- [x] 5.4 Run `pixi run typecheck` and fix type errors.
- [x] 5.5 Run `pixi run test` and fix regressions.
- [x] 5.6 Confirm `openspec status --change define-storage-layer-contract --json` reports the change apply-ready.
