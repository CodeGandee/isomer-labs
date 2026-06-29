# Setup Topic Env

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run directly and use **Targeted Fast-Forward Recovery** from the entrypoint when the missing predecessor can be created by the canonical flow.
2. Require `ensure-topic-registration` evidence:
   - Refuse before service delegation if the Research Topic or Topic Workspace is not Project Manifest-backed.
   - Refuse if `topic_registration_status` is blocked.
   - Refuse if Pixi cannot resolve either an explicit `topic_standalone_pixi_bindings.manifest_path_or_dir` target or the implicit registered Topic Workspace directory default required by `isomer-srv-topic-env-setup`.
3. Resolve the selected Research Topic and Topic Workspace:
   - Use registration evidence, Project Manifest evidence, and any topic or specialization outputs that exist.
   - Refuse to run if the Topic Workspace is missing or provisional without authoritative registration.
4. Read available setup context:
   - Include `topic.intent.overview`, `topic.intent.topic_env_requirements`, prompt-supplied runnable target, specialization outputs when present, copied template setup notes when present, draft packet/profile inputs when present, and any environment requirements from topic material.
   - Do not require specialization outputs solely to prepare the Topic Workspace environment.
5. Require a usable setup source:
   - Continue when `topic.intent.topic_env_requirements` is usable or an explicit manual topic env target spec exists.
   - If source intent is missing and the prompt or topic material gives a clear runnable target, route to `resolve-topic-env-gate` to create or update that concise source intent.
   - If the runnable target is unclear, ask the user for the target and stop before service delegation.
6. Select the service setup mode:
   - Use `auto` for `fast-forward`, direct setup, or concrete setup requests.
   - Use `manual` when the caller is `step-by-step`, asks for confirmation, or wants to inspect choices before each service step.
7. Prepare the derived target spec boundary:
   - Ensure `topic.env.topic_setup_target_spec` exists, is supplied explicitly, or can be created from `topic.intent.topic_env_requirements` before service materialization.
   - Keep the source intent concise and user-editable; put operational commands, repo acquisition details, projection access intent, and verification details in the derived target spec.
8. Delegate heavy Topic Workspace environment setup:
   - Call `$isomer-srv-topic-env-setup setup-topic-env <research_topic_id> <auto|manual>`.
   - Pass the registered Research Topic, resolved Topic Workspace, active environment binding evidence, `topic.intent.topic_env_requirements` metadata or explicit target spec source, and relevant topic/setup notes as context.
   - Let `isomer-srv-topic-env-setup` handle source-gate reading, target-spec validation, Topic Main Development Repository setup, canonical external repo materialization, external repo projection materialization, dependency inference, Pixi mutation, and topic-root or repo-specific verification only.
   - Require delegated output to record resource checks and conservative skip, defer, or blocker decisions before any heavy setup or verification command such as compilation, deep model inference, full dataset download, large archive extraction, or broad test suite execution.
9. Map the service output using **Service Output Mapping**:
   - Record source and target semantic labels, resolved paths, storage profiles, sources, source details, diagnostics, Topic Workspace predecessor readiness status, Topic Main Development Repository Git state, projection metadata, resource check status, commands run, changed files, repo warnings, blockers, and validation refs.
   - Record `per_agent_readiness_status: not checked` when the service reports it as durable setup evidence.
10. Report `topic_environment_status` as ready, changed, deferred, blocked, or not checked, with the next safe subcommand. Do not report per-Agent Workspace cwd readiness from this subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a service-delegation plan from the topic material, template requirements, available `topic.intent.topic_env_requirements` intent or explicit target spec source, `isomer-srv-topic-env-setup` output contract, and guardrails, then execute only the operator-safe handoff and reporting portions.

## Prerequisite Artifacts

Required predecessor artifacts or inputs:

- Registration assurance from `ensure-topic-registration`, including Project Manifest-backed `registered_research_topic_ref`, `registered_topic_workspace_ref`, `topic_registration_status: registered`, and explicit, implicit-default, or blocked environment binding evidence.
- A usable `topic.intent.topic_env_requirements` source surface, an explicit manual topic env target spec, or a clear runnable target from the prompt, topic overview, or existing topic-team material that can be routed to `resolve-topic-env-gate`.

