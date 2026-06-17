---
name: isomer-rsch-finalize
description: Consolidate final research claims, limitations, recommendations, and closure or handoff state.
---

Use this skill when a Research Thread or Research Task may be ready to stop,
pause, publish, archive, or start a new loop.

Read first:

- `../isomer-rsch-shared/SKILL.md`
- Source analysis: `../../../context/explore/deepscientist-skill-analysis/finalize.md`

## Entry Signals

- A Research Thread or Research Task may be ready to stop, pause, publish,
  archive, or start a new loop.
- Comparator state, accepted runs, analysis outputs, writing outputs, reviews,
  blockers, and Gates are available for closure review.
- The Operator Agent needs a final claim ledger, handoff, or completion Gate.

## Exit Criteria

- Supported, partial, failed, refuted, and open claims are separated.
- Final limitations, caveats, reopen conditions, and remaining risks are
  visible.
- A final Decision Record and any required completion Gate are durable.

## Procedure

1. Gather comparator state, accepted runs, analysis outputs, writing outputs,
   reviews, blockers, Decision Records, and open Gates.
2. Check whether closure is actually justified.
3. Separate supported, partial, failed, refuted, and open claims.
4. Write limitations, caveats, reopen conditions, and remaining risks.
5. Recommend stop, pause, publish, archive, continue, or new loop.
6. Build a handoff packet that supports later resumption.
7. Record the final Decision Record and open a Gate for true completion when
   human approval is needed.

## Durable Outputs

- Final claim ledger or claim-status summary.
- Final report or handoff Artifact.
- Final Decision Record.
- Gate for completion approval when required.

## Guardrails

- Do not finalize from conversation memory alone.
- Do not hide failures or partial support.
- Do not finalize a report or manuscript while coverage, evidence, or language
  checks still block the deliverable.
- Use `[[tbd-surface:schema-gate]]` for unsettled completion Gates.
