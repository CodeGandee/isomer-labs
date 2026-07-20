# Brief Shaping Playbook

Use this reference when a candidate direction is still fuzzy and needs to become a structured, ranking-ready brief.

This playbook borrows the useful part of product-style brainstorming without importing a full software-spec workflow.
The goal is not a long design document.
The goal is a compact candidate brief that is clear enough to compare, rank, and either submit as `submission_mode='candidate'` or reject.

## 1. Clarify before widening

Before generating more variants, resolve the minimum ambiguity around:

- the concrete bottleneck
- the evaluation or comparability boundary
- the main hard constraint: data, metric, compute, latency, memory, interface, or training budget
- the current incumbent or baseline that this brief must beat or complement

If one unknown would materially change every candidate, clarify it first instead of generating a noisy slate.
Prefer one question at a time when clarification is genuinely needed.
If the answer is already available from durable state, use that instead of asking.

## 2. Generate a small differentiated slate

Default target: `2-3` serious approaches.

The slate should usually include:

- one incumbent-deepening refinement
- one orthogonal mechanism
- one broader shift candidate when justified

Do not produce several renamed variants of the same mechanism family.
If two variants differ only by parameter choice or patch detail, keep only the sharper one.

For each candidate, write:

- bottleneck
- why_current_line_is_limited
- mechanism
- why_now
- keep_unchanged
- expected_gain
- main_risks

## 3. Compare on one shared surface

Before recommending a winner, compare the serious candidates on the same dimensions:

- expected upside
- comparability safety
- implementation surface
- mechanism distinctness
- failure risk
- reason this route is better now than the nearby alternatives

Do not let each candidate justify itself with a different scoring story.
Use one comparison surface so ranking is auditable.

## 4. Recommend exactly one lead brief

After comparison, recommend one lead brief and explain:

- why it is the best next move now
- why the main alternatives are deferred instead of promoted
- what evidence would quickly disconfirm the lead brief

Do not say “all are promising” and promote everything.
If the slate is still too close to call, return to widening once or narrow the slate further.

## 5. Self-check before submission

Before calling `artifact.submit_idea(..., submission_mode='candidate', ...)`, check:

- Is the bottleneck concrete rather than generic?
- Does `why_current_line_is_limited` explain a real gap instead of restating the mechanism?
- Does `why_now` explain what changed in evidence, failure pattern, or frontier state?
- Is the comparability boundary explicit?
- Is the recommendation based on tradeoffs rather than implementation convenience?
- Would the brief still make sense if handed to another agent with no chat context?

If any answer is no, refine the brief before submission.

## 6. Output shape

A good final brief package is short and structured:

1. brief title
2. one-paragraph bottleneck and constraint summary
3. a `2-3` candidate comparison table or bullet slate
4. recommended brief with tradeoff summary
5. self-check outcome
6. fields ready for the method brief template

Keep it compact.
This is a shaping pass for optimization candidates, not a paper draft or engineering spec.
