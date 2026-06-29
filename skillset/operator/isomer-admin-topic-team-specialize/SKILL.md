---
name: isomer-admin-topic-team-specialize
description: "Initialize and specialize Isomer Research Topics into static topic-team material. Use when an operator needs topic-team setup for one Research Topic: help, init-topic, resolve-topic-intent, clarify-topic, ensure-topic-registration, resolve-topic-env-gate, specialize-team, clarify-topic-team, setup-topic-env through isomer-srv-topic-env-setup, resolve-agent-env-gate, setup-agent-workspace, validate-topic-team, finalize-topic-team, approval, or materialization boundaries for a Domain Agent Team Template."
---

# Isomer Admin Topic Team Specialize

Use this as the module-level operator workflow for Topic Team Specialization. It helps an operator start from a Research Topic, resolve Project and Topic Workspace context, write high-level user-editable intent through semantic labels, create or update operator-owned target specs, route environment materialization to service skills, adapt one Domain Agent Team Template into copied topic-specific material, validate static material readiness, maintain durable setup state, and write a final topic-team summary. The canonical setup path is `team specialization invoked -> resolve-project -> resolve-topic-intent -> resolve-topic-env-gate -> create topic env target spec -> setup-topic-env -> specialize-team when team material is needed -> resolve-agent-env-gate -> create agent env target spec -> setup-agent-env -> validate-topic-team -> finalize-topic-team`. Always resolve intent and target-spec surfaces through Workspace Path Resolution before reading, writing, or reporting them: `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.agent_env_requirements`, `topic.env.topic_setup_target_spec`, and `topic.env.agent_setup_target_spec`. Route Topic Workspace dependency, Pixi, Topic Main Development Repository setup, canonical external repo acquisition, external projection materialization, and topic-root or repo-specific command verification work only through `isomer-srv-topic-env-setup` from `setup-topic-env`, after `ensure-topic-registration` has proved manifest-backed topic refs, a resolvable Topic Workspace Pixi binding, and a usable `topic.intent.topic_env_requirements` surface or explicit topic target spec. Record that output as Topic Workspace predecessor evidence, not as per-Agent Workspace cwd readiness. When per-Agent Workspace cwd command proof, selected-agent repair, or launch-facing Agent Workspace readiness is requested, require `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, Topic Workspace predecessor evidence, Topic Main Development Repository predecessor evidence, projection predecessor evidence when required, semantic label evidence for `topic.repos.main`, `agent.workspace`, and required `agent.*` support paths, and authoritative Agent Names; then delegate worktree creation and cwd verification to `isomer-srv-agent-env-setup` from `setup-agent-workspace`. Use `isomer-admin-topic-workspace-mgr` only for optional topology inspection, branch helpers, boundary summaries, or legacy compatibility diagnostics. This skill does not run the team, create live Agent Instances, mutate Workspace Runtime, or launch execution adapters.

## Planning Required

Topic Team Specialization is a complicated, multi-stage process with many predecessor artifacts, semantic path bindings, service handoffs, and readiness distinctions. It is easy to skip a required intent surface, confuse topic-level readiness with per-Agent Workspace readiness, or mutate the wrong layer. Before executing any nontrivial invocation, use the agent's built-in planning tool to break the request into stages and substeps, name predecessor artifacts for each step, identify which subcommand owns each action, and track blockers as the work proceeds. Update the plan as substeps complete, and proceed carefully rather than relying on memory of the canonical flow.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Default help mode**:
   - Match when this skill is invoked without a prompt.
   - Select `help`, load [references/help.md](references/help.md), execute its workflow, and report its output.
2. **Manual mode**:
   - Match when the user asks for help, names one subcommand, or asks for one bounded operation.
   - Select that subcommand from the **Subcommands** tables.
   - Guardrail: load only its detail page.
   - Load only its detail page, execute its workflow, and report its output.
3. **Guided mode**:
   - Match when the user asks to specialize step by step, proceed interactively, or confirm each stage.
   - Select `step-by-step`, load [references/step-by-step.md](references/step-by-step.md), and execute the static topic-team setup path one step at a time.
4. **Automatic mode**:
   - Match when the user asks to fully specialize, prepare, adapt end-to-end, or says `fast-forward`.
   - Select `fast-forward`, load [references/fast-forward.md](references/fast-forward.md), and execute the static topic-team setup path through `finalize-topic-team`.
   - Stop at the approval or materialization boundary unless explicitly instructed otherwise.
5. Prefer the narrowest subcommand family:
   - Prefer a procedural subcommand when the user names a public single-step workflow action.
   - Prefer a helper subcommand only when the user explicitly asks for a lower-level implementation step.
   - Prefer `help` for unclear empty invocations.
6. Preserve the **Guardrails** and **Output Contract** for all modes.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the project context, copied-template constraints, subcommands, output contract, and guardrails in this skill, then execute the plan.

## User-Facing Flow

The normal procedural flow is:

```text
init-topic
  -> resolve-topic-intent
  -> clarify-topic (optional)
  -> ensure-topic-registration
  -> resolve-topic-env-gate
  -> setup-topic-env (create topic target spec, then materialize topic env, topic-main, and projections)
  -> specialize-team
  -> clarify-topic-team (optional)
  -> setup-topic-env (optional rerun when specialization changes runnable requirements)
  -> resolve-agent-env-gate
  -> setup-agent-workspace (create agent target spec, then materialize worktrees and cwd readiness through agent env setup)
  -> validate-topic-team
  -> finalize-topic-team
  -> approve-profile / materialize-profile when explicitly requested
