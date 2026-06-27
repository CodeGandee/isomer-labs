# Fast Forward

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Determine whether the user supplied a concrete Research Topic, an explicit registered topic ref with concrete topic material, or enough source material to seed a topic. If no topic substance is supplied, ask for the actual research topic and stop before running `init-topic`.
2. Run `init-topic` when topic material or the topic workspace directory is missing or provisional setup is requested.
3. Run `clarify-topic` only when missing or unclear topic details block specialization.
4. Run `ensure-topic-registration` to verify or create Project Manifest-backed Research Topic and Topic Workspace refs, then verify the Topic Workspace Pixi binding needed by `isomer-srv-topic-env-setup`. Stop on registration or binding blockers.
5. Run `setup-topic-env` before specialization when an existing `env-gate.md` is available or the user supplied a clear runnable target; it delegates heavy Topic Workspace setup to `$isomer-srv-topic-env-setup setup-topic-env <research_topic_id> auto`.
6. Run `specialize-team` to select or confirm one Domain Agent Team Template and execute the helper specialization path through draft profile output.
7. Run `clarify-topic-team` only when specialization outputs contain open questions that block setup or validation.
8. Run or rerun `setup-topic-env` when specialization adds or changes runnable environment requirements, then run `setup-agent-workspace`.
9. Run `validate-topic-team`, then run `finalize-topic-team` to create `isomer-topic-summary.md`.
10. Stop at final topic-team summary output. Run `approve-profile` or `materialize-profile` only when the user explicitly asks for that static profile-material boundary and required validation or approval inputs are available.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the selected topic, template, procedural subcommands, output contract, and guardrails, then execute the plan.

## Output Contract

Report the topic overview path, registration status, registered topic and workspace refs, environment binding status, selected Domain Agent Team Template, copied material paths, topic environment status, Agent Workspace paths, topic-team validation status, `isomer-topic-summary.md` path, blockers, deferrals, and next operator action.
