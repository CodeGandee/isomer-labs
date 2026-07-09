# Prepare Topic Service Master

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve Project, Research Topic, Topic Workspace, requester, authorization, and allowed service surfaces.
2. Run `isomer-cli --print-json project integrations houmao status` and classify Houmao integration as `enabled`, `disabled`, or `not_configured`.
3. If integration is `disabled`, record Topic Service Master preparation as skipped with the returned skip reason and continue only non-Houmao readiness work.
4. If integration is `not_configured`, report the returned next action and mark Topic Service Master preparation blocked, not skipped.
5. If integration is `enabled`, run `isomer-cli --print-json project integrations houmao prepare-skills`, then run `isomer-cli --print-json project integrations houmao skill-context prepare-topic-service-master --topic <research-topic-id>`.
6. Read `topic_service_master.suggested_names` from the returned skill context. Pass the suggested `specialist_name`, `launch_profile_name`, and `managed_agent_name` to the Houmao-owned preparation procedure; do not invent or rename them in prose.
7. Read the returned `houmao_skill_path` and follow that projected route for Houmao-specific credentials, tool choice, specialist creation, launch profile creation, mailbox, gateway, and launch-material preparation.
8. Tell the active agent to run Houmao commands with `--project-dir <houmao_project_path>` and not to rely on implicit `.houmao/` discovery from the Topic Workspace cwd.
9. After Houmao-owned preparation reports created or updated entities, record the binding with `isomer-cli --print-json project integrations houmao topic-service-master binding record --topic <research-topic-id> --status prepared --specialist-name <specialist_name> --launch-profile-name <launch_profile_name> --managed-agent-name <managed_agent_name> --updated-by isomer-srv-topic-service-agent-support`.
10. Report preparation readiness, suggested names, recorded binding status, projected route path, Houmao Project path, Topic Workspace path, blockers, and support Artifact refs.

## Guardrails

Prepare only. Do not launch a live Topic Service Master from Topic Workspace creation or actor setup.

Do not write a planned Topic Service Master binding before Houmao-owned preparation succeeds. Disabled, not-configured, blocked, or failed preparation stays in readiness output and diagnostics.

Do not ask the user to install Houmao-owned system skills into their ordinary operator skill home.
