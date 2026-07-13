# Env Remove Packages

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, Pixi manifest, Pixi environment, and semantic paths through `storage-resolve`.
2. Load the removal request from the prompt or a named Markdown, YAML, JSON, TOML, requirements-style, or copied blocker file.
3. Infer package names, package ecosystem, removal purpose, dependent workflows, requester skill, and desired post-removal verification checks.
4. For every named package, consult `isomer-misc-pkg-specifics` before generic removal planning; record selected package-specific breakage risks, companion-package caveats, verification expectations, blockers, or `no package-specific rule`.
5. Plan a Pixi-scoped removal route and identify likely dependency, lockfile, gate, package-specific runtime, accelerator, and companion-package risks before mutation.
6. Mutate only after clear operator intent, using Pixi-bound commands for the selected Topic Workspace manifest and environment.
7. Verify that relevant topic, actor, agent, figure, document, PPTX, CLI, package-specific runtime, or task-specific checks still pass after removal.
8. Report removed, not-present, skipped, failed, and blocked packages with commands, changed files, package-specific evidence, verification evidence, repair guidance, and next action.

If the user's task does not map cleanly to these steps, produce an inspect-only removal plan and ask for missing package names or mutation approval.

## Output

Report the removal outcome and selected Research Topic, then summarize Pixi context, the request and plan, package-specific guidance, commands, verification, changed paths, blockers, and the next action.

## Guardrails

Package removal can break topic readiness. Do not remove packages from the selected Topic Workspace Pixi environment until dependency risks and verification checks are explicit.

Do not choose a generic removal route before checking package-specific guidance for a named package. Treat package-specific runtime, accelerator, or companion-package caveats as removal blockers or post-removal verification requirements when they apply.
