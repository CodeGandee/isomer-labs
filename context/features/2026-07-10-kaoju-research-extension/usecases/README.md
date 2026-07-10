# Use Cases

This directory contains feature-specific use cases for the Kaoju Research Extension.

## Index

| ID | Use Case | Status |
| --- | --- | --- |
| `UC-01` | [Understand a Field Through a Related-Work Landscape](uc-01-understand-a-field-through-a-related-work-landscape.md) | Draft |
| `UC-02` | [Ingest Curated References and Codebases into a Survey](uc-02-ingest-curated-references-and-codebases-into-a-survey.md) | Draft |
| `UC-03` | [Expand a Survey from Interesting Seed Works](uc-03-expand-a-survey-from-interesting-seed-works.md) | Draft |
| `UC-04` | [Compare Named Works in Theory](uc-04-compare-named-works-in-theory.md) | Draft |
| `UC-05` | [Test a Paper Method with Real or Generated Data](uc-05-test-a-paper-method-with-real-or-generated-data.md) | Draft |
| `UC-06` | [Compare Methods with Actual Runs](uc-06-compare-methods-with-actual-runs.md) | Draft |
| `UC-07` | [Register Local Datasets for Later Survey Runs](uc-07-register-local-datasets-for-later-survey-runs.md) | Draft |
| `UC-08` | [Clarify a Survey Request Before Execution](uc-08-clarify-a-survey-request-before-execution.md) | Draft |
| `UC-09` | [Audit and Synthesize Survey Evidence](uc-09-audit-and-synthesize-survey-evidence.md) | Draft |

## Coverage Notes

- `UC-01` covers a literature-first broad field survey from scope and source discovery through bounded acquisition, Related-Work Catalog construction, coverage audit, and Field Summary synthesis.
- `UC-02` covers priority intake of user-nominated references and codebases, one Source Digest or Source Access Blocker plus a terminal disposition per item, and an audited Curated Source Intake Delta.
- `UC-03` covers seed-directed survey expansion through cited predecessors, topic neighbors, forward citations, and time-bounded post-seed discovery, producing a curated Related-Work Catalog Delta.
- `UC-04` covers a source-grounded theory comparison of named works using domain-derived dimensions and a Theory Comparison Artifact linked into the survey.
- `UC-05` covers a paper-method trial with intended or generated data, including faithful and repaired evidence separation, Run-linked numbers, and the boundary between reproduction and capability probes.
- `UC-06` covers the full actual-run comparison goal: Comparison Intent Document, user checkpoint, candidate preparation, controlled Runs, uncertainty, fairness checks, and explicit `not comparable` outcomes.
- `UC-07` covers governed registration of user-provided local datasets through a topic-local manifest and managed symlinks, plus manifest-first reuse during later survey Runs.
- `UC-08` covers clarification-first interaction across survey workflows, including read-only task inspection, structured A/B/C/D questions, user-controlled continuation, and an explicit proceed transition.
- `UC-09` covers independent evidence audit, calibrated survey synthesis, final claim status, limitations, and optional downstream DeepSci handoff.

## Skill Coverage

The use cases follow user goals rather than creating one use case per implementation skill. The interface design still gives every proposed public skill a distinct owner boundary.

