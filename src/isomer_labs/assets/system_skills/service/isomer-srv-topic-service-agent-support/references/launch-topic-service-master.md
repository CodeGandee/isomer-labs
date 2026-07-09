# Launch Topic Service Master

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve Project, Research Topic, Topic Workspace, requester authorization, and expected Topic Service Master identity.
2. Run `isomer-cli --print-json project integrations houmao status`.
3. If integration is `disabled`, report skipped launch with the returned skip reason and do not inspect Houmao runtime state.
4. If integration is `not_configured`, report the returned next action and stop.
5. Run `isomer-cli --print-json project integrations houmao skill-context launch-topic-service-master --topic <research-topic-id>`.
6. Read the returned `houmao_skill_path` and follow it for Houmao-specific launch profile, mailbox, gateway, and managed-agent lifecycle procedure.
7. Start the Topic Service Master from the Topic Workspace cwd only when the route confirms preparation is sufficient.
8. Run Houmao commands with `--project-dir <houmao_project_path>` and do not rely on implicit `.houmao/` discovery from cwd.
9. Report launch status, agent identity, cwd, Houmao Project path, blockers, and validation refs.

## Guardrails

Do not launch from Topic Creator setup. Launch is an explicit lifecycle operation.

Do not store credentials or live process secrets in support Artifacts.
