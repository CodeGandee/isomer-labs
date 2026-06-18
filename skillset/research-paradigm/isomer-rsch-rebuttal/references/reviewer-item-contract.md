# Reviewer Item Contract

Use this reference before any reviewer-linked experiment, manuscript rewrite, or response drafting.

## Purpose

Rebuttal work converts concrete reviewer pressure into the smallest honest revision program that can be executed. It does not invent a separate research workflow. It routes text, literature, baseline, analysis, figure, claim-scope, and decision work through the normal Isomer skill stages.

## Atomic Item Rules

Normalize every substantive reviewer comment into stable atomic items. Each item must have a stable id such as `R1-C1`, reviewer identity if known, source-faithful wording or clipped quote, explicit or inferred flag, class, severity, stance, primary route, affected claim, evidence anchor or gap, required action, status, and notes.

Controlled ellipsis is allowed when the original comment is long, but semantic rewriting is not. Inferred items are allowed only when comments are incomplete or the user provided rough prose; mark them clearly as inferred.

## Comment Classes

- `editorial`: wording, organization, typo, presentation.
- `text_only`: explanation gap, related-work gap, clarity gap, or missing discussion.
- `evidence_gap`: missing table, figure, comparison, or stronger analysis already latent in existing results.
- `experiment_gap`: genuinely new supplementary runs are required.
- `claim_scope`: current claim is too broad and needs narrowing or downgrade.
- `cannot_fully_address`: request is infeasible, out of scope, or impossible within the real evidence budget.

## Stance and Route Values

Use stance values: `agree`, `partially_agree`, `clarify`, and `respectful_disagree`.

Use primary route values: `text_revision`, `evidence_repackaging`, `literature_positioning`, `baseline_recovery`, `supplementary_experiment`, `claim_downgrade`, and `explicit_limitation`.

## Source-Term Mapping

| Source concept | Isomer framing |
| --- | --- |
| review matrix file | Reviewer item matrix Artifact |
| action plan file | Rebuttal action plan Artifact |
| response letter file | Response letter Artifact |
| text deltas file | Manuscript delta Artifact |
| evidence update file | Evidence update Artifact |
| baseline execution policy | Gate or Decision Record over comparator recovery |
| manuscript edit mode | Capability Binding or deliverable format constraint |
| analysis campaign launch | Decision Record routing reviewer-linked slices to `isomer-rsch-analysis` |
| artifact or memory operations | Artifacts, Evidence Items, Findings, Decision Records, Gates, or host APIs |
| command execution | Capability Binding through an Execution Adapter using `[[tbd-surface:api-execution-command]]` |

## TBD Surfaces

Use paper Artifact through Workspace Path Resolution for concrete manuscript or rebuttal layouts, `[[tbd-surface:api-artifact-record]]` for record updates, `[[tbd-surface:schema-evidence-item]]` for unsettled evidence fields, and `[[tbd-surface:provider-literature-search]]` for literature provider uncertainty.

| ID | Kind | Missing decision |
| --- | --- | --- |
| paper Artifact | resolved path surface | Resolved through Workspace Path Resolution. |
| api-artifact-record | api | API for recording Artifacts and Provenance Records. |
| api-execution-command | api | Execution command surface, permissions, and logging behavior. |
| provider-literature-search | provider | Literature search and paper-reading provider. |
| schema-evidence-item | schema | Evidence Item fields and validation. |

## Non-negotiable Rules

Do not invent experiment results, response claims, manuscript changes, citations, or reviewer intent. Do not promise future work unless that response style is allowed and the work is genuinely planned. Do not ignore hard reviewer concerns because they are inconvenient. Do not answer with rhetoric when the issue requires evidence.
