---
name: isomer-op-topic-team-specialize
description: "Use only when the user explicitly invokes Topic Team Specialization or the prompt or authoritative context establishes a formal Agent Team target and applies the requested action to that team. Initialize and specialize one Isomer Research Topic into static topic-team material through direct requests such as specialize a team path over a topic, help, init-topic, resolve-topic-intent, clarify-topic, ensure-topic-registration, resolve-topic-env-gate, adapt-team-template, clarify-topic-team, setup-topic-env through isomer-srv-topic-env-setup, resolve-agent-env-gate, setup-agent-workspace, validate-topic-team, finalize-topic-team, approval, or materialization boundaries for a Domain Agent Team Template."
---

# Isomer Admin Topic Team Specialize

Use this as the module-level operator workflow for Topic Team Specialization. It helps an operator start from a Research Topic, consume or delegate reusable topic preparation, resolve Project and Topic Workspace context, write high-level user-editable intent through semantic labels, create or update operator-owned target specs, route environment materialization to service skills, adapt one Domain Agent Team Template into copied topic-specific material, validate static material readiness, maintain durable setup state, and write a final topic-team summary. The canonical procedural dependency graph is recorded in [references/step-dependencies.json](references/step-dependencies.json); query it with [scripts/query_step_dependencies.py](scripts/query_step_dependencies.py) instead of reconstructing dependency paths from prose. Prepared-topic evidence from `isomer-op-topic-creator` summaries, Topic Workspace registration, and Topic Manager topology evidence can satisfy reusable prerequisites such as Research Topic refs, Topic Workspace refs, topic overview, Workspace Runtime readiness, topic environment readiness, `topic.repos.main` readiness, current Topic Actor roster, and Topic Actor Workspace refs. Always resolve intent and target-spec surfaces through Workspace Path Resolution before reading, writing, or reporting them: `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.agent_env_requirements`, `topic.env.topic_setup_target_spec`, and `topic.env.agent_setup_target_spec`. Route Topic Workspace dependency, Pixi, Topic Main Development Repository setup, canonical external repo acquisition, external projection materialization, and topic-root or repo-specific command verification work only through `isomer-srv-topic-env-setup` from `setup-topic-env`, after `ensure-topic-registration` or prepared-topic evidence has proved manifest-backed topic refs, a resolvable Topic Workspace Pixi binding, and a usable `topic.intent.topic_env_requirements` surface or explicit topic target spec. Record that output as Topic Workspace predecessor evidence, not as per-Agent Workspace cwd readiness. When per-Agent Workspace cwd command proof, selected-agent repair, or launch-facing Agent Workspace readiness is requested, require `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, Topic Workspace predecessor evidence, Topic Main Development Repository predecessor evidence, projection predecessor evidence when required, semantic label evidence for `topic.repos.main`, `agent.workspace`, and required `agent.*` support paths, and authoritative Agent Names; then delegate worktree creation and cwd verification to `isomer-srv-agent-env-setup` from `setup-agent-workspace`. Use `isomer-op-topic-mgr` storage, actor, team, and environment verification commands for existing Topic Actor topology preservation, actor-scoped diagnostics, optional topology inspection, branch helpers, boundary summaries, stale topology repair, or topology diagnostics. Route Houmao loop explanation, adapter customization guidance, Domain Agent Team Template to Houmao mapping, mailbox or gateway support, and runtime inspection to `isomer-srv-houmao-interop` only as bounded service support. This skill does not run the team, create live Agent Instances, delete Topic Actors, mutate Workspace Runtime, or launch execution adapters.

## Planning Required

Topic Team Specialization is a complicated, multi-stage process with many predecessor artifacts, semantic path bindings, service handoffs, and readiness distinctions. It is easy to skip a required intent surface, confuse topic-level readiness with per-Agent Workspace readiness, or mutate the wrong layer. Before executing any nontrivial invocation, use the agent's built-in planning tool to break the request into stages and substeps, name predecessor artifacts for each step, identify which subcommand owns each action, and track blockers as the work proceeds. Update the plan as substeps complete, and proceed carefully rather than relying on memory of the canonical flow.

## Intent Routing

Treat natural-language requests such as `specialize <team-path> over topic <topic>`, `specialize this team for this topic`, or `adapt this template to this research topic` as full Topic Team Specialization requests. Select `fast-forward` by default, carrying the supplied team path as the selected Domain Agent Team Template and the supplied topic as the Research Topic input. Select `step-by-step` only when the user asks to proceed interactively or confirm each stage.

Do not route direct "specialize team" language to `adapt-team-template`. That subcommand is an internal stage for adapting copied template material after topic intent, registration, and environment predecessor work exist. Route directly to `adapt-team-template` only when the user explicitly names `adapt-team-template` or asks for the internal template-adaptation stage and the required predecessor artifacts already exist.

Before planning, template discovery, or mutation, confirm how this skill was selected. A direct user invocation of `isomer-op-topic-team-specialize` or a named specialization subcommand establishes specialization intent. A delegated request must preserve prompt or authoritative context that identifies a formal Agent Team target and asks to deploy, specialize, instantiate, materialize, validate, repair, launch, or use that team. If a delegated request contains only generic topic preparation, launch-facing language, readiness gaps, missing summaries, missing Agent Workspaces, a Research Topic, or Topic Workspace context, return it to `isomer-op-topic-creator`, `isomer-op-topic-mgr`, or the applicable setup owner without entering automatic mode or searching for a Domain Agent Team Template.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Default help mode**:
   - Match when this skill is invoked without a prompt.
   - Select `help`, load [references/help.md](references/help.md), execute its workflow, and report its output.
2. **Manual mode**:
   - Match when the user asks for help, explicitly names one subcommand, or asks for one bounded operation.
   - Do not treat the verb `specialize` in a natural-language request as explicit selection of the internal `adapt-team-template` stage.
   - Select that subcommand from the **Subcommands** tables.
   - Guardrail: load only its detail page.
   - Load only its detail page, execute its workflow, and report its output. If required predecessor artifacts are missing, apply **Targeted Fast-Forward Recovery** before any mutation.
3. **Guided mode**:
   - Match when the user asks to specialize step by step, proceed interactively, or confirm each stage.
   - Select `step-by-step`, load [references/step-by-step.md](references/step-by-step.md), and execute the static topic-team setup path one step at a time.
4. **Automatic mode**:
   - Match when direct invocation or preserved formal Agent Team context is established and the user asks to fully specialize, prepare the selected Agent Team, adapt the selected team end-to-end, says `fast-forward`, or gives a direct command like `specialize <team-path> over topic <topic>`.
   - Select `fast-forward`, load [references/fast-forward.md](references/fast-forward.md), and execute the static topic-team setup path through `finalize-topic-team`.
   - If prepared-topic evidence is missing, create or consume topic setup evidence before team-specific stages.
   - Stop at the approval or materialization boundary unless explicitly instructed otherwise.
5. Prefer the narrowest subcommand family:
   - Prefer a procedural subcommand when the user names a public single-step workflow action.
   - Prefer a helper subcommand only when the user explicitly asks for a lower-level implementation step.
   - Prefer `help` for unclear empty invocations.
6. Preserve the **Guardrails** and **Output Contract** for all modes.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the project context, copied-template constraints, subcommands, output contract, and guardrails in this skill, then execute the plan.

## Targeted Fast-Forward Recovery

When a selected procedural subcommand cannot run because required predecessor artifacts are missing, do not stop with only a refusal. Refuse to run the subcommand directly, name the missing predecessor artifacts, then offer targeted fast-forward recovery to the selected subcommand.

Targeted fast-forward is bounded by the selected subcommand. It is not the same as full `fast-forward`, which runs the topic-team setup path through `finalize-topic-team`. Query [scripts/query_step_dependencies.py](scripts/query_step_dependencies.py) to compute the path:

```bash
python scripts/query_step_dependencies.py path --target <subcommand> --include-target
python scripts/query_step_dependencies.py path --target <subcommand> --exclude-target
python scripts/query_step_dependencies.py explain --target <subcommand>
```

The script reads [references/step-dependencies.json](references/step-dependencies.json). It describes expected dependency paths, prerequisite artifacts, produced outputs, mutation notes, and unrecoverable blockers; it does not verify that those artifacts exist in the current workspace.

Use these recovery modes:

- **Inclusive**, default: run the missing predecessor stages in canonical order, then run the selected subcommand when its prerequisites are satisfied.
- **Exclusive**: run the missing predecessor stages in canonical order, then stop before the selected subcommand and report that the target is ready or name any remaining blocker.

Before targeted fast-forward mutates the workspace, ask the user to confirm inclusive mode, choose exclusive mode, or stop, unless the user already gave clear permission to proceed automatically. Mutating recovery includes creating or updating topic intent, registration, derived target specs, environment material, topic-team material, Agent Workspace material, validation summaries, approval material, or materialized profile material.

Use this concise response pattern when prerequisites are missing:

```text
Cannot run <subcommand> directly because <missing predecessor artifacts>.

