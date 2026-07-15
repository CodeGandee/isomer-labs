# Checkpoint Memory Template

Use this when later turns could otherwise resume from the wrong node, route, or blocker. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **State the current route**. Record current route label, current stage or anchor, and short route judgment.
2. **Name the authoritative resume point**. Identify active branch, run, paper node, report pair, or equivalent runtime state and why it is authoritative now.
3. **Preserve node history**. Name predecessor nodes, superseded nodes or routes, and why the current node beat or replaced them.
4. **Record retained result or blocker**. Name the strongest still-valid result or dominant blocker.
5. **Mark do-not-reopen routes**. List experiments, routes, or closure paths that should stay closed unless new evidence appears.
6. **Name next resume step and first-read files**. Record the single best next step plus route-critical files, reports, manifests, or handoffs.
7. **Define reopen condition**. State the exact condition that would justify reopening an older node or switching away.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer one compact checkpoint-style memory card over a long narrative (if the resume point did not change, otherwise skip the memory write).
- Prefer explicit do-not-reopen rules when stale routes caused confusion (if none exist, otherwise omit rather than invent one).
- Prefer first-read artifacts that make the next turn operational immediately.

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- DEEPSCI:DECISION-CHECKPOINT-MEMORY must be written when the decision changes the authoritative resume point.
- The checkpoint must not leave later turns guessing which node, branch, run, or blocker is active.
- Reopen conditions must be concrete enough to prevent accidental churn.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Checkpoint-field coverage: fraction of current route, active node, node history, strongest retained result or blocker, do-not-reopen list, next resume step, first-read files, and reopen condition fields completed; higher is better.
- Reopen-ambiguity count: number of routes, experiments, closure paths, or decisions that lack a clear do-not-reopen or reopen condition; lower is better.

### Checks

- Resume clarity: the next turn can identify the current active node and next step without rereading the entire history.
- History clarity: superseded routes and do-not-reopen items are explicit.
- Evidence clarity: the strongest retained result or blocker is named.
- Reopen clarity: old routes reopen only under stated conditions.
