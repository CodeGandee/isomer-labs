# Kaoju Artifact Semantics

This storage-neutral page is a bundle-local projection for quick reading. Run `isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT` for authoritative meaning, minimum content, ownership, record kind, profile, semantic label, content mode, relationships, revision, scope, latest selection, validation, acceptance, and migration. Preserve the exact uppercase identifier returned by the query.

## Workspace and Control

- `KAOJU:WORKSPACE-READINESS`: resolved Topic Workspace readiness, limits, blockers, and next allowed stage.
- `KAOJU:BINDING-INDEX`: validation result for the selected semantic contracts and supporting profiles.
- `KAOJU:SURVEY-CONTRACT`: accepted question, boundary, source classes, cutoff, depth, resources, Gates, and stop conditions.
- `KAOJU:DIRECTION-SET`: actor-reviewed direction proposals, choices, custom entries, feasibility notes, and history.
- `KAOJU:COMPARISON-INTENT`: actor-reviewed plan for a source-grounded or empirical comparison.
- `KAOJU:PROCEED-DECISION`: explicit clarify, proceed, pause, reject, or stop decision.
- `KAOJU:SURVEY-TERMINAL-REPORT`: complete, paused, or blocked outcome with accepted refs, limitations, and resume point.

## Discovery and Acquisition

- `KAOJU:DISCOVERY-LEDGER`: bounded searches, routes, dates, identities, version families, dispositions, gaps, and frontier.
- `KAOJU:READING-LIST`: one direction-scoped priority and secondary target set with target derivation, achieved counts, coverage, and shortage notes; absent target metadata retains the legacy three-plus-three default.
- `KAOJU:RELATED-WORK-CATALOG`: current identity-resolved catalog of relevant primary works and supporting materials.
- `KAOJU:RELATED-WORK-DELTA`: auditable additions, changes, exclusions, and evidence against a catalog revision.
- `KAOJU:CURATED-INTAKE-DELTA`: dispositions and survey effects of actor-nominated materials.
- `KAOJU:ARTIFACT-LIBRARY`: current state of acquired papers, reports, repositories, datasets, models, and related materials.
- `KAOJU:ASSOCIATED-SOURCE-CODE`: verified relationship between a work identity and an immutable repository identity.
- `KAOJU:MATERIAL-ACQUISITION-MANIFEST`: observed identities, availability, checksums or commits, access posture, and provenance.
- `KAOJU:TOPIC-DATASET-MANIFEST`: actor-authorized inventory of external and managed datasets available to the topic.
- `KAOJU:SOURCE-ACCESS-BLOCKER`: evidence, claim impact, and recovery route for one failed bounded acquisition.

## Examination, Comparison, Audit, and Synthesis

- `KAOJU:SOURCE-DIGEST`: inspected source identity, exact locators, statements, interpretations, contradictions, and depth.
- `KAOJU:CLAIM-EVIDENCE-LEDGER`: current mapping from claim ids to supporting, challenging, provisional, and missing evidence.
- `KAOJU:THEORY-COMPARISON`: exact-evidence comparison of named works without empirical execution.
- `KAOJU:COMPARISON-MATRIX`: audited cross-method view with evidence, variability, adaptations, failures, and non-comparability.
- `KAOJU:COMPARISON-RUN`: immutable first-hand execution evidence for one comparison candidate and attempt.
- `KAOJU:AUDIT-REPORT`: non-mutating readiness assessment, defects, affected claims, repair routes, and decision.
- `KAOJU:CLAIM-STATUS-TABLE`: current conclusion status, depth, evidence, contradictions, and limits.
- `KAOJU:FIELD-SUMMARY`: bounded themes, chronology, taxonomy, representative works, disagreements, gaps, and limits.
- `KAOJU:KAOJU-DOSSIER`: navigable assembly of accepted survey outputs and exact refs.

## Environment and Trials

