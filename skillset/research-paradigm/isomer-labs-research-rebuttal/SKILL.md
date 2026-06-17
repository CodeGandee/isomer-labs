---
name: isomer-labs-research-rebuttal
description: Map reviewer feedback into evidence actions, manuscript deltas, and durable rebuttal or revision responses.
---

Use this skill when reviewer or external critique material must become
structured response work, evidence updates, manuscript changes, or final
revision handoff.

Read first:

- `../isomer-labs-research-shared/SKILL.md`
- Source analysis: `../../../context/explore/deepscientist-skill-analysis/rebuttal.md`

## Entry Signals

- Reviewer or external critique material needs structured response work.
- The response may require evidence updates, manuscript deltas, claim
  downgrades, limitation wording, literature positioning, or comparator work.
- A revision package or point-by-point response must remain source-faithful.

## Exit Criteria

- Reviewer items are normalized into a durable matrix with ids, severity,
  affected claims, routes, and status.
- Evidence updates, text deltas, and response material are linked to the matrix.
- Feasible reviewer-critical rows are resolved or explicitly routed.

## Procedure

1. Normalize reviewer material into source-faithful atomic items.
2. Assign stable item ids, severity, class, affected claim, evidence anchor,
   route, and status.
3. Decide whether each item needs explanation, evidence repackaging, new
   analysis, claim downgrade, limitation, literature positioning, comparator
   work, or manuscript rewrite.
4. Route literature issues to scout, comparator gaps to baseline, new evidence
   to analysis, and text changes to write.
5. Refresh the rebuttal matrix after each routed fix.
6. Assemble point-by-point response, evidence update, text deltas, and final
   revision handoff.

## Durable Outputs

- Reviewer item matrix.
- Action plan.
- Evidence update Artifact.
- Text delta Artifact.
- Response letter or revision package.

## Guardrails

- Do not launch free-floating ablations.
- Do not rewrite reviewer meaning during normalization.
- Do not pretend limitations are solved when they are only reframed.
- Do not finalize while reviewer-critical feasible rows remain unresolved.
