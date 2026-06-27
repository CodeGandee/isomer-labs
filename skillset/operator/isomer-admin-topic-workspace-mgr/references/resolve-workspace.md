# Resolve Workspace

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root and Project Manifest through the same Isomer context rules used by operator project commands: explicit selector, current directory, supported environment overrides, and Project Manifest registration.
2. Resolve the selected Research Topic and Topic Workspace through Project Manifest-backed context, including explicit topic or workspace selectors if the user supplied them.
3. Confirm that the Topic Workspace belongs to the selected Research Topic and resolves inside the Project root.
4. Resolve semantic workspace labels with `isomer-cli project paths get` or equivalent API calls. Required labels for read-only planning are `topic.main_repo`, `topic.main_repo.isomer_managed`, `topic.agents_root`, `topic.records`, and `topic.runtime`; resolve `agent.workspace` and support labels for each planned Agent Name when agent planning is in scope.
5. Report existing packet or profile material that can provide active role bindings, `agent_name` plans, branch plans, and derived compatibility `agent_workspace_ref` values.
6. Stop with a blocker if the Project, Research Topic, or Topic Workspace cannot be selected unambiguously.

If the user's task does not map cleanly to these steps, use your native planning tool to resolve the smallest safe Isomer context first, then report what remains unknown.

## Output

Report `research_topic_ref`, `topic_workspace_ref`, `topic_workspace_path`, `semantic_paths` with label, path, source, readiness, and diagnostics, candidate packet/profile files, blockers, and `next_operator_action`.

## Guardrails

Do not infer the selected Topic Workspace by scanning directories. Directory inspection can confirm material after Project Manifest-backed selection, but it must not choose the topic.

Do not create files from this subcommand. It is a read-only context and semantic path planning stage. Do not create or rewrite `topic-workspace.toml`; use explicit default materialization only when the operator asks for creation.
