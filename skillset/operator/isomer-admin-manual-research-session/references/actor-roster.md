# Actor Roster

## Workflow

When this reference is loaded, execute the following steps in order.

1. Start from the existing roster with `isomer-cli --print-json project topic-actors list --topic <topic>`.
2. Normalize requested actor names as topic-local path-safe names, such as `operator`, `claude-scout`, `codex-exp-a`, or `houmao-writer-a`.
3. For each missing actor, ask `isomer-admin-topic-workspace-mgr` to register it with `isomer-cli --print-json project topic-actors register <topic-actor-name> --topic <topic> --actor-kind <operator|manual_worker|houmao_backed|service_assisted|custom.*> --runtime-kind <human_cli|claude_code|codex|houmao|shell|custom.*> --role-kind <operator|scout|coder|experimenter|analyst|writer|reviewer|custom.*> --controller-kind <project_operator_session|operator_agent|human_user|houmao|custom.*> --materialize`.
4. For each existing actor with stale or missing workspace material, ask `isomer-admin-topic-workspace-mgr` to run `project topic-actors materialize`, `repair`, or `diagnose`.
5. Resolve each actor's cwd with `isomer-cli --print-json project paths get topic.actors.workspace --topic <topic> --topic-actor <topic-actor-name>`.
6. Resolve support labels `topic.actors.tmp`, `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, and `topic.actors.links` for every selected actor that will receive a start pack.
7. Record blockers for unknown enum values, unsafe names, branch conflicts, missing `topic.repos.main`, alternate source repository requests, or unresolved actor-scoped paths.

If the user's task does not map cleanly to these steps, produce a roster table with one row per actor and route incomplete rows to the Topic Workspace Manager.

## Roster Columns

| Field | Meaning |
| --- | --- |
| topic_actor_name | Topic-local path-safe actor name. |
| actor_kind | `operator`, `manual_worker`, `houmao_backed`, `service_assisted`, or `custom.*`. |
| runtime_kind | `human_cli`, `claude_code`, `codex`, `houmao`, `shell`, or `custom.*`. |
| role_kind | `operator`, `scout`, `coder`, `experimenter`, `analyst`, `writer`, `reviewer`, or `custom.*`. |
| controller_kind | `project_operator_session`, `operator_agent`, `human_user`, `houmao`, or `custom.*`. |
| cwd_label | Normally `topic.actors.workspace`. |
| cwd_path_status | Resolved, missing, blocked, or not requested. |
| branch | Normally `per-topic-actor/<topic-actor-name>/main`. |
| blockers | Missing or unsafe readiness signal. |
