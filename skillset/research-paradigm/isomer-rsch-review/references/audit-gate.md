# Audit Gate

Use this reference before judging a substantial draft, report, or manuscript package. The reader is an Isomer agent acting as an independent reviewer.

## Purpose

The review stage converts "the draft feels close" into a skeptical, technically grounded Gate. It should identify core claims, likely rejection routes, evidence sufficiency, novelty and positioning risks, language hygiene problems, display weaknesses, citation gaps, and the next route.

## Scope Fit

Use review when a real draft or report exists and the task is independent audit. Use `isomer-rsch-write` for ordinary drafting from accepted evidence. Use `isomer-rsch-rebuttal` when concrete external reviewer comments already exist.

## Audit Plan

Before writing the report, identify package maturity, one to three core claims, strongest evidence, weakest evidence, top likely rejection reasons, real ready experiment or analysis group count, user-specified evidence target if any, closest high-quality comparators, manuscript process-language risks, and likely next route.

## Stop-Loss Rule

If novelty, evidence sufficiency, or reader value has collapsed beyond reasonable claim narrowing, recommend `isomer-rsch-decision` for stop, branch, or scope downgrade. Do not recommend another cosmetic revision pass. When the route depends on user publication, scope, cost, or non-paper preference, record or ask for a Gate through the Operator Agent.

## Source-Term Mapping

| Source concept | Isomer framing |
| --- | --- |
| review follow-up policy | Gate or Decision Record controlling audit-only, user-gated follow-up, or approved auto-follow-up |
| manuscript edit mode | Capability Binding or deliverable format constraint, not a global runtime mode |
| review milestone interaction | Operator-facing Artifact, Finding, or progress note |
| experiment todo file | Evidence TODO Artifact or analysis frontier linked to a Decision Record |
| paper coverage validation call | Gate over manuscript coverage, evidence provenance, citations, language, figures, and bundle state |
| artifact or memory operations | Artifacts, Evidence Items, Findings, Decision Records, Gates, or host APIs |
| command execution | Capability Binding through an Execution Adapter using `[[tbd-surface:api-execution-command]]` |

## TBD Surfaces

Use `[[tbd-surface:path-paper-layout]]` for concrete manuscript layouts, `[[tbd-surface:api-artifact-record]]` for record updates, `[[tbd-surface:api-finding-query]]` for durable context queries, `[[tbd-surface:provider-literature-search]]` for literature search providers, and `[[tbd-surface:schema-evidence-item]]` for unsettled evidence fields.

| ID | Kind | Missing decision |
| --- | --- | --- |
| path-paper-layout | path | Report or manuscript layout. |
| api-artifact-record | api | API for recording Artifacts and Provenance Records. |
| api-finding-query | api | API for querying and writing Findings or durable context. |
| api-execution-command | api | Execution command surface, permissions, and logging behavior. |
| provider-literature-search | provider | Literature search and paper-reading provider. |
| schema-evidence-item | schema | Evidence Item fields and validation. |

## Review Gate Pass Conditions

The review gate passes only when the review report, revision log, and any evidence TODOs are durable; highest-risk issues are explicit; serious comments are tied to evidence or text locations; and the next route is unambiguous.
