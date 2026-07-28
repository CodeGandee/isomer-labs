## Context

Kaoju currently routes paper work at `skim` or `triage` depth to `paper.skimming` and work at `deep` or `full-text` depth to `paper.deep-dive`. Both routes produce ordinary examination evidence, but neither carries a durable promise about how prominently the paper will appear in the final survey. The existing Mindset Source v2 contract already supports another packaged key, a default question set with `question_ids: "all"`, topic specialization, immutable Run snapshots, and verified missing-Source operation.

The examination owner already produces `KAOJU:SOURCE-DIGEST` and `KAOJU:CLAIM-EVIDENCE-LEDGER`. Synthesis consumes accepted evidence into the Field Summary and related views. Writing consumes accepted audit and synthesis state, creates canonical MyST, stores figures and tables as `KAOJU:PAPER-DISPLAY`, and maintains the Citation Map. The change must preserve these ownership boundaries and the rule that mindset content is reflective, optional topic-derived intent rather than workflow authority.

## Goals / Non-Goals

**Goals:**

- Add one canonical lecture-depth paper route and packaged `paper.lecture` Mindset Source.
- Make selection of `paper.lecture` a durable intent to present that paper in a dedicated, substantial survey section.
- Require lecture examination to gather enough accepted, exactly located material to support a self-contained explanation of the paper's method.
- Carry lecture-section commitments through synthesis so writing cannot silently reduce them to ordinary related-work mentions.
- Reuse current Artifacts and producer boundaries while adding validation and skill guidance.

**Non-Goals:**

- Replace the original paper as the authority for proofs, audit, or reproduction.
- Make every deeply read paper a lecture paper or automatically escalate `paper.deep-dive`.
- Add Mindset Source inheritance, executable mindset fields, a new Artifact semantic id, or a new schema version.
- Let examination write final survey prose or publication displays.
- Require a fixed word count, a fixed number of equations or displays, or the same exposition pattern for every paper type.

## Decisions

### Use `paper.lecture` with one canonical `lecture` depth

The checked process contract will add `paper.lecture` for actions `ingest-reading-item` and `examine`, source kinds `paper` and `report`, and depth `lecture`. The route will be selected explicitly from requested inspection depth. A skim or deep-dive Run may recommend lecture examination, but a new Run is required to establish the lecture commitment.

Using one canonical depth avoids treating output states such as “section-ready” as input synonyms. `lecture-ready` is an examination result, not a route selector.

The alternative was a specialized question set within `paper.deep-dive`. That would hide a paper-production commitment inside question-set selection and would not give Run routing, status reporting, or downstream consumers a stable key.

### Package a self-contained twelve-question seed

The new seed will have a single `default` question set with the standard fallback triggering condition and `question_ids: "all"`. Its ordered question inventory will cover:

1. `survey-section-role`
2. `reader-contract`
3. `problem-setting-and-notation`
4. `method-intuition`
5. `method-walkthrough`
6. `worked-trace`
7. `equation-teaching-plan`
8. `display-teaching-plan`
9. `evidence-and-results`
10. `comparison-and-positioning`
11. `limitations-and-failure-modes`
12. `section-outline-and-readiness`

The seed duplicates necessary deep-dive concerns rather than inheriting from `paper.deep-dive`. A Mindset Source therefore remains independently editable and snapshot-readable. Topic creation may specialize its question catalog and add many-to-many question sets under the existing v2 rules.

### Derive the presentation commitment from the selected Run key

The selected key `paper.lecture` establishes the detailed-presentation commitment whether the Run disposition is `recorded` or `skipped_source_missing`. A missing topic Source suppresses optional reflection, but it does not change the meaning of the checked process route. This keeps workflow semantics separate from low-authority Mindset Source content.

Deep-dive selection does not create the commitment. A lecture commitment remains active until fulfilled or explicitly superseded through an accepted survey-planning or synthesis revision that names the affected Run or Source Digest and records the rationale. A consumer cannot infer supersession from omission.

### Extend Source Digest content instead of adding an Artifact

For a `paper.lecture` Run, examination will add a structured `lecture_exposition` section to the source-scoped `KAOJU:SOURCE-DIGEST`. The section will include:

- The selected lecture Run and mindset resolution.
- The paper's intended survey-section role and reader learning outcome.
- Reader prerequisites, problem setup, definitions, and symbol glossary.
- Method intuition, ordered walkthrough, and a worked example or trace when applicable.
- Essential equations with exact locators, symbol explanations, interpretation, and planned presentation.
- Essential figures and tables with exact locators, teaching role, caption and surrounding context, interpretation, and handling posture.
- Accepted claim and evidence refs, evaluation results, comparison points, limitations, and failure modes.
- A proposed dedicated-section outline.
- Status `lecture-ready` or `blocked`, plus every unresolved blocker.