- `KAOJU:GENERATED-DATASET`: reproducible generated input definition, outputs, checks, purpose, and limitations.
- `KAOJU:ENV-PREP-PLAN`: dependencies, critical path, candidate environments, risks, authorization, and expected smoke outputs.
- `KAOJU:ENV-GATE-REVISION`: before-and-after environment Gate state and authorized change.
- `KAOJU:PIXI-ENV-REF`: exact resolved packages, lock identity, declared flexible intent, and readiness.
- `KAOJU:SMOKE-RUN-SCRIPT`: durable task-critical smoke program.
- `KAOJU:SMOKE-RUN-RESULT`: immutable smoke observation, environment, command request, outputs, and verdict.
- `KAOJU:METHOD-TRIAL-PLAN`: bounded source, environment, data, wrapper, evaluator, metrics, resources, fidelity, and retry policy.
- `KAOJU:METHOD-TRIAL-WRAPPER`: durable minimal wrapper for a compatible upstream command or the smallest recorded adaptation.
- `KAOJU:METHOD-TRIAL`: readable compatibility result for a historical reproduction-owned trial.
- `KAOJU:METHOD-TRIAL-RUN`: immutable execution attempt with exact source, environment, data, command, timing, logs, and status.
- `KAOJU:METHOD-TRIAL-RESULT`: immutable interpreted verdict, checks, depth, fidelity, adaptations, and limitations.

## MyST-First Paper

- `KAOJU:PAPER-CONTRACT`: accepted audience, questions, evidence boundary, structure profile, quality policy, and build policy.
- `KAOJU:PAPER-STRUCTURE-MYST`: canonical typed section jobs and display plan in MyST.
- `KAOJU:PAPER-TEMPLATE-MYST`: one stable mutable named canonical MyST-oriented template tree.
- `KAOJU:PAPER-TEMPLATE-MUTATION-AUDIT`: lightweight named-template mutation evidence without prior template bytes.
- `KAOJU:PAPER-DRAFT-MYST`: canonical grounded paper draft in MyST.
- `KAOJU:PAPER-DRAFT-MD`: deterministic non-canonical Markdown derivation.
- `KAOJU:PAPER-DISPLAY`: file-backed figure or table content referenced from MyST by a typed stable ref.
- `KAOJU:CITATION-MAP`: citation roles, source refs, locators, claim links, display links, and evidence status.
- `KAOJU:PAPER-TEMPLATE-EXPORT`: registered non-canonical working-directory observation for a stable named template.
- `KAOJU:PAPER-TEMPLATE-MANIFEST`: named-template export identity, state token, tree digests, path, time, and actor provenance.
- `KAOJU:PAPER-REVISION-LOG`: append-only canonical paper changes, evidence effects, and actor decisions.
- `KAOJU:PAPER-TEMPLATE-TEX`: derived TeX template tree and compatibility fingerprint.
- `KAOJU:PAPER-DRAFT-TEX`: derived TeX draft tree, citations, included files, and conversion diagnostics.
- `KAOJU:PAPER-PDF`: immutable built PDF output.
- `KAOJU:PAPER-COMPILE-LOG`: immutable compiler command, diagnostics, output, and fallback rationale.
- `KAOJU:PAPER-PDF-REVISION-LOG`: append-only authorized build repairs and material-change Gates.
- `KAOJU:PAPER-BUILD-RUN`: immutable document build attempt and terminal state.
- `KAOJU:PAPER-VALIDATION-REPORT`: syntax, structure, citation, textual, visual, evidence, and publication assessment.
- `KAOJU:PUBLICATION-BUNDLE`: accepted canonical and derived paper refs with audit and provenance.
- `KAOJU:SURVEY-MANUSCRIPT`: readable compatibility record for historical LaTeX-first manuscripts.
- `KAOJU:WRITING-TEMPLATE`: readable compatibility record for historical LaTeX-first templates.

## Wiki Export and Viewer

- `KAOJU:LLM-WIKI-EXPORT`: checksummed managed Markdown and JSON survey export.
- `KAOJU:LLM-WIKI-METADATA`: canonical topic, artifact, revision, checksum, page, relationship, and provenance mapping.
- `KAOJU:LLM-WIKI-VIEWER`: independently implemented packaged static viewer deployment.
- `KAOJU:LLM-WIKI-VIEWER-MANIFEST`: viewer version, file checksums, wiki target, launch metadata, and exposure posture.
