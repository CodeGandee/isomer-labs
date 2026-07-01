# Controlled Brainstorming Playbook

Use this reference when the current route is not already obvious and idea work needs a real divergence pass. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Enter only after framing**. Confirm <OBJECTIVE_CONTRACT> and <CURRENT_BOARD_PACKET> are clear enough to guide widening.
2. **Choose the family mix**. Decide whether the pass admits mechanism, objective, measurement, and infrastructure families.
3. **Generate a bounded slate**. Produce six to twelve raw ideas when the space allows, including local refinement, orthogonal alternative, objective or measurement change, and infrastructure route when relevant.
4. **Filter aggressively**. Remove candidates that only improve a surrogate, violate constraints, repeat stale routes, are micro-variants, or lack cheap falsification.
5. **Force why now**. Require each serious candidate to say what changed and why this family deserves attention now.
6. **End with structured candidates**. Carry forward family type, targeted limitation, why now, prior-work overlap, anti-win condition, minimal validation, and abandonment condition.

## Preferences

- Prefer bounded divergence over open-ended brainstorming (if strong evidence already forces one route, otherwise record why widening was abbreviated).
- Prefer a mixed family slate over mechanism-only routes (if objective, measurement, or infrastructure may be the blocker, otherwise include those families).
- Prefer evidence-per-run over novelty theater when choosing the final serious candidates.

## Constraints

- Brainstorming must not start before objective and board grounding.
- The raw slate must not be scored too early.
- The serious frontier must not keep candidates with no cheap falsification path.
- Stale routes must not be reopened without new evidence.

## Quality Gates

### Metrics

- Raw slate size: number of raw ideas generated before aggressive filtering; closer to the 6-12 source target is better.
- Serious frontier size: number of serious candidates retained after collapse; closer to 2-3 is better, and more than 5 is worse.

### Checks

- Framing gate: <OBJECTIVE_CONTRACT> and <CURRENT_BOARD_PACKET> are explicit before widening.
- Diversity gate: the slate contains at least one non-incumbent family when the problem permits.
- Filtering gate: weak surrogate-only, stale, invalid, and unfalsifiable ideas are removed or downgraded.
- Structured-output gate: <CANDIDATE_IDEA_FRONTIER> has enough fields to feed <PRE_IDEA_DRAFT>.
