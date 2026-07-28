## Why

Kaoju currently distinguishes paper triage from full-text claim examination, but neither reading depth establishes that a selected paper will receive a self-contained, detailed treatment in the final survey. A lecture-depth option is needed for papers whose method must be taught through dedicated prose, equations, figures, tables, evidence, and limitations without requiring the reader to consult the original paper for basic method comprehension.

## What Changes

- Add a packaged `paper.lecture` Mindset Source with canonical inspection depth `lecture`, a complete default question set, and questions for pedagogical structure, notation, method walkthrough, equations, displays, evidence, comparison, limitations, and section readiness.
- Extend deterministic mindset routing, Run resolution, topic derivation, validation, and documentation from three packaged keys to four.
- Revise paper ingestion and examination skills so lecture-depth reading produces a lecture-ready `KAOJU:SOURCE-DIGEST` and Claim-Evidence Ledger updates with exact source locators, a pedagogical outline, equation explanations, display candidates, rights-handling posture, and explicit readiness blockers.
- Revise synthesis and writing skills so an accepted lecture-ready paper is treated as a commitment to a dedicated, substantial survey section rather than an ordinary citation or brief related-work entry.
- Require the writing stage to ground the detailed section in accepted evidence, create selected figures and tables as file-backed `KAOJU:PAPER-DISPLAY` Artifacts, maintain citation and display lineage, and preserve unresolved or blocked lecture commitments rather than silently shortening or omitting them.
- Preserve the existing division of responsibility: examination records lecture-ready evidence and presentation plans, while synthesis and writing create conclusions, final prose, and publication displays.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `kaoju-mindsets`: Add the `paper.lecture` packaged seed, applicability route, question inventory, Run resolution, and topic-derived Source behavior.
- `kaoju-research-extension`: Require lecture-depth examination output and carry the resulting detailed-presentation commitment through examination and synthesis handoffs.
- `kaoju-paper-production`: Require a dedicated, detailed, evidence-grounded survey section for each accepted lecture-ready paper and define blocked or superseded commitment handling.

## Impact

The change affects packaged Kaoju mindset resources, the checked survey-process contract, Mindset Source validation, Run mindset resolution, topic creation, public entrypoint routing, reading ingestion, examination, synthesis, writing guidance, domain documentation, and unit and integration tests. It extends the existing `KAOJU:SOURCE-DIGEST`, `KAOJU:CLAIM-EVIDENCE-LEDGER`, `KAOJU:PAPER-DISPLAY`, and citation-map workflows without adding a new Artifact semantic id or changing the Mindset Source schema version.
