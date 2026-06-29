# Init Project

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the target Project root and optional generated content root from the user's prompt. See `references/project-concepts.md`.
2. Check whether `.isomer-labs/manifest.toml` already exists:
   - If it exists, stop and report that `isomer-cli project init` refuses to overwrite an existing Project.
   - Suggest `cleanup-project` with `isomer-cli project cleanup --part bootstrap --dry-run`.
3. Confirm Houmao bootstrap can use the supported CLI boundary from `references/houmao-bootstrap.md`.
4. Run the supported init command:
   - Use `pixi run isomer-cli project init` from the Project root.
   - Add `--content-dir <content-dir>` when the user selected a custom generated content root.
   - Use `pixi run isomer-cli project --root <project-root> init --content-dir <content-dir>` when operating from another directory with a custom content root.
5. Report the created or selected surfaces:
   - `.isomer-labs/manifest.toml`.
   - Selected generated content root, using `isomer-content/` by default or `<content-dir>/` when supplied.
   - Generated `README.md` and `.gitignore` policy files.
   - Isomer-managed Houmao Project directory `.isomer-labs/`.
   - Isomer-managed Houmao overlay `.isomer-labs/.houmao/`.
   - Diagnostics and next operator action.
6. State Research Topic creation status:
   - The Project has no Research Topic until the user runs `pixi run isomer-cli project topics create <topic-id> --statement "<research topic>"` or a topic-team specialization flow routes through that command.
7. Explain selected content root policy:
   - The selected content root's `README.md` and `.gitignore` are generated policy files.
   - Generated content under the selected root is ignored by default unless the user intentionally tracks selected files.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the Project root, CLI command boundaries, Houmao bootstrap boundary, and guardrails, then execute the plan.

## Guardrails

- Do not create `.isomer-labs/` by hand when `isomer-cli project init` can run.
- Do not treat a failed Houmao bootstrap as a successful Project init.
- Do not run `project runtime init`, `project runtime prepare`, or team launch commands from this subcommand unless the user explicitly asks for a later step.
