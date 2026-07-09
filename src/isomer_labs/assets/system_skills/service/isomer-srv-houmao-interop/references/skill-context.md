# Isomer Service Houmao Interop — Skill Context

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root and, when relevant, the selected Research Topic and Topic Workspace.
2. Run `isomer-cli --print-json project integrations houmao status` from the Project root or with `--root <project-root>`.
3. If `integration_status` is `disabled`, report skipped Houmao integration work and do not inspect credentials, launch profiles, mailboxes, gateways, or runtime state.
4. If `integration_status` is `not_configured`, report the returned `next_action` and stop before Houmao-specific procedure.
5. For enabled integration, run `isomer-cli --print-json project integrations houmao skill-context <route-name>` and include `--topic <research-topic-id>` when a Topic Workspace is selected.
6. When the payload includes `topic_service_master.suggested_names`, pass those exact `specialist_name`, `launch_profile_name`, and `managed_agent_name` values to Houmao-owned procedures. Do not invent names, abbreviate names, or derive alternate launch profile names in prose.
7. When the payload includes `topic_service_master.binding`, prefer the recorded Houmao specialist, launch profile, and managed-agent names for launch, inspect, stop, and repair routes. If the payload reports drift, keep the drift in Isomer terms and route repair instead of choosing new names.
8. Follow only the returned `houmao_skill_path`. Tell the agent to run Houmao commands with `--project-dir <houmao_project_path>` and not to rely on implicit `.houmao/` discovery from cwd.
9. Report the Isomer request, route name, returned paths, Topic Service Master suggested names or binding status, skip state or blocker, and next safe Isomer owner route.

## Guardrails

Do not fabricate projected skill paths from a requested route name. Unknown routes must come from the CLI diagnostic.

Do not fabricate Topic Service Master specialist, launch profile, or managed-agent names. Use `topic_service_master.suggested_names` before preparation and `topic_service_master.binding` after a binding exists.

Do not route to Houmao-owned skills from the user's ordinary skill home as the primary Isomer path. Use Project-local `.isomer-labs/houmao-skills/` context returned by Isomer CLI.
