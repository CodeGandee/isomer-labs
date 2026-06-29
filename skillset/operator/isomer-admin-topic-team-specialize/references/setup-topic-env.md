# Setup Topic Env

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Require `ensure-topic-registration` evidence. Refuse before service delegation if the Research Topic or Topic Workspace is not Project Manifest-backed, if `topic_registration_status` is blocked, or if Pixi cannot resolve either an explicit `topic_standalone_pixi_bindings.manifest_path_or_dir` target or the implicit registered Topic Workspace directory default required by `isomer-srv-topic-env-setup`.
3. Resolve the selected Research Topic and Topic Workspace from registration evidence, Project Manifest evidence, and any topic or specialization outputs that exist. Refuse to run if the Topic Workspace is missing or provisional without authoritative registration.
4. Read the topic overview, existing source gate, prompt-supplied runnable target, specialization outputs when present, copied template setup notes when present, draft packet/profile inputs when present, and any environment requirements from topic material. Do not require specialization outputs solely to prepare the Topic Workspace environment.
5. Ensure the source gate exists at `<topic-workspace>/user-intent/src/env-gate.md`. If it exists, use it as the handoff contract. If it is missing and the prompt or topic material gives a clear runnable target, create or update a concise `env-gate.md` that states what must run after setup. If the runnable target is unclear, ask the user for the target and stop before service delegation.
6. Select the service setup mode. Use `auto` for `fast-forward`, direct setup, or concrete setup requests. Use `manual` when the caller is `step-by-step`, asks for confirmation, or wants to inspect choices before each service step.
7. Delegate heavy Topic Workspace environment setup to `$isomer-srv-topic-env-setup setup-topic-env <research_topic_id> <auto|manual>`, passing the registered Research Topic, resolved Topic Workspace, active environment binding evidence, `env_gate_path`, and relevant topic/setup notes as context. Let `isomer-srv-topic-env-setup` handle source-gate reading, repo materialization, derived gate generation, dependency inference, Pixi mutation, and topic-root verification only.
8. Map the service output using **Service Output Mapping**. Record `env_gate_path`, `derived_gate_path`, Topic Workspace predecessor readiness status, commands run, changed files, repo warnings, blockers, validation refs, and `per_agent_readiness_status: not checked` when reported as durable setup evidence.
9. Report `topic_environment_status` as ready, changed, deferred, blocked, or not checked, with the next safe subcommand. Do not report per-Agent Workspace cwd readiness from this subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a service-delegation plan from the topic material, template requirements, available `env-gate.md` intent, `isomer-srv-topic-env-setup` output contract, and guardrails, then execute only the operator-safe handoff and reporting portions.

## Prerequisite Artifacts

Required predecessor artifacts or inputs:

- Registration assurance from `ensure-topic-registration`, including Project Manifest-backed `registered_research_topic_ref`, `registered_topic_workspace_ref`, `topic_registration_status: registered`, and explicit, implicit-default, or blocked environment binding evidence.
- A usable `<topic-workspace>/user-intent/src/env-gate.md`, or a clear runnable target from the prompt, topic overview, or existing topic-team material that can be written to that source gate.

Specialized topic-team material, `<topic-workspace>/team-profile/`, Topic Agent Team Profile material, draft profile inputs, Agent Team Instance records, roles, and agent count are optional context for this subcommand. Do not refuse solely because they are absent. If the requested runnable target explicitly depends on files produced by specialization and those files are missing, report that specific missing runnable-target input instead of treating team-profile material as a general prerequisite.

If registration evidence is missing, refuse to run, explain that service setup needs manifest-backed Research Topic and Topic Workspace refs, and tell the user to run `ensure-topic-registration` first. If Pixi cannot resolve the effective Topic Workspace Pixi binding target, report that blocker and do not call `isomer-srv-topic-env-setup`.

## Source Gate Handoff

`env-gate.md` is the boundary between the operator workflow and service environment setup. It should describe the user-specified runnable target, success criteria, important repos or data expectations, and any setup notes from the prompt, topic material, or specialized team material when that material already exists.

Do not invent runnable requirements from vague topic text. If the source gate is missing and no clear runnable target exists, ask the user what should be able to run after environment setup and stop before calling `isomer-srv-topic-env-setup`.

## Service Delegation

Use `isomer-srv-topic-env-setup` for the heavy setup path:

```text
$isomer-srv-topic-env-setup setup-topic-env <research_topic_id> auto
$isomer-srv-topic-env-setup setup-topic-env <research_topic_id> manual
```

Use `auto` when this subcommand is reached from `fast-forward` or a direct concrete setup request. Use `manual` when reached from `step-by-step` or when the user asks for confirmation before service setup decisions.

## Service Output Mapping

| `isomer-srv-topic-env-setup` Output | Operator Output |
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

Treat installed packages, environment files, setup commands, validation records, skipped actions, and blockers as durable Topic Workspace predecessor preparation. Topic Team material may consume this evidence later, but it is not a prerequisite for this subcommand.

Do not hide mutating setup work inside topic clarification or team specialization.

Do not infer packages, choose repo sources, install dependencies, repair Pixi files, or run verification commands directly from this operator subcommand. Delegate that work to `isomer-srv-topic-env-setup` and record its output.

Do not read `agent-env-gate.md`, write `isomer-agent-env-gate.md`, or claim Agent Workspace cwd readiness from this operator subcommand. Use `setup-agent-workspace` when the caller requested per-Agent Workspace proof.

Do not start live team execution, launch execution adapters, or create runtime service state from this subcommand.

Do not store credentials, API keys, command payloads, live provider state, or adapter state in topic profile material.

Do not claim Topic Workspace environment readiness unless `isomer-srv-topic-env-setup` reports readiness, or unless readiness is explicitly deferred or blocked with named evidence. Topic Workspace readiness does not satisfy Agent Workspace cwd readiness.
