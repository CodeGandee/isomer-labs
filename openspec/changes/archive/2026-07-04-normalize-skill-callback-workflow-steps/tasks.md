## 1. Skill Asset Rewrite

- [x] 1.1 Rewrite production DeepSci `SKILL.md` workflow sections to remove free-floating `User Skill Callback reminder` prose.
- [x] 1.2 Add numbered `Apply begin callbacks` workflow steps after the mandatory context or entry-fit check and before the first skill-specific action.
- [x] 1.3 Add numbered `Apply end callbacks` workflow steps after tentative outputs or validation state and before completion, handoff, or final response.
- [x] 1.4 Keep callback resolution commands concrete to each production DeepSci skill name.

## 2. Validation

- [x] 2.1 Update `scripts/validate_research_paradigm_skillset.py` to reject free-floating callback reminder prose.
- [x] 2.2 Require `begin` and `end` callback resolution commands to appear in numbered workflow steps.
- [x] 2.3 Update validation tests to cover missing numbered callback steps and the old reminder-only anti-pattern.

## 3. Verification

- [x] 3.1 Run focused research-paradigm skill validation tests.
- [x] 3.2 Run `pixi run test`.
- [x] 3.3 Run `openspec validate normalize-skill-callback-workflow-steps --strict`.
