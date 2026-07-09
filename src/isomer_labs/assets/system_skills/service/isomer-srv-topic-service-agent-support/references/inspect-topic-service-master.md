# Inspect Topic Service Master

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve Project, Research Topic, Topic Workspace, requester authorization, and any selected Topic Service Master ref.
2. Run `isomer-cli --print-json project integrations houmao status`.
3. If integration is `disabled`, report skipped inspection with the returned skip reason.
4. If integration is `not_configured`, report the returned next action and stop.
5. Run `isomer-cli --print-json project integrations houmao topic-service-master binding show --topic <research-topic-id>` and include suggested names, current binding, or absent-binding status in the inspection report.
6. Run `isomer-cli --print-json project integrations houmao skill-context inspect-topic-service-master --topic <research-topic-id>`.
7. Read `topic_service_master.binding` from skill context and inspect the recorded specialist, launch profile, and managed-agent identity when present.
8. Read the returned `houmao_skill_path` and follow it for read-only Houmao-specific agent, mailbox, gateway, and runtime inspection.
9. Run Houmao commands with `--project-dir <houmao_project_path>` and do not rely on implicit `.houmao/` discovery from cwd.
10. Report readiness as ready, skipped, blocked, not configured, or stale, with binding status, drift diagnostics, exact evidence, and blockers.

## Guardrails

Prefer read-only inspection. Route prompt, stop, repair, or launch actions to their explicit lifecycle subcommands.
