# Show Context

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root and any topic, workspace, profile, template, task, run, Agent Team Instance, or Agent Instance selectors from the prompt.
2. Run the context command:
   - Use `isomer-cli --print-json project context show` from the Project root.
   - Use `isomer-cli --print-json project --root <project-root> context show` when operating from another directory.
   - Include the selected `--topic`, `--status`, and other selectors.
3. If context cannot resolve, report the diagnostics and the selector or Project registration needed to proceed.
4. Return the selected Project, Research Topic, Topic Workspace, Domain Agent Team Template, Topic Agent Team Profile, Workspace Runtime refs, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the Effective Topic Context selectors and guardrails, then execute the plan.

## Guardrails

- Keep this subcommand read-only.
- Do not create missing topics, workspaces, runtime state, or profile material from context inspection alone.
