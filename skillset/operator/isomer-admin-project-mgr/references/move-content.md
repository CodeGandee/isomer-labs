# Move Content

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root and requested destination generated content root from the user's prompt.
2. Start with a dry-run command:
   - Use `pixi run isomer-cli --print-json project content-root move --to <content-dir> --dry-run` from the Project root.
   - Use `pixi run isomer-cli --print-json project --root <project-root> content-root move --to <content-dir> --dry-run` when operating from another directory.
3. Explain the relocation plan in plain text:
   - Old generated content root and new generated content root.
   - Managed moves, manifest updates, skipped entries, unmanaged leftovers, diagnostics, and warnings.
4. Warn about stale runtime paths:
   - Existing Workspace Runtime records, Pixi environments, installed packages, adapter runtime material, logs, and stored path plans may contain old paths after relocation.
   - Tell the user to reinstall or reinitialize those runtimes if needed.
5. If the user confirms relocation after reviewing the plan, run the same command with `--yes` instead of `--dry-run`.
6. Report relocation output:
   - Include `project_root`, `project_manifest_path`, old generated content root, new generated content root, and `relocation_plan`.
   - Include applied moves, unmanaged leftovers, diagnostics, warnings, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the Project root, content-root destination, CLI command boundaries, and guardrails, then execute the plan.

## Guardrails

- Default to `isomer-cli project content-root move --to <content-dir> --dry-run` unless the user has already reviewed a relocation plan and explicitly asks to apply it.
- Do not use `--yes` without user confirmation.
- Do not hand-edit `.isomer-labs/manifest.toml` for supported generated content-root relocation workflows.
- Do not rename the whole old content root as an opaque directory; supported relocation preserves unmanaged leftovers.
- Do not rewrite `state.sqlite`, stored path plans, Pixi environments, installed package metadata, adapter runtime records, logs, or generated runtime internals.
- Treat destination path refusals, destination conflicts, missing Project Manifest, malformed Project Manifest, and symlink content roots as blockers.
