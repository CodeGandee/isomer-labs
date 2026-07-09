# Edit Callback Declarations

## Workflow

1. **Resolve the manifest** at the Toolbox source root and confirm `kind = "toolbox-callback-bundle"` and `toolbox_id` are present or should be authored.
2. **Resolve callback declaration intent**: add, update, remove, repair, or explain `[[callbacks]]` entries.
3. **Validate local identity**. Use `key` for the toolbox-local callback key and reject `id` as a manifest alias.
4. **Validate target shape**. Require target skill, stage, source kind, and source path. Check the target skill and stage against the insertion-point catalog when possible.
5. **Edit only the requested declaration rows** and preserve unrelated callbacks.
6. **Report declaration output** with toolbox-local keys, installed callback ids, target skill, stage, source refs, diagnostics, and next validation command.

If the callback declaration request does not map cleanly to these steps, use your native planning tool to separate declaration repair from source authoring and stop before ambiguous edits.

## Do and Do Not

Do group callback declaration CRUD here: add a row, update a row, remove a row, explain rows, and repair local keys.

Do not expose separate helper subcommands such as `add-callback`, `update-callback`, `remove-callback`, and `list-callbacks`; they all target the same manifest material and would make the skill harder to route.

