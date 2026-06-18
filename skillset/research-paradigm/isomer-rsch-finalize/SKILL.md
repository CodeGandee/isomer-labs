---
name: isomer-rsch-finalize
description: Consolidate final research claims, limitations, recommendations, and closure or handoff state.
---

# Isomer Research Finalize

## Overview

Use this skill when a Research Inquiry or Research Task may be ready to stop, pause, publish, archive, or start a new loop.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Load required context**. Read `references/isomer-research-contract.md` first and read `references/provenance.md` when source provenance or license context matters.
2. **Select supporting references** from **Reference Routing** when closure checklist, claim ledger, package inventory, resume packet, or Gate detail matters.
3. **Confirm finalize fit** using **Entry Signals** and **Closure Gate**. If major evidence, writing, review, or package gaps remain, route through decision instead of forcing closure.
4. **Gather the accepted evidence and package inventory** from baselines, Runs, analysis outputs, writing outputs, reviews, blockers, Decision Records, Gates, and Provenance Records.
5. **Build the final claim ledger** by separating supported, partial, failed, refuted, deferred, and open claims with evidence and caveats.
6. **Write limitations, caveats, reopen conditions, and recommendation** for stop, pause, publish, archive, continue, reset, or new loop.
7. **Create the final handoff** with final report or summary Artifact, final Decision Record, completion Gate when required, and resume packet when later continuation is plausible.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user request, then execute the plan.

## Reference Routing

Read first:

- `references/isomer-research-contract.md` for local terminology, truth-source, runtime-boundary, and TBD-surface rules.
- `references/provenance.md` when source provenance or license context matters.

Read references as needed:

- `references/finalization-checklist.md` before closing, pausing, archiving, publishing, or handing off.
- `references/claim-ledger.md` when classifying final claim status and belief changes.
- `references/package-inventory.md` when code, experiment, analysis, report, paper, review, or release outputs must be checked.
- `references/resume-packet.md` when the Research Inquiry may continue later.
- `references/closure-gate-guidance.md` when deciding whether to stop, park, publish, archive, continue, or run Gate Policy preflight for Operator Agent approval.

## Entry Signals

- A Research Inquiry or Research Task may be ready to stop, pause, publish, archive, or start a new loop.
- Comparator state, accepted Runs, analysis outputs, writing outputs, reviews, blockers, and Gates are available for closure review.
- The Operator Agent needs a final claim ledger, handoff, or completion Gate.

## Exit Criteria

- Supported, partial, failed, refuted, and open claims are separated.
- Final limitations, caveats, reopen conditions, and remaining risks are visible.
- A final Decision Record and any required completion Gate are durable.
- Package inventory and resume state are clear enough for later resumption or publication handoff.

## Durable Outputs

- Final claim ledger or claim-status summary.
- Final report or handoff Artifact.
- Final Decision Record.
- Gate for completion approval when required.
- Resume packet or closure handoff when later continuation is plausible.

## Guardrails

- Do not finalize from conversation memory alone.
- Do not hide failures or partial support.
- Do not finalize a report or manuscript while coverage, evidence, review, proofing, or language checks still block the deliverable.
- Do not claim completion without showing what is supported, what failed, what remains open, and what would justify reopening.
- Do not drop the package inventory needed for resumption, review, publication, or archive.
- Use the accepted Gate fields for completion Gates.
