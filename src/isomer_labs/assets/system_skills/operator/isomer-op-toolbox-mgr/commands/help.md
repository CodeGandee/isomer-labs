# Help

## Workflow

1. **Summarize the skill** as the Project Operator surface for creating and managing project-local Toolboxes.
2. **List public procedural subcommands**: `author-toolbox`, `convert-skill`, `insert-callback`, `define-runtime-params`, `manage-toolbox`, and `identify-insertion-points`.
3. **Explain required inputs**: Project root, Toolbox ID or source path, target skill and stage when inserting callbacks, Runtime Param keys when configuring params, and Toolbox Scope when mutating or inspecting effective state.
4. **State safe defaults**: new source lives under `skillset/toolboxes/<toolbox-id>/`, inspection is read-only, mutation goes through existing `isomer-cli` commands, and Project-scope changes must be explicit.
5. **Report a concise next action** by suggesting the narrowest subcommand that fits the user's visible goal.

If the user's help request does not map cleanly to these steps, use your native planning tool to produce a short orientation from the skill's subcommands, guardrails, and output contract.

## Output

Report:

- `skill`: `isomer-op-toolbox-mgr`.
- `public_subcommands`: procedural subcommands only.
- `safe_start`: the narrowest recommended subcommand.
- `required_inputs`: missing Project, Toolbox, target, scope, or Runtime Param details.
- `guardrails`: no schema changes, no direct registry or manifest mutation when CLI owns it, no secret-like material.