| Proposed Skill | Primary Use Cases |
| --- | --- |
| `isomer-kaoju-shared` | All use cases through latest-context, source-identity, evidence-state, lineage, handoff, and worker-output rules. |
| `isomer-kaoju-workspace-mgr` | Material and repository readiness in `UC-01`, `UC-02`, `UC-05`, and `UC-06`, plus dataset registry coordination in `UC-07`. |
| `isomer-kaoju-frame` | Survey scope in `UC-01`; curated intake in `UC-02`; direction expansion in `UC-03`; theory comparison in `UC-04`; method trial in `UC-05`; empirical comparison in `UC-06`; manifest-first dataset selection in `UC-07`; and ambiguity handling in `UC-08`. |
| `isomer-kaoju-discover` | Landscape discovery in `UC-01`, curated-source identity resolution in `UC-02`, multi-route expansion in `UC-03`, supplemental dimension discovery in `UC-04`, paper implementation discovery in `UC-05`, and bounded metric or benchmark context discovery in `UC-06`. |
| `isomer-kaoju-acquire` | Bounded survey corpus acquisition in `UC-01`, curated materials in `UC-02`, expansion candidates in `UC-03`, theory sources in `UC-04`, method materials in `UC-05`, comparison candidates in `UC-06`, and registered-dataset lookup in `UC-07`. |
| `isomer-kaoju-examine` | Work summaries in `UC-01`, Source Digests in `UC-02`, candidate examination in `UC-03`, theory evidence in `UC-04`, paper-to-code and execution-contract examination in `UC-05`, and candidate run-path inspection in `UC-06`. |
| `isomer-kaoju-reproduce` | Intended-data reproduction and capability probes in `UC-05`, candidate readiness work in `UC-06`, and registered-dataset compatibility checks in `UC-07`. |
| `isomer-kaoju-compare` | Source-grounded comparison in `UC-04`, empirical intent and results phases in `UC-06`, and registered-dataset reuse planning in `UC-07`. |
| `isomer-kaoju-audit` | Coverage and claim checks in `UC-01` through `UC-06`, plus full survey evidence audit in `UC-09`. |
| `isomer-kaoju-synthesize` | Field Summary in `UC-01`, survey deltas in `UC-02` and `UC-03`, Theory Comparison Artifact integration in `UC-04`, trial Findings in `UC-05`, empirical comparison integration in `UC-06`, and final dossier synthesis in `UC-09`. |
| `isomer-kaoju-pipeline` | `landscape-pass` in `UC-01`, `curated-intake-pass` in `UC-02`, `direction-expansion-pass` in `UC-03`, `theory-comparison-pass` in `UC-04`, `method-trial-pass` in `UC-05`, `comparative-pass` in `UC-06`, and the shared clarification-first checkpoint in `UC-08`. |

## Boundary Notes

- Kaoju is claim-centric and provenance-first. It investigates what existing sources and implementations establish.
- A top-level Kaoju use case represents a user-visible survey goal. Framing, source acquisition, claim tracing, repository refresh, and lineage-preserving resume remain reusable stage behavior rather than separate use cases.
- DeepSci remains hypothesis-centric. It selects and tests new research routes. Kaoju may hand evidence to DeepSci but does not require the `deepsci` extension.
- Search provider output is orientation material until it becomes a durable Artifact with Provenance Records and is deliberately linked as an Evidence Item.
- Passing an upstream test is execution evidence, not automatically reproduction of a paper claim or fair comparison with another system.
- Numbers from a generated-data capability probe describe only the declared probe conditions; they are not paper reproduction or benchmark evidence.
- A Theory Comparison Artifact compares source-backed descriptions and interpretations; its cells retain `reported`, `located`, or `inspected` depth until first-hand comparative Runs exist.
- Seed-directed expansion records backward, neighboring, forward, and post-seed discovery routes; citation count, recency, and provider rank are signals rather than automatic inclusion rules.
- An explicit clarification-first request blocks acquisition, mutation, and research Runs until the user chooses to proceed; read-only inspection may continue so questions can be grounded in accepted context.
- Every empirical comparison begins with a durable Comparison Intent Document and user checkpoint; field conventions guide the proposal but do not replace explicit source, metric, readiness, fairness, and evidence rationales.
- Before asking for or downloading a dataset, Kaoju queries the Topic Dataset Manifest and validates registered candidates; a managed symlink is a convenience locator, not dataset identity or write authorization.
- User-nominated sources receive priority review and a recorded disposition, not automatic authority or inclusion. Curated intake is read-only by default, preserves exact source support, and does not imply broad survey coverage.
