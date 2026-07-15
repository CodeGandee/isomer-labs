# Resolve Topic Input

## Workflow

When this helper subcommand is selected, execute the following steps in order.

1. Resolve concrete Research Topic source material from the user prompt, a supplied Markdown file, selected context, or a registered concrete topic statement.
2. Reject missing or generic topic material such as `default`, `default Research Topic`, or non-substantive placeholders.
3. Derive or confirm a path-safe `<topic-id>` from the concrete Research Topic material without treating sibling directories as authority.
4. Resolve the Topic Workspace candidate:
   - When the user explicitly supplies a custom Topic Workspace directory, preserve that directory as the candidate after confirming it is project-scoped and does not collide with registered Project material.
   - Otherwise, use the Project Manifest `topic_workspace_base_dir` when present and append `<topic-id>`.
   - When the Project Manifest does not define `topic_workspace_base_dir`, use the built-in `isomer-content/topic-ws/` base, producing `isomer-content/topic-ws/<topic-id>`.
5. Report topic statement, `<topic-id>`, source material, Topic Workspace candidate, candidate source, blockers, and readiness state.

If the user's task does not map cleanly to these steps, ask for the actual Research Topic and stop before deriving a topic slug, choosing a Topic Workspace path, registering a topic, or writing intent files.

## Operational Notes

- Use Project Manifest-backed context and semantic path resolution once a Topic Workspace exists.

## Guardrails

- DO NOT use this helper to write `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, `topic.env.topic_setup_target_spec`, or `topic.env.actor_env_gates`.
- DO NOT use a bare `<topic-id>` as the Topic Workspace candidate or later pass it as `--workspace-dir <topic-workspace-dir>` unless the user explicitly supplied that project-root-relative custom directory.
