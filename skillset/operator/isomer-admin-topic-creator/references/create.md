# Create

## Workflow

When this command is selected, execute the following steps in order.

1. Run the `plan` workflow and summarize proposed mutations before performing them.
2. Run `ensure-project` when the Project is missing, invalid, or not selected.
3. Run `define-topic` when the topic statement, topic id, or topic intent evidence is missing or unclear.
4. Run `register-topic` when the Research Topic or Topic Workspace is not Project Manifest-backed.
5. Run `init-runtime` when Workspace Runtime is absent or invalid for the selected topic.
6. Run `setup-topic-env` when topic environment readiness, `topic.env.topic_setup_target_spec`, `topic.repos.main`, or projection predecessor evidence is missing.
7. Run `setup-actors` for the default `operator` Topic Actor unless explicitly opted out, plus any requested manual Topic Actors.
8. Run `bootstrap-research` to validate base topic readiness, Topic Actor readiness, selected v2 placeholder bindings, and storage recording guidance.
9. Run `start-manual-research` to write start-pack records, actor-local pointers, cwd instructions, and next actions.
10. Report Essential Output by default, including the next incomplete stage if any stage blocked.

If the user's task does not map cleanly to these steps, use `plan` first, then run only the safe subset of stage commands that match the user's request and approval.

## Idempotence

`create` must validate and reuse ready evidence. It must not rerun ready destructive or expensive stages unless the user explicitly asks. It stops at the first blocker that prevents later stages from being meaningful and reports the next command to resume.