The existing Source Digest remains the examination authority and already has synthesis and writing as consumers. Conditional semantic validation will require the lecture exposition when the selected Run key is `paper.lecture`. Ordinary Source Digests remain compatible.

A separate lecture dossier was considered. It would duplicate source identity, findings, revision, scope, and acceptance behavior while requiring a new binding and profile. The Source Digest extension provides the required handoff with less state and no new top-level lifecycle.

### Separate evidence planning from authored presentation

Examination records which equations, figures, and tables are needed and how they could be presented. It does not create final paper prose or `KAOJU:PAPER-DISPLAY`.

The display handling posture will be one of `reproduce`, `adapt`, `redraw`, `describe`, or `omit`, with source attribution, provenance, and the recorded license or permission evidence available to the workflow. Unsupported reproduction will not be selected merely because the original asset is pedagogically useful. Writing creates a file-backed `KAOJU:PAPER-DISPLAY` for each selected figure or table and cites it through a typed MyST placeholder. Equations are authored in canonical MyST with exact source and evidence links in the Citation Map.

### Make synthesis carry an explicit lecture commitment inventory

Synthesis will inspect accepted evidence for Runs selected with `paper.lecture` and carry a lecture-section inventory in its accepted Field Summary or equivalent requested synthesis view. Each entry will name the paper identity, lecture Run, Source Digest, readiness state, proposed section job, required equations and displays, blockers, and any explicit supersession decision.

This inventory prevents the writing skill from discovering lecture intent through file scanning or prose inference. It also lets audit and synthesis expose incomplete lecture work before drafting.

### Require one dedicated substantial section per active lecture commitment

Writing will map every active, accepted, lecture-ready commitment to a dedicated named section in `KAOJU:PAPER-STRUCTURE-MYST`. The exact heading level remains adaptive to the paper structure, but the paper must be the primary subject of that section and cannot be reduced to a citation, a list item, or a shared short related-work paragraph.

The filled section will teach the problem and prerequisites, notation, intuition, method flow, essential equations and displays, supporting results, comparison, limitations, and unresolved boundaries to the degree applicable to that paper. Content-based checks replace fixed length or media counts. A paper with no essential table, for example, may mark that element not applicable with evidence rather than fabricate one.

If an active commitment is blocked, missing from accepted synthesis, or unsupported by accepted evidence, drafting pauses or keeps an explicit unresolved structure obligation. Writing cannot silently omit, merge, or shorten the section. An explicit accepted supersession can remove the obligation while preserving its lineage and rationale.

## Risks / Trade-offs

- [Lecture requests can expand survey scope substantially] → Require explicit `lecture` depth, a new Run, and a visible synthesis commitment inventory.
- [A detailed explanation can overstate unsupported paper claims] → Keep every statement, equation, and display tied to exact accepted evidence and preserve source statement versus interpretation.
- [Original figures and tables may not be suitable for direct reuse] → Require a recorded handling posture and use adaptation, redraw, or description when reproduction is not supported.
- [A rigid checklist may fit theoretical, empirical, and systems papers differently] → Permit supported not-applicable answers and topic-specific question sets while keeping the default completeness test.
- [Existing topics will initially lack the fourth Source] → Preserve verified missing-Source behavior; explicit Kaoju topic preparation creates the new topic-owned Source.
- [Writing could overlook a lecture Run among many evidence records] → Make synthesis produce a deterministic commitment inventory and require writing to reconcile it before structure acceptance.

## Migration Plan

1. Add and validate the fourth packaged seed, route, key inventory, and exact question catalog.
2. Update topic creation so explicit initialization creates a missing `paper.lecture` Source while preserving every valid existing Source.
3. Update Run resolution, entrypoint, ingestion, examination, synthesis, and writing guidance and tests.
4. Add conditional Source Digest and paper-structure validation for lecture commitments.
5. Update domain language, process documentation, package inventory checks, and affected acceptance fixtures.

Existing Mindset Sources, Runs, Records, Source Digests, synthesis records, and paper drafts remain unchanged. Existing topics acquire the new Source only through explicit topic preparation. Existing non-lecture work retains its current behavior. A rollback may stop creating new lecture Runs, but it must leave already recorded Runs and generic Artifact content readable.

## Open Questions

None. The proposal uses `lecture` as the canonical requested depth, `lecture-ready` as the successful examination state, and a dedicated named section as the writing obligation.
