# Use Cases

This directory contains feature-specific use cases for the Kaoju Research Extension.

## Index

| ID | Use Case | Status |
| --- | --- | --- |
| `UC-01` | [Frame an Evidence-Led Kaoju Inquiry](uc-01-frame-an-evidence-led-kaoju-inquiry.md) | Draft |
| `UC-02` | [Discover and Acquire a Versioned Source Corpus](uc-02-discover-and-acquire-a-versioned-source-corpus.md) | Draft |
| `UC-03` | [Trace Claims Across Papers and Implementations](uc-03-trace-claims-across-papers-and-implementations.md) | Draft |
| `UC-04` | [Reproduce a Published Claim with First-Hand Runs](uc-04-reproduce-a-published-claim-with-first-hand-runs.md) | Draft |
| `UC-05` | [Compare Existing Implementations Under a Fair Protocol](uc-05-compare-existing-implementations-under-a-fair-protocol.md) | Draft |
| `UC-06` | [Audit and Synthesize a Kaoju Dossier](uc-06-audit-and-synthesize-a-kaoju-dossier.md) | Draft |
| `UC-07` | [Resume and Refresh a Kaoju Investigation](uc-07-resume-and-refresh-a-kaoju-investigation.md) | Draft |

## Coverage Notes

- `UC-01` establishes the Research Inquiry, coverage contract, evidence targets, resource envelope, and selected pipeline pass.
- `UC-02` covers discovery, inclusion decisions, canonical external repository registration, paper and documentation snapshots, and governed model or dataset acquisition.
- `UC-03` covers exact claim location, paper-to-code mapping, artifact identity, implementation drift, and contradiction recording without requiring execution.
- `UC-04` covers faithful execution, isolated repair, first-hand Run evidence, and reproduction verdicts for one selected claim.
- `UC-05` covers multi-system normalization, controlled Runs, uncertainty, fairness checks, and explicit `not comparable` outcomes.
- `UC-06` covers independent evidence audit, calibrated synthesis, final claim status, limitations, and optional downstream DeepSci handoff.
- `UC-07` covers durable resume, source and implementation drift detection, targeted invalidation, and lineage-preserving refresh.

## Skill Coverage

The use cases follow user goals rather than creating one use case per implementation skill. The interface design still gives every proposed public skill a distinct owner boundary.

| Proposed Skill | Primary Use Cases |
| --- | --- |
| `isomer-kaoju-shared` | All use cases through latest-context, source-identity, evidence-state, lineage, handoff, and worker-output rules. |
| `isomer-kaoju-workspace-mgr` | `UC-01`, with readiness and material-policy consequences used by `UC-02`, `UC-04`, `UC-05`, and `UC-07`. |
| `isomer-kaoju-frame` | `UC-01` and the reframing portion of `UC-07`. |
| `isomer-kaoju-discover` | `UC-02` and source-drift refresh in `UC-07`. |
| `isomer-kaoju-acquire` | `UC-02` and changed-material refresh in `UC-07`. |
| `isomer-kaoju-examine` | `UC-03` and affected-claim refresh in `UC-07`. |
| `isomer-kaoju-reproduce` | `UC-04` and stale-Run refresh in `UC-07`. |
| `isomer-kaoju-compare` | `UC-05` and stale-comparison refresh in `UC-07`. |
| `isomer-kaoju-audit` | Audit portion of `UC-06` and refreshed audit in `UC-07`. |
| `isomer-kaoju-synthesize` | Synthesis portion of `UC-06` and refreshed dossier in `UC-07`. |
| `isomer-kaoju-pipeline` | Pass selection in `UC-01`, orchestration across `UC-02` through `UC-06`, and bounded resume in `UC-07`. |

## Boundary Notes

- Kaoju is claim-centric and provenance-first. It investigates what existing sources and implementations establish.
- DeepSci remains hypothesis-centric. It selects and tests new research routes. Kaoju may hand evidence to DeepSci but does not require the `deepsci` extension.
- Search provider output is orientation material until it becomes a durable Artifact with Provenance Records and is deliberately linked as an Evidence Item.
- Passing an upstream test is execution evidence, not automatically reproduction of a paper claim or fair comparison with another system.
