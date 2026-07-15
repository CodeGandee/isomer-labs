# Repair Topic Service Master

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve Project, Research Topic, Topic Workspace, requester authorization, and the failed Topic Service Master readiness evidence.
2. Run `isomer-cli --print-json project integrations houmao status`.
3. If integration is `disabled`, report skipped repair with the returned skip reason.
4. If integration is `not_configured`, report the returned next action and stop.
5. Run `isomer-cli --print-json project integrations houmao prepare-skills` to refresh Project-local projected support material.
6. Run `isomer-cli --print-json project integrations houmao topic-service-master binding show --topic <research-topic-id>` and compare the current binding with suggested names.
7. Run `isomer-cli --print-json project integrations houmao skill-context repair-topic-service-master --topic <research-topic-id>`.
8. Read `topic_service_master.suggested_names`, `topic_service_master.binding`, and any drift diagnostics before following Houmao-owned repair steps.
9. Read the returned `houmao_skill_path` and follow it for Houmao-specific repair of projection, specialist, launch profile, mailbox, gateway, runtime, or workspace-support material.
10. Run Houmao commands with `--project-dir <houmao_project_path>` and do not rely on implicit `.houmao/` discovery from cwd.
11. If repair creates or updates the Houmao entities, record the refreshed binding with `isomer-cli --print-json project integrations houmao topic-service-master binding record --topic <research-topic-id> --status prepared ...`.
12. Report repaired, skipped, blocked, or not configured status with binding evidence, changed support material, and remaining blockers.

If the user's task does not map cleanly to these steps, use your native planning tool to build a support-material repair plan from the failed readiness evidence, current binding, drift diagnostics, and projected Houmao route, then execute the plan.

## Operational Contract

- Repair support material only.

## Guardrails

- DO NOT change research decisions, Topic Team membership, or accepted research Artifacts.
