# Codegen Route

Use this reference when choosing how implementation work should proceed after a method brief or frontier decision.

## Brief-Only

Use no-code candidate briefs when the direction is underspecified, multiple distinct directions still need ranking, or a new Research Inquiry Relationship should not be promoted yet.

## Stepwise Generation

Prefer stepwise generation for the first substantial implementation of a new durable line, especially when the line touches data processing, model design, training, evaluation, or multiple subsystems.

## Diff or Patch Generation

Prefer a bounded patch when a strong current implementation exists, the change is local enough to preserve most of the line, or the task is improve, exploit, debug, or most fusion work.

## Full Rewrite

Use full rewrite only when the existing implementation is structurally broken, the desired architecture no longer matches the current code shape, or patching would be more fragile than replacement.

## Response Shape

1. short plan
2. bounded implementation surface
3. keep-unchanged contract
4. validation step

## Guardrail

Do not jump from a vague idea directly into a large patch with no intermediate plan.
