# Audit Gate

Use this reference before judging a substantial draft, report, or manuscript package. The reader is an Isomer agent acting as an independent reviewer.

## Purpose

The review stage converts "the draft feels close" into a skeptical, technically grounded Gate. It should identify core claims, likely rejection routes, evidence sufficiency, novelty and positioning risks, language hygiene problems, display weaknesses, citation gaps, and the next route.

## Scope Fit

Use review when a real draft or report exists and the task is independent audit. Use `isomer-rsch-write-v1` for ordinary drafting from accepted evidence. Use `isomer-rsch-rebuttal-v1` when concrete external reviewer comments already exist.

## Audit Plan

Before writing the report, identify package maturity, one to three core claims, strongest evidence, weakest evidence, top likely rejection reasons, real ready experiment or analysis group count, user-specified evidence target if any, closest high-quality comparators, manuscript process-language risks, and likely next route.

## Stop-Loss Rule

If novelty, evidence sufficiency, or reader value has collapsed beyond reasonable claim narrowing, recommend `isomer-rsch-decision-v1` for stop, Research Inquiry Relationship, or scope downgrade. Do not recommend another cosmetic revision pass. When the route depends on publication-facing output, scope, cost, privacy, external upload, or non-paper preference, run Gate Policy preflight and open or reference a Gate when Operator Agent judgment is required.

## Source-Term Mapping

| Source concept | Isomer framing |
| --- | --- |
| review follow-up policy | Gate or Decision Record controlling audit-only, user-gated follow-up, or approved auto-follow-up |
| manuscript edit mode | Capability Binding or deliverable format constraint, not a global runtime mode |
| review milestone interaction | Operator-facing Artifact, Finding, or progress note |
| experiment todo file | Evidence TODO Artifact or analysis frontier linked to a Decision Record |
| paper coverage validation call | Gate over manuscript coverage, evidence provenance, citations, language, figures, and bundle state |
| artifact or memory operations | Artifacts, Evidence Items, Findings, Decision Records, Gates, or host APIs |
| command execution | Execution Adapter Command Request with applicable Research Operation Extension Point, Capability Binding, policy, workspace, and recording refs |

## Resolved Extension Surfaces

Use paper Artifact through Workspace Path Resolution for concrete manuscript layouts, the accepted Artifact and Provenance recording API for record updates, the accepted Finding query/write API for durable context queries, Literature Provider Binding refs for literature search providers, Execution Adapter Command Requests for executable inspection, and the accepted Evidence Item fields for evidence fields.

| Surface | Resolution |
| --- | --- |
| paper Artifact | Resolved through Workspace Path Resolution. |
| command execution | Resolved through Execution Adapter Command Requests. |
| literature provider | Resolved through Literature Provider Binding refs. |

## Review Gate Pass Conditions

The review gate passes only when the review report, revision log, and any evidence TODOs are durable; highest-risk issues are explicit; serious comments are tied to evidence or text locations; and the next route is unambiguous.
