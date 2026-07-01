# Candidate Ranking Template

Use this reference when several serious briefs or implementation candidates need one promotion-ready ranking. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Define the candidate set**. List candidate ids, ranking scope, current frontier context, and shared comparison surface.
2. **Score on shared criteria**. Compare expected information gain, feasibility, comparator fit, implementation surface, novelty, distinctiveness, overlap risk, incumbent improvement, mechanism-family diversity, and change-layer diversity.
3. **Rank explicitly**. For each candidate, state score summary, why it ranks there, and promote, hold, fuse, debug, reject, or archive action.
4. **Justify the winner**. Explain why the selected candidate should become a durable line or active attempt now.
5. **Explain non-winners**. State why alternatives are deferred, fused, rejected, or held rather than erased.
6. **Apply promotion cap**. State how many candidates should be promoted now and why more promotion would dilute the frontier.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer one shared scoring surface over candidate-specific stories (if criteria differ, otherwise explain why).
- Prefer each mechanism family contributing at most one promoted line (if overriding the cap, otherwise justify dominance).
- Prefer returning to brief shaping when top candidates are all same-family (if one clearly dominates, otherwise promote only that one).
- Prefer promotion-ready output over vague enthusiasm (if no winner is ready, otherwise route to brief or stop).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- <CANDIDATE_RANKING> must state candidate set, criteria, ranked candidates, winner, non-winner handling, and promotion cap.
- "All promising" must not justify promoting everything.
- Ranking must not ignore family diversity and change-layer diversity.
- Promotion must not exceed the cap without a stated reason.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Ranked candidate count: number of serious candidates given a score summary and promote, hold, or reject verdict; higher is better until the serious frontier is fully ranked.
- Promotion dilution count: number of extra promotions that would dilute the frontier without a clear reason; lower is better.

### Checks

- Set gate: candidates and ranking scope are explicit.
- Criteria gate: comparison uses one shared surface.
- Diversity gate: family and change-layer collapse are checked.
- Winner gate: selected candidate and why-now reason are explicit.
- Non-winner gate: alternatives have hold, fuse, reject, or archive rationale.
- Promotion gate: cap is stated and respected.
