# Controlled Brainstorming Playbook

Use this reference when the current route is not already obvious and idea work needs a real divergence pass. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Enter only after framing**. Confirm DEEPSCI:OBJECTIVE-CONTRACT and DEEPSCI:CURRENT-BOARD-PACKET are clear enough to guide widening.
2. **Choose the family mix**. Decide whether the pass admits mechanism, objective, measurement, and infrastructure families.
3. **Generate a bounded slate**. Produce six to twelve raw ideas when the space allows, including local refinement, orthogonal alternative, objective or measurement change, and infrastructure route when relevant.
4. **Filter aggressively**. Remove candidates that only improve a surrogate, violate constraints, repeat stale routes, are micro-variants, or lack cheap falsification.
5. **Force why now**. Require each serious candidate to say what changed and why this family deserves attention now.
6. **End with structured candidates**. Carry forward family type, targeted limitation, why now, prior-work overlap, anti-win condition, minimal validation, and abandonment condition.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer bounded divergence over open-ended brainstorming (if strong evidence already forces one route, otherwise record why widening was abbreviated).
- Prefer a mixed family slate over mechanism-only routes (if objective, measurement, or infrastructure may be the blocker, otherwise include those families).
- Prefer evidence-per-run over novelty theater when choosing the final serious candidates.

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- Brainstorming must not start before objective and board grounding.
- The raw slate must not be scored too early.
- The serious frontier must not keep candidates with no cheap falsification path.
- Stale routes must not be reopened without new evidence.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Raw slate size: number of raw ideas generated before aggressive filtering; closer to the 6-12 source target is better.
- Serious frontier size: number of serious candidates retained after collapse; closer to 2-3 is better, and more than 5 is worse.

### Checks

- Framing gate: DEEPSCI:OBJECTIVE-CONTRACT and DEEPSCI:CURRENT-BOARD-PACKET are explicit before widening.
- Diversity gate: the slate contains at least one non-incumbent family when the problem permits.
- Filtering gate: weak surrogate-only, stale, invalid, and unfalsifiable ideas are removed or downgraded.
- Structured-output gate: DEEPSCI:CANDIDATE-IDEA-FRONTIER has enough fields to feed DEEPSCI:PRE-IDEA-DRAFT.
