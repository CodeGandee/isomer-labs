# Define Runtime Params

## Workflow

1. **Resolve the Runtime Param task**: design declarations, write default bundles, add imports, set or unset explicit values, get current values, explain resolution, or validate.
2. **Resolve scope selectors**: Project, Research Topic, Topic Actor, or Topic Agent. Use `--topic-agent` for Topic Agent selection.
3. **Draft source declarations or bundles** with [edit-runtime-params.md](edit-runtime-params.md) when the user is authoring Toolbox source.
4. **Use CLI-backed mutation** for installed configuration: `isomer-cli project toolbox-params set`, `unset`, `import add`, `import remove`, `validate`, `get`, or `explain` as appropriate.
5. **Inspect effective state** with [inspect-effective-state.md](inspect-effective-state.md) or read-only `toolbox-params get` and `explain` commands.
6. **Report Essential Output** with param ids, selected scope, previous and new values when mutation occurred, source file or import path, diagnostics, blockers, and next action.

If the Runtime Param request does not map cleanly to these steps, use your native planning tool to separate source authoring from installed configuration mutation, then execute the safe subset.

## Runtime Param Rules

- Effective ids use `<toolbox_id>:<param-key>`.
- Stored rows keep `toolbox_id` and `key` separate.
- Import files are param-only. Do not put Toolbox registrations, callbacks, nested imports, or unsupported tables in default bundles.
- Do not write secret-like values. Ask the user to store secrets in the approved runtime or credential path instead.

