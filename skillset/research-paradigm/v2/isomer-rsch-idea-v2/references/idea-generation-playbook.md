# Idea Generation Playbook

Use this reference when the idea stage needs a concrete creation flow for producing a new idea slate. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Confirm literature readiness**. Do not start serious ideation until <LITERATURE_SURVEY_REPORT> and closest-prior-work coverage are sufficient or explicitly reused.
2. **Write one limitation card**. Capture observed symptom, condition, metric or claim importance, and strongest evidence.
3. **Split the limitation**. Separate symptom, mechanism hypothesis, and consequence, then preserve competing hypotheses.
4. **Name the lever bucket**. Choose the primary data, model, objective, optimization, inference, evaluation, or infrastructure lever.
5. **Generate direction families**. Produce <RAW_IDEA_SLATE> with six to twelve raw ideas when the space is not tiny, then collapse to <CANDIDATE_IDEA_FRONTIER> with two or three serious candidates and at most five.
6. **Record selected, deferred, and rejected buckets**. Create <REJECTED_AND_DEFERRED_IDEAS> with durable reasons for why each non-selected route is not first.
7. **Prepare challenge drafts**. Send serious surviving candidates into `references/pre-idea-draft-template.md` before final promotion.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer direction families over within-family micro-variants (if the mechanism family is already chosen, otherwise route within-family shaping to optimize).
- Prefer candidates that can change the capability boundary, claim boundary, or evidence value (if a small local tweak survives, otherwise state why broader routes failed).
- Prefer durable rejected and deferred rationale over chat-only brainstorming notes (if a route remains plausible, otherwise mark why it is deferred).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- Serious ideation must not begin before a real literature pass or a recorded reuse justification.
- <RAW_IDEA_SLATE> must not be only renamed variants of one mechanism family.
- <CANDIDATE_IDEA_FRONTIER> must keep candidates as compact decision packages, not slogans.
- <REJECTED_AND_DEFERRED_IDEAS> must preserve enough rationale to prevent later rediscovery.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Competing hypothesis count: number of competing hypotheses kept alive near the top of the idea pass; closer to 2-3 is better.
- Literature coverage layer count: number of required literature layers completed across direct-field frontier, strongest nearby prior work, and adjacent-domain mechanism pass when relevant; higher is better.

### Checks

- Literature gate: serious generation follows survey coverage and closest-prior-work checks.
- Diversity gate: the frontier contains meaningfully different route families or records why it cannot.
- Decision-package gate: each serious candidate includes limitation, mechanism, why now, prior-work overlap, evidence burden, falsification path, and research value.
- Outcome gate: selected, deferred, and rejected buckets are durable.
