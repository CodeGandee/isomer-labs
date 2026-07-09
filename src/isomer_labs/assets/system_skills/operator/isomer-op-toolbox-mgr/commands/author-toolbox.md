# Author Toolbox

## Workflow

1. **Resolve intent** from the prompt, intent file, existing notes, or plain-language task. Identify desired callbacks, target skills, stages, Toolbox skills, Toolbox skill subcommands, Runtime Params, and install scope.
2. **Choose or derive the Toolbox ID**. Use a stable path-safe kebab-case id, confirm it with the user when the prompt is ambiguous, and default source to `skillset/toolboxes/<toolbox-id>/`.
3. **Plan source material** by calling the helper logic in [author-toolbox-source.md](author-toolbox-source.md), [edit-callback-declarations.md](edit-callback-declarations.md), and [edit-runtime-params.md](edit-runtime-params.md) as needed.
4. **Write only project-local source files** needed for the requested Toolbox. Do not install unless the user asked for install or refresh.
5. **Validate or prepare validation** with `isomer-cli project toolboxes validate --toolbox-dir <path>` when that command is available, or report the exact validation command family to run when the local CLI lacks the final command.
6. **Optionally install** with `isomer-cli project toolboxes install --toolbox-dir <path>` plus the selected Project or topic selector only when requested.
7. **Report Essential Output** with status, Toolbox ID, source path, authored files, callback ids, Toolbox skill invocation posture, Runtime Param ids, scope, validation result, blockers, rollback hint, and next action.

If the authoring request does not map cleanly to these steps, use your native planning tool to build a bounded Toolbox authoring plan from the user's intent, available insertion points, Runtime Params, scope, and validation constraints.

## Authoring Rules

- Create a manifest with `kind = "toolbox-callback-bundle"` and `toolbox_id = "<toolbox-id>"`.
- Use `key` for toolbox-local callback keys; do not use callback `id` as a manifest alias.
- Prefer `prompt_file` callback routers that invoke a named Toolbox skill subcommand for a purpose.
- Author Toolbox skill `agents/openai.yaml` with `policy.allow_implicit_invocation: false` by default.
- Use direct `skill_dir` callbacks only as an explicit supplemental-instruction exception, not as automatic skill execution.
- Report installed callback ids as `<toolbox_id>:<toolbox-local-key>`.
- Keep Runtime Param rows split into `toolbox_id` and `key`; report effective ids as `<toolbox_id>:<param-key>`.
- Put reusable default Runtime Param values in Toolbox-local TOML bundle files rather than in Project or Topic manifests.
