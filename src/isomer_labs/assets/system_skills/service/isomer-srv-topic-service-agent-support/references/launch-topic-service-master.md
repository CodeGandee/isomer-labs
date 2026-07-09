# Launch Topic Service Master

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve Project, Research Topic, Topic Workspace, requester authorization, and expected Topic Service Master identity.
2. Run `isomer-cli --print-json project integrations houmao status`.
3. If integration is `disabled`, report skipped launch with the returned skip reason and do not inspect Houmao runtime state.
4. If integration is `not_configured`, report the returned next action and stop.
5. Run `isomer-cli --print-json project integrations houmao topic-service-master binding show --topic <research-topic-id>` and require either a prepared binding or an explicit repair route before launch.
6. Run `isomer-cli --print-json project integrations houmao skill-context launch-topic-service-master --topic <research-topic-id>`.
7. Read `topic_service_master.binding` from skill context and use its recorded Houmao specialist, launch profile, and managed-agent names when present. If the binding drifts from suggested names, report drift and route repair instead of choosing new names.
8. Read the returned `houmao_skill_path` and follow it for Houmao-specific launch profile, mailbox, gateway, and managed-agent lifecycle procedure.
9. Start the Topic Service Master from the Topic Workspace cwd only when the route confirms preparation is sufficient.
10. Run Houmao commands with `--project-dir <houmao_project_path>` and do not rely on implicit `.houmao/` discovery from cwd.
11. Report launch status, binding status, agent identity, cwd, Houmao Project path, blockers, and validation refs.

## Guardrails

Do not launch from Topic Creator setup. Launch is an explicit lifecycle operation.

Do not store credentials or live process secrets in support Artifacts.