I can fast-forward to <subcommand>.

Default, inclusive:
run the path returned by `query_step_dependencies.py path --target <subcommand> --include-target`.

Alternative, exclusive:
run the path returned by `query_step_dependencies.py path --target <subcommand> --exclude-target`.

Reply "yes" for the default inclusive path, "exclusive", or "stop".
```

If the missing input is not recoverable from the canonical flow, ask for the specific missing information instead of inventing topic substance, runnable requirements, Agent Names, selected-agent scope, cwd readiness criteria, approval provenance, or safety decisions. Targeted recovery stops on the same clarification, registration, environment-binding, resource-safety, and live-runtime blockers as the normal flow.

## User-Facing Flow

The normal procedural flow is:

```text
init-topic
  -> resolve-topic-intent
  -> clarify-topic (optional)
  -> ensure-topic-registration
  -> resolve-topic-env-gate
  -> setup-topic-env (create topic target spec, then materialize topic env, topic-main, and projections)
  -> adapt-team-template
  -> clarify-topic-team (optional)
  -> setup-topic-env (optional rerun when specialization changes runnable requirements)
  -> resolve-agent-env-gate
  -> setup-agent-workspace (create agent target spec, then materialize worktrees and cwd readiness through agent env setup)
  -> validate-topic-team
  -> finalize-topic-team
  -> approve-profile / materialize-profile when explicitly requested
