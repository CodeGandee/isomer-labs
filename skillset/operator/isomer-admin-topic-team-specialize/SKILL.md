---
name: isomer-admin-topic-team-specialize
description: Specialize a Domain Agent Team Template into topic-specific copied material for one Research Topic. Use this skill whenever the user asks an operator to instantiate, specialize, adapt, copy, or understand a domain team template for a topic, especially when `team-specialization-guide.md`, `team-specialization-plan.md`, Topic Team Instantiation Packet inputs, or Topic Agent Team Profile Bundle material are needed.
---

# Isomer Admin Topic Team Specialize

Use this as the module-level operator workflow for Domain Agent Team Template understanding and Topic Team Specialization. The workflow acts like one function:

```text
isomer-admin-topic-team-specialize(project_root, topic_ref_or_prompt, domain_team_template_ref)
```

## Operating Model

Run the workflow from a Project Operator Session or Operator Agent that is already pointed at the Isomer Project root, or that can resolve the project root from the user's prompt or current working directory.

Treat project awareness, template inspection, topic context resolution, Service Request routing, placeholder reconciliation, profile drafting, review approval, materialization, and launch orchestration as local subskills inside this module skill. The user should not have to invoke separate skills just to get copied topic-specialized template material.

Use this workflow for one Research Topic and one Domain Agent Team Template at a time. Topic-level parallelism means separate Research Topics can each have their own dedicated Topic Agent Team Profile Bundle; it does not mean one Research Topic should get multiple competing teams.

## Workflow

1. Execute the **Project Awareness** subskill to identify `project_root`, the Project Manifest, the selected Research Topic, the selected Topic Workspace, existing Topic Agent Team Profile Bundle refs, Workspace Runtime refs, Domain Agent Team Template refs, and known Topic Service Agent refs.
2. Execute the **Template Inspection** subskill for the selected `domain_team_template_ref`; read template manifest data, copyable material declarations, placeholder or instantiation parameters, role binding slots, workflow stages, workspace contracts, and diagnostics.
3. Execute the **Topic Context Resolution** subskill to gather Effective Topic Context, Workspace Runtime readiness, policies, Capability Binding refs, Skill Binding Projection refs, provider refs, and Gate policy refs.
4. Execute the **Service Request Routing** subskill only when bounded Service Team support is needed for environment readiness, copied material diagnostics, placeholder reconnaissance, monitoring, or support Artifact writing.
5. Create or confirm the selected Topic Workspace and the Topic Agent Team Profile Bundle root at `<topic-workspace>/team-profile/`, then copy selected Domain Agent Team Template material before editing it. For `deepsci-mini`, the default copied template root is `<topic-workspace>/team-profile/execplan/`.
6. In the copied template root, handle `team-specialization-guide.md`. If it exists, read it first before adaptation; if it is missing, create it in the copied root with the required generated marker. See **Generated Guide Rule**.
7. Create `team-specialization-plan.md` in the copied template root before adaptation. The plan must include a checklist that names intended adaptations, unresolved decisions, expected validation, and packet/profile outputs. See **Plan Structure**.
8. Execute the **Placeholder Reconciliation** subskill, then adapt only the copied template material according to the plan. Resolve placeholders, rewrite role instructions, update prompt text, adjust contract refs, and revise code-like template material as needed for the Research Topic.
9. Append or update a `Final Report` section in `team-specialization-plan.md`, then execute the **Topic Profile Drafting** subskill to report draft Topic Team Instantiation Packet and Topic Agent Team Profile Bundle inputs.
10. Stop at specialization output unless the user explicitly asks for the next boundary. For approval, materialization, or launch work, execute the matching boundary subskill from the **Subskills** table and preserve all validation and provenance checks.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the project context, copied-template constraints, subskills, output contract, and guardrails in this skill, then execute the plan.

## Subskills

Load only the subskill pages needed for the user's task.

| Subskill | Use For | Detail |
| --- | --- | --- |
| Project Awareness | Resolve Project, Research Topic, Topic Workspace, templates, profile refs, runtime refs, and Topic Service Agent refs | [references/project-awareness.md](references/project-awareness.md) |
| Template Inspection | Inspect Domain Agent Team Template manifests, placeholders, roles, workflow stages, copyable material, and diagnostics | [references/template-inspection.md](references/template-inspection.md) |
| Topic Context Resolution | Resolve Effective Topic Context, Workspace Runtime readiness, policies, bindings, provider refs, and Gate policy refs | [references/topic-context-resolution.md](references/topic-context-resolution.md) |
| Service Request Routing | Route bounded Service Requests to Topic Service Agents when operational support is needed | [references/service-request-routing.md](references/service-request-routing.md) |
| Placeholder Reconciliation | Map template placeholders to concrete topic values, copied material plans, topic edits, deferrals, blockers, and packet-shaped provenance | [references/placeholder-reconciliation.md](references/placeholder-reconciliation.md) |
| Topic Profile Drafting | Draft reviewable Topic Agent Team Profile Bundle material from specialization outputs | [references/topic-profile-drafting.md](references/topic-profile-drafting.md) |
| Profile Review Approval | Review draft profile material and prepare bundle-local approval provenance | [references/profile-review-approval.md](references/profile-review-approval.md) |
| Profile Materialization | Validate and write an approved Topic Agent Team Profile Bundle under the selected Topic Workspace | [references/profile-materialization.md](references/profile-materialization.md) |
| Team Launch Orchestration | Cross from approved profile material into Workspace Runtime and Houmao Execution Adapter launch work | [references/team-launch-orchestration.md](references/team-launch-orchestration.md) |

## Generated Guide Rule

If the copied template root lacks `team-specialization-guide.md`, create one before planning. Put this exact marker near the top:

```markdown
> Generated Guide: This file was generated by the Project Operator Session from copied Domain Agent Team Template material because no source `team-specialization-guide.md` existed. Review before treating it as authoritative.
```

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
- `next_operator_action`: usually request approval, materialize an approved bundle, dispatch a Service Request, or stop on blockers.

## Guardrails

Do not edit the Domain Agent Team Template source while specializing a topic. The source template remains topic-neutral.

Do not create a Topic Workspace `teams/` directory for topic-specific profiles. Store topic-specific copied material inside `<topic-workspace>/team-profile/`, and keep only discovery refs in the Project Manifest.

Do not bypass Topic Team Instantiation Packet validation, Topic Agent Team Profile validation, user or deterministic approval provenance, Workspace Runtime recording, or execution adapter preflight.

Do not treat generated guides as authoritative template source. They are copied-root explanations that need review before reuse.

Do not launch a team from copied template material alone. Launch requires an approved Topic Agent Team Profile Bundle and the runtime or adapter checks appropriate to the command.
