# Writing Contract

Use this contract before drafting, revising, packaging, or routing a paper-like deliverable. The reader is an Isomer agent turning durable research evidence into honest prose.

## Truth-Source Order

Prefer durable records over recollection:

1. Operator Agent instruction and explicit Gates.
2. Selected outline, claim-evidence map, experiment or analysis matrix, bibliography, figure/table catalog, manuscript bundle, Decision Records, Research Claims, Evidence Items, Artifacts, and Provenance Records.
3. Run records, validated logs, figure renders, tables, code or configuration facts verified through an approved Capability Binding and Execution Adapter.
4. Current conversation context, only when durable state is absent or being interpreted.

## Pre-write Revision Strategy Gate

Before editing prose, produce a concrete revision strategy from the current evidence state. Separate evidence gaps, manuscript-mapping gaps, unsupported writing, narrative or positioning gaps, citation gaps, and metadata drift. For each issue, choose exactly one action: route to analysis, downgrade or remove the claim, add an existing result to main text, move the result to appendix with a bridge, add or repair a display, add verified citations, repair the outline, route to review or decision, or mark a blocker.

Never make an unsupported claim sound more convincing. If evidence is missing, obtain evidence, narrow the claim, or mark the blocker.

## Paper Contract Surfaces

Keep these surfaces aligned when they exist: selected outline Artifact, evidence ledger or claim-evidence map, experiment or analysis matrix, references bibliography, figure/table catalog, manuscript source or rendered bundle, review or rebuttal packet, and bundle manifest. Concrete paths and storage layouts are not defined by this skill; use paper Artifact or another semantic Artifact kind resolved by Workspace Path Resolution when a concrete layout must be named.

## Source-Term Mapping

| Source concept | Isomer framing |
| --- | --- |
| paper contract health call | Gate or validation report over outline, evidence, figures, citations, and bundle state |
| paper bundle submission call | Artifact and Provenance Record for draft checkpoint, review package, or submission package |
| outline submit or compile call | Outline Artifact, section-level writing plan, and Gate over outline readiness |
| analysis campaign launch | Decision Record that routes to `isomer-rsch-analysis` |
| memory read or write | Finding query, Evidence Item lookup, Artifact note, or durable context query through `[[tbd-surface:api-finding-query]]` |
| shell or document build execution | Capability Binding through an Execution Adapter using `[[tbd-surface:api-execution-command]]` |
| literature provider | literature search capability with provider unsettled by `[[tbd-surface:provider-literature-search]]` |

## Registered TBD Surfaces

| ID | Kind | Missing decision |
| --- | --- | --- |
| paper Artifact | resolved path surface | Resolved through Workspace Path Resolution. |
| semantic Artifact kind | resolved path surface | Resolved through Workspace Path Resolution. |
| api-finding-query | api | API for querying and writing Findings or durable context. |
| api-execution-command | api | Execution command surface, permissions, and logging behavior. |
| provider-literature-search | provider | Literature search and paper-reading provider. |

## Section Job Discipline

Draft by bounded section jobs: introduction, related work, method, experiments, analysis, limitations, conclusion, appendix, abstract, and integration. Write the abstract late, after evidence order and claim scope stabilize. A section job should state its local claim, evidence basis, target display, citation needs, appendix bridge, and open blockers before prose is treated as stable.

## Publishability Stop-Loss

If current evidence, novelty boundary, or reader value cannot support a defensible paper after reasonable claim narrowing, stop drafting and route to `isomer-rsch-decision` for stop, branch, scope downgrade, or non-paper objective. Cosmetic revision is not an answer to collapsed evidence or value.

## Validation

Before treating a writing pass as durable, check that every important claim points to Evidence Items, verified citations, or an explicit gap; figures and tables exist or are blockers; appendix bridges are concrete; artifact availability language is consistent; manuscript prose contains no local process language; and the output ends as a stronger draft, explicit blocker, or route-back Decision Record.
