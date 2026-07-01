# Resolve Topic Input

## Workflow

When this helper subcommand is selected, execute the following steps in order.

1. Resolve concrete Research Topic source material from the user prompt, a supplied Markdown file, selected context, or a registered concrete topic statement.
2. Reject missing or generic topic material such as `default`, `default Research Topic`, or non-substantive placeholders.
3. Derive or confirm a path-safe topic id and Topic Workspace candidate from the concrete Research Topic material without treating sibling directories as authority.
4. Report topic statement, topic id, source material, Topic Workspace candidate, blockers, and next subcommand.

If the user's task does not map cleanly to these steps, ask for the actual Research Topic and stop before deriving a topic slug, choosing a Topic Workspace path, registering a topic, or writing intent files.

## Guardrails

This helper does not write `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, `topic.env.topic_setup_target_spec`, or `topic.env.actor_env_gates`. Use Project Manifest-backed context and semantic path resolution once a Topic Workspace exists.
