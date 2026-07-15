# Research Route Criteria

Use this reference when choosing among candidate branches, idea packages, experiment groups, paper-facing routes, or optimization-frontier actions. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Name the insufficiency**. State what exact problem, blocker, result gap, evidence conflict, or route ambiguity this decision must resolve.
2. **Compress evidence**. Build DEEPSCI:DECISION-EVIDENCE-PACKET with strongest support, strongest contradiction, main risk, main cost, reversibility, and genuinely new evidence.
3. **Compare the serious frontier**. Identify the winner, strongest alternatives, selection criteria, expected learnings, and why rejected options lost.
4. **Apply route-specific gates**. For paper routes, apply publishability and exploration-depth gates; for algorithm-first routes, consult the optimization frontier; for baseline reuse, confirm concrete attachment path.
5. **Check user sensitivity**. Ask the user only when preference, scope, or cost cannot be resolved safely from local evidence.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer durable evidence over vibe, momentum, or optimism.
- Prefer routes that attack a real bottleneck, stay compatible with the existing architecture when possible, produce interpretable evidence, and remain defensible later.
- Prefer careful judgment from durable evidence over launching tie-break runs by reflex.
- Prefer branch or stop when publishability, evidence sufficiency, or reader value has collapsed beyond reasonable narrowing.

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- DEEPSCI:ROUTE-QUESTION must name the real choice before evidence is judged.
- DEEPSCI:DECISION-EVIDENCE-PACKET must name support, contradiction, cost, risk, reversibility, and user-preference sensitivity when relevant.
- Paper routes must not advance to write, review, or finalize without publishability and coverage gates.
- Algorithm-first routes must not override the optimization frontier unless newer durable evidence clearly dominates.
- A blocked state must not be hidden behind a vague continue decision.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Route-criteria coverage: fraction of evidence support, opportunity cost, blocker severity, route reversibility, user preference, and next-action clarity criteria checked for the route choice; higher is better.
- Expected-information-gain gap: number of analysis or experiment launches whose expected information gain is not stated relative to cost; lower is better.

### Checks

- Evidence fit: the chosen route follows the strongest durable evidence, not inertia.
- Tradeoff visibility: novelty, feasibility, verification cost, architecture fit, immediate progress, and long-term research value are named when relevant.
- Alternative quality: rejected alternatives are visible and rejected for stated criteria.
- User-sensitivity quality: user input is requested only for real preference, scope, or cost choices.
