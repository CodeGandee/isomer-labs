## 1. Path and Mutable Binding Contracts

- [x] 1.1 Add `topic.paper.template_exchange_root` with default path `intent/derived/writing-template` and test catalog, override, materialization, source, and path-safe-child behavior.
- [x] 1.2 Add mutable named-state as a binding revision mode with one stable current record per exact template-name scope and opaque state-token concurrency.
- [x] 1.3 Change `KAOJU:PAPER-TEMPLATE-MYST` from paper-line-scoped ordinary-file revisioned content to template-name-scoped managed directory-manifest mutable content.
- [x] 1.4 Require path-safe `template_name` metadata and allow bounded agent-authored entrypoint, use-guidance, and extension metadata without defining a universal template schema.
- [x] 1.5 Define lightweight template-mutation audit evidence with stable ref, name, actor, operation, source refs, time, and before-and-after tokens and digests but no prior template bytes.
- [x] 1.6 Revise template export and manifest bindings for stable mutable source refs, state tokens, tree digests, paths, and actor provenance.
- [x] 1.7 Update Kaoju semantic resources, binding validation, format profiles, generated references, and inventory tests for mutable named templates and ordinary named copies.

## 2. Low-Level Named-Template CRUD

- [x] 2.1 Implement exact named-template list and show returning stable ref, current tree digest, state token, status, authored metadata, and default working path without revision or snapshot classification.
- [x] 2.2 Implement create from an integrity-valid prepared directory tree with a new unique path-safe name.
- [x] 2.3 Implement create from an existing named template so the new name receives exact current content and allowed metadata as an ordinary independent template.
- [x] 2.4 Implement update from a prepared directory with expected-state validation and atomic replacement of the stable named record's current managed tree.
- [x] 2.5 Implement exact update from another named template, copying current source content and applicable metadata without merging or changing the source.
- [x] 2.6 Implement low-level file put and remove with safe relative paths, expected-state validation, atomic tree-manifest replacement, and reserved-file rejection.
- [x] 2.7 Implement bounded JSON metadata patch while protecting identity, scope, binding, digest, state token, and audit fields.
- [x] 2.8 Implement archive and reference-safe delete behavior for ordinary names, including dependent paper-state diagnostics.
- [x] 2.9 Ensure ordinary mutations update the same stable record, emit lightweight audit evidence, and create no `revision_of`, `supersedes`, historical content record, or automatic named copy.
- [x] 2.10 Return deterministic JSON with operation, stable ref, name, prior and current state token and digest, affected metadata, audit ref, diagnostics, and next actions.

## 3. Flexible Trees and Export Exchange

- [x] 3.1 Implement managed template-tree manifests for arbitrary safe MyST-oriented files, configurations, includes, assets, and guidance without a required filename.
- [x] 3.2 Define `.isomer-template-export.json` with name, stable canonical ref, state token, canonical and exported tree digests, observed path, and time.
- [x] 3.3 Implement tree-digest calculation that excludes reserved exchange metadata and diagnostics while including safe relative paths and file bytes.
- [x] 3.4 Implement registered-export listing and status with unchanged, edited, missing, identity-invalid, and canonical-changed posture.
- [x] 3.5 Implement safe export to the stable resolved named directory or authorized target, defaulting unnamed export to canonical `main`.
- [x] 3.6 Implement idempotent clean refresh and edited or unrecognized target refusal without creating versioned sibling directories.
- [x] 3.7 Implement export observation for an agent-prepared reconciled working tree without promoting it to canonical state.
- [x] 3.8 Make managed-tree and working-tree mutations staged and atomic and test path traversal, symlink, reserved-file, digest, and partial-write failures.

## 4. CLI Surface and Legacy Retirement

- [x] 4.1 Add `ext kaoju paper template list`, `show`, `create`, `update`, `file put`, `file remove`, `metadata patch`, `archive`, and safe delete commands.
- [x] 4.2 Add create-from-template and update-from-template options as ordinary copy and exact replacement operations with no snapshot terminology or metadata.
- [x] 4.3 Add `template exports` and `template export` commands backed by the resolved exchange surface and export observation state.
- [x] 4.4 Require expected state tokens for every destructive update, metadata edit, archive, or delete and return stale-state diagnostics without mutation.
- [x] 4.5 Return guidance to use Kaoju agent construction when callers request high-level conversion or merge of an arbitrary user-edited directory.
- [x] 4.6 Retire old flat `export-template` and `apply-template` behavior and direct callers to named CRUD, export, or agentic reconciliation.
- [x] 4.7 Disable mutation in `ext research templates`, preserve generic legacy record reads, and diagnose legacy LaTeX directory conflicts non-destructively.
- [x] 4.8 Update CLI metadata, JSON contracts, examples, diagnostics, and manual reference pages without adding snapshot or automatic revision commands.

