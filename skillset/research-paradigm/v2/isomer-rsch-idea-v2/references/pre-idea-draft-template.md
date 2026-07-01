# Pre-Idea Draft Template

Use this reference after bounded brainstorming and before formal idea submission. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Choose serious candidates only**. Write <PRE_IDEA_DRAFT> for the top one to three candidates after raw slate filtering, not for every raw idea.
2. **Fill the required fields**. Include candidate id, family, one-sentence claim, targeted bottleneck, why now, novelty type, closest prior work, assumptions, outside-family alternative, rejection case, hypothesis, falsification path, minimal experiment, abandonment condition, and verdict.
3. **Expose hidden assumptions**. State which assumptions about data, objective, evaluator, system boundary, or mechanism must hold.
4. **Check local-optimum lock-in**. Ask whether the candidate looks best because it is familiar, cheap, or already half-built.
5. **Write the rejection case**. State the strongest reason to reject now and which alternative evidence would beat it.
6. **Record a verdict**. Promote, defer, or reject with a reason before selection.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer updating the same durable draft when a candidate survives revisions (if the candidate changes meaningfully, otherwise preserve lineage rather than scattering drafts).
- Prefer a compact challenge memo over long persuasive prose (if the route is still unclear, otherwise clarify before promotion).
- Prefer outside-family or assumption-reversal alternatives in the draft (if no plausible outside-family route exists, otherwise record why).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- A candidate must not become <SELECTED_HYPOTHESIS> without <PRE_IDEA_DRAFT> or equivalent challenge memo.
- <PRE_IDEA_DRAFT> must surface hidden assumptions, local-optimum risk, strongest rejection case, and cheapest falsification path.
- Weak candidates must be filtered before draft effort rather than documented for paperwork.
- The draft must compare the likely winner against the incumbent and at least one outside-family or assumption-reversal alternative when available.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Candidate focus count: number of top candidates maintained in the pre-idea draft set; closer to 1-3 is better.
- Challenge-question coverage: fraction of the nine required candidate challenge questions answered explicitly; higher is better.

### Checks

- Assumption gate: the most fragile assumptions are explicit.
- Rejection gate: the draft states why the candidate might be wrong now.
- Falsification gate: the minimal experiment and abandonment condition are concrete.
- Promotion gate: the route looks stronger than the incumbent continuation, easiest small tweak, and at least one serious alternative.
