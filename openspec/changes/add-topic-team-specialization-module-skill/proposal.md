## Why

The operator skillset needs a single Topic Team Specialization entrypoint, but that entrypoint must look like a proper skill bundle rather than a broad helper script. Redoing this change with `skill-creator` conventions and the Imsight skill formatting style makes `isomer-admin-topic-team-specialize` easier for agents to invoke, validate, and maintain.

## What Changes

- Add or refine `skillset/operator/isomer-admin-topic-team-specialize/` as the module-level operator/admin skill for adapting one Domain Agent Team Template to one Research Topic.
- Keep the skill bundle lean: `SKILL.md`, `agents/openai.yaml`, and directly useful local subcommand pages under `references/`; do not add an `evals/` directory or auxiliary docs for this skill.
- Keep required support knowledge self-contained inside the skill directory, including local domain-language and runtime-boundary references instead of links to project-global notes.
- Use `skill-creator` conventions for skill naming, minimal `SKILL.md` frontmatter, concise trigger description, progressive disclosure, UI metadata in `agents/openai.yaml`, and `quick_validate.py` validation.
- Format the skill and each subcommand page in the Imsight style: a near-top `## Workflow`, numbered concise steps, detail sections for longer rules, explicit subcommand routing when needed, and a freeform fallback that tells the agent to plan from the available constraints when the default steps do not fit.
- Add a local `help` subcommand that prints what the skill is and how to use it, and make no-prompt invocation default to `help`.
- Incorporate project awareness, template inspection, topic context resolution, placeholder reconciliation, topic profile drafting, profile review approval, profile materialization, and team launch orchestration as short local subcommands of `isomer-admin-topic-team-specialize` instead of requiring separate operator skills.
- Add `step-by-step` as the guided mode that executes the same required Topic Team Specialization path as `fast-forward`, but explains each step and waits for user confirmation before continuing.
- Add `fast-forward` as the automatic mode that executes the full Topic Team Specialization path through draft profile output while preserving approval, materialization, and launch boundaries.
- Remove the standalone operator skill folders that are now incorporated as local subcommands.
- Preserve canonical Isomer domain boundaries: Topic Team Specialization adapts copied Domain Agent Team Template material inside the selected Topic Workspace's Topic Agent Team Profile Bundle and ends before Agent Team Instance launch.
- Keep `team-specialization-guide.md` and `team-specialization-plan.md` as copied-template-root artifacts, including the generated-guide marker and the `Final Report` rule.
- Keep approval, Topic Team Instantiation Packet validation, Topic Agent Team Profile validation, Workspace Runtime recording, and Execution Adapter launch checks outside the module skill.

## Capabilities

### New Capabilities
- `topic-team-specialization-module-skill`: Defines the lean `isomer-admin-topic-team-specialize` skill bundle, its skill-creator layout rules, local subcommand pages, Imsight workflow formatting, copied template material workflow, guide and plan artifacts, generated-guide behavior, final report behavior, `step-by-step`, `fast-forward`, and validation boundaries.

### Modified Capabilities
- None.

## Impact

- Affected skill files: `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md`, `skillset/operator/isomer-admin-topic-team-specialize/agents/openai.yaml`, and `skillset/operator/isomer-admin-topic-team-specialize/references/*.md`.
- Removed skill artifacts: `skillset/operator/isomer-admin-topic-team-specialize/evals/` is out of scope for this skill.
- Affected template material: `teams/deepsci-mini/execplan/team-specialization-guide.md` remains the source guide for the primary supported Domain Agent Team Template.
- Affected docs and validators: operator skillset docs and validation should recognize the module skill, the no-`evals/` bundle shape, required local subcommands including `help` and `step-by-step`, local support references, required guide and plan terms, no `route-service` subcommand, `fast-forward`, and Imsight workflow structure for the entrypoint and subcommand pages.
- Affected implementation boundaries: the module skill must use its local subcommands and must not bypass packet, profile, runtime, approval, or adapter validation.
