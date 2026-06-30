# Optimization Prompt Patterns

Use this reference when an optimize subroutine needs a stable prompt or reasoning contract. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Use a stable skeleton**. Include introduction, task description, prior lessons, previous solution or line, instructions, optional response lead-in, and explicit response format.
2. **Enforce the reasoning contract**. Require what is changing, why current line is limited, how the change addresses the limitation, what stays unchanged, and the next action.
3. **Use plateau pattern when stagnating**. State plateau, forbid trivial same-family tweaks when deeper change is needed, and require a larger representational, architectural, objective, or route shift.
4. **Use fusion pattern when combining lines**. Identify source strengths, explain complementarity, avoid combining everything, and preserve comparison surface.
5. **Use debug pattern when repairing**. Restate error, likely root cause, minimal targeted fix, and original solution intent unless the bug invalidates the design.
6. **Write <PROMPT_CONTRACT> only when it prevents drift**.

## Preferences

- Prefer explicit response formats for ranking, debug, fusion, and code-generation tasks (if free-form answer risks drift, otherwise keep it concise).
- Prefer a keep-unchanged clause whenever comparability matters.
- Prefer prompt contracts that move the frontier or stop stale work (if the prompt only generates activity, otherwise revise it).

## Constraints

- <PROMPT_CONTRACT> must not omit what changes, why it changes, how it helps, keep-unchanged conditions, and next action.
- Plateau prompts must not permit another trivial tweak when route change is required.
- Fusion prompts must not combine unrelated or redundant mechanisms.
- Debug prompts must not turn into new-method prompts.

## Quality Gates

- Skeleton gate: context, prior line, instructions, and response shape are present when needed.
- Reasoning gate: what, why, how, keep-unchanged, and next action are explicit.
- Drift gate: prompt prevents activity without frontier movement.
- Mode gate: plateau, fusion, and debug prompts enforce their route boundaries.
