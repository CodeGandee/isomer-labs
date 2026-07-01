# Init Runtime

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root and selected Research Topic or Topic Workspace.
2. Run `isomer-cli --print-json project context show --topic <topic-id>` first when the selected topic is unclear.
3. Run `isomer-cli --print-json project runtime init --topic <topic-id>` once the target topic is explicit.
4. Report Workspace Runtime database path, initialized or reopened status, created runtime directories, diagnostics, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from runtime boundaries, selected topic context, and guardrails, then execute the plan.

## Guardrails

- `project runtime init` is the explicit boundary for `state.sqlite` and default runtime directories.
- Do not run `project runtime prepare` or team launch work unless the user asks for those later steps.
