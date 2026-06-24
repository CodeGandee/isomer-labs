## 1. Skill Workflow and Public Surface

- [x] 1.1 Update `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md` so the description, user-facing flow, procedural subcommands, output contract, and guardrails describe static Topic Team material plus durable setup preparation, and no longer list `launch-team`.
- [x] 1.2 Update `references/help.md` so the public table omits `launch-team`, explains static material scope, keeps `setup-topic-env` and `setup-agent-workspace`, and avoids live runtime or adapter launch wording.
- [x] 1.3 Update `references/fast-forward.md` and `references/step-by-step.md` so their required paths stop at `finalize-topic-team` and do not present launch as an optional local tail step.
- [x] 1.4 Remove `skillset/operator/isomer-admin-topic-team-specialize/references/launch-team.md`.

## 2. Static Setup and Profile-Material Boundaries

- [x] 2.1 Revise `references/setup-topic-env.md` to frame installed packages, environment files, setup commands, validation evidence, skipped actions, and blockers as durable static preparation, while forbidding live team execution, adapter launch, credentials, and live provider state in profile material.
- [x] 2.2 Revise `references/setup-agent-workspace.md` to frame Agent Workspace directories and boundary notes as static preparation, while forbidding Agent Instance creation, Workspace Runtime registration, and live launch.
- [x] 2.3 Revise `references/validate-topic-team.md` and `references/finalize-topic-team.md` so they validate and summarize static material readiness instead of Workspace Runtime readiness or launch readiness.
- [x] 2.4 Revise `references/approve-profile.md` and `references/materialize-profile.md` so approval and materialization remain explicit static profile-material boundaries and do not imply Agent Team Instance attachment or adapter preflight.

## 3. Helper and Support References

- [x] 3.1 Revise `references/resolve-project.md`, `references/resolve-context.md`, and `references/draft-profile.md` to remove required runtime refs, Workspace Runtime readiness, launch blockers, and adapter launch language from normal static-material operation.
- [x] 3.2 Revise `references/specialize-team.md`, `references/clarify-topic-team.md`, `references/map-placeholders.md`, `references/inspect-template.md`, `references/isomer-domain-language.md`, and `references/runtime-and-file-boundaries.md` as needed so launch and runtime concepts appear only as out-of-scope boundary warnings.
- [x] 3.3 Update `agents/openai.yaml` default prompt so it describes static Topic Team material, durable setup preparation, validation, and final summary without live launch.

## 4. Validators and Tests

- [x] 4.1 Update `scripts/validate_skillsets.py` constants and checks so `launch-team.md` is not required, `references/launch-team.md` is rejected as an unexpected page, static setup terms remain required, and helper/public subcommand grouping matches the new scope.
- [x] 4.2 Update `tests/unit/test_validate_skillsets.py` fixtures and assertions to match the static-material subcommand set and to fail if `launch-team` is required or listed in public help.
- [x] 4.3 Update already-active topic-team OpenSpec artifacts that still require `launch-team` so they remain compatible with this static-material boundary before validation.

## 5. Validation

- [x] 5.1 Run `pixi run python /home/huangzhe/.codex/skills/.system/skill-creator/scripts/quick_validate.py skillset/operator/isomer-admin-topic-team-specialize`.
- [x] 5.2 Run `pixi run validate-operator-skills`.
- [x] 5.3 Run `pixi run python -m unittest tests.unit.test_validate_skillsets`.
- [x] 5.4 Run `openspec validate limit-topic-team-specialize-to-static-materials --strict`.
- [x] 5.5 Run `openspec validate --all`.
