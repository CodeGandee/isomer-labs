## 1. Replace the Canonical Template

- [x] 1.1 Overwrite `skillset/operator/isomer-op-topic-creator/templates/topic-overview.md` with the current contents of `tests/topics/topic-template.md`.
- [x] 1.2 Verify the new template sections are `Research Topic`, `Motivation`, `Topic Breakdown` (`Do's`/`Don'ts`), `Expected Outcome`, and `Related Links`.

## 2. Update Research Intent Reference Pages

- [x] 2.1 Edit `skillset/operator/isomer-op-topic-creator/references/create-research-intent.md` to populate the new template sections (`Research Topic`, `Motivation`, `Topic Breakdown` with `Do's`/`Don'ts`, `Expected Outcome`, `Related Links`) and remove references to the old sections.
- [x] 2.2 Ensure `create-research-intent.md` instructs stripping any `>` example blocks from the written overview.
- [x] 2.3 Edit `skillset/operator/isomer-op-topic-creator/references/clarify-research-intent.md` so the Coverage and Clarity Scan checks the new template sections: `Research Topic`, `Motivation`, `Topic Breakdown` (`Do's`/`Don'ts`), `Expected Outcome`, `Related Links`.
- [x] 2.4 Update `clarify-research-intent.md` Direct Topic Overview Integration table to map answers to the new sections.

## 3. Update Skill Help and Main SKILL Page

- [x] 3.1 Update `skillset/operator/isomer-op-topic-creator/references/help.md` subcommand descriptions to mention the new template sections for `create-research-intent` and `clarify-research-intent`.
- [x] 3.2 Update `skillset/operator/isomer-op-topic-creator/SKILL.md` if it lists old section names or template source language.

## 4. Update Validation and Tests

- [x] 4.1 Update `scripts/validate_skillsets.py` `TOPIC_CREATOR_REFERENCE_REQUIRED_TERMS` for `create-research-intent.md` to require the new template section names and strip-example wording.
- [x] 4.2 Update `scripts/validate_skillsets.py` `TOPIC_CREATOR_REFERENCE_REQUIRED_TERMS` for `clarify-research-intent.md` to require the new coverage categories.
- [x] 4.3 Update unit test fixtures in `tests/unit/test_validate_skillsets.py` to match the new required terms.
- [x] 4.4 Update `tests/unit/test_manual_research_topic_skills.py` fixtures or expectations as needed.

## 5. Verify the Change

- [x] 5.1 Run `openspec validate update-topic-overview-template --strict`.
- [x] 5.2 Run `pixi run lint`.
- [x] 5.3 Run `pixi run typecheck`.
- [x] 5.4 Run `pixi run test`.
