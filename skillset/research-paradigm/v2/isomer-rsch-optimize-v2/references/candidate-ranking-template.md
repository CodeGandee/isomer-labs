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

- Prefer one shared scoring surface over candidate-specific stories (if criteria differ, otherwise explain why).
- Prefer each mechanism family contributing at most one promoted line (if overriding the cap, otherwise justify dominance).
- Prefer returning to brief shaping when top candidates are all same-family (if one clearly dominates, otherwise promote only that one).
- Prefer promotion-ready output over vague enthusiasm (if no winner is ready, otherwise route to brief or stop).

## Constraints

- <CANDIDATE_RANKING> must state candidate set, criteria, ranked candidates, winner, non-winner handling, and promotion cap.
- "All promising" must not justify promoting everything.
- Ranking must not ignore family diversity and change-layer diversity.
- Promotion must not exceed the cap without a stated reason.

## Quality Gates

- Set gate: candidates and ranking scope are explicit.
- Criteria gate: comparison uses one shared surface.
- Diversity gate: family and change-layer collapse are checked.
- Winner gate: selected candidate and why-now reason are explicit.
- Non-winner gate: alternatives have hold, fuse, reject, or archive rationale.
- Promotion gate: cap is stated and respected.
