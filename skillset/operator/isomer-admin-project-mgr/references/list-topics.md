# List Topics

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root from the user-provided path or current working directory.
2. Run `pixi run isomer-cli --print-json topics list` through the selected Project root.
3. Run `pixi run isomer-cli --print-json workspaces list` through the selected Project root.
4. Report registered Research Topic ids, Topic Workspace ids and paths, defaults, diagnostics, and any missing Project blockers.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the Project Manifest-backed topic and workspace listing commands, then execute the plan.

## Guardrails

- Use Project Manifest-backed CLI output as authority.
- Do not treat unregistered files under `.isomer-labs/research-topics/` or directories under `topic-workspaces/` as managed topics.
