# Brief Shaping Playbook

Use this reference when a candidate direction is still fuzzy and needs to become a structured, ranking-ready brief. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Clarify before widening**. Resolve the concrete bottleneck, comparability boundary, hard constraint, current incumbent, and baseline or frontier state before generating more variants.
2. **Generate a small differentiated slate**. Produce `2-3` serious approaches by default: one incumbent-deepening refinement, one orthogonal mechanism, and one broader shift candidate when justified.
3. **Compare on one shared surface**. Compare expected upside, comparability safety, implementation surface, mechanism distinctness, failure risk, and why this route is best now.
4. **Recommend exactly one lead brief**. Explain why it is best now, why alternatives are deferred, and what would quickly disconfirm it.
5. **Self-check before promotion**. Verify bottleneck, limitation, why-now, comparability boundary, tradeoff basis, and handoff clarity.
6. **Emit the brief package**. Create <CANDIDATE_BRIEF> or <METHOD_BRIEF> with fields ready for ranking or promotion.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer one clarification question at a time (if durable evidence already answers it, otherwise inspect before asking).
- Prefer mechanism-level distinctness over many renamed variants (if two variants differ only by parameter detail, otherwise keep the sharper one).
- Prefer a slate small enough to rank seriously (if the slate is too close to call, otherwise widen once or narrow further).
- Prefer a compact brief package over a paper draft or engineering spec (if implementation is not yet justified, otherwise keep it branchless).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- Candidate shaping must not jump from intuition directly to branch creation.
- <CANDIDATE_BRIEF> must answer what bottleneck is targeted, why the current line is limited, how the mechanism addresses it, and what must remain unchanged.
- Same-mechanism variants must not be counted as a differentiated slate.
- More than one lead brief must not be promoted without an explicit promotion cap reason.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Serious approach count: number of differentiated serious approaches generated before ranking; closer to the source 2-3 default target is better.
- Shared-comparison coverage: fraction of serious candidates compared on the same bottleneck, mechanism, expected gain, implementation cost, risk, and fast-disconfirmation surface; higher is better.

### Checks

- Ambiguity gate: bottleneck, constraint, comparator boundary, and incumbent are clear enough to shape candidates.
- Diversity gate: serious slate covers distinct mechanism families or explains why it cannot.
- Comparison gate: all serious candidates are judged on one shared surface.
- Recommendation gate: one lead brief, deferred alternatives, and disconfirmation signal are explicit.
- Handoff gate: <CANDIDATE_BRIEF> or <METHOD_BRIEF> can be ranked by another agent without chat context.
