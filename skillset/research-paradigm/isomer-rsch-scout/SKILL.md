---
name: isomer-rsch-scout
description: Frame a research task, narrow unknowns, inspect literature or local evidence, and recommend baseline, idea, or blocker routing.
---

# Isomer Research Scout

## Overview

Use this skill when the research frame, metric, benchmark neighborhood, or baseline direction is not clear enough to choose the next Workflow Stage Cursor.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Load required context**. Read `references/isomer-research-contract.md` first and read `references/provenance.md` when source provenance or license context matters.
2. **Select supporting references** from **Reference Routing** when paper triage, literature notes, evaluation contracts, baseline shortlists, or operational guidance matter.
3. **Confirm entry fit** using **Entry Signals**. If the frame is already stable and the next stage is obvious, route directly to baseline, idea, experiment, decision, or finalize.
4. **Reconstruct the current frame from durable state**: Research Topic, task, dataset, split, metric, baseline status, blockers, Findings, Artifacts, and Decision Records.
5. **Identify only unknowns that change the next stage** and classify whether they block baseline work, idea work, both, or only a non-blocking future detail.
6. **Reuse local evidence before broad search**. Query durable Findings and inspect local Artifacts first, then use Literature Provider Binding refs only for the unresolved benchmark, paper, repo, or evaluation neighborhood.
7. **Record the evaluation contract, baseline shortlist, and next route** as durable Artifacts or a Decision Record, then stop when baseline, idea, Gate, Decision Record, or blocker is clear.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user request, then execute the plan.

## Reference Routing

Read first:

- `references/isomer-research-contract.md` for local terminology, truth-source, runtime-boundary, and TBD-surface rules.
- `references/provenance.md` when source provenance or license context matters.

Read references as needed:

- `references/paper-triage-playbook.md` when building the smallest useful paper, repo, or benchmark neighborhood.
- `references/literature-scout-template.md` when external search materially changes the frame and must be recorded.
- `references/evaluation-contract-template.md` when dataset, split, metric, fairness, or useful-improvement thresholds must become durable.
- `references/baseline-shortlist-template.md` when recommending attach, import, reproduce, or reject routes for comparator candidates.
- `references/operational-guidance.md` when memory reuse, bounded search, blocked-state handling, or handoff detail matters.

## Entry Signals

- The research frame, metric, benchmark neighborhood, or baseline direction is too unclear for route selection.
- Local evidence or literature could change whether the next stage is baseline, idea, Gate, Decision Record, or blocker.
- The Operator Agent needs a bounded scout result, not an exhaustive survey.

## Exit Criteria

- The task frame and evaluation contract are recorded.
- A comparator shortlist exists, or the handoff justifies why ideation can proceed without more baseline scouting.
- The next Workflow Stage Cursor, Gate, Decision Record, or blocker is explicit.
- If external search changed the route, the retained references and rejected references are recorded.

## Durable Outputs

- Task frame and evaluation contract Artifact.
- Comparator shortlist or route justification.
- Literature notes only when they change routing.
- Next Workflow Stage Cursor or blocker.
- Optional Decision Record when scout resolves a contested route.

## Guardrails

- Do not turn scouting into an exhaustive survey.
- Stop searching once the next stage is clear.
- Do not ask for routine technical clarification before checking local evidence.
- Do not write long paper summaries that do not change the next stage.
- Search for disconfirming evidence, not only supporting evidence.
- Use Literature Provider Binding refs for paper search and Execution Adapter Command Requests for command or repository inspection surfaces.
