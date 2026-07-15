# Prep Runtime

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root and selected Research Topic.
2. Confirm Workspace Runtime exists or run `init-runtime` first if the user authorizes runtime creation.
3. Run `isomer-cli --print-json project runtime prepare --topic <topic-id>` to record Topic Environment Readiness.
4. Run `isomer-cli --print-json project runtime validate --topic <topic-id> --require-ready-readiness` to check launch-facing readiness.
5. Report readiness status, diagnostics, blockers, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from readiness boundaries, selected topic context, and guardrails, then execute the plan.

## Guardrails

- DO NOT install Pixi environments or repair dependencies implicitly.
- DO NOT launch teams from readiness preparation alone.
- MUST treat failed or blocked readiness as an operator-visible blocker.
