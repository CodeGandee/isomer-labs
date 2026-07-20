# Help

## Workflow

1. **Summarize the skill** as the Project Operator surface for creating and managing project-local Toolboxes.
2. **List public procedural subcommands**: `author-toolbox`, `convert-skill`, `insert-callback`, `define-runtime-params`, `manage-toolbox`, and `identify-insertion-points`.
3. **Explain required inputs**: Project root, Toolbox ID or source path, target skill and stage when inserting callbacks, Runtime Param keys when configuring params, and Toolbox Scope when mutating or inspecting effective state.
4. **State safe defaults**: new source lives under `skillset/toolboxes/<toolbox-id>/`, Toolbox skills are routed or manually invoked with `allow_implicit_invocation: false`, inspection is read-only, mutation goes through existing `isomer-cli` commands, and Project-scope changes must be explicit.
5. **Report a concise next action** by suggesting the narrowest subcommand that fits the user's visible goal.

If the user's help request does not map cleanly to these steps, use your native planning tool to produce a short orientation from the skill's subcommands, guardrails, and output contract.

## Output

Identify `isomer-op-toolbox-mgr` as the owner, list only its public procedural subcommands, and recommend the narrowest safe start. Name missing Project, Toolbox, target, scope, or Runtime Param inputs and summarize the mutation, auto-invocation, schema, and secret-handling guardrails in natural language.
