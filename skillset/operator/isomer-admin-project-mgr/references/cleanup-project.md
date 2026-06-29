# Cleanup Project

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve cleanup inputs:
   - Project root.
   - Requested cleanup parts.
   - Optional Research Topic ids.
   - Optional generated content root.
   - Whether the user wants dry-run review or confirmed deletion.
2. Start with a dry-run command:
   - Base command: `pixi run isomer-cli --print-json project cleanup --part <part> --dry-run`.
   - Add repeated `--part <part>`, `--topic <topic-id>`, `--all-topics`, or `--content-dir <content-dir>` when needed.
3. Explain the cleanup plan in plain text: selected parts, authority source, planned targets, absent targets, refused targets, warnings, and diagnostics.
4. Apply cleanup only after review:
   - If the user confirms deletion after reviewing the plan, run the same command with `--yes` instead of `--dry-run`.
   - For whole content-root deletion, include `--purge-content-root` only when the user explicitly asks to remove the entire selected generated content root.
5. Report `project_root`, `project_manifest_path`, selected cleanup parts, `cleanup_plan`, removed targets, skipped targets, diagnostics, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the Project root, cleanup parts, CLI command boundaries, and guardrails, then execute the plan.

## Cleanup Parts

- `bootstrap`: Project config, Isomer-managed Houmao overlay, generated content-root policy files, and known init-created Topic Workspace directories.
- `project-config`: `.isomer-labs/`.
- `houmao-overlay`: Isomer-managed `.isomer-labs/.houmao/`; root `.houmao/` is external and preserved.
- `content-policy`: selected content root `README.md` and `.gitignore`.
- `topic-workspace`: selected registered Topic Workspace directories.
- `runtime`: `state.sqlite`, runtime-owned directories, and adapter runtime material under selected Topic Workspaces.
- `content-root`: the selected generated content root, only with `--purge-content-root`.

## Guardrails

- Default to `isomer-cli project cleanup --part <part> --dry-run` unless the user has already reviewed a cleanup plan and explicitly asks to apply it.
- Do not use `--yes` for destructive cleanup without user confirmation.
- Do not use `--purge-content-root` unless the user explicitly requests whole generated content root removal.
- Do not infer Research Topics or Topic Workspaces from unregistered directories when the Project Manifest is missing or malformed.
- Do not stop live Houmao agents, inspect gateways, delete external worktrees, remove root `.houmao/`, or treat Project cleanup as live Houmao cleanup.
- Preserve unknown files by default.
