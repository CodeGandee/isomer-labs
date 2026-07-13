## 1. Add the Kaoju Paper-Writing Capability

- [ ] 1.1 Create the packaged `isomer-kaoju-write` skill with release-aligned OpenAI metadata, a publication-boundary workflow, and explicit dependencies on accepted Kaoju audit and synthesis records.
- [ ] 1.2 Add writer references for the Paper Contract, citation and claim lineage, `.tex` manuscript structure, LaTeX title metadata, compiler-owned section numbering, template-native unnumbered and appendix sections, and revision rules.
- [ ] 1.3 Add writer references for reproducible Tectonic-first `document_build` execution, recorded LaTeX-toolchain fallback, rejection of Markdown-to-PDF commands, text extraction, page-image inspection, and the `ready`, `ready-with-warnings`, and `not-ready` validation states.
- [ ] 1.4 Add `isomer-kaoju-write/artifact-bindings.md` with the five publication semantic IDs, neutral profile refs, record kinds, owners, consumers, lineage, revision behavior, file refs, and deterministic record commands.
- [ ] 1.5 Add survey-writing references adapted from DeepSci's evidence-first practice: reader-facing and evidence views, survey-specific section jobs, citation-first drafting, comparison and display planning, calibrated gap language, skeptical review, and novelty-optional contribution framing.
- [ ] 1.6 Define the survey-quality profile with explicit metric populations, exclusions, cutoffs, source refs, thresholds, per-dimension verdicts, and rules that prevent source counts, discovery saturation, or composite scores from overriding mandatory failures.

## 2. Add the Pipeline Procedure and Routing

- [ ] 2.1 Add `paper-pass` to `isomer-kaoju-pipeline` as an orchestration procedure that checks readiness, resolves accepted survey inputs, delegates manuscript and publication work to `isomer-kaoju-write`, applies the Gate, and returns the accepted Publication Bundle or a precise blocker.
- [ ] 2.2 Add `create-paper-template` to `isomer-kaoju-pipeline` as a bounded procedure that generates an editable LaTeX template tree at `intent/derived/writing-template/<template-name>/` (default `main`), supports multiple named templates, compiles a proof-of-compilation PDF preview, records the template artifact, and returns the accepted template ref.
- [ ] 2.3 Update the Kaoju pipeline command list, family README, and operator extension-skill index so paper requests route to the dedicated writer, named end-to-end paper procedures route through `paper-pass`, and template generation routes through `create-paper-template`.
- [ ] 2.4 Update the Kaoju shared semantic registry and workspace binding-index guidance so the five publication semantic IDs participate in readiness and binding coverage without making generated files canonical state, and so the template artifact ref is a recognized paper-contract input.

## 3. Register Publication Record Formats

- [ ] 3.1 Extend the Kaoju record-format profile catalog with family-neutral profiles for `paper-contract`, `survey-manuscript`, `paper-build-run`, `paper-validation-report`, and `publication-bundle`, including required payload, relationship, file, facet, renderer, and lifecycle fields.
- [ ] 3.2 Define current-state revision behavior for the Paper Contract, Survey Manuscript, and Publication Bundle, and immutable descendant behavior for build runs and validation reports.
- [ ] 3.3 Extend artifact-format unit tests and the Kaoju record lifecycle integration test to cover creation, query, revision, lineage, file references, and preservation of publication records.
- [ ] 3.4 Add profile fields and validation fixtures for survey questions, contribution posture, reader-facing and evidence views, `.tex` entry point and included files, LaTeX template and engine posture, quality metric definitions, observed values, missing cases, per-dimension verdicts, and route-back diagnostics.

## 4. Package, Discover, and Validate the Twelfth Skill

- [ ] 4.1 Add `isomer-kaoju-write`, `paper-pass`, and `create-paper-template` to the packaged system-skill manifest, skill metadata, command inventory, callback insertion points, and generated or projected assets.
- [ ] 4.2 Update installer, discovery, CLI `show`, operator routing, and family inventory expectations from eleven to exactly twelve Kaoju skills and from eight to nine public pipeline procedures.
- [ ] 4.3 Extend skill asset and artifact-binding validators to require the writer bundle, paper command, publication semantic coverage, neutral profile refs, callback guidance, and direct-publication-state prohibitions.
- [ ] 4.4 Add focused unit tests for installation, upgrade, removal, manifest validation, callback resolution, inventory discovery, command discovery, and missing or malformed paper-writing assets.

