# Repair Topic Service Master

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve Project, Research Topic, Topic Workspace, requester authorization, and the failed Topic Service Master readiness evidence.
2. Run `isomer-cli --print-json project integrations houmao status`.
3. If integration is `disabled`, report skipped repair with the returned skip reason.
4. If integration is `not_configured`, report the returned next action and stop.
5. Run `isomer-cli --print-json project integrations houmao prepare-skills` to refresh Project-local projected support material.
6. Run `isomer-cli --print-json project integrations houmao skill-context repair-topic-service-master --topic <research-topic-id>`.
7. Read the returned `houmao_skill_path` and follow it for Houmao-specific repair of projection, launch profile, mailbox, gateway, runtime, or workspace-support material.
8. Run Houmao commands with `--project-dir <houmao_project_path>` and do not rely on implicit `.houmao/` discovery from cwd.
9. Report repaired, skipped, blocked, or not configured status with evidence, changed support material, and remaining blockers.

## Guardrails

Repair support material only. Do not change research decisions, Topic Team membership, or accepted research Artifacts.
