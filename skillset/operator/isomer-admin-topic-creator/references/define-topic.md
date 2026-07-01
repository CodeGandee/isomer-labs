# Define Topic

## Workflow

When this command is selected, execute the following steps in order.

1. Resolve the concrete Research Topic statement from the user prompt, registered topic refs, or operator-provided topic brief.
2. Derive or confirm a path-safe topic id or slug without treating sibling directories as authority.
3. Create or validate topic intent evidence, including `topic.intent.overview`, through the selected Topic Workspace semantic path when registration already exists.
4. Report topic statement, topic id, overview status, semantic label evidence, blockers, and next command.

If the user's task does not map cleanly to these steps, ask for the actual research topic and stop before creating or registering anything.

## Guardrails

Do not write canonical topic understanding to legacy topic-definition paths. Use `topic.intent.overview` and Project Manifest-backed Topic Workspace context when available.
