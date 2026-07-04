## 1. Add Topic Overview Template

- [x] 1.1 Copy `tests/topics/topic-template.md` to `skillset/operator/isomer-op-topic-creator/templates/topic-overview.md`.
- [x] 1.2 Verify the template renders as Markdown and preserves the intended research-proposal structure.
- [x] 1.3 Mirror the template into `src/isomer_labs/assets/system_skills/operator/isomer-op-topic-creator/templates/topic-overview.md`.

## 2. Update `create-research-intent`

- [x] 2.1 Revise `skillset/operator/isomer-op-topic-creator/references/create-research-intent.md` to populate `topic-overview.md` from `templates/topic-overview.md`.
- [x] 2.2 Document that inferred sections are filled and missing sections are kept as empty headings.
- [x] 2.3 Document that `> Example:` blocks are stripped from generated overviews.
- [x] 2.4 Mirror the updated `create-research-intent.md` into packaged assets.

## 3. Add `clarify-research-intent` Subcommand

- [x] 3.1 Create `skillset/operator/isomer-op-topic-creator/references/clarify-research-intent.md` following the structure of `isomer-op-topic-team-specialize/references/clarify-topic.md` (Workflow, Coverage and Clarity Scan, Question Format, Sequential Clarification Loop, Direct Topic Overview Integration, Prerequisite Artifacts, Guardrails), but with coverage categories aligned to the Topic Creator template and a human-in-the-loop resolution of open questions.
- [x] 3.2 Ensure the subcommand is interactive, user-facing, and not invoked by `fast-forward` or `run-to`.
- [x] 3.3 Mirror the new reference page into packaged assets.

## 4. Update Skill Entrypoint and Help

- [x] 4.1 Update `skillset/operator/isomer-op-topic-creator/SKILL.md` to list `clarify-research-intent` in Misc Subcommands and document the template population behavior.
- [x] 4.2 Update `skillset/operator/isomer-op-topic-creator/references/help.md` to list `clarify-research-intent` and mention the template.
- [x] 4.3 Update `skillset/operator/isomer-op-topic-creator/references/run-to.md` to exclude `clarify-research-intent` from valid targets.
- [x] 4.4 Update `skillset/operator/isomer-op-topic-creator/references/fast-forward.md` to state that `clarify-research-intent` is not part of the automatic flow and may be recommended on blocked intent.
- [x] 4.5 Mirror all updated skill files into packaged assets.

## 5. Update Skill Validator

- [x] 5.1 Add `clarify-research-intent.md` to `TOPIC_CREATOR_COMMANDS` in `scripts/validate_skillsets.py`.
- [x] 5.2 Add required-term checks for `clarify-research-intent.md` in `TOPIC_CREATOR_REFERENCE_REQUIRED_TERMS`.
- [x] 5.3 Update existing `create-research-intent.md` required-term checks if needed.
- [x] 5.4 Run `python scripts/validate_skillsets.py` and fix any diagnostics.

## 6. Validate and Finalize

- [x] 6.1 Run `pixi run lint`.
- [x] 6.2 Run `pixi run typecheck`.
- [x] 6.3 Run `pixi run test`.
- [ ] 6.4 Run `openspec verify-change add-topic-overview-template-and-clarify-research-intent`.
- [x] 6.5 Run `openspec validate add-topic-overview-template-and-clarify-research-intent --strict` if available.

Note: `openspec verify-change` is not a recognized CLI command in this OpenSpec installation. `openspec validate --strict` passed and the full unit-test suite passes.
