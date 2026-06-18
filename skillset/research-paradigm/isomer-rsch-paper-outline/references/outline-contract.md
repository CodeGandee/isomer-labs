# Outline Contract

Use this contract before creating, selecting, validating, or repairing a paper-native outline.

## Core Split

Keep one selected outline, but split two views. `paper_view` is what the paper says to readers. `evidence_view` is where exact runs, settings, metrics, sources, reproducibility details, caveats, and unmapped items live.

The paper must stay faithful to evidence, but it should not repeat local execution history or agent workflow.

## Truth-Source Order

Prefer durable records over recollection: Operator Agent instructions and Gates; selected outline, Evidence Items, Research Claims, Decision Records, Artifacts, and Provenance Records; run records and validated outputs; then conversation context only when durable state is absent.

## Required Thinking Steps

Find the one-sentence paper idea. Separate observed facts from allowed interpretations. Define what the paper must not claim. Build the paper view with story spine, scoped claims, method abstraction, evaluation plan, analysis plan, reviewer objections, and evidence grounding. Build the evidence view with claim-to-item links, sections, unmapped items, appendix reproducibility, and unresolved gaps.

## Source-Term Mapping

| Source concept | Isomer framing |
| --- | --- |
| outline submit or selected outline call | Outline Artifact and Decision Record |
| outline validation call | Gate over outline maturity, claim support, analysis plan, and process-language cleanliness |
| writing-plan compile call | Section-level writing plan Artifact |
| paper contract | Bundle of outline, claim-evidence map, experiment or analysis matrix, bibliography, displays, and manuscript state |
| artifact or memory operations | Artifacts, Evidence Items, Findings, Decision Records, Gates, or host APIs |
| paper paths | paper layout or Artifact layout TBD surfaces |

## TBD Surfaces

Use `[[tbd-surface:api-artifact-record]]` for unsettled outline recording, paper Artifacts resolved by Workspace Path Resolution for manuscript outputs, `[[tbd-surface:schema-research-claim]]` for claim fields, `[[tbd-surface:schema-evidence-item]]` for evidence fields, and `[[tbd-surface:schema-decision-record]]` for outline selection decisions.

| ID | Kind | Missing decision |
| --- | --- | --- |
| api-artifact-record | api | API for recording Artifacts and Provenance Records. |
| paper Artifact | resolved path surface | Resolved through Workspace Path Resolution. |
| schema-decision-record | schema | Decision Record fields and validation. |
| schema-evidence-item | schema | Evidence Item fields and validation. |
| schema-research-claim | schema | Research Claim state and fields. |

## Good Outline Definition

A good outline has a point, stays honest, and helps a reader. It presents one clear lesson or claim, ties every claim to Evidence Items and limits, and teaches something beyond "this setup produced a number."

## Validation

Before handing to write, check that the outline has one clear idea, one to three scoped claims, evidence and falsification boundaries, novelty boundary, reviewer objections, a useful analysis plan or waiver, and no local process language in paper-facing fields.
