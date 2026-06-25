# List Topics

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root from the user-provided path or current working directory.
2. Run `pixi run isomer-cli --print-json project topics list` through the selected Project root.
3. Run `pixi run isomer-cli --print-json project workspaces list` through the selected Project root.
4. If the user asks to inspect one topic, run `pixi run isomer-cli --print-json project topics show <topic-id>`.
5. If the user asks how to mutate topic lifecycle state, report the authoritative surfaces: `project topics create <topic-id> --statement "<research topic>"`, `project topics update <topic-id>`, `project topics delete <topic-id> --dry-run`, and `project topics delete <topic-id> --yes` after reviewed dry-run output.
6. Report registered Research Topic ids, Topic Workspace ids and paths, defaults, diagnostics, and any missing Project blockers.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the Project Manifest-backed topic and workspace listing commands, then execute the plan.

## Guardrails

- Use Project Manifest-backed CLI output as authority.
- Start Research Topic deletion with `isomer-cli project topics delete <topic-id> --dry-run`; use `--yes` only after the user reviews the plan.
- Do not treat unregistered files under `.isomer-labs/research-topics/` or directories under a Topic Workspace base such as `isomer-content/topic-ws/` as managed topics.
