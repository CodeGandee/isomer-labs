# Fast Forward

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Determine whether the Research Topic is already registered or whether `init-topic` must create a provisional topic workspace seed first.
2. Run `init-topic` when topic material or the topic workspace directory is missing or provisional setup is requested.
3. Run `clarify-topic` only when missing or unclear topic details block specialization.
4. Run `specialize-team` to select or confirm one Domain Agent Team Template and execute the helper specialization path through draft profile output.
5. Run `clarify-topic-team` only when specialization outputs contain open questions that block setup or validation.
6. Run `setup-topic-env`, then run `setup-agent-workspace`.
7. Run `validate-topic-team`, then run `finalize-topic-team` to create `isomer-topic-summary.md`.
8. Stop at final topic-team summary output. Run `approve-profile` or `materialize-profile` only when the user explicitly asks for that static profile-material boundary and required validation or approval inputs are available.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the selected topic, template, procedural subcommands, output contract, and guardrails, then execute the plan.

## Output Contract

Report the topic overview path, selected Domain Agent Team Template, copied material paths, topic environment status, Agent Workspace paths, topic-team validation status, `isomer-topic-summary.md` path, blockers, deferrals, and next operator action.
