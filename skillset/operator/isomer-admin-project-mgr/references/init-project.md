# Init Project

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the target Project root and optional Research Topic id or topic statement from the user's prompt. See `references/project-concepts.md`.
2. Check whether `.isomer-labs/manifest.toml` already exists; if it does, stop and report that `isomer-cli init` refuses to overwrite an existing Project.
3. Confirm Houmao bootstrap can use the supported CLI boundary from `references/houmao-bootstrap.md`.
4. Run `pixi run isomer-cli init <topic-id> --topic-statement "<topic statement>"` from the Project root, or use `pixi run isomer-cli --project <project-root> init <topic-id> --topic-statement "<topic statement>"` when operating from another directory.
5. Report `.isomer-labs/manifest.toml`, `.isomer-labs/research-topics/<topic-id>.toml`, `topic-workspaces/<topic-id>/`, `.houmao/`, diagnostics, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the Project root, CLI command boundaries, Houmao bootstrap boundary, and guardrails, then execute the plan.

## Guardrails

- Do not create `.isomer-labs/` by hand when `isomer-cli init` can run.
- Do not treat a failed Houmao bootstrap as a successful Project init.
- Do not run `runtime init`, `runtime prepare`, or team launch commands from this subcommand unless the user explicitly asks for a later step.
