# Operational Guidance

Use this reference when the decision route needs longer tactical notes than the entrypoint. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Use planning files only as state**. Read planning or status files as evidence, but do not open a new planning loop when the real need is a route judgment.
2. **Choose the smallest action**. Keep runtime-specific branch or artifact details out of the default payload unless they matter now.
3. **Handle baseline reuse concretely**. When the judgment lands on baseline reuse or attachment, leave a concrete attach or confirm path, blocker, or waiver.
4. **Select among packages explicitly**. When multiple candidates exist, record candidates, criteria, winner, and why alternatives lost.
5. **Apply paper-route checks**. Judge method fidelity, evidence support, story coherence, exploration depth, publishability, and stop-loss conditions before write, review, or finalize.
6. **Ask the user only for real choices**. Use <USER_DECISION_REQUEST> when preference, scope, or cost cannot be derived locally.
7. **Write checkpoint memory when needed**. Create <DECISION_CHECKPOINT_MEMORY> when the authoritative resume point changes.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer route judgment over another planning loop (if active state is too ambiguous, otherwise route to intake or scout-style reconciliation).
- Prefer artifact, evidence, and Workspace Runtime state over chat-only recollection.
- Prefer a narrow user decision request with one to three concrete options when user choice is genuinely required.
- Prefer checkpoint memory only when the decision created a reusable lesson or changed the authoritative resume point.

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- Decision must not bypass tool or evidence contracts just to reach a faster route.
- Baseline reuse must not be implied resolved unless the concrete attachment and confirmation path is clear.
- Candidate package selection must not omit criteria, winner, and rejected alternatives.
- User requests must not be used for routine ambiguity that local evidence can resolve.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- User-option count: number of concrete options presented in a necessary user decision request; closer to the source 1-3 option target is better.
- Repeated-decision count: number of repeated route decisions made without new evidence; lower is better.

### Checks

- Tactical fit: the decision changes the route once instead of re-explaining the same state.
- Baseline fit: reuse, attach, or publish decisions leave a concrete next path or blocker.
- Package-selection fit: candidate decisions name the winner and why alternatives lost.
- User-request fit: <USER_DECISION_REQUEST> is used only for genuine preference, scope, or cost choices.
