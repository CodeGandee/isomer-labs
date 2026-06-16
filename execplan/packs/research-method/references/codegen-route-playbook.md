# Codegen Route Playbook

Choose the code-generation route deliberately.

## Use brief-only

Use no-code candidate briefs when:

- the direction is still underspecified
- multiple distinct directions still need ranking
- a new line should not be promoted yet

## Use stepwise generation

Prefer stepwise generation when:

- a new durable line is being implemented for the first time
- the change spans data processing, model design, and training/evaluation
- a modular decomposition will reduce large integrated errors
- a plan -> refine -> implement sequence is safer than one monolithic edit

## Use diff / patch generation

Prefer diff / patch generation when:

- a strong current implementation already exists
- the current change is local enough to preserve most of the line
- the task is improve, exploit, debug, or most fusion work
- the desired change can be described as a bounded delta from the current solution

## Use full rewrite

Use a full rewrite only when:

- the existing implementation is structurally broken
- the desired architecture no longer matches the current codebase shape
- diff patching would be more fragile than replacement

Do not jump to a rewrite merely because one local patch failed.

## Response shape

For non-trivial codegen work, prefer this shape:

1. short plan
2. bounded implementation surface
3. keep-unchanged contract
4. validation step

Do not go from a vague idea directly into a large patch with no intermediate plan.
