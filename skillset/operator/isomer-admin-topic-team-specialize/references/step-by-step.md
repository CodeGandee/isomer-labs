# Step by Step

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Explain that `step-by-step` follows the same required static topic-team setup path as `fast-forward`, but pauses before each step for user confirmation.
2. Prepare a progress tracker with these steps: `init-topic`, `clarify-topic` when needed, `ensure-topic-registration`, optional independent `setup-topic-env` when an env gate or clear runnable target exists, `specialize-team`, `clarify-topic-team` when needed, optional repeated `setup-topic-env` when specialization changes runnable requirements, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, and optional later approval or materialization boundaries. If the user has not supplied concrete Research Topic substance, ask for it before confirming or running `init-topic`.
3. Before each step, tell the user what will happen, what inputs or files may be read or changed, and what output should exist after the step. For `ensure-topic-registration`, explain that it may run supported Isomer Project registration commands and will block instead of hand-editing Project Config or inventing missing bindings. For `setup-topic-env`, explain that the operator step only needs registration, a Pixi binding, and an `env-gate.md` or clear runnable target; it then delegates heavy Topic Workspace setup to `$isomer-srv-topic-env-setup setup-topic-env <research_topic_id> manual` and records predecessor evidence. For `setup-agent-workspace`, explain that it first records or delegates Git-backed topology evidence, then prepares `<topic-workspace>/user-intent/src/agent-env-gate.md` from the user task if per-Agent Workspace cwd proof is requested and the file is missing, and only then delegates readiness proof to `$isomer-srv-agent-env-setup setup-agent-env <research_topic_id>` after source gate, predecessor evidence, authoritative Agent Names, and topology evidence exist.
4. Ask the user to confirm before running the step. Continue only after explicit confirmation; if the user declines or asks to stop, report progress, blockers, and the next safe step.
5. Execute exactly one confirmed step, then summarize what changed, what was deferred, and whether the next step is safe.
6. Ask the user to confirm before moving to the next step, repeating the confirm-execute-summarize cycle until `finalize-topic-team` creates or updates `isomer-topic-summary.md`.
7. Stop at final topic-team summary output. Run `approve-profile` or `materialize-profile` only when the user explicitly asks for that static profile-material boundary and required validation or approval inputs are available.

If the user's task does not map cleanly to these steps, use your native planning tool to build a guided confirmation plan from the selected topic, template, procedural subcommands, output contract, and guardrails, then execute one confirmed step at a time.
