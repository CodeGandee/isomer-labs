---
name: isomer-labs-research-intake
description: Audit and reconcile an existing research state before choosing the next Isomer Labs research-stage handoff.
---

Use this skill when a Research Thread or Research Task already has drafts,
baselines, runs, reviews, files, or user-provided state and the next Workflow
Stage is not trustworthy yet.

Read first:

- `../isomer-labs-research-shared/SKILL.md`
- Source analysis: `../../../context/explore/deepscientist-skill-analysis/intake-audit.md`

## Entry Signals

- The Research Thread or Research Task already has drafts, baselines, runs,
  reviews, files, or user-provided state.
- The current board is stale, conflicting, incomplete, or not trustworthy
  enough for a stage transition.
- The Operator Agent needs a recommended next Workflow Stage, Gate, Decision
  Record, or blocker.

## Exit Criteria

- A trust-ranked current-board packet exists as a durable Artifact.
- Conflicts, stale assets, blockers, and missing evidence are visible.
- The handoff names the recommended next Workflow Stage, Gate, Decision
  Record, or blocker.

## Procedure

1. Read the current Research Goal, latest Operator Agent instruction, active
   Research Task, and known status.
2. Query durable Findings or prior context before inspecting files.
3. Inventory only decision-relevant Artifacts: baseline evidence, main runs,
   analysis outputs, writing outputs, review material, and provenance.
4. Trust-rank each asset as accepted, stale, conflicting, reference-only, or
   insufficiently evidenced.
5. Reconcile valid assets into Artifacts, Evidence Items, Findings, Decision
   Records, or Research Claims.
6. Build one current-board packet with the mainline, trusted evidence,
   blockers, stale routes, and recommended next Workflow Stage.

## Durable Outputs

- State audit Artifact.
- Current-board packet Artifact.
- Recommended next Workflow Stage, Gate, Decision Record, or blocker.
- Repair notes for missing or conflicting durable evidence.

## Guardrails

- Do not trust conversation memory over durable state.
- Do not invent a cleaned-up history when evidence conflicts.
- Do not inspect the whole repository when a smaller evidence set answers the
  routing issue.
- Use `[[tbd-surface:api-execution-command]]` for any unsettled command surface.
