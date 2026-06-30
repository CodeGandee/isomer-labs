# Codegen Route Playbook

Use this reference to choose the code-generation route deliberately instead of using the same implementation shape for every optimization step. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Check whether code is justified**. Use brief-only when the direction is underspecified, multiple distinct directions still need ranking, or a new line should not be promoted yet.
2. **Choose stepwise generation for first substantial implementations**. Use it when a new durable line touches multiple subsystems and plan-refine-implement reduces integrated errors.
3. **Choose diff or patch generation for bounded deltas**. Use it when a strong current implementation exists and the desired change preserves most of the line.
4. **Choose full rewrite only for structural mismatch**. Use it when the current implementation is too broken or mismatched for safe patching.
5. **Write <CODEGEN_ROUTE_PLAN>**. Include short plan, bounded implementation surface, keep-unchanged contract, and validation step.

## Preferences

- Prefer brief-only before code when ranking is unresolved (if a durable line is selected, otherwise move to implementation planning).
- Prefer stepwise generation for broad first implementations (if the change is local, otherwise use patch generation).
- Prefer diff or patch for improve, exploit, debug, and most fusion work (if current structure is usable, otherwise avoid rewrites).
- Prefer full rewrite only after structural evidence (if one local patch failed, otherwise do not rewrite by reflex).

## Constraints

- <CODEGEN_ROUTE_PLAN> must name what stays unchanged for comparability.
- Large patches should not begin from a vague idea with no implementation surface.
- Debug route must not use full rewrite unless the existing implementation is structurally broken.
- Fusion route must preserve the comparison surface unless the route explicitly changes it.

## Quality Gates

- Route gate: brief-only, stepwise, patch, or rewrite route is justified.
- Scope gate: implementation surface is bounded.
- Stability gate: keep-unchanged contract is explicit.
- Validation gate: the first check after implementation is named.
