# Fast-Forward

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Summarize the intended mutations and stop for missing topic statement, Project root, actor roster, or mutation approval.
2. Run `ensure-project` when the Project is missing, invalid, or not selected.
3. Run `resolve-topic-input` when the topic statement, topic id, or Topic Workspace candidate is missing or unclear.
4. Run `register-topic` when the Research Topic or Topic Workspace is not Project Manifest-backed.
5. Run `create-research-intent` when `topic.intent.overview` is missing, stale, or unclear.
6. Run `init-runtime` when Workspace Runtime is absent or invalid for the selected topic.
7. Run `define-topic-env` when `topic.intent.topic_env_requirements` is missing or stale; in fast-forward mode, report generated assumptions and continue without an interactive verification stop.
8. Run `setup-topic-env` when topic environment readiness, `topic.env.topic_setup_target_spec`, `topic.repos.main`, or projection predecessor evidence is missing.
9. Run `define-actors` when `topic.intent.actor_definitions` is missing or stale; create the default `operator` actor definition unless explicitly opted out or a richer actor roster is supplied.
10. Run `setup-actors` for actors from `topic.intent.actor_definitions`, including the default `operator` Topic Actor unless explicitly opted out, and verify derived actor env gates from actor cwd.
11. Run `bootstrap-research` to validate base topic readiness, Topic Actor readiness, selected v2 placeholder bindings, and storage recording guidance.
12. Run `finalize` to validate Topic Workspace preparation, write `topic.workspace.summary`, and print ready/verified/blocked state.
13. Report Essential Output by default, including the blocked stage and missing evidence if any stage blocked.

If the user's task does not map cleanly to these steps, inspect readiness first, then run only the safe subset of stage subcommands that match the user's request and approval.

## Idempotence

`fast-forward` must validate and reuse ready evidence. It must not rerun ready destructive or expensive stages unless the user explicitly asks. It stops at the first blocker that prevents later stages from being meaningful and reports the blocked stage and missing evidence without prescribing a next research command.
