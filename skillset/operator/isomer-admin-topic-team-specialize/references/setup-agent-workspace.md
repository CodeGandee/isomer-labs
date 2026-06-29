# Setup Agent Workspace

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run directly and use **Targeted Fast-Forward Recovery** from the entrypoint when the missing predecessor can be created by the canonical flow.
2. Read setup inputs:
   - Specialized topic-team shape, expected Agent Roles, draft profile inputs, registration evidence, and registered Topic Workspace path.
   - Topic Workspace predecessor evidence, `topic.env.topic_setup_target_spec`, and the user task or requested Agent Workspace cwd readiness target.
3. Require topic-main predecessor evidence before Agent Workspace setup:
   - Require topic env setup output that includes Topic Main Development Repository Git state, Isomer-managed namespace posture, and projection metadata when the target depends on projected external repos.
   - If this evidence is missing, stale, blocked, or failed, route repair to `setup-topic-env` and stop before service delegation.
4. Require a per-agent source intent before cwd verification:
   - Apply this when the user requested per-Agent Workspace cwd verification, agent environment readiness, selected-agent repair, or launch-facing Agent Workspace readiness.
   - Continue when a usable `topic.intent.agent_env_requirements` source surface or an explicit manual agent env target spec exists.
   - If source intent is missing and the task gives a clear per-agent cwd readiness target, route to `resolve-agent-env-gate` before service delegation.
   - If the target is unclear, ask the user what every planned Agent Workspace cwd must be able to run and stop before service delegation.
5. Prepare the derived agent target spec boundary:
   - Ensure `topic.env.agent_setup_target_spec` exists, is supplied explicitly, or can be created from `topic.intent.agent_env_requirements` before service materialization.
   - Keep source intent high level; put per-agent verification matrix, required projection predecessor references, expected results, and blockers in the derived target spec.
6. Delegate gate-driven Agent Workspace environment setup only after required evidence exists:
   - Require `topic.intent.agent_env_requirements` or an explicit target spec source.
   - Require Topic Workspace predecessor evidence including `topic.env.topic_setup_target_spec`, Topic Main Development Repository predecessor evidence, projection predecessor evidence when required, and authoritative Agent Names.
   - Call `$isomer-srv-agent-env-setup setup-agent-env <research_topic_id>` or the needed direct subcommand.
   - Require delegated output to include `topic.env.agent_setup_target_spec`, its `## Gate Checklist`, readiness by Agent Name, and whether every required per-agent checklist item is checked with supporting cwd execution, path, dependency, resource, projection, or expected-result evidence before accepting overall readiness.
   - Require delegated output to record resource checks and bounded real-path verification decisions before any heavy per-agent cwd verification command such as compilation, deep model inference, full dataset download, large archive extraction, or broad test suite execution. Selected-agent partial checks can reduce how many Agent Workspaces run the check, but the selected command must still exercise the requested build, inference, dataset, or benchmark path. If no bounded real-path command can run safely, require a blocker with evidence instead of readiness.
   - Record `agent_env_source_label`, `agent_env_source_path`, `agent_env_target_spec_label`, `agent_env_target_spec_path`, Topic Main Development Repository predecessor evidence, projection predecessor evidence, Agent Names, resolved `agent.workspace` paths, branch plan, worktree status by agent, gate checklist completion evidence, resource check status, readiness by agent, overall readiness, commands run, changed files, blockers, and next action as service evidence.
   - Preserve selected-agent partial evidence as partial; it cannot satisfy `overall_readiness_status: ready` unless the complete planned Agent Name matrix has already passed.
7. Treat non-Git static setup as an explicit blocker or exception for launch-facing worker Agent Workspaces:
   - If the user intentionally requests non-Git support material, record why it is outside the standard worker layout.
