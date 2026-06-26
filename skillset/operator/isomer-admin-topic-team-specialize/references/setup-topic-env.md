# Setup Topic Env

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Resolve the selected Research Topic and Topic Workspace from the operator context, Project Manifest evidence, and specialization outputs. Refuse to run if the Topic Workspace is missing or provisional without a safe setup target.
3. Read the topic overview, specialization outputs, copied template setup notes, draft packet/profile inputs, and any environment requirements from topic material.
4. Ensure the source gate exists at `<topic-workspace>/user-intent/src/env-gate.md`. If it exists, use it as the handoff contract. If it is missing and the prompt or topic material gives a clear runnable target, create or update a concise `env-gate.md` that states what must run after setup. If the runnable target is unclear, ask the user for the target and stop before service delegation.
5. Select the service setup mode. Use `auto` for `fast-forward`, direct setup, or concrete setup requests. Use `manual` when the caller is `step-by-step`, asks for confirmation, or wants to inspect choices before each service step.
6. Delegate heavy environment setup to `$isomer-srv-env-setup setup-for-topic-workspace <research_topic_id> <auto|manual>`, passing the resolved Topic Workspace, `env_gate_path`, and relevant topic/setup notes as context. Let `isomer-srv-env-setup` handle source-gate reading, repo materialization, derived gate generation, dependency inference, Pixi mutation, and verification.
7. Map the service output using **Service Output Mapping**. Record `env_gate_path`, `derived_gate_path`, service readiness status, commands run, changed files, repo warnings, blockers, and validation refs as durable setup evidence.
8. Report `topic_environment_status` as ready, changed, deferred, blocked, or not checked, with the next safe subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a service-delegation plan from the topic material, template requirements, available `env-gate.md` intent, `isomer-srv-env-setup` output contract, and guardrails, then execute only the operator-safe handoff and reporting portions.

## Prerequisite Artifacts

Required predecessor artifacts from `specialize-team` or `clarify-topic-team`:

- `<topic-dir>/topic-def/topic-overview.md`.
- `<topic-workspace>/team-profile/execplan/team-specialization-plan.md` with `Final Report` content or explicit pending items.
- Draft profile or packet/profile input summary from `draft-profile`.

If the specialized topic-team material is missing, refuse to run, explain that environment setup depends on the specialized team shape and requirements, and tell the user to run `specialize-team` first.

## Source Gate Handoff

`env-gate.md` is the boundary between operator specialization and service environment setup. It should describe the user-specified runnable target, success criteria, important repos or data expectations, and any setup notes copied from the specialized team material.

Do not invent runnable requirements from vague topic text. If the source gate is missing and no clear runnable target exists, ask the user what should be able to run after environment setup and stop before calling `isomer-srv-env-setup`.

## Service Delegation

Use `isomer-srv-env-setup` for the heavy setup path:

```text
$isomer-srv-env-setup setup-for-topic-workspace <research_topic_id> auto
$isomer-srv-env-setup setup-for-topic-workspace <research_topic_id> manual
```

Use `auto` when this subcommand is reached from `fast-forward` or a direct concrete setup request. Use `manual` when reached from `step-by-step` or when the user asks for confirmation before service setup decisions.

## Service Output Mapping

| `isomer-srv-env-setup` Output | Operator Output |
| --- | --- |
| `readiness_status: ready` | `topic_environment_status: ready` |
| `readiness_status: blocked` | `topic_environment_status: blocked` |
| `readiness_status: failed` | `topic_environment_status: blocked`, with failed command evidence |
| `readiness_status: not checked` | `topic_environment_status: deferred` or `not checked`, based on whether setup was intentionally deferred |
| `env_gate_path` | `env_gate_path` setup evidence |
| `derived_gate_path` | `derived_gate_path` validation ref |
| `commands_run` | setup command evidence |
| `changed_files` | changed setup file evidence |
| `inferred_source_warnings` | setup warnings and later validation notes |
| `blockers` | operator blockers and `next_operator_action` |

## Guardrails

Treat installed packages, environment files, setup commands, validation records, skipped actions, and blockers as durable static preparation for the Topic Team.

Do not hide mutating setup work inside topic clarification or team specialization.

Do not infer packages, choose repo sources, install dependencies, repair Pixi files, or run verification commands directly from this operator subcommand. Delegate that work to `isomer-srv-env-setup` and record its output.

Do not start live team execution, launch execution adapters, or create runtime service state from this subcommand.

Do not store credentials, API keys, command payloads, live provider state, or adapter state in topic profile material.

Do not claim environment readiness unless `isomer-srv-env-setup` reports readiness, or unless readiness is explicitly deferred or blocked with named evidence.
