---
name: isomer-admin-topic-team-specialize
description: Specialize a Domain Agent Team Template into topic-specific copied material for one Research Topic. Use this skill whenever the user asks an operator to instantiate, specialize, adapt, copy, or understand a domain team template for a topic, especially when `team-specialization-guide.md`, `team-specialization-plan.md`, Topic Team Instantiation Packet inputs, or Topic Agent Team Profile Bundle material are needed.
---

# Isomer Admin Topic Team Specialize

Use this as the module-level operator workflow for Domain Agent Team Template understanding and Topic Team Specialization. It helps an operator adapt one reusable domain team template for one research topic by copying template material into the topic workspace, guiding topic-specific edits, and producing reviewable packet/profile inputs.

## Operating Model

Run the workflow from a Project Operator Session or Operator Agent that is already pointed at the Isomer Project root, or that can resolve the project root from the user's prompt or current working directory.

Treat project awareness, template inspection, topic context resolution, placeholder reconciliation, profile drafting, review approval, materialization, and launch orchestration as local subcommands inside this module skill. The user should not have to invoke separate skills just to get copied topic-specialized template material.

Use this workflow for one Research Topic and one Domain Agent Team Template at a time. Topic-level parallelism means separate Research Topics can each have their own dedicated Topic Agent Team Profile Bundle; it does not mean one Research Topic should get multiple competing teams.

## Workflow

When this skill is invoked, choose one of four modes.

1. **Default help mode**: If this skill is invoked without a prompt, select `help`, load [references/help.md](references/help.md), execute its workflow, and report its output.
2. **Manual mode**: If the user asks for help, names one subcommand, or asks for one bounded operation, select that subcommand from the **Subcommands** table, load only its detail page, execute its workflow, and report its output.
3. **Guided mode**: If the user asks to specialize step by step, proceed interactively, or confirm each stage, select `step-by-step`, load [references/step-by-step.md](references/step-by-step.md), execute one required specialization step at a time, and wait for user confirmation before continuing.
4. **Automatic mode**: If the user asks to fully specialize, instantiate, adapt end-to-end, or says `fast-forward`, select `fast-forward`, load [references/fast-forward.md](references/fast-forward.md), execute the full specialization workflow, and stop at the approval/materialization/launch boundary unless explicitly instructed otherwise.
5. If the request is ambiguous, prefer manual mode when a single bounded operation is clearly named; prefer `step-by-step` when the user asks for guided confirmation; otherwise prefer `fast-forward` for a request to specialize a Domain Agent Team Template for a Research Topic.
6. Preserve the **Guardrails** and **Output Contract** for all modes.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the project context, copied-template constraints, subcommands, output contract, and guardrails in this skill, then execute the plan.

## Subcommands

Load only the subcommand pages needed for the user's task.

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `help` | Print what this skill does, how to invoke it, available modes, subcommands, outputs, and guardrails | [references/help.md](references/help.md) |
| `resolve-project` | Resolve Project, Research Topic, Topic Workspace, template refs, profile refs, and runtime refs | [references/resolve-project.md](references/resolve-project.md) |
| `inspect-template` | Inspect Domain Agent Team Template manifests, placeholders, roles, Workflow Stages, copyable material, and diagnostics | [references/inspect-template.md](references/inspect-template.md) |
| `resolve-context` | Resolve Effective Topic Context, Workspace Runtime readiness, policies, bindings, provider refs, and Gate policy refs | [references/resolve-context.md](references/resolve-context.md) |
| `map-placeholders` | Map template placeholders to topic values, copied material plans, topic edits, deferrals, blockers, and packet-shaped provenance | [references/map-placeholders.md](references/map-placeholders.md) |
| `draft-profile` | Draft reviewable Topic Agent Team Profile Bundle material from specialization outputs | [references/draft-profile.md](references/draft-profile.md) |
| `approve-profile` | Review draft profile material and prepare bundle-local approval provenance | [references/approve-profile.md](references/approve-profile.md) |
| `materialize-profile` | Validate and write an approved Topic Agent Team Profile Bundle under the selected Topic Workspace | [references/materialize-profile.md](references/materialize-profile.md) |
| `launch-team` | Cross from approved profile material into Workspace Runtime and Houmao Execution Adapter launch work | [references/launch-team.md](references/launch-team.md) |
| `fast-forward` | Automatically execute the full Topic Team Specialization path through draft profile output | [references/fast-forward.md](references/fast-forward.md) |
| `step-by-step` | Execute the same required specialization path as `fast-forward`, but pause for user confirmation before each step | [references/step-by-step.md](references/step-by-step.md) |

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
- [ ] Record deferrals and launch blockers.
- [ ] Validate packet/profile inputs and copied material paths.

## Planned Edits

## Validation Plan

## Final Report
```

Leave `Final Report` empty or marked pending until adaptation is complete. After adaptation, fill it with completed edits, deferred edits, generated-guide status, validation status, packet/profile outputs, and unresolved blockers.

## Output Contract

When reporting results, include these fields in structured prose or JSON, depending on the caller's print mode:

- `research_topic_ref`: the resolved Research Topic.
- `topic_workspace_ref`: the resolved Topic Workspace.
- `domain_team_template_ref`: the source Domain Agent Team Template.
- `copied_template_root`: usually `<topic-workspace>/team-profile/execplan/` for `deepsci-mini`.
- `team_specialization_guide_path`: the copied or generated `team-specialization-guide.md`.
- `team_specialization_plan_path`: the `team-specialization-plan.md` with checklist and `Final Report`.
- `changed_copied_material_paths`: copied-root files edited for the topic.
- `placeholder_resolutions`: concrete topic values for template placeholders.
- `deferrals`: unresolved items, with launch-blocking status.
- `packet_profile_inputs`: proposed Topic Team Instantiation Packet and Topic Agent Team Profile Bundle inputs.
- `validation_status`: commands or validators run, plus any blockers.
- `next_operator_action`: usually request approval, materialize an approved bundle, or stop on blockers.

## Guardrails

Do not edit the Domain Agent Team Template source while specializing a topic. The source template remains topic-neutral.

Do not create a directory named `teams` under a Topic Workspace for topic-specific profiles. Store topic-specific copied material inside `<topic-workspace>/team-profile/`, and keep only discovery refs in the Project Manifest.

Do not bypass Topic Team Instantiation Packet validation, Topic Agent Team Profile validation, user or deterministic approval provenance, Workspace Runtime recording, or execution adapter preflight.

Do not treat generated guides as authoritative template source. They are copied-root explanations that need review before reuse.

Do not launch a team from copied template material alone. Launch requires an approved Topic Agent Team Profile Bundle and the runtime or adapter checks appropriate to the command.
