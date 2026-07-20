# Manage Toolbox

## Workflow

1. **Classify the management action**: validate, install, list, show, explain, enable, disable, update source, uninstall, or callback refresh.
2. **Resolve Toolbox identity and scope**. Use `toolbox_id` from the manifest for install; use explicit Toolbox ID for installed-state actions.
3. **Prefer read-only commands** for list, show, explain, validate, and diagnostics.
4. **Use mutating CLI commands only when requested**. Use `isomer-cli project toolboxes install --toolbox-dir <path>`, `enable`, `disable`, `update-source`, or `uninstall` with the selected scope and confirmation flags required by the CLI.
5. **Warn before broad changes**. Project-scope disable, uninstall, and source replacement can affect every compatible topic context.
6. **Inspect effective state** after mutation when useful, using [inspect-effective-state.md](inspect-effective-state.md).
7. **Report Essential Output** with action, Toolbox ID, source path, scope, status, callback and Runtime Param effect, diagnostics, rollback hint, and next action.

If the management request does not map cleanly to these steps, use your native planning tool to choose the smallest read-only inspection or the safest explicit mutation command.

## Command Families

- Full bundle install or registration refresh: `isomer-cli project toolboxes install --toolbox-dir <path>`.
- Read-only management: `project toolboxes list`, `show`, `explain`, and `validate`.
- Status mutation: `project toolboxes enable` and `disable`.
- Source mutation: `project toolboxes update-source`.
- Removal: `project toolboxes uninstall`, scoped to the selected layer.

