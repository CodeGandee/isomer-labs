# Setup Topic Env

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Read the topic overview, specialization outputs, copied template setup notes, and any environment requirements from the selected Domain Agent Team Template or topic material.
3. Identify required development environment steps, including package installs, local build commands, data preparation, credentials placeholders, and validation commands.
4. Before running mutating setup commands, tell the user what will change when the command is not clearly safe or already requested.
5. Run or report explicit environment setup steps, then capture commands, changed files, skipped actions, blockers, and validation refs.
6. Report `topic_environment_status` as ready, changed, deferred, blocked, or not checked, with the next safe subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step environment setup plan from the topic material, template requirements, available commands, and guardrails, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifacts from `specialize-team` or `clarify-topic-team`:

- `<topic-dir>/topic-def/topic-overview.md`.
- `<topic-workspace>/team-profile/execplan/team-specialization-plan.md` with `Final Report` content or explicit pending items.
- Draft profile or packet/profile input summary from `draft-profile`.

If the specialized topic-team material is missing, refuse to run, explain that environment setup depends on the specialized team shape and requirements, and tell the user to run `specialize-team` first.

## Guardrails

Do not hide mutating setup work inside topic clarification or team specialization.

Do not store credentials, API keys, command payloads, or live provider state in topic profile material.

Do not claim environment readiness without a validation command, explicit evidence, or a named deferral.
