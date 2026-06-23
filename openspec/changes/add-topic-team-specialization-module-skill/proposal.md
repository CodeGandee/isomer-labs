## Why

The operator skillset needs a single Topic Team Specialization entrypoint, but that entrypoint must look like a proper skill bundle rather than a broad helper script. Redoing this change with `skill-creator` conventions and the Imsight skill formatting style makes `isomer-admin-topic-team-specialize` easier for agents to invoke, validate, and maintain.

## What Changes

- Add or refine `skillset/operator/isomer-admin-topic-team-specialize/` as the module-level operator/admin skill for adapting one Domain Agent Team Template to one Research Topic.
- Keep the skill bundle lean: `SKILL.md`, `agents/openai.yaml`, and directly useful local subskill pages under `references/`; do not add an `evals/` directory or auxiliary docs for this skill.
- Use `skill-creator` conventions for skill naming, minimal `SKILL.md` frontmatter, concise trigger description, progressive disclosure, UI metadata in `agents/openai.yaml`, and `quick_validate.py` validation.
- Format the skill and each subskill page in the Imsight style: a near-top `## Workflow`, numbered concise steps, detail sections for longer rules, explicit subskill routing when needed, and a freeform fallback that tells the agent to plan from the available constraints when the default steps do not fit.
- Incorporate project awareness, template inspection, topic context resolution, Service Request routing, placeholder reconciliation, topic profile drafting, profile review approval, profile materialization, and team launch orchestration as local subskills of `isomer-admin-topic-team-specialize` instead of requiring the module skill to call separate operator skills.
- Remove the standalone operator skill folders that are now incorporated as local subskills.
- Preserve canonical Isomer domain boundaries: Topic Team Specialization adapts copied Domain Agent Team Template material inside the selected Topic Workspace's Topic Agent Team Profile Bundle and ends before Agent Team Instance launch.
- Keep `team-specialization-guide.md` and `team-specialization-plan.md` as copied-template-root artifacts, including the generated-guide marker and the `Final Report` rule.
- Keep approval, Topic Team Instantiation Packet validation, Topic Agent Team Profile validation, Workspace Runtime recording, and Execution Adapter launch checks outside the module skill.

## Capabilities

### New Capabilities
- `topic-team-specialization-module-skill`: Defines the lean `isomer-admin-topic-team-specialize` skill bundle, its skill-creator layout rules, local subskill pages, Imsight workflow formatting, copied template material workflow, guide and plan artifacts, generated-guide behavior, final report behavior, and validation boundaries.

### Modified Capabilities
- None.

## Impact

- Affected skill files: `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md`, `skillset/operator/isomer-admin-topic-team-specialize/agents/openai.yaml`, and `skillset/operator/isomer-admin-topic-team-specialize/references/*.md`.
- Removed skill artifacts: `skillset/operator/isomer-admin-topic-team-specialize/evals/` is out of scope for this skill.
- Affected template material: `teams/deepsci-mini/execplan/team-specialization-guide.md` remains the source guide for the primary supported Domain Agent Team Template.
- Affected docs and validators: operator skillset docs and validation should recognize the module skill, the no-`evals/` bundle shape, required local subskills, required guide and plan terms, and Imsight workflow structure for the entrypoint and subskill pages.
- Affected implementation boundaries: the module skill must use its local subskills and must not bypass packet, profile, runtime, approval, or adapter validation.