## 5. Enforce Manuscript and PDF Acceptance

- [ ] 5.1 Add fixtures and focused validation tests that accept LaTeX structural commands without numeric prefixes, rely on document-class numbering, and reject manually numbered section or appendix commands.
- [ ] 5.2 Add tests that require LaTeX title metadata to render outside the section hierarchy and require acknowledgments, references, and appendices to follow the template-native unnumbered or appendix policy.
- [ ] 5.3 Add build-run tests for the `.tex` entry point, source and included-file hashes, arguments, environment, Tectonic-first attempt, selected engine, fallback reason, logs, output refs, and failed compilation. Add template-generation tests that verify the proof-of-compilation preview build, template artifact ref, and failure handling for `create-paper-template`.
- [ ] 5.4 Add post-render validation tests for text extraction, heading sequence, duplicate-number detection, citations and references, page count, page-image inspection, clipping, overflow, blank pages, and suspicious density.
- [ ] 5.5 Prove that compilation success alone cannot yield `ready`, that unavailable mandatory inspection produces `not-ready`, and that the Publication Bundle cannot be accepted without a successful build and accepted validation report for the same manuscript revision.
- [ ] 5.6 Add survey-quality tests for scope-cell and protocol accounting, identity and version resolution, verification-depth and locator coverage, comparison comparability and matched depth, citation and display traceability, contradiction and limitation propagation, reporting clarity, and calibrated gap language.
- [ ] 5.7 Add tests showing that novelty is optional, source counts and bounded discovery saturation do not prove completeness, unknown denominators remain visible, and a composite score cannot override a mandatory failed dimension.
- [ ] 5.8 Add tests that reject Pandoc, browser-print, and other Markdown-to-PDF publication builds, accept recorded Tectonic builds, and accept standard LaTeX fallback only after a concrete Tectonic blocker or failure is recorded.

## 6. Documentation and Verification

- [ ] 6.1 Document the dedicated-skill ownership decision, the `paper-pass` and `create-paper-template` orchestration boundaries, the `isomer-cli ext research templates` CLI surface, DeepSci practices adapted for survey reporting, novelty-optional contribution posture, survey-quality profile, `.tex` publication-source requirement, compiler-owned numbering, Tectonic-first build and LaTeX fallback policy, record-versus-file semantics, validation states, and migration from ad hoc Kaoju paper builds.
- [ ] 6.2 Run skill asset generation or synchronization and the focused Kaoju skill, artifact-format, lifecycle, installer, CLI, and research-templates CLI tests; resolve all diagnostics caused by this change.
- [ ] 6.3 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`, and record unrelated pre-existing failures separately.
- [ ] 6.4 Run `openspec validate add-kaoju-paper-writing --strict` and verify every requirement scenario has corresponding implementation or test evidence.

## 7. Add `isomer-cli ext research templates` CLI Surface

- [ ] 7.1 Add `isomer-cli ext research templates` as a Click command group under `isomer-cli ext research`, alongside `records` and `ideas`.
- [ ] 7.2 Implement `create` with default `main`, `--name`, `--venue`, `--paper-type`, and `--from-record` options; generate files under `intent/derived/writing-template/<name>/`, compile a preview PDF, and create or update a `kaoju:writing-template` research record.
- [ ] 7.3 Implement `list` to query template records by semantic-id `kaoju:writing-template`, mark `main` as default, and support `--venue` and `--paper-type` filters.
- [ ] 7.4 Implement `show` to return template metadata, file tree, preview PDF ref, and README content for a named or default template.
- [ ] 7.5 Implement `refresh` to regenerate files, compile a new preview, and create a descendant record with lineage to the prior template record; support `--preserve-edits`.
- [ ] 7.6 Implement `compile` to re-run the preview build without regenerating LaTeX source and update the template record's preview status.
- [ ] 7.7 Implement `remove` to archive the template record, with `--delete-files` to also remove the template directory.
- [ ] 7.8 Add unit and integration tests for each CLI command, default `main` resolution, named templates, failed preview handling, record lineage, and `paper-pass` integration.
