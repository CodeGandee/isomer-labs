# Env Update Packages

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, Pixi manifest, Pixi environment, and semantic paths through `storage-resolve`.
2. Load the update request from the prompt or a named Markdown, YAML, JSON, TOML, requirements-style, or copied blocker file.
3. Infer requested package updates, downgrades, constraints, purpose, requester skill, package ecosystem, and desired verification checks.
4. For every named package, consult `isomer-misc-pkg-specifics` before generic update, source, variant, runtime-wiring, or verification choices; record selected package-specific evidence or `no package-specific rule`.
5. Plan a Pixi-scoped update route for each package, preserving package-specific variant, accelerator, runtime, compatibility, and verification expectations, and avoiding broad environment upgrades unless the user explicitly asks for them.
6. Check current package availability and version evidence through the selected Topic Workspace Pixi environment.
7. Mutate only after clear operator intent, using Pixi-bound commands for the selected Topic Workspace manifest and environment.
8. Verify relevant imports, R libraries, CLI tools, document builds, figures, PPTX generation, package-specific runtime expectations, or task-specific smoke checks after mutation.
9. Report updated, already-current, skipped, failed, and blocked packages with commands, changed files, package-specific evidence, verification evidence, blockers, and next action.

If the user's task does not map cleanly to these steps, build an inspect-only update plan and ask for the missing package names, version constraints, or mutation approval.

## Output

Report the update outcome and selected Research Topic, then summarize Pixi context, the request and plan, package-specific guidance, commands, verification, changed paths, blockers, and the next action.

## Guardrails

- DO NOT create local `venv`, `.venv`, or `virtualenv` environments, run ambient `pip`, mutate system package managers, run `sudo`, edit global shell profiles, or perform machine-global package setup.

- DO NOT choose a generic update route before checking package-specific guidance for a named package. Do not report package-specific runtime readiness from solver success, package metadata, or generic import success when `isomer-misc-pkg-specifics` requires stronger evidence.
