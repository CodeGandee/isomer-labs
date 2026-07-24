## 1. Packaged Template Defaults

- [x] 1.1 Add protected Kaoju write resources for neutral `content/main` and `latex/main` trees with versioned authored metadata, safe entrypoints, use guidance, and a checked LaTeX composition contract.
- [x] 1.2 Implement a packaged-template loader that resolves only the declared role-local defaults and returns immutable identity, version, tree digest, root, and authored metadata.
- [x] 1.3 Extend Kaoju package and contract validation to reject missing inventory, unsafe members, reserved files, invalid content metadata, and invalid LaTeX entrypoint, composition, or build metadata.
- [x] 1.4 Add unit tests proving packaged resource inventory, deterministic digests, role separation, installed-package availability, and failure diagnostics without repository fallbacks.

## 2. Default Selection and Fallback

- [x] 2.1 Add a shared typed template-selection result that distinguishes explicit topic stock, omitted role-local topic `main`, packaged fallback, invalid topic state, and explicit-selection failure.
- [x] 2.2 Implement ordered content and LaTeX default resolution so ready topic stock wins, verified absence selects the packaged default, and invalid or ambiguous existing state blocks fallback.
- [x] 2.3 Update draft creation and TeX initialization to snapshot packaged trees directly into paper-local Artifacts and record selection source, packaged identity, version, digest, role, and name without creating topic stock.
- [x] 2.4 Extend export metadata and observation handling for packaged-default exports without a topic state token, and require named-template create when promoting such an edited export.
- [x] 2.5 Keep explicit missing names and refs strict across draft, export, and TeX composition commands, with selected-context diagnostics and no default substitution.
- [x] 2.6 Add unit and integration tests for topic-stock precedence, packaged content and LaTeX fallback, invalid-topic blocking, strict explicit selectors, non-mutating paper consumption, and packaged export promotion.

## 3. Kaoju Topic Initialization

- [x] 3.1 Add an idempotent typed ensure-defaults service operation that creates missing content and LaTeX `main` records from packaged resources through the existing managed-tree, audit, and query-index boundaries.
- [x] 3.2 Add the selected-topic CLI command and structured per-role output for ensure-defaults, including created, preserved, exported, fallback-available, invalid, and conflicting posture.
- [x] 3.3 Make ensure-defaults export absent safe working copies while preserving edited, identity-invalid, canonical-changed, or unrecognized existing targets without overwrite.
- [x] 3.4 Update public Kaoju `create-topic` and `isomer-kaoju-topic-creator` to run generic overview and runtime prerequisites, create missing Mindset Sources, invoke ensure-defaults, and report one resumable initialization result.
- [x] 3.5 Remove stale skill guidance that lets ordinary research actions create missing Mindset Sources or topic template stock implicitly, while preserving `skipped_source_missing` and packaged template fallback.
- [x] 3.6 Add integration tests for fresh initialization, repeated initialization, one-role partial resume, preserved customized stock, protected edited exports, missing runtime, and invalid existing state.

## 4. Plural Exchange Root and Migration

- [x] 4.1 Change the built-in `topic.paper.template_exchange_root` default to `intent/derived/writing-templates` while preserving the semantic label, compatibility id, environment override, and explicit binding precedence.
- [x] 4.2 Add exact legacy singular-root diagnostics for explicit singular bindings and unbound `intent/derived/writing-template` content without arbitrary directory scanning or implicit resolution fallback.
- [x] 4.3 Extend template migration preview with singular and plural inventory, role/name validation, digests, export metadata, registered observations, proposed targets, and conflict reporting.
- [x] 4.4 Implement state-checked migration apply using staging, digest verification, atomic plural publication, applicable new export observations, and post-verification singular cleanup without rewriting canonical named records.
- [x] 4.5 Add path-resolution and migration tests for new defaults, explicit legacy bindings, singular-only preview and apply, stale previews, equivalent content, conflicting dual roots, rollback safety, and historical observation preservation.
- [x] 4.6 Update every active code, process-resource, skill, test, manual-check, and documentation reference from the built-in singular path to the plural role-aware layout, retaining singular text only where it explicitly documents compatibility or migration.

## 5. Derived-Intent Review and Apply Workflow

- [x] 5.1 Update Kaoju `create-topic` output guidance to inventory the actual recognized `intent/derived` materials, explain purpose and supported adjustments, distinguish direct intent from non-canonical exchange and generated output, and stop at the requested initialization boundary.
- [x] 5.2 Add public entrypoint routing for natural-language apply requests that pins one topic, inventories only semantic or registered material, and completes a read-only preflight before any template-record mutation.
- [x] 5.3 Implement per-material apply orchestration that validates changed Mindset Sources, assesses and promotes content and LaTeX exports through typed create or update, and redirects generated derived-file edits to their source owner.
- [x] 5.4 Report the future-effective boundary, per-material statuses, current Source digests, template state tokens and audit refs, unsupported paths, and exact recovery routes without creating a synthetic aggregate Artifact.
- [x] 5.5 Preserve active and completed Run resolutions, Mindset Records, paper drafts, TeX snapshots, PDFs, and other historical Artifacts, and require explicit targets before routing retrospective revision or regeneration.
- [x] 5.6 Add conversational and integration tests for immediate and later apply requests, ambiguous topic context, malformed Mindset Sources, stale and packaged-origin exports, no-change requests, generated-file rejection, mixed outcomes, and historical snapshot preservation.

## 6. Validation and Documentation

- [x] 6.1 Update Kaoju README, welcome command maps, CLI reference, architecture documentation, domain-language notes, and topic-creation output guidance to distinguish topic stock, non-canonical plural-path exports, immutable packaged fallback, and future-only apply behavior.
- [x] 6.2 Add skill-asset validation fixtures for complete initialization guidance, protected template resource ownership, role-aware plural paths, strict explicit selectors, derived-material inventory and apply routing, and the absence of implicit topic or historical mutation.
- [x] 6.3 Run targeted Kaoju template, paper-production, mindset, semantic-path, system-skill, package-installation, migration, and derived-apply unit and integration tests.
- [x] 6.4 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`, then resolve every regression introduced by the change.