## 5. Kaoju Agent Discovery and Construction

- [x] 5.1 Update `manage-paper-template` and `isomer-kaoju-write` to use low-level named CRUD while keeping arbitrary template construction and reconciliation agent-owned.
- [x] 5.2 Use explicit template name, canonical ref, template path, or export path directly when supplied, after validation, without implicit discovery.
- [x] 5.3 For an update with no locator, inspect registered export status and select exactly one eligible edited export before considering the topic-directory fallback.
- [x] 5.4 Treat multiple edited exports, duplicate claims, or inconsistent identity as ambiguity and ask the user with concrete candidates.
- [x] 5.5 If no edited export qualifies, use `<topic-workspace>/intent/derived/writing-template/main/` when it exists, regardless of whether database `main` exists.
- [x] 5.6 If neither source exists, ask the user which template or path to use instead of selecting an unrelated database record.
- [x] 5.7 Make the agent inspect source and target trees, interpret intended changes, identify entrypoints, resolve authorized differences, and prepare a clean candidate before low-level update.
- [x] 5.8 Require user clarification for material structural or content choices not authorized by the request and record an agent assessment and change summary.
- [x] 5.9 When target state is absent, require explicit create; when present, update it with the current state token and report lost-update conflicts.
- [x] 5.10 Update `create-paper-template`, `draft-paper`, and `paper-pass` for mutable named directory templates, canonical `main` paper-use defaults, and observed-digest lineage.

## 6. Explicit Named Copies, Replacement, and Agentic Merge

- [x] 6.1 Teach skills that ordinary updates preserve no prior template content and never create another name automatically.
- [x] 6.2 Map requests to save or preserve a template state to create-from-template with an agent- or user-chosen ordinary name.
- [x] 6.3 Ensure the chosen saved-state name has no snapshot flag, type, lifecycle, special list, or restricted behavior.
- [x] 6.4 Map restore or exact replace requests to update-from-template and leave the source named template unchanged.
- [x] 6.5 Map merge requests to agent inspection and candidate construction followed by update-from-directory, never to generic CLI merge.
- [x] 6.6 Require authorization before the agent creates an additional named copy on its own and report the name before mutating the target.
- [x] 6.7 Update shared process contracts, artifact guidance, README material, and skill validation to use flat-name copy terminology and remove revision and snapshot concepts.

## 7. Migration

- [x] 7.1 Add migration inspection for old paper-line scopes, active candidates, content digests, entrypoint ambiguity, historical revisions, and versioned export paths without mutation.
- [x] 7.2 Migrate one unambiguous active template into stable mutable name `main` and require explicit names for distinct active templates.
- [x] 7.3 Preserve pre-migration historical records as legacy reads without importing each revision as a new named template.
- [x] 7.4 Wrap selected single-file templates into flexible directory manifests without semantic rewriting and require agent review for ambiguous tree or entrypoint choices.
- [x] 7.5 Preserve historical export directories and legacy LaTeX trees non-destructively while stopping their use as new defaults.

## 8. Verification and Documentation

- [x] 8.1 Add unit tests for flat exact-name lookup, stable record identity, arbitrary directory content, mutable update, state-token concurrency, and absence of automatic revisions.
- [x] 8.2 Add tests for explicit create-from-template, independent later mutation, exact update-from-template, source preservation, and absence of snapshot metadata or special listing.
- [x] 8.3 Add tests for file CRUD, metadata patch allowlists, reserved fields, audit evidence, reference-safe archive or delete, and stale-state rejection.
- [x] 8.4 Add tests for export metadata, digest exclusions, edited detection, clean refresh, edited-target refusal, and agent-prepared export observation.
- [x] 8.5 Add skill and integration tests for the exact unnamed-update order: one edited export, several edited exports, topic `main/` fallback, and no discoverable source.
- [x] 8.6 Prove the second fallback checks the current Topic Workspace directory rather than database `main` existence.
- [x] 8.7 Add tests with varied template trees proving CLI integrity behavior and agent ownership of arbitrary conversion and merge.
- [x] 8.8 Add migration tests for one current template, multiple named candidates, ignored historical revisions, flexible-tree wrapping, legacy collisions, and preserved old exports.
- [x] 8.9 Update user documentation for mutable named templates, explicit named copies, exact replacement, destructive-update trade-offs, stable exports, ordered discovery, and agentic merge.
- [x] 8.10 Update the changelog with breaking path, scope, mutable-state, no-automatic-history, flat-name, CLI, and migration changes.
- [x] 8.11 Run targeted template, Kaoju, binding, path-resolution, skill-validation, and documentation tests.
- [x] 8.12 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`, then strictly validate the OpenSpec change and record unrelated pre-existing failures.
