---
name: isomer-admin-topic-team-specialize
description: "Initialize and specialize Isomer Research Topics into static topic-team material. Use when an operator needs topic-team setup for one Research Topic: help, init-topic, clarify-topic, specialize-team, clarify-topic-team, setup-topic-env, setup-agent-workspace, validate-topic-team, finalize-topic-team, approval, or materialization boundaries for a Domain Agent Team Template."
---

# Isomer Admin Topic Team Specialize

Use this as the module-level operator workflow for Topic Team Specialization. It helps an operator start from a Research Topic, prepare topic definition material, adapt one Domain Agent Team Template into copied topic-specific material, prepare the topic environment and Agent Workspaces as durable setup state, validate static material readiness, and write a final topic-team summary. It does not run the team, create live Agent Instances, mutate Workspace Runtime, or launch execution adapters.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Default help mode**: If this skill is invoked without a prompt, select `help`, load [references/help.md](references/help.md), execute its workflow, and report its output.
2. **Manual mode**: If the user asks for help, names one subcommand, or asks for one bounded operation, select that subcommand from the **Subcommands** tables, load only its detail page, execute its workflow, and report its output.
3. **Guided mode**: If the user asks to specialize step by step, proceed interactively, or confirm each stage, select `step-by-step`, load [references/step-by-step.md](references/step-by-step.md), and execute the static topic-team setup path one step at a time.
4. **Automatic mode**: If the user asks to fully specialize, prepare, adapt end-to-end, or says `fast-forward`, select `fast-forward`, load [references/fast-forward.md](references/fast-forward.md), execute the static topic-team setup path through `finalize-topic-team`, and stop at the approval or materialization boundary unless explicitly instructed otherwise.
5. Prefer a procedural subcommand when the user names a public single-step workflow action. Prefer a helper subcommand only when the user explicitly asks for a lower-level implementation step. Prefer `help` for unclear empty invocations.
6. Preserve the **Guardrails** and **Output Contract** for all modes.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the project context, copied-template constraints, subcommands, output contract, and guardrails in this skill, then execute the plan.

## User-Facing Flow

The normal procedural flow is:

```text
init-topic
  -> clarify-topic (optional)
  -> specialize-team
  -> clarify-topic-team (optional)
  -> setup-topic-env
  -> setup-agent-workspace
  -> validate-topic-team
  -> finalize-topic-team
  -> approve-profile / materialize-profile when explicitly requested
```

`fast-forward` runs this path automatically where possible. `step-by-step` runs the same path but asks the user to confirm before each stage.

When `init-topic` receives a user-supplied clear concrete Research Topic without an explicit output directory, it derives a provisional topic workspace seed under the effective Topic Workspace base, normally `isomer-content/topic-ws/<topic-slug>/`. A Project Manifest default topic, the id `default`, or a generic `default Research Topic` statement created by `isomer-cli project init` is not enough topic substance by itself; ask the user for the actual research topic before creating files.

## Subcommands

Load only the subcommand pages needed for the user's task.

### Procedural Subcommands

Procedural subcommands are the public single-step workflow API.

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `init-topic` | Create a provisional topic workspace seed and `topic-overview.md` for a new or unclear Research Topic | [references/init-topic.md](references/init-topic.md) |
| `clarify-topic` | Refine the Research Topic and update topic overview open questions before team specialization | [references/clarify-topic.md](references/clarify-topic.md) |
| `specialize-team` | Select a Domain Agent Team Template and run the topic-team specialization path | [references/specialize-team.md](references/specialize-team.md) |
| `clarify-topic-team` | Revise specialized topic-team outputs before setup, approval, or materialization | [references/clarify-topic-team.md](references/clarify-topic-team.md) |
| `setup-topic-env` | Install or prepare the topic development environment with explicit setup records | [references/setup-topic-env.md](references/setup-topic-env.md) |
| `setup-agent-workspace` | Create or report per-agent Agent Workspace directories and boundaries | [references/setup-agent-workspace.md](references/setup-agent-workspace.md) |
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
- `topic_overview_path`: the `<topic-dir>/topic-def/topic-overview.md` path when topic material was created or revised.
- `topic_registration_status`: registered, provisional, blocked, or not checked.
- `selected_domain_team_template_ref`: the selected Domain Agent Team Template.
- `domain_team_template_ref`: the source Domain Agent Team Template when specialization has begun.
- `copied_template_root`: usually `<topic-workspace>/team-profile/execplan/` for `deepsci-mini`.
- `team_specialization_guide_path`: the copied or generated `team-specialization-guide.md`.
- `team_specialization_plan_path`: the `team-specialization-plan.md` with checklist and `Final Report`.
- `changed_copied_material_paths`: copied-root files edited for the topic.
- `placeholder_resolutions`: concrete topic values for template placeholders.
- `topic_team_revision_status`: unchanged, revised, blocked, or not requested.
- `topic_environment_status`: ready, changed, deferred, blocked, or not checked.
- `agent_workspace_paths`: per-agent Agent Workspace paths or blockers.
- `topic_team_validation_status`: ready, ready-with-deferrals, blocked, or not checked for static material readiness.
- `isomer_topic_summary_path`: the `isomer-topic-summary.md` path when finalization runs.
- `deferrals`: unresolved items, with static-material or later-operation impact.
- `packet_profile_inputs`: proposed Topic Team Instantiation Packet and Topic Agent Team Profile Bundle inputs.
- `validation_status`: commands or validators run, plus any blockers.
- `next_operator_action`: usually clarify topic, specialize team, setup environment, validate, finalize, request approval, materialize an approved bundle, hand off to a later runtime workflow, or stop on blockers.

## Guardrails

Do not edit the Domain Agent Team Template source while specializing a topic. The source template remains topic-neutral.

Do not treat a provisional topic workspace seed as an authoritative Isomer Research Topic or Topic Workspace registration. Stop at the registration boundary or route through supported Isomer CLI/API surfaces instead of hand-editing `.isomer-labs/manifest.toml`.

Do not run a procedural subcommand when required predecessor artifacts are missing. Refuse to run, name the missing artifacts, explain which previous subcommand should create them, and stop before mutation.

Do not hide environment installation, Agent Workspace creation, static-material validation, profile approval, or profile materialization behind earlier topic clarification or specialization commands.

Do not create a directory named `teams` under a Topic Workspace for topic-specific profiles. Store topic-specific copied material inside `<topic-workspace>/team-profile/`, and keep only discovery refs in the Project Manifest.

Do not bypass Topic Team Instantiation Packet validation, Topic Agent Team Profile validation, user or deterministic approval provenance, or profile materialization checks.

Do not treat generated guides as authoritative template source. They are copied-root explanations that need review before reuse.

Do not run live teams, create Agent Instances, mutate Workspace Runtime, or launch execution adapters from this skill. Live operation belongs to a later runtime workflow.
