# Env Update Packages

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, Pixi manifest, Pixi environment, and semantic paths through `storage-resolve`.
2. Load the update request from the prompt or a named Markdown, YAML, JSON, TOML, requirements-style, or copied blocker file.
3. Infer requested package updates, downgrades, constraints, purpose, requester skill, package ecosystem, and desired verification checks.
4. Plan a Pixi-scoped update route for each package, avoiding broad environment upgrades unless the user explicitly asks for them.
5. Check current package availability and version evidence through the selected Topic Workspace Pixi environment.
6. Mutate only after clear operator intent, using Pixi-bound commands for the selected Topic Workspace manifest and environment.
7. Verify relevant imports, R libraries, CLI tools, document builds, figures, PPTX generation, or task-specific smoke checks after mutation.
8. Report updated, already-current, skipped, failed, and blocked packages with commands, changed files, verification evidence, blockers, and next action.

If the user's task does not map cleanly to these steps, build an inspect-only update plan and ask for the missing package names, version constraints, or mutation approval.

## Output

Report `status`, `topic`, `pixi`, `request`, `plan`, `commands_run`, `verification`, `changed_paths`, blockers, and `next_action`.

## Guardrails

Do not create local `venv`, `.venv`, or `virtualenv` environments, run ambient `pip`, mutate system package managers, run `sudo`, edit global shell profiles, or perform machine-global package setup.