8. Create or report Agent Workspace directories only after the specialized team shape is clear and the target paths are safe.
9. Record durable setup material:
   - Include agent names, resolved `agent.workspace` paths, required `agent.*` support paths, `topic.repos.main.tmp` and `agent.tmp` posture, path sources, role ownership, worker visibility boundary notes, and generated-link notes.
   - Include delegated `isomer-srv-agent-env-setup` evidence, skipped actions, blockers, and validation refs.
10. Report Agent Workspace setup output:
   - Include `agent_names`, `agent_workspace_paths`, `semantic_paths`, `local_tmp_path_status`, `isomer_managed_path_status`, `branch_plan`, `topic_main_repo`, `records_root`, and delegated derived `agent_workspace_ref` evidence when present.
   - Include agent env source and target semantic labels, resolved paths, storage profiles, sources, source details, diagnostics, `agent_environment_service_output`, readiness by agent, generated links, unresolved workspace blockers, and whether `validate-topic-team` can proceed.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step Agent Workspace setup plan from the specialized team shape, Topic Workspace boundary, and guardrails, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifacts:

- Specialized topic-team shape and draft profile or packet/profile input summary from `adapt-team-template`.
- Registration assurance from `ensure-topic-registration`, including Project Manifest-backed Research Topic and Topic Workspace refs or an explicit registration blocker.
- `topic_environment_status` or explicit Topic Workspace predecessor setup blocker from `setup-topic-env`.
- `topic.env.topic_setup_target_spec`, Topic Main Development Repository predecessor evidence, projection predecessor evidence when required, and Topic Workspace predecessor evidence from `isomer-srv-topic-env-setup` before per-Agent Workspace cwd verification or selected-agent repair.
- A usable `topic.intent.agent_env_requirements`, an explicit manual agent env target spec, or a clear per-agent cwd readiness target from the task, topic-team material, or user prompt that can be routed to `resolve-agent-env-gate`.

If the Topic Workspace predecessor evidence is missing, refuse to run directly, explain that Agent Workspace environment proof depends on topic env predecessor evidence, and offer targeted fast-forward recovery to `setup-agent-workspace`. Use `python scripts/query_step_dependencies.py path --target setup-agent-workspace --include-target` for the inclusive default path and `python scripts/query_step_dependencies.py path --target setup-agent-workspace --exclude-target` for the exclusive path.

If registration evidence is missing or only names a provisional topic workspace seed, refuse to run directly, explain that Agent Workspace setup needs authoritative Topic Workspace refs, and offer targeted fast-forward recovery through `ensure-topic-registration` to `setup-agent-workspace`. If registration is blocked, ask for the missing registration input instead of mutating Project Config by hand.

If per-Agent Workspace cwd verification or selected-agent repair is requested and `topic.intent.agent_env_requirements` is missing, offer targeted fast-forward recovery through `resolve-agent-env-gate` only when the task clearly states commands, expected results, success criteria, and cwd assumptions for planned Agent Workspaces. If the task is too vague, ask the user for those readiness requirements and stop before calling `isomer-srv-agent-env-setup`.

## Agent Env Gate Handoff

`topic.intent.agent_env_requirements` is the operator-owned source contract for `isomer-srv-agent-env-setup`. It should describe what every authoritative planned Agent Workspace cwd must be able to do after setup. When the user did not create it, route to `resolve-agent-env-gate` only if the task supplies enough concrete setup intent. Its default `isomer-default.v1` path is `<topic-workspace>/intent/src/agent-env-gate.md`, but the semantic label is the contract.

Use this source-gate structure when generating the file:

```markdown
# Agent Environment Gate

## Source Task

## Agent Scope

## Topic Env Predecessor

## Topic Main Predecessor

## Projection Preconditions

## Required Cwd Commands

## Expected Results

## Cwd Assumptions

## Out-of-Scope Requests

## Open Questions
```

