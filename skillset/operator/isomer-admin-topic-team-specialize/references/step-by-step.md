# Step by Step

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Explain that `step-by-step` follows the same required static topic-team setup path as `fast-forward`, but pauses before each step for user confirmation.
2. Prepare a progress tracker with these steps: `init-topic`, `clarify-topic` when needed, `specialize-team`, `clarify-topic-team` when needed, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, and optional later approval or materialization boundaries. If the user has not supplied concrete Research Topic substance, ask for it before confirming or running `init-topic`.
3. Before each step, tell the user what will happen, what inputs or files may be read or changed, and what output should exist after the step. For `setup-topic-env`, explain that the operator step prepares or checks `env-gate.md`, then delegates heavy setup to `$isomer-srv-env-setup setup-for-topic-workspace <research_topic_id> manual`.
4. Ask the user to confirm before running the step. Continue only after explicit confirmation; if the user declines or asks to stop, report progress, blockers, and the next safe step.
5. Execute exactly one confirmed step, then summarize what changed, what was deferred, and whether the next step is safe.
6. Ask the user to confirm before moving to the next step, repeating the confirm-execute-summarize cycle until `finalize-topic-team` creates or updates `isomer-topic-summary.md`.
7. Stop at final topic-team summary output. Run `approve-profile` or `materialize-profile` only when the user explicitly asks for that static profile-material boundary and required validation or approval inputs are available.

If the user's task does not map cleanly to these steps, use your native planning tool to build a guided confirmation plan from the selected topic, template, procedural subcommands, output contract, and guardrails, then execute one confirmed step at a time.
