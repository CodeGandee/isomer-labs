---
name: isomer-rsch-rebuttal-v1
description: Map reviewer feedback into evidence actions, manuscript deltas, and durable rebuttal or revision responses.
---

# Isomer Research Rebuttal

## Overview

Use this skill when concrete reviewer comments, editor letters, external critiques, or revision requests must become a durable response matrix, action plan, evidence update, manuscript delta, and response letter.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Load required context**. Read `references/reviewer-item-contract.md` first and read `references/provenance.md` when source provenance or license context matters.
2. **Select supporting references** from **Reference Routing** when matrix construction, action planning, response drafting, evidence updates, manuscript deltas, or route choices matter.
3. **Confirm entry fit and normalize inputs**. Use **Entry Signals** to confirm concrete review pressure exists, then normalize comments into stable atomic reviewer items without changing meaning.
4. **Classify each item and choose a route**. Separate wording gaps, literature or novelty gaps, evidence repackaging, missing comparators, true supplementary evidence, claim downgrades, and explicit limitations.
5. **Plan and route work before execution**. Use the action plan to decide which items go to write, scout, baseline, analysis, figure-polish, decision, or blocker.
6. **Update evidence and text surfaces**. Keep the review matrix, evidence update, text deltas, and paper experiment or analysis plan synchronized after every routed fix.
7. **Assemble the response package**. Draft calm, direct, evidence-backed responses that answer each item honestly and show the manuscript or evidence delta.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user request, then execute the plan.

## Reference Routing

Read first:

- `references/reviewer-item-contract.md` for atomic item rules, class taxonomy, stance values, route values, source-term mappings, and TBD-surface rules.
- `references/provenance.md` when source provenance or license context matters.

Read references as needed:

- `references/review-matrix-template.md` when building or refreshing the durable reviewer matrix.
- `references/action-plan-template.md` when deciding item-by-item evidence, text, baseline, literature, limitation, or claim-scope actions.
- `references/response-letter-template.md` when drafting rebuttal-ready author responses.
- `references/evidence-update-template.md` when mapping completed, missing, blocked, or downgraded evidence to reviewer items.
- `references/text-delta-template.md` when recording manuscript changes, claim narrowing, section replacements, or LaTeX-ready replacement text.
- `references/rebuttal-routing.md` when choosing between write, scout, baseline, analysis, figure-polish, decision, finalize, or blocker.

## Entry Signals

- Reviewer comments, a meta-review, editor letter, revision request, decision letter, or external critique is available.
- The work requires point-by-point response, evidence updates, manuscript deltas, claim downgrades, limitation wording, literature positioning, comparator recovery, or reviewer-linked analysis.
- A response package must remain source-faithful and auditable.

## Exit Criteria

- Reviewer items are normalized into a durable matrix with stable ids, source-faithful wording, class, severity, stance, primary route, affected claims, evidence anchor or gap, and status.
- Evidence updates, text deltas, and response material link back to reviewer item ids.
- Feasible reviewer-critical rows are resolved, explicitly downgraded, or blocked with an honest limitation and route note.

## Durable Outputs

- Reviewer item matrix Artifact.
- Rebuttal action plan Artifact.
- Evidence update Artifact.
- Text delta Artifact.
- Response letter or revision package Artifact.
- Decision Record or Gate for supplementary evidence, baseline recovery, claim downgrade, scope limitation, or final revision handoff.

## Guardrails

- Do not invent experiment results, response claims, manuscript changes, citations, or reviewer intent.
- Do not rewrite reviewer meaning during normalization; mark inferred items clearly.
- Do not launch free-floating supplementary work; every slice must answer named reviewer items.
- Do not route reviewer-linked baseline-dependent analysis as ready unless the accepted comparator is durable or a Baseline-Waiver Policy ref plus required Gate or Decision Record is durable.
- Do not treat novelty or positioning pressure as an automatic experiment request.
- Do not pretend a limitation is solved when it is only reframed.
- Do not finalize while reviewer-critical feasible rows remain unresolved without an explicit blocker or limitation note.
