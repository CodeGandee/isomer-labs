# Prepare Topic Service Master

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve Project, Research Topic, Topic Workspace, requester, authorization, and allowed service surfaces.
2. Run `isomer-cli --print-json project integrations houmao status` and classify Houmao integration as `enabled`, `disabled`, or `not_configured`.
3. If integration is `disabled`, record Topic Service Master preparation as skipped with the returned skip reason and continue only non-Houmao readiness work.
4. If integration is `not_configured`, report the returned next action and mark Topic Service Master preparation blocked, not skipped.
5. If integration is `enabled`, run `isomer-cli --print-json project integrations houmao prepare-skills`, then run `isomer-cli --print-json project integrations houmao skill-context prepare-topic-service-master --topic <research-topic-id>`.
6. Read the returned `houmao_skill_path` and follow that projected route for Houmao-specific credentials, tool choice, profile naming, mailbox, gateway, and launch-material preparation.
7. Tell the active agent to run Houmao commands with `--project-dir <houmao_project_path>` and not to rely on implicit `.houmao/` discovery from the Topic Workspace cwd.
8. Report preparation readiness, projected route path, Houmao Project path, Topic Workspace path, blockers, and support Artifact refs.

## Guardrails

Prepare only. Do not launch a live Topic Service Master from Topic Workspace creation or actor setup.

Do not ask the user to install Houmao-owned system skills into their ordinary operator skill home.
