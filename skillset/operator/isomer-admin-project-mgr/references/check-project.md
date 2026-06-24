# Check Project

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root from the user-provided path or current working directory.
2. Run `pixi run isomer-cli --print-json validate` from the Project root, or include `--project <project-root>` when needed.
3. Run `pixi run isomer-cli --print-json doctor` for Project-level diagnostics; include `--topic <topic-id>` when the user asks about one Research Topic.
4. If `.houmao/` exists or Houmao status matters, run the read-only Houmao Project status command from `references/houmao-bootstrap.md`.
5. Report Project validity, Houmao Project overlay status, diagnostics, and the next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the Project root, read-only command boundaries, Houmao status checks, and guardrails, then execute the plan.

## Guardrails

- Keep this subcommand read-only.
- Do not repair config, initialize runtime, or launch agents unless the user explicitly requests that next operation.
- Do not infer Research Topics or Topic Workspaces from unregistered directories.
