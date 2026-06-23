## 1. Module Skill Bundle

- [x] 1.1 Create `skillset/operator/isomer-admin-topic-team-specialize/` with `SKILL.md` and `agents/openai.yaml`.
- [x] 1.2 Write the module skill workflow as `isomer-admin-topic-team-specialize(project_root, topic_ref_or_prompt, domain_team_template_ref)`.
- [x] 1.3 Document the workflow steps: resolve topic workspace, copy template material, read or generate guide, create plan checklist, adapt copied material, append `Final Report`, and report packet/profile inputs.
- [x] 1.4 State guardrails that the skill must not edit Domain Agent Team Template source, must not create a Topic Workspace `teams/` directory, and must not bypass packet/profile/runtime/adapter validation.
- [x] 1.5 Reference lower-level operator skills only as helper functions or supporting concepts, not as required user-facing steps.

## 2. Specialization Guide and Plan Artifacts

- [x] 2.1 Add `teams/deepsci-mini/execplan/team-specialization-guide.md`.
- [x] 2.2 Ensure the `deepsci-mini` guide describes placeholders and definitions, assumptions, team workflow, contracts used by the team, and an example cooperation flow among lead, scout, and synthesis-reviewer roles.
- [x] 2.3 Document the generated-guide rule in the module skill, including a required visible marker when no source `team-specialization-guide.md` exists.
- [x] 2.4 Document `team-specialization-plan.md` structure in the module skill, including a pre-adaptation checklist and post-adaptation `Final Report` section.
- [x] 2.5 Specify the default copied-root placement for `deepsci-mini` as `<topic-workspace>/team-profile/execplan/`.

## 3. Documentation and Skillset Integration

- [x] 3.1 Update `skillset/operator/README.md` so `isomer-admin-topic-team-specialize` is the preferred entrypoint for Domain Agent Team Template specialization.
- [x] 3.2 Update operator README examples to call the module skill for template understanding and adaptation before approval/materialization/launch steps.
- [x] 3.3 Update `skillset/README.md` if needed so the operator skillset description includes module-level skills.
- [x] 3.4 Update relevant OpenSpec or team docs that still describe the specialization workflow only as many fine-grained operator skill calls.

## 4. Validation and Tests

- [x] 4.1 Ensure `pixi run validate-operator-skills` accepts the new `isomer-admin-topic-team-specialize` bundle.
- [x] 4.2 Add or update validation/tests to require `teams/deepsci-mini/execplan/team-specialization-guide.md`.
- [x] 4.3 Add a unit or manual smoke test that checks the module skill documentation names `team-specialization-guide.md`, `team-specialization-plan.md`, generated-guide behavior, and `Final Report`.
- [x] 4.4 Add a focused fixture or test expectation showing copied `deepsci-mini` material places guide and plan files under `team-profile/execplan/`.

## 5. Verification

- [x] 5.1 Run `openspec validate add-topic-team-specialization-module-skill --strict`.
- [x] 5.2 Run `openspec validate --all`.
- [x] 5.3 Run `pixi run validate-skills`.
- [x] 5.4 Run `pixi run lint`.
- [x] 5.5 Run `pixi run typecheck`.
- [x] 5.6 Run `pixi run test`.
- [x] 5.7 Run a focused topic-team profile materialization or UC-01 smoke test that exercises copied `deepsci-mini` material.
- [x] 5.8 Run `git diff --check`.
