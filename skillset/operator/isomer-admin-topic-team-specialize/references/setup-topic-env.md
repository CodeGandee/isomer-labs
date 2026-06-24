# Setup Topic Env

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Read the topic overview, specialization outputs, copied template setup notes, and any environment requirements from the selected Domain Agent Team Template or topic material.
2. Identify required development environment steps, including package installs, local build commands, data preparation, credentials placeholders, and validation commands.
3. Before running mutating setup commands, tell the user what will change when the command is not clearly safe or already requested.
4. Run or report explicit environment setup steps, then capture commands, changed files, skipped actions, blockers, and validation refs.
5. Report `topic_environment_status` as ready, changed, deferred, blocked, or not checked, with the next safe subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step environment setup plan from the topic material, template requirements, available commands, and guardrails, then execute the plan.

## Guardrails

Do not hide mutating setup work inside topic clarification or team specialization.

Do not store credentials, API keys, command payloads, or live provider state in topic profile material.

Do not claim environment readiness without a validation command, explicit evidence, or a named deferral.
