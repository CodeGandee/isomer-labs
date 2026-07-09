# Insert Callback

## Workflow

1. **Resolve the insertion point**: target packaged system skill, stage, and whether the point exists in the packaged insertion-point catalog.
2. **Resolve Toolbox source**: Toolbox ID, source directory, toolbox-local callback key, source kind, and callback instruction path.
3. **Author or update source files** with [author-toolbox-source.md](author-toolbox-source.md) when callback material is missing. Prefer a prompt-file router that invokes a Toolbox skill subcommand for the insertion-point purpose.
4. **Draft or update manifest declaration** with [edit-callback-declarations.md](edit-callback-declarations.md), using `key` for the toolbox-local key.
5. **Validate the Toolbox manifest** before install or refresh.
6. **Install or refresh only when requested**. Use `isomer-cli project toolboxes install --toolbox-dir <path>` for a full bundle, or the lower-level `isomer-cli project skill-callbacks install --toolbox-dir <path>` primitive for callback-only repair or migration.
7. **Report Essential Output** with target skill, stage, Toolbox ID, local key, installed callback id, source kind, invocation posture, scope, validation result, and blockers.

If the callback insertion request does not map cleanly to these steps, use your native planning tool to identify the smallest safe insertion plan and stop on missing target, stage, source path, or scope.

## Callback Rules

- The installed callback id is `<toolbox_id>:<toolbox-local-key>`.
- The toolbox-local key cannot contain `.`, `:`, whitespace, or path traversal.
- The default callback source for Toolbox skill behavior is `prompt_file`, with text that names the installed skill, subcommand, and purpose.
- A `skill_dir` source is supplemental instruction material, not automatic skill execution.
- Multiple Toolboxes may target the same insertion point. Do not remove other callbacks for the same target skill and stage.
