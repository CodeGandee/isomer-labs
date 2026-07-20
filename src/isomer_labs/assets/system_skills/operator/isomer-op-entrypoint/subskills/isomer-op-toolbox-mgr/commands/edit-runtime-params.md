# Edit Runtime Params

## Workflow

1. **Resolve the Runtime Param target**: manifest declaration, default bundle row, import row, explicit installed value, or effective-value explanation.
2. **Keep source and installed configuration separate**. Write Toolbox source declarations and default bundles directly; use `isomer-cli project toolbox-params` for installed Project or Topic configuration.
3. **Validate key shape**. Runtime Param declarations use toolbox-local `key`; effective ids are `<toolbox_id>:<param-key>`.
4. **Apply the requested grouped operation**: declare, update, remove, write bundle, add import, remove import, set explicit value, unset explicit value, get, explain, or validate.
5. **Report param output** with effective param ids, scope, source file, import path, previous and new value when applicable, diagnostics, and next action.

If the Runtime Param edit does not map cleanly to these steps, use your native planning tool to split source edits from CLI-backed installed configuration and execute only the unambiguous part.

## Do and Do Not

Do group Runtime Param CRUD here because declarations, bundles, imports, explicit values, and explanation all target the same user concept.

Do not create separate helper subcommands such as `add-param`, `set-param`, `unset-param`, `import-param`, and `explain-param`.