```

`fast-forward` runs this path automatically where possible. `step-by-step` runs the same path but asks the user to confirm before each stage.

When `init-topic` receives a user-supplied clear concrete Research Topic without an explicit output directory, it derives a provisional topic workspace seed under the effective Topic Workspace base, normally `isomer-content/topic-ws/<topic-slug>/`. A Project Manifest default topic, the id `default`, a literal `default Research Topic`, or any other generic placeholder statement is not enough topic substance by itself; ask the user for the actual research topic before creating files. Before specialization or setup proceeds from a provisional seed, run `ensure-topic-registration` to verify or create Project Manifest-backed Research Topic and Topic Workspace refs, verify the Topic Workspace Pixi binding required by environment setup, and report blockers.

## Subcommands

Load only the subcommand pages needed for the user's task.

### Procedural Subcommands

Procedural subcommands are the public single-step workflow API.

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `init-topic` | Create or select a provisional topic workspace seed for a new or unclear Research Topic | [references/init-topic.md](references/init-topic.md) |
| `resolve-topic-intent` | Resolve the Research Topic into `topic.intent.overview` before setup or specialization | [references/resolve-topic-intent.md](references/resolve-topic-intent.md) |
| `clarify-topic` | Refine the Research Topic and update `topic.intent.overview` open questions before team specialization | [references/clarify-topic.md](references/clarify-topic.md) |
| `ensure-topic-registration` | Verify or create authoritative Project Manifest-backed Research Topic and Topic Workspace registration before registration-dependent work | [references/ensure-topic-registration.md](references/ensure-topic-registration.md) |
| `resolve-topic-env-gate` | Resolve high-level Topic Workspace environment requirements into `topic.intent.topic_env_requirements` | [references/resolve-topic-env-gate.md](references/resolve-topic-env-gate.md) |
| `specialize-team` | Select a Domain Agent Team Template and run the topic-team specialization path | [references/specialize-team.md](references/specialize-team.md) |
| `clarify-topic-team` | Revise specialized topic-team outputs before setup, approval, or materialization | [references/clarify-topic-team.md](references/clarify-topic-team.md) |
| `setup-topic-env` | Create or validate the topic env target spec, then delegate Topic Workspace, topic-main, external repo, projection, dependency, and verification materialization to `isomer-srv-topic-env-setup` | [references/setup-topic-env.md](references/setup-topic-env.md) |
| `resolve-agent-env-gate` | Resolve high-level per-Agent Workspace cwd requirements into `topic.intent.agent_env_requirements` | [references/resolve-agent-env-gate.md](references/resolve-agent-env-gate.md) |
| `setup-agent-workspace` | Create or validate the agent env target spec, then delegate per-agent worktree creation and cwd proof to `isomer-srv-agent-env-setup` after topic-main predecessor evidence exists | [references/setup-agent-workspace.md](references/setup-agent-workspace.md) |
| `validate-topic-team` | Check topic definition, specialized team material, environment posture, Agent Workspaces, deferrals, and blockers | [references/validate-topic-team.md](references/validate-topic-team.md) |
| `finalize-topic-team` | Write `isomer-topic-summary.md` with the topic team, goal, working logic, setup, validation, blockers, and next actions | [references/finalize-topic-team.md](references/finalize-topic-team.md) |
| `approve-profile` | Review draft profile material and prepare bundle-local approval provenance | [references/approve-profile.md](references/approve-profile.md) |
| `materialize-profile` | Validate and write an approved Topic Agent Team Profile Bundle under the selected Topic Workspace | [references/materialize-profile.md](references/materialize-profile.md) |

### Helper Subcommands

Helper subcommands are five lower-level implementation commands called by procedural subcommands. They remain callable for manual operation.

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `resolve-project` | Resolve Project, Research Topic, Topic Workspace, template refs, profile refs, provisional status, and blockers | [references/resolve-project.md](references/resolve-project.md) |
| `inspect-template` | Inspect Domain Agent Team Template manifests, placeholders, roles, Workflow Stages, copyable material, and diagnostics | [references/inspect-template.md](references/inspect-template.md) |
| `resolve-context` | Resolve Effective Topic Context, policies, bindings, provider refs, and packet/profile refs needed for static material | [references/resolve-context.md](references/resolve-context.md) |
| `map-placeholders` | Map template placeholders to topic values, copied material plans, topic edits, deferrals, blockers, and packet-shaped provenance | [references/map-placeholders.md](references/map-placeholders.md) |
| `draft-profile` | Draft reviewable Topic Agent Team Profile Bundle material from specialization outputs | [references/draft-profile.md](references/draft-profile.md) |

### Misc Subcommands

Misc subcommands are public support commands and shortcuts.

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `help` | Print what this skill does, how to invoke it, available modes, subcommands, outputs, and guardrails | [references/help.md](references/help.md) |
| `fast-forward` | Automatically execute the full topic-team setup path through final topic-team summary output | [references/fast-forward.md](references/fast-forward.md) |
| `step-by-step` | Execute the same required setup path as `fast-forward`, but pause for user confirmation before each step | [references/step-by-step.md](references/step-by-step.md) |

## Generated Guide Rule

If the copied template root lacks `team-specialization-guide.md`, create one before planning. Put this exact fenced block near the top:

````markdown
```generated-guide
Generated Guide: This file was generated by the Project Operator Session from copied Domain Agent Team Template material because no source `team-specialization-guide.md` existed.

