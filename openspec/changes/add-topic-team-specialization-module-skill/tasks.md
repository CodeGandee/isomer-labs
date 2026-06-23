## 1. Skill Bundle Shape

- [x] 1.1 Confirm `skillset/operator/isomer-admin-topic-team-specialize/` contains `SKILL.md` and `agents/openai.yaml`.
- [x] 1.2 Keep `SKILL.md` frontmatter limited to `name` and `description`, with the name matching the folder.
- [x] 1.3 Keep `agents/openai.yaml` synchronized with `display_name`, `short_description`, and a `default_prompt` that names `$isomer-admin-topic-team-specialize`.
- [x] 1.4 Remove `skillset/operator/isomer-admin-topic-team-specialize/evals/` and keep eval scaffolding out of this skill.
- [x] 1.5 Add only directly useful local subcommand pages under `skillset/operator/isomer-admin-topic-team-specialize/references/`; avoid auxiliary skill docs such as README, changelog, installation guide, or quick reference files inside this skill.
- [x] 1.6 Add local support references for Isomer domain language and runtime/file boundaries inside the skill directory.

## 2. Imsight Workflow Format

- [x] 2.1 Put `## Workflow` near the top of `SKILL.md`, before detailed guide, plan, helper, output, or guardrail sections.
- [x] 2.2 Write the workflow as concise numbered steps covering default help mode, manual single-subcommand mode, guided `step-by-step` mode, and automatic `fast-forward` mode.
- [x] 2.3 Keep longer procedures in named detail sections such as `Subcommands`, `Generated Guide Rule`, `Plan Structure`, `Output Contract`, and `Guardrails`.
- [x] 2.4 Add the Imsight fallback for tasks that do not map cleanly to the default workflow, telling the agent to build and execute a step-by-step plan from this skill's constraints and subcommands.
- [x] 2.5 Ensure every local subcommand page has a near-top numbered `## Workflow` and a freeform fallback.

## 3. Local Subcommand Incorporation

- [x] 3.1 Add a `## Subcommands` table in `SKILL.md` that links to one-level local reference pages.
- [x] 3.2 Add usage output as `references/help.md`.
- [x] 3.3 Incorporate project awareness as `references/resolve-project.md`.
- [x] 3.4 Incorporate template inspection as `references/inspect-template.md`.
- [x] 3.5 Incorporate topic context resolution as `references/resolve-context.md`.
- [x] 3.6 Incorporate placeholder reconciliation as `references/map-placeholders.md`.
- [x] 3.7 Incorporate topic profile drafting as `references/draft-profile.md`.
- [x] 3.8 Incorporate profile review approval as `references/approve-profile.md`.
- [x] 3.9 Incorporate profile materialization as `references/materialize-profile.md`.
- [x] 3.10 Incorporate team launch orchestration as `references/launch-team.md`.
- [x] 3.11 Incorporate automatic full specialization as `references/fast-forward.md`.
- [x] 3.12 Incorporate guided full specialization as `references/step-by-step.md`.
- [x] 3.13 Remove `references/route-service.md` from this module workflow.
- [x] 3.14 Remove the incorporated standalone operator skill folders.

## 4. Topic Team Specialization Contract

- [x] 4.1 Explain the module-level operator purpose in plain text instead of using code-like invocation syntax.
- [x] 4.2 Document that selected Domain Agent Team Template material is copied into `<topic-workspace>/team-profile/` before topic-specific editing.
- [x] 4.3 Keep the `deepsci-mini` copied template root as `<topic-workspace>/team-profile/execplan/`.
- [x] 4.4 Require `team-specialization-guide.md` to be read first when present, or generated with the visible generated marker when missing.
- [x] 4.5 Require `team-specialization-plan.md` to contain a pre-adaptation checklist and a post-adaptation `Final Report`.
- [x] 4.6 State guardrails that the skill must not edit Domain Agent Team Template source, create a Topic Workspace `teams/` directory, bypass packet/profile/runtime/adapter validation, or claim launch readiness from copied material alone.

## 5. Documentation and Validation

- [x] 5.1 Update operator skillset docs so `isomer-admin-topic-team-specialize` is the preferred entrypoint for Topic Team Specialization and uses local subcommands.
- [x] 5.2 Keep `teams/deepsci-mini/execplan/team-specialization-guide.md` present and covering placeholders, assumptions, workflow, contracts, and cooperation examples.
- [x] 5.3 Ensure repository validation checks the module skill terms, local subcommand pages, local support references, no-`evals/` rule, absence of incorporated standalone skill folders, and absence of external support refs.
- [x] 5.4 Run `pixi run python /home/huangzhe/.codex/skills/.system/skill-creator/scripts/quick_validate.py skillset/operator/isomer-admin-topic-team-specialize`.
- [x] 5.5 Run `python skillset/skill-creator/scripts/quick_validate.py skillset/operator/isomer-admin-topic-team-specialize`.
- [x] 5.6 Run `pixi run validate-operator-skills`.
- [x] 5.7 Run `openspec validate add-topic-team-specialization-module-skill --strict`.
- [x] 5.8 Run `openspec status --change add-topic-team-specialization-module-skill`.