Specialized topic-team material, `<topic-workspace>/team-profile/`, Topic Agent Team Profile material, draft profile inputs, Agent Team Instance records, roles, and agent count are optional context for this subcommand. Do not refuse solely because they are absent. If the requested runnable target explicitly depends on files produced by specialization and those files are missing, report that specific missing runnable-target input instead of treating team-profile material as a general prerequisite.

If registration evidence is missing, refuse to run directly, explain that service setup needs manifest-backed Research Topic and Topic Workspace refs, and offer targeted fast-forward recovery to `setup-topic-env`. Use `python scripts/query_step_dependencies.py path --target setup-topic-env --include-target` for the inclusive default path and `python scripts/query_step_dependencies.py path --target setup-topic-env --exclude-target` for the exclusive path.

If `topic.intent.topic_env_requirements` is missing and the prompt or topic material gives a clear runnable target, offer targeted fast-forward recovery through `resolve-topic-env-gate` to `setup-topic-env`. If the runnable target is unclear, ask the user what should be able to run after environment setup and stop before service delegation.

If Pixi cannot resolve the effective Topic Workspace Pixi binding target, report that blocker and do not call `isomer-srv-topic-env-setup`.

## Source Intent Handoff

`topic.intent.topic_env_requirements` is the boundary between the operator workflow and service environment setup. It should describe the user-specified runnable target, success criteria, important repos or data expectations, and any setup notes from the prompt, topic material, or specialized team material when that material already exists. Its default `isomer-default.v1` path is `<topic-workspace>/intent/src/topic-env-gate.md`, but the semantic label is the contract.

Do not invent runnable requirements from vague topic text. If the source intent is missing and no clear runnable target exists, ask the user what should be able to run after environment setup and stop before calling `isomer-srv-topic-env-setup`.

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
| `topic_env_source_label`, `topic_env_source_path`, `topic_env_source_storage_profile`, `topic_env_source`, `topic_env_source_detail` | source intent setup evidence |
| `topic_env_target_spec_label`, `topic_env_target_spec_path`, `topic_env_target_spec_storage_profile`, `topic_env_target_spec_source`, `topic_env_target_spec_source_detail` | target spec validation ref |
| `path_diagnostics` or label diagnostics | operator blockers or warnings with the relevant semantic label |
| `topic_main_repository` | topic-main predecessor evidence for later agent setup |
| `external_repo_projections`, `external_repo_projection_manifest` | projection predecessor evidence for later agent setup |
| `resource_check_status`, `resource_check_evidence`, `resource_conservative_decisions` | operator-visible evidence that heavy setup or verification work checked host capacity first and chose smoke-test, skip, defer, or blocker decisions instead of overloading the system |
| `commands_run` | setup command evidence |
| `changed_files` | changed setup file evidence |
| `inferred_source_warnings` | setup warnings and later validation notes |
| `blockers` | operator blockers and `next_operator_action` |

## Guardrails

Treat installed packages, environment files, setup commands, validation records, skipped actions, and blockers as durable Topic Workspace predecessor preparation. Topic Team material may consume this evidence later, but it is not a prerequisite for this subcommand.

Do not hide mutating setup work inside topic clarification or team specialization.

Do not infer packages, choose repo sources, install dependencies, repair Pixi files, create topic-main, project external repos, or run verification commands directly from this operator subcommand. Delegate that work to `isomer-srv-topic-env-setup` and record its output.

Do not read `topic.intent.agent_env_requirements`, write `topic.env.agent_setup_target_spec`, or claim Agent Workspace cwd readiness from this operator subcommand. Use `resolve-agent-env-gate` and `setup-agent-workspace` when the caller requested per-Agent Workspace proof.

Do not start live team execution, launch execution adapters, or create runtime service state from this subcommand.

Do not store credentials, API keys, command payloads, live provider state, or adapter state in topic profile material.

Do not claim Topic Workspace environment readiness unless `isomer-srv-topic-env-setup` reports readiness, or unless readiness is explicitly deferred or blocked with named evidence. Topic Workspace readiness does not satisfy Agent Workspace cwd readiness.
