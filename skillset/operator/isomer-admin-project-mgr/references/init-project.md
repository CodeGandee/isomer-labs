# Init Project

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the target Project root, optional Research Topic id, optional topic statement, and optional generated content root from the user's prompt. See `references/project-concepts.md`.
2. Check whether `.isomer-labs/manifest.toml` already exists; if it does, stop and report that `isomer-cli project init` refuses to overwrite an existing Project, then suggest `cleanup-project` with `isomer-cli project cleanup --part bootstrap --dry-run`.
3. Confirm Houmao bootstrap can use the supported CLI boundary from `references/houmao-bootstrap.md`.
4. Run `pixi run isomer-cli project init <topic-id> --topic-statement "<topic statement>"` from the Project root, adding `--content-dir <content-dir>` when the user selected a custom generated content root, or use `pixi run isomer-cli project --root <project-root> init <topic-id> --topic-statement "<topic statement>" --content-dir <content-dir>` when operating from another directory with a custom content root.
5. Report `.isomer-labs/manifest.toml`, `.isomer-labs/research-topics/<topic-id>.toml`, the selected generated content root (`isomer-content/` by default or `<content-dir>/` when supplied), the first Topic Workspace (`isomer-content/topic-ws/<topic-id>/` by default or `<content-dir>/topic-ws/<topic-id>/` when supplied), the Isomer-managed Houmao Project directory `.isomer-labs/`, the Isomer-managed Houmao overlay `.isomer-labs/.houmao/`, diagnostics, and next operator action.
6. Explain that the selected content root's `README.md` and `.gitignore` are generated policy files, and that generated content under the selected root is ignored by default unless the user intentionally tracks selected files.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the Project root, CLI command boundaries, Houmao bootstrap boundary, and guardrails, then execute the plan.

## Guardrails

- Do not create `.isomer-labs/` by hand when `isomer-cli project init` can run.
- Do not treat a failed Houmao bootstrap as a successful Project init.
- Do not run `project runtime init`, `project runtime prepare`, or team launch commands from this subcommand unless the user explicitly asks for a later step.