`## Source Task` should quote or summarize the user-provided task that caused this gate. `## Agent Scope` should name all planned Agent Names, or state that the authoritative Agent Names must come from the Topic Team Instantiation Packet or Topic Agent Team Profile material. `## Topic Main Predecessor` should reference topic env setup evidence for `topic.repos.main` instead of asking agent env setup to create it. `## Projection Preconditions` should name any external repo projections that must be visible from each Agent Workspace cwd. `## Required Cwd Commands` should list concrete commands or state the exact blocker if the task did not give them. `## Expected Results` should say what counts as success. `## Cwd Assumptions` should state whether commands must run from every `agent.workspace` cwd or a selected-agent partial scope. `## Out-of-Scope Requests` should preserve any request for live Agent Instances, Workspace Runtime mutation, Houmao launch, Execution Adapter launch, privileged host mutation, dependency mutation, or research decisions as blockers for the service skill. `## Open Questions` should contain `None.` only when the task is precise enough for service delegation.

Do not put concrete per-agent verification commands into the source intent. The operator flow may create or update `topic.env.agent_setup_target_spec`, but the operational details belong in that derived target spec, not in `topic.intent.agent_env_requirements`.

## Service Delegation

Use `isomer-srv-agent-env-setup` for gate-driven Agent Workspace environment readiness after source intent preparation, Topic Workspace predecessor evidence, Topic Main Development Repository predecessor evidence, required projection predecessor evidence, and authoritative Agent Names:

```text
$isomer-srv-agent-env-setup setup-agent-env <research_topic_id>
$isomer-srv-agent-env-setup verify-agent-env-gate <research_topic_id> --agent <agent-name>
```

Use the full `setup-agent-env` flow for overall readiness. Use direct selected-agent verification only when the user explicitly asks for partial selected-agent repair or rerun evidence.

Accept delegated `overall_readiness_status: ready` only when every required per-agent `## Gate Checklist` item is checked with cwd evidence for every planned Agent Name. If the service output contains unchecked, failed, blocked, partial, or not-checked checklist items, record those exact items, Agent Names, reasons, and next actions instead of summarizing the agent environment as ready.

## Guardrails

Use **Topic Workspace** for the topic-level work area and **Agent Workspace** for per-agent work areas.

Do not create Agent Workspaces before team specialization defines expected Agent Roles.

Do not hand-roll Git worktree or `isomer-managed/` setup inside this subcommand. Use `isomer-srv-agent-env-setup` for per-agent worktree creation and cwd verification. Use `isomer-admin-topic-workspace-mgr` only for optional topology inspection, branch helpers, boundary summaries, or legacy compatibility diagnostics.

Do not hand-roll per-Agent Workspace environment verification inside this subcommand. Use `isomer-srv-agent-env-setup` for source intent reading, `topic.env.agent_setup_target_spec`, worktree creation, per-agent cwd verification, selected-agent partial evidence, and no-runtime-mutation guardrails.

Do not accept a weaker smoke-test substitution as normal Agent Workspace readiness. If the service records a user downgrade from a critical-path checklist item, preserve that limitation in the setup evidence, validation refs, and later summaries.

Do not call `isomer-srv-agent-env-setup` before `topic.intent.agent_env_requirements` exists, unless the caller supplied an explicit manual agent env target spec. Route to `resolve-agent-env-gate` only when commands, expected results, and cwd assumptions are clear enough for the service to derive a per-agent verification matrix.

Do not accept stale workspace setup evidence that names legacy support roots, top-level Topic Main Development Repository collaboration directories, or default-looking directories without semantic labels and path sources as current readiness. Ask for delegated `isomer-srv-agent-env-setup` verification when worktree or cwd readiness is missing, or for optional `isomer-admin-topic-workspace-mgr` inspection when the user only needs topology diagnostics.

Do not accept tmp contents as readiness evidence. `topic.repos.main.tmp` and `agent.tmp` evidence is limited to resolved paths, ignored local disposable posture, and tracked-content diagnostics.

Do not create Agent Instances, start processes, register Workspace Runtime state, or launch agents from this subcommand.

Do not use Agent Workspace setup as a substitute for later runtime registration when runtime records are required by a different workflow.
