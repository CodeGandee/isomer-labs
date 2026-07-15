# Codegen Route Playbook

Use this reference to choose the code-generation route deliberately instead of using the same implementation shape for every optimization step. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Check whether code is justified**. Use brief-only when the direction is underspecified, multiple distinct directions still need ranking, or a new line should not be promoted yet.
2. **Choose stepwise generation for first substantial implementations**. Use it when a new durable line touches multiple subsystems and plan-refine-implement reduces integrated errors.
3. **Choose diff or patch generation for bounded deltas**. Use it when a strong current implementation exists and the desired change preserves most of the line.
4. **Choose full rewrite only for structural mismatch**. Use it when the current implementation is too broken or mismatched for safe patching.
5. **Write DEEPSCI:CODEGEN-ROUTE-PLAN**. Include short plan, bounded implementation surface, keep-unchanged contract, and validation step.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer brief-only before code when ranking is unresolved (if a durable line is selected, otherwise move to implementation planning).
- Prefer stepwise generation for broad first implementations (if the change is local, otherwise use patch generation).
- Prefer diff or patch for improve, exploit, debug, and most fusion work (if current structure is usable, otherwise avoid rewrites).
- Prefer full rewrite only after structural evidence (if one local patch failed, otherwise do not rewrite by reflex).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- DEEPSCI:CODEGEN-ROUTE-PLAN must name what stays unchanged for comparability.
- Large patches should not begin from a vague idea with no implementation surface.
- Debug route must not use full rewrite unless the existing implementation is structurally broken.
- Fusion route must preserve the comparison surface unless the route explicitly changes it.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Codegen-plan coverage: fraction of short plan, bounded implementation surface, keep-unchanged contract, and validation step fields completed before code generation; higher is better.
- Comparability-risk count: number of generated-code changes without an explicit keep-unchanged condition when comparability matters; lower is better.

### Checks

- Route gate: brief-only, stepwise, patch, or rewrite route is justified.
- Scope gate: implementation surface is bounded.
- Stability gate: keep-unchanged contract is explicit.
- Validation gate: the first check after implementation is named.
