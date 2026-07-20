# Step-by-Step

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Establish the same main workflow order as `fast-forward`: `ensure-project`, `resolve-topic-input`, `register-topic`, `create-research-intent`, `init-runtime`, `define-topic-env`, `setup-topic-env`, `define-actors`, `setup-actors`, and `finalize`.
2. Before each step, print a pre-step preview with the step name, planned action, inputs to read, artifacts or semantic labels that may be written or updated, whether the step may mutate state, and blockers that can stop the step.
3. If the step has multiple valid choices, unresolved decisions, or open questions, show a Markdown option table with option IDs such as `A`, `B`, and `C`.
4. In each option row, include what the option means, pros, cons, related open questions, whether it is recommended, and the recommendation rationale.
5. Wait for explicit user acknowledgement or an option selection before running the step. A no-choice step still requires acknowledgement; do not invent artificial choices just to show a table.
6. If the user declines acknowledgement, asks to pause, or chooses a different path, stop or update the planned stage according to the user's instruction. Do not continue mutating later stages under the old plan.
7. Reuse ready stages and stop at blockers using the same readiness rules as `fast-forward`.
8. When every predecessor stage is ready, skipped by explicit scope, or completed, preview `finalize`, wait for acknowledgement, run it, and print its ready/verified/blocked report.

If the user's task does not map cleanly to these steps, show the closest planned step, the unresolved question, and a short option table when choices exist.

## Option Table Template

Use this table shape whenever choices affect execution.

| Option | What It Does | Pros | Cons | Open Questions | Recommendation |
| --- | --- | --- | --- | --- | --- |
| A | <choice> | <benefits> | <tradeoffs> | <questions> | Recommended if <reason>. |
| B | <choice> | <benefits> | <tradeoffs> | <questions> | Use if <condition>. |

## Operational Contract

- Keep `step-by-step` aligned with `fast-forward`; interaction changes, but stage order and readiness rules do not.

## Operational Notes

- Report ready, verified, skipped, blocked, and the summary path.

## Guardrails

- DO NOT mutate Project, Topic Workspace, runtime, repository, actor, actor onboarding, or summary state before the user acknowledges the current step preview or selects an option that authorizes proceeding.
- DO NOT route to a next research command after `finalize`.
