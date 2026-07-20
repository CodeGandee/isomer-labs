# Stop Topic Service Master

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve Project, Research Topic, Topic Workspace, requester authorization, and selected Topic Service Master identity.
2. Run `isomer-cli --print-json project integrations houmao status`.
3. If integration is `disabled`, report skipped stop with the returned skip reason.
4. If integration is `not_configured`, report the returned next action and stop.
5. Run `isomer-cli --print-json project integrations houmao topic-service-master binding show --topic <research-topic-id>` and use the recorded binding to identify what should be stopped.
6. Run `isomer-cli --print-json project integrations houmao skill-context stop-topic-service-master --topic <research-topic-id>`.
7. Read `topic_service_master.binding` from skill context and use its recorded Houmao names when present.
8. Read the returned `houmao_skill_path` and follow it for Houmao-specific stop or pause procedure.
9. Run Houmao commands with `--project-dir <houmao_project_path>` and do not rely on implicit `.houmao/` discovery from cwd.
10. Report stopped, skipped, blocked, or not configured status with binding evidence and remaining runtime refs.

If the user's task does not map cleanly to these steps, use your native planning tool to build a stop or pause plan from the recorded binding, projected Houmao route, and cleanup boundary, then execute the plan.

## Guardrails

- DO NOT delete Project-local Houmao overlay state, projected skills, Topic Workspace files, or runtime records unless a separate owner workflow explicitly authorizes cleanup.
