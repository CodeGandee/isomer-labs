# Init Project

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the target Project root and optional generated content root from the user's prompt. See `references/project-concepts.md`.
2. Check whether `.isomer-labs/manifest.toml` already exists:
   - If it exists, stop and report that `isomer-cli project init` refuses to overwrite an existing Project.
   - Suggest `cleanup-project` with `isomer-cli project cleanup --part bootstrap --dry-run`.
3. Confirm Houmao bootstrap can use the supported CLI boundary from `references/houmao-bootstrap.md`.
4. Run the supported init command:
   - Use `isomer-cli project init` from the Project root.
   - Add `--content-dir <content-dir>` when the user selected a custom generated content root.
   - Use `isomer-cli project --root <project-root> init --content-dir <content-dir>` when operating from another directory with a custom content root.
5. Report the created or selected surfaces:
   - `.isomer-labs/manifest.toml`.
   - Selected generated content root, using `isomer-content/` by default or `<content-dir>/` when supplied.
   - Generated `README.md` and `.gitignore` policy files.
   - Isomer-managed Houmao Project directory `.isomer-labs/`.
   - Isomer-managed Houmao overlay `.isomer-labs/.houmao/`.
   - Diagnostics and next operator action.
6. Unless the user explicitly opts out of detected-extension registration, delegate `isomer-op-system-skill-mgr reconcile-extensions` after Project initialization succeeds:
   - Let that owner trust Project declarations, inspect only agent-known project roots, then classify the current host's live inventory.
   - Let it remember complete usable receipt-backed or live-inventory extensions additively.
   - If reconciliation fails, preserve the successful Project result, report extension reconciliation as a distinct partial outcome, and offer `isomer-op-system-skill-mgr reconcile-extensions` as the retry route.
   - If the user opts out, skip registration and optionally delegate `detect-extensions` for read-only observations.
7. State Research Topic creation status:
   - The Project has no Research Topic until the user runs `isomer-cli project topics create <topic-id> --statement "<research topic>"` or a topic-team specialization flow routes through that command.
8. Explain selected content root policy:
   - The selected content root's `README.md` and `.gitignore` are generated policy files.
   - Generated content under the selected root is ignored by default unless the user intentionally tracks selected files.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the Project root, CLI command boundaries, Houmao bootstrap boundary, and guardrails, then execute the plan.

## Operational Notes

- Those are separate operator-skill actions.

## Guardrails

- DO NOT create `.isomer-labs/` by hand when `isomer-cli project init` can run.
- DO NOT treat a failed Houmao bootstrap as a successful Project init.
- DO NOT run `project runtime init`, `project runtime prepare`, or team launch commands from this subcommand unless the user explicitly asks for a later step.
- DO NOT imply that direct `isomer-cli project init` performs agent-host discovery or extension registration.