```

`fast-forward` runs this full path automatically where possible. It can consume prepared-topic evidence instead of recreating common preparation artifacts, and it must preserve active Topic Actor bindings and Topic Actor Workspace refs. `step-by-step` runs the same path but asks the user to confirm before each stage. Targeted fast-forward recovery runs only the predecessor path returned by `scripts/query_step_dependencies.py`, then either runs that subcommand in inclusive mode or stops before it in exclusive mode.

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
| `adapt-team-template` | Internal stage that selects or confirms a Domain Agent Team Template, copies it into the Topic Workspace, maps placeholders, and adapts copied template material after prerequisites exist | [references/adapt-team-template.md](references/adapt-team-template.md) |
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

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format. When important handoff detail is omitted, say that Complete Output is available on request.

### Essential Output

Lead with the Topic Team Specialization, validation, or setup outcome. Name the Research Topic and Topic Workspace, registration posture, selected Domain Agent Team Template, and copied material status. Include important created or changed paths, Topic and Agent environment readiness when checked, validation, blockers or deferrals, and the next safe operator step.

Treat `topic-overview.md` as the canonical topic overview artifact and keep execution plans under `<topic-workspace>/team-profile/execplan/`; mention those paths only when they materially affect the result.

### Complete Output

When requested, include grouped handoff and audit fields:

- **Identity and registration**: `research_topic_ref`, `topic_workspace_ref`, `topic_overview_label`, `topic_overview_path`, `topic_registration_status`, `registration_command_evidence`, `registered_research_topic_ref`, `registered_topic_workspace_ref`, `environment_binding_status`, `environment_binding_ref`, and `registration_blockers`.
- **Prepared topic and actors**: reused common preparation refs, current Topic Actor roster, Topic Actor Workspace refs, actor blockers, and coexistence notes.
- **Template adaptation**: `selected_domain_team_template_ref`, `domain_team_template_ref`, `copied_template_root`, `team_specialization_guide_path`, `team_specialization_plan_path`, `changed_copied_material_paths`, `placeholder_resolutions`, and `topic_team_revision_status`.
- **Topic environment**: `topic_environment_status`, `topic_env_source_label`, `topic_env_source_path`, `topic_env_target_spec_label`, `topic_env_target_spec_path`, and summarized or full `topic_environment_service_output`.
- **Agent environment**: `agent_env_source_label`, `agent_env_source_path`, `agent_env_target_spec_label`, `agent_env_target_spec_path`, and summarized or full `agent_environment_service_output`.
- **Workspace paths**: `semantic_paths`, semantic labels, path sources, `agent_workspace_paths`, `isomer-managed/` path status, and `local_tmp_path_status`.
- **Validation and finalization**: `topic_team_validation_status`, `isomer_topic_summary_path`, `deferrals`, `packet_profile_inputs`, `validation_status`, blockers, and `next_operator_action`.

## Guardrails

Do not edit the Domain Agent Team Template source while specializing a topic. The source template remains topic-neutral.

Do not treat a provisional topic workspace seed as an authoritative Isomer Research Topic or Topic Workspace registration. Stop at the registration boundary or route through `ensure-topic-registration`, which may use `isomer-cli project topics create <topic-id> --statement "<research topic>" --workspace-dir <topic-workspace-dir>` and related supported Isomer CLI/API surfaces instead of hand-editing `.isomer-labs/manifest.toml` or Research Topic Config files.

Do not call `isomer-srv-topic-env-setup` from a provisional Topic Workspace or from a registered topic whose effective Topic Workspace Pixi binding cannot be resolved. Require `ensure-topic-registration` evidence first. Accept an explicit `topic_standalone_pixi_bindings.manifest_path_or_dir` target or the implicit registered Topic Workspace directory default when Pixi resolves it as confined to the Topic Workspace; otherwise report the Pixi binding blocker instead of editing Project Config by hand.

Do not run a procedural subcommand directly when required predecessor artifacts are missing. Refuse the direct run, name the missing artifacts, offer targeted fast-forward recovery, and stop before mutation until the user confirms inclusive mode, chooses exclusive mode, or has already given clear permission to proceed automatically.

Do not hide environment installation, Agent Workspace creation, static-material validation, profile approval, or profile materialization behind earlier topic clarification or specialization commands.

Do not require Topic Agent Team Profile material, `team-profile/`, Agent Team Instance records, Agent Workspace plans, roles, or agent count before `setup-topic-env`. That operator subcommand needs manifest-backed topic registration, Topic Workspace Pixi binding evidence, and a usable `topic.intent.topic_env_requirements` surface or an explicit manual topic env target spec.

Do not perform dependency inference, repo acquisition, Pixi installation, package repair, or environment verification directly inside `setup-topic-env`. Prepare the operator handoff and route Topic Workspace environment setup through `isomer-srv-topic-env-setup`.

Do not perform `topic.intent.agent_env_requirements` translation, Agent Workspace worktree creation, per-agent cwd command verification, or selected-agent repair directly inside `setup-agent-workspace`. Prepare the operator handoff and route that work through `isomer-srv-agent-env-setup` only after source `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, Topic Workspace predecessor evidence, Topic Main Development Repository predecessor evidence, required projection predecessor evidence, and authoritative Agent Names exist.

