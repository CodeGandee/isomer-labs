# Kaoju Artifact Semantics

This storage-neutral page is generated from `../../contracts/bindings.v2.json`. The JSON registry is the only authority for record kind, profile, semantic label, content mode, producer, consumers, relationships, revision, scope, latest selection, validation, acceptance, and migration. Skills use the meanings below and ask the typed Artifact service to resolve their physical contracts.

## Workspace and Control

- `kaoju:workspace-readiness`: resolved Topic Workspace readiness, limits, blockers, and next allowed stage.
- `kaoju:binding-index`: validation result for the selected semantic contracts and supporting profiles.
- `kaoju:survey-contract`: accepted question, boundary, source classes, cutoff, depth, resources, Gates, and stop conditions.
- `kaoju:direction-set`: actor-reviewed direction proposals, choices, custom entries, feasibility notes, and history.
- `kaoju:comparison-intent`: actor-reviewed plan for a source-grounded or empirical comparison.
- `kaoju:proceed-decision`: explicit clarify, proceed, pause, reject, or stop decision.
- `kaoju:survey-terminal-report`: complete, paused, or blocked outcome with accepted refs, limitations, and resume point.

## Discovery and Acquisition

- `kaoju:discovery-ledger`: bounded searches, routes, dates, identities, version families, dispositions, gaps, and frontier.
- `kaoju:reading-list`: one direction-scoped priority and secondary target set with coverage and shortage notes.
- `kaoju:related-work-catalog`: current identity-resolved catalog of relevant primary works and supporting materials.
- `kaoju:related-work-delta`: auditable additions, changes, exclusions, and evidence against a catalog revision.
- `kaoju:curated-intake-delta`: dispositions and survey effects of actor-nominated materials.
- `kaoju:artifact-library`: current state of acquired papers, reports, repositories, datasets, models, and related materials.
- `kaoju:associated-source-code`: verified relationship between a work identity and an immutable repository identity.
- `kaoju:material-acquisition-manifest`: observed identities, availability, checksums or commits, access posture, and provenance.
- `kaoju:topic-dataset-manifest`: actor-authorized inventory of external and managed datasets available to the topic.
- `kaoju:source-access-blocker`: evidence, claim impact, and recovery route for one failed bounded acquisition.

## Examination, Comparison, Audit, and Synthesis

- `kaoju:source-digest`: inspected source identity, exact locators, statements, interpretations, contradictions, and depth.
- `kaoju:claim-evidence-ledger`: current mapping from claim ids to supporting, challenging, provisional, and missing evidence.
- `kaoju:theory-comparison`: exact-evidence comparison of named works without empirical execution.
- `kaoju:comparison-matrix`: audited cross-method view with evidence, variability, adaptations, failures, and non-comparability.
- `kaoju:comparison-run`: immutable first-hand execution evidence for one comparison candidate and attempt.
- `kaoju:audit-report`: non-mutating readiness assessment, defects, affected claims, repair routes, and decision.
- `kaoju:claim-status-table`: current conclusion status, depth, evidence, contradictions, and limits.
- `kaoju:field-summary`: bounded themes, chronology, taxonomy, representative works, disagreements, gaps, and limits.
- `kaoju:kaoju-dossier`: navigable assembly of accepted survey outputs and exact refs.

## Environment and Trials

- `kaoju:generated-dataset`: reproducible generated input definition, outputs, checks, purpose, and limitations.
- `kaoju:env-prep-plan`: dependencies, critical path, candidate environments, risks, authorization, and expected smoke outputs.
- `kaoju:env-gate-revision`: before-and-after environment Gate state and authorized change.
- `kaoju:pixi-env-ref`: exact resolved packages, lock identity, declared flexible intent, and readiness.
- `kaoju:smoke-run-script`: durable task-critical smoke program.
- `kaoju:smoke-run-result`: immutable smoke observation, environment, command request, outputs, and verdict.
- `kaoju:method-trial-plan`: bounded source, environment, data, wrapper, evaluator, metrics, resources, fidelity, and retry policy.
- `kaoju:method-trial-wrapper`: durable minimal wrapper for a compatible upstream command or the smallest recorded adaptation.
- `kaoju:method-trial`: readable compatibility result for a historical reproduction-owned trial.
- `kaoju:method-trial-run`: immutable execution attempt with exact source, environment, data, command, timing, logs, and status.
- `kaoju:method-trial-result`: immutable interpreted verdict, checks, depth, fidelity, adaptations, and limitations.

## MyST-First Paper

- `kaoju:paper-contract`: accepted audience, questions, evidence boundary, structure profile, quality policy, and build policy.
- `kaoju:paper-structure-myst`: canonical typed section jobs and display plan in MyST.
- `kaoju:paper-template-myst`: canonical actor-editable MyST structure template.
- `kaoju:paper-draft-myst`: canonical grounded paper draft in MyST.
- `kaoju:paper-draft-md`: deterministic non-canonical Markdown derivation.
- `kaoju:paper-display`: file-backed figure or table content referenced from MyST by a typed stable ref.
- `kaoju:citation-map`: citation roles, source refs, locators, claim links, display links, and evidence status.
- `kaoju:paper-template-export`: versioned actor-editable template exchange directory.
- `kaoju:paper-template-manifest`: source revision, base digest, tied draft, paper line, and export policy.
- `kaoju:paper-revision-log`: append-only canonical paper changes, evidence effects, and actor decisions.
- `kaoju:paper-template-tex`: derived TeX template tree and compatibility fingerprint.
- `kaoju:paper-draft-tex`: derived TeX draft tree, citations, included files, and conversion diagnostics.
- `kaoju:paper-pdf`: immutable built PDF output.
- `kaoju:paper-compile-log`: immutable compiler command, diagnostics, output, and fallback rationale.
- `kaoju:paper-pdf-revision-log`: append-only authorized build repairs and material-change Gates.
- `kaoju:paper-build-run`: immutable document build attempt and terminal state.
- `kaoju:paper-validation-report`: syntax, structure, citation, textual, visual, evidence, and publication assessment.
- `kaoju:publication-bundle`: accepted canonical and derived paper refs with audit and provenance.
- `kaoju:survey-manuscript`: readable compatibility record for historical LaTeX-first manuscripts.
- `kaoju:writing-template`: readable compatibility record for historical LaTeX-first templates.

## Wiki Export and Viewer

- `kaoju:llm-wiki-export`: checksummed managed Markdown and JSON survey export.
- `kaoju:llm-wiki-metadata`: canonical topic, artifact, revision, checksum, page, relationship, and provenance mapping.
- `kaoju:llm-wiki-viewer`: independently implemented packaged static viewer deployment.
- `kaoju:llm-wiki-viewer-manifest`: viewer version, file checksums, wiki target, launch metadata, and exposure posture.