Review before treating it as authoritative.
```
````

The generated guide must still explain placeholders and definitions, assumptions, how the team works, contracts used by the team, and an example cooperation flow. Mark uncertain interpretations as assumptions instead of hiding them.

## Plan Structure

Create `team-specialization-plan.md` before editing copied material. Use this structure:

```markdown
# Team Specialization Plan

## Topic Context

## Copied Template Root

## Adaptation Checklist

- [ ] Resolve topic and workspace identifiers.
- [ ] Resolve role bindings, agent workspaces, skill bindings, capability bindings, and policy refs.
- [ ] Rewrite topic-facing instructions and examples in copied material.
- [ ] Record deferrals and static-material blockers.
- [ ] Validate packet/profile inputs and copied material paths.

## Planned Edits

## Validation Plan

## Final Report
```

Leave `Final Report` empty or marked pending until adaptation is complete. After adaptation, fill it with completed edits, deferred edits, generated-guide status, validation status, packet/profile outputs, and unresolved blockers.

## Output Contract

When reporting results, include these fields in structured prose or JSON, depending on the caller's print mode:

- `research_topic_ref`: the resolved Research Topic or provisional topic label.
- `topic_workspace_ref`: the resolved Topic Workspace or provisional topic workspace seed.
- `topic_overview_label`: `topic.intent.overview` when topic material was created or revised.
- `topic_overview_path`: the resolved `topic.intent.overview` path, defaulting under `<topic-workspace>/intent/src/topic-overview.md`.
- `topic_registration_status`: registered, provisional, blocked, or not checked.
- `registration_command_evidence`: supported Isomer CLI/API command evidence used to create or verify registration, or `not needed` when no mutation was required.
- `registered_research_topic_ref`: the Project Manifest-backed Research Topic ref when registration is verified.
- `registered_topic_workspace_ref`: the Project Manifest-backed Topic Workspace ref when registration is verified.
- `environment_binding_status`: active, implicit-default, blocked, or not checked for the explicit `topic_standalone_pixi_bindings.manifest_path_or_dir` target or implicit Topic Workspace directory default needed by `isomer-srv-topic-env-setup`.
- `environment_binding_ref`: the binding source, `manifest_path_or_dir`, Pixi-resolved manifest path, and Pixi environment when available.
- `registration_blockers`: missing topic statement, unsafe path, colliding workspace, unsupported config mutation, missing environment binding, or other blockers from `ensure-topic-registration`.
- `selected_domain_team_template_ref`: the selected Domain Agent Team Template.
- `domain_team_template_ref`: the source Domain Agent Team Template when specialization has begun.
- `copied_template_root`: usually `<topic-workspace>/team-profile/execplan/` for `deepsci-mini`.
- `team_specialization_guide_path`: the copied or generated `team-specialization-guide.md`.
- `team_specialization_plan_path`: the `team-specialization-plan.md` with checklist and `Final Report`.
- `changed_copied_material_paths`: copied-root files edited for the topic.
- `placeholder_resolutions`: concrete topic values for template placeholders.
- `topic_team_revision_status`: unchanged, revised, blocked, or not requested.
- `topic_environment_status`: ready, changed, deferred, blocked, or not checked, mapped from `isomer-srv-topic-env-setup` Topic Workspace predecessor readiness output when environment setup runs.
- `topic_env_source_label`: `topic.intent.topic_env_requirements` when topic env source intent is resolved or used.
- `topic_env_source_path`: the resolved `topic.intent.topic_env_requirements` path, defaulting under `<topic-workspace>/intent/src/topic-env-gate.md`.
- `topic_env_target_spec_label`: `topic.env.topic_setup_target_spec` when the operator flow creates, validates, or supplies the operational target spec used by `isomer-srv-topic-env-setup`.
- `topic_env_target_spec_path`: the resolved `topic.env.topic_setup_target_spec` path, defaulting under `<topic-workspace>/intent/derived/isomer-env-gate.md`.
- `topic_environment_service_output`: summarized `isomer-srv-topic-env-setup` output, including service subcommand, mode, Topic Workspace predecessor readiness status, Topic Main Development Repository Git state, projection metadata, resource check status for heavy setup or verification commands, commands run, changed files, per-agent readiness not checked when reported, and blockers when present.
- `agent_env_source_label`: `topic.intent.agent_env_requirements` when agent env setup consumes source intent.
- `agent_env_source_path`: the resolved `topic.intent.agent_env_requirements` path, defaulting under `<topic-workspace>/intent/src/agent-env-gate.md`.
- `agent_env_target_spec_label`: `topic.env.agent_setup_target_spec` when the operator flow creates, validates, or supplies the per-agent operational target spec used by `isomer-srv-agent-env-setup`.
- `agent_env_target_spec_path`: the resolved `topic.env.agent_setup_target_spec` path, defaulting under `<topic-workspace>/intent/derived/isomer-agent-env-gate.md`.
- `agent_environment_service_output`: summarized `isomer-srv-agent-env-setup` output, including service subcommand, Topic Main Development Repository predecessor evidence, projection predecessor evidence, Agent Names, resolved `agent.workspace` paths, branch plan, worktree status by agent, tmp ignore posture, resource check status for heavy per-agent verification commands, readiness by agent, overall readiness, commands run, changed files, blockers, and next action.
- `semantic_paths`: delegated resolved labels, paths, path sources, and blockers for Topic Main Development Repository, projection labels, Agent Workspace, local tmp labels, and worker-facing support labels when setup runs.
- `agent_workspace_paths`: per-agent resolved `agent.workspace` paths or blockers, including delegated Git-backed worktree paths, semantic labels, path sources, and `agent_workspace_ref` evidence when available.
- `isomer_managed_path_status`: delegated `isomer-managed/` tracked, agent-owned, topic-owned, and generated-link regime evidence when Git-backed Agent Workspaces are requested.
- `local_tmp_path_status`: delegated `topic.repos.main.tmp` and `agent.tmp` local ignored disposable posture when Git-backed Agent Workspaces are requested; tmp contents are not durable readiness evidence.
- `topic_team_validation_status`: ready, ready-with-deferrals, blocked, or not checked for static material readiness.
- `isomer_topic_summary_path`: the `isomer-topic-summary.md` path when finalization runs.
- `deferrals`: unresolved items, with static-material or later-operation impact.
- `packet_profile_inputs`: proposed Topic Team Instantiation Packet and Topic Agent Team Profile Bundle inputs.
- `validation_status`: commands or validators run, plus any blockers.
- `next_operator_action`: usually clarify topic, ensure topic registration, specialize team, setup environment, validate, finalize, request approval, materialize an approved bundle, hand off to a later runtime workflow, or stop on blockers.

## Guardrails

Do not edit the Domain Agent Team Template source while specializing a topic. The source template remains topic-neutral.

Do not treat a provisional topic workspace seed as an authoritative Isomer Research Topic or Topic Workspace registration. Stop at the registration boundary or route through `ensure-topic-registration`, which may use `isomer-cli project topics create <topic-id> --statement "<research topic>" --workspace-dir <topic-workspace-dir>` and related supported Isomer CLI/API surfaces instead of hand-editing `.isomer-labs/manifest.toml` or Research Topic Config files.

Do not call `isomer-srv-topic-env-setup` from a provisional Topic Workspace or from a registered topic whose effective Topic Workspace Pixi binding cannot be resolved. Require `ensure-topic-registration` evidence first. Accept an explicit `topic_standalone_pixi_bindings.manifest_path_or_dir` target or the implicit registered Topic Workspace directory default when Pixi resolves it as confined to the Topic Workspace; otherwise report the Pixi binding blocker instead of editing Project Config by hand.

Do not run a procedural subcommand when required predecessor artifacts are missing. Refuse to run, name the missing artifacts, explain which previous subcommand should create them, and stop before mutation.

Do not hide environment installation, Agent Workspace creation, static-material validation, profile approval, or profile materialization behind earlier topic clarification or specialization commands.

Do not require Topic Agent Team Profile material, `team-profile/`, Agent Team Instance records, Agent Workspace plans, roles, or agent count before `setup-topic-env`. That operator subcommand needs manifest-backed topic registration, Topic Workspace Pixi binding evidence, and a usable `topic.intent.topic_env_requirements` surface or an explicit manual topic env target spec.

Do not perform dependency inference, repo acquisition, Pixi installation, package repair, or environment verification directly inside `setup-topic-env`. Prepare the operator handoff and route heavy Topic Workspace environment setup through `isomer-srv-topic-env-setup`.

Do not perform `topic.intent.agent_env_requirements` translation, Agent Workspace worktree creation, per-agent cwd command verification, or selected-agent repair directly inside `setup-agent-workspace`. Prepare the operator handoff and route that work through `isomer-srv-agent-env-setup` only after source `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, Topic Workspace predecessor evidence, Topic Main Development Repository predecessor evidence, required projection predecessor evidence, and authoritative Agent Names exist.

Do not ask service skills to prove readiness by overloading the host. When setup or verification would run resource-heavy work such as compilation, deep model inference, full dataset download, large archive extraction, or broad test suites, require the delegated service output to include a conservative resource check, a bounded smoke-test or deferred-verification decision, and blockers when capacity is insufficient or unclear.

Do not call `isomer-srv-agent-env-setup` without a usable `topic.intent.agent_env_requirements` surface or an explicit manual agent env target spec. If the user did not create source intent and the task clearly states what every planned Agent Workspace cwd must be able to run, route to `resolve-agent-env-gate`; otherwise ask for the per-agent cwd readiness target and stop before service delegation.

Do not create a directory named `teams` under a Topic Workspace for topic-specific profiles. Store topic-specific copied material inside `<topic-workspace>/team-profile/`, and keep only discovery refs in the Project Manifest.

Do not bypass Topic Team Instantiation Packet validation, Topic Agent Team Profile validation, user or deterministic approval provenance, or profile materialization checks.

Do not treat generated guides as authoritative template source. They are copied-root explanations that need review before reuse.

Do not run live teams, create Agent Instances, mutate Workspace Runtime, or launch execution adapters from this skill. Live operation belongs to a later runtime workflow.