Do not delete, archive, or repurpose active Topic Actor bindings or Topic Actor Workspaces during Topic Team Specialization. Preserve them unless the user explicitly asks for Topic Actor archive or repair through `isomer-op-topic-mgr actors-manage`.

Do not ask service skills to prove readiness by overloading the host, but do not allow them to skip essential source-intent code paths. Require delegated env setup output to include:

- `operation_classification` from `isomer-misc-bounded-run-tips`, including classification source, result, reason, resource dimensions, and affected scope.
- bounded-run guidance, resource check evidence, bounded real-path command, expected result, and blocker condition for operations classified as `heavy` or `unknown-risk`.
- a no-plan reason for operations classified as `light` or `not-applicable`.
- blocker evidence when no bounded real-path command can safely exercise the required source-intent path.

Examples of bounded tactics include fewer build jobs, selected build targets, tiny model or tensor shapes, sample data, reduced iterations, reduced batch size, selected tests, and short benchmark cases. These are examples; bounded-run tips owns the classification decision. A generic smoke test that misses the requested build, inference, dataset, or benchmark path is not enough to claim readiness.

Do not call `isomer-srv-agent-env-setup` without a usable `topic.intent.agent_env_requirements` surface or an explicit manual agent env target spec. If the user did not create source intent and the task clearly states what every planned Agent Workspace cwd must be able to run, route to `resolve-agent-env-gate`; otherwise ask for the per-agent cwd readiness target and stop before service delegation.

Do not create a directory named `teams` under a Topic Workspace for topic-specific profiles. Store topic-specific copied material inside `<topic-workspace>/team-profile/`, and keep only discovery refs in the Project Manifest.

Do not bypass Topic Team Instantiation Packet validation, Topic Agent Team Profile validation, user or deterministic approval provenance, or profile materialization checks.

Do not treat generated guides as authoritative template source. They are copied-root explanations that need review before reuse.

Do not run live teams, create Agent Instances, mutate Workspace Runtime, or launch execution adapters from this skill. Live operation belongs to a later runtime workflow.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
