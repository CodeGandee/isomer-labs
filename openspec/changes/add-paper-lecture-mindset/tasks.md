## 1. Mindset Seed and Routing

- [x] 1.1 Add the packaged `paper.lecture` Mindset Source v2 resource with the exact twelve-question inventory, default `question_ids: "all"` set, collector contract, and `lecture` applicability.
- [x] 1.2 Extend `DEFAULT_KEYS`, exact seed-question validation, protected resource inventories, process-contract route validation, and Run mindset resolution to accept all four checked keys.
- [x] 1.3 Add the `paper.lecture` route to `survey-process.v2.json` and update selection tests for explicit, automatic, ambiguous, missing-Source, and immutable Run-resolution behavior.
- [x] 1.4 Update Kaoju topic creation and packaged installation checks so explicit preparation creates a missing lecture Source while preserving valid existing topic Sources and historical state.

## 2. Lecture Examination Contract

- [x] 2.1 Extend Source Digest semantic validation with the conditional `lecture_exposition` contract, including readiness state, exact-locator equation and display entries, handling posture, outline, blockers, and selected lecture Run provenance.
- [x] 2.2 Revise the public Kaoju entrypoint, `ingest-reading-item`, and Examine skill guidance to select `paper.lecture`, preserve its detailed-presentation commitment for both `recorded` and `skipped_source_missing`, and forbid silent deep-dive downgrade.
- [x] 2.3 Revise Examine output guidance so lecture work records prerequisites, notation, intuition, method walkthrough, worked trace, equations, displays, evidence, comparisons, limitations, and section readiness without creating final prose or `KAOJU:PAPER-DISPLAY`.
- [x] 2.4 Add unit and integration coverage for lecture-ready and blocked Source Digests, display handling postures, exact evidence locators, missing optional Mindset Records, and non-lecture backward compatibility.

## 3. Synthesis and Paper Commitment Handoff

- [x] 3.1 Revise the Synthesize skill and applicable structured-output guidance to carry a deterministic lecture-section commitment inventory with active, blocked, and explicitly superseded postures into accepted Field Summary state.
- [x] 3.2 Add validation and tests that preserve every audited `paper.lecture` commitment through synthesis and reject implicit supersession by omission, a later non-lecture Run, or a shorter proposed treatment.
- [x] 3.3 Revise `draft-paper`, the Write skill, and paper-contract and manuscript-structure references to reconcile the lecture inventory and create one dedicated named section job per active lecture-ready paper.
- [x] 3.4 Extend paper validation so each active lecture section covers its accepted method-exposition obligations, equations, displays, limitations, Citation Map lineage, blockers, and explicit not-applicable postures without imposing fixed length or media counts.
- [x] 3.5 Ensure writing creates selected figures and tables as file-backed `KAOJU:PAPER-DISPLAY` Artifacts, authors essential equations in canonical MyST, records source and transformation posture, and preserves blocked or superseded commitments in paper revision state.

## 4. Documentation and Verification

- [x] 4.1 Update canonical domain language, Kaoju README and process documentation, topic-creator inventory guidance, skill routing text, and packaged default counts from three mindsets to four.
- [x] 4.2 Update system-skill installation, process-contract, mindset, survey Artifact, synthesis, and paper-production fixtures and acceptance tests for the new resource and behavior.
- [x] 4.3 Run `openspec validate --change add-paper-lecture-mindset`, `pixi run lint`, `pixi run typecheck`, and `pixi run test`, then resolve all diagnostics caused by the change.
