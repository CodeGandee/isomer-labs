## 1. Clarification Subcommand Updates

- [x] 1.1 Update `skillset/operator/isomer-admin-topic-team-specialize/references/clarify-topic.md` with a coverage and clarity scan for `topic-overview.md`, bounded question constraints, one-question-at-a-time loop, answer validation, direct `topic-overview.md` integration, and predictable stop/report rules.
- [x] 1.2 Update `skillset/operator/isomer-admin-topic-team-specialize/references/clarify-topic-team.md` with the same bounded option-asking loop adapted to copied topic-team material, specialization plan, `Final Report`, placeholder resolutions, deferrals, and draft packet/profile inputs.
- [x] 1.3 Confirm neither `clarify-topic` nor `clarify-topic-team` instructs the agent to create ADRs, decision logs, user-decision records, or separate clarification transcripts as durable sources of truth.

## 2. Consistency Checks

- [x] 2.1 Review `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md`, `references/fast-forward.md`, `references/step-by-step.md`, and `references/help.md` to confirm existing routing still matches the revised `clarify-*` behavior without listing private helpers or adding new subcommands.
- [x] 2.2 Keep the existing predecessor-artifact refusal rules in both `clarify-*` pages intact.
- [x] 2.3 Avoid adding new reference pages unless implementation also updates the operator skill validator and unit tests that enforce the allowlist.

## 3. Validation

- [x] 3.1 Run `openspec validate revise-topic-team-clarify-option-loop --strict`.
- [x] 3.2 Run `pixi run validate-operator-skills`.
- [x] 3.3 Run `pixi run python /home/huangzhe/.codex/skills/.system/skill-creator/scripts/quick_validate.py skillset/operator/isomer-admin-topic-team-specialize`.
- [x] 3.4 Run `git diff --check`.
