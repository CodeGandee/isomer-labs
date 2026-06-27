# Resolve Workspace

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root and Project Manifest through the same Isomer context rules used by operator project commands: explicit selector, current directory, supported environment overrides, and Project Manifest registration.
2. Resolve the selected Research Topic and Topic Workspace through Project Manifest-backed context, including explicit topic or workspace selectors if the user supplied them.
3. Confirm that the Topic Workspace belongs to the selected Research Topic and resolves inside the Project root.
4. Compute the expected shared repository path `<topic-workspace-dir>/repos/topic-main`, Isomer-managed namespace `<topic-workspace-dir>/repos/topic-main/isomer-managed`, and Agent Workspace root `<topic-workspace-dir>/agents/`.
5. Report existing packet or profile material that can provide active role bindings, `agent_name` plans, branch plans, and derived compatibility `agent_workspace_ref` values.
6. Stop with a blocker if the Project, Research Topic, or Topic Workspace cannot be selected unambiguously.

If the user's task does not map cleanly to these steps, use your native planning tool to resolve the smallest safe Isomer context first, then report what remains unknown.

## Output

Report `research_topic_ref`, `topic_workspace_ref`, `topic_workspace_path`, `topic_main_repo_path`, `topic_main_isomer_managed_path`, `agent_workspace_root`, candidate packet/profile files, blockers, and `next_operator_action`.

## Guardrails

Do not infer the selected Topic Workspace by scanning directories. Directory inspection can confirm material after Project Manifest-backed selection, but it must not choose the topic.

Do not create files from this subcommand. It is a read-only context and path planning stage.
