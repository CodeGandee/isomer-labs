## Why

`tests/topics/topic-template.md` has been rewritten into a simpler, more focused shape with sections `Research Topic`, `Motivation`, `Topic Breakdown` (`Do's`/`Don'ts`), `Expected Outcome`, and `Related Links`. The Topic Creator skill still ships and populates the older, longer research-proposal template. We need to align the skill's canonical template and subcommands with the new source file so that `create-research-intent` and `clarify-research-intent` produce overviews that match the current convention.

## What Changes

- Replace `skillset/operator/isomer-op-topic-creator/templates/topic-overview.md` with the content of the updated `tests/topics/topic-template.md`.
- Update `references/create-research-intent.md` to populate the new template sections (`Motivation`, `Topic Breakdown` with `Do's`/`Don'ts`, `Expected Outcome`) and strip the updated example blocks.
- Update `references/clarify-research-intent.md` coverage categories to match the new template sections.
- Update `references/help.md` and `SKILL.md` subcommand descriptions if they mention old section names.
- Update `scripts/validate_skillsets.py` required-term checks for `create-research-intent.md` and `clarify-research-intent.md` to match the new template language.
- Update unit test fixtures in `tests/unit/test_validate_skillsets.py` and `tests/unit/test_manual_research_topic_skills.py` as needed.
- Mirror the template into packaged system-skill assets (same inode, automatic).

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `topic-creator-skill`: the canonical `topic.intent.overview` template shape and the coverage scan categories for `clarify-research-intent` are changing.

## Impact

- `skillset/operator/isomer-op-topic-creator/templates/topic-overview.md`
- `skillset/operator/isomer-op-topic-creator/references/create-research-intent.md`
- `skillset/operator/isomer-op-topic-creator/references/clarify-research-intent.md`
- `skillset/operator/isomer-op-topic-creator/SKILL.md`
- `skillset/operator/isomer-op-topic-creator/references/help.md`
- `scripts/validate_skillsets.py`
- `tests/unit/test_validate_skillsets.py`
- `tests/unit/test_manual_research_topic_skills.py`

Existing `topic-overview.md` files created with the old template remain readable; `clarify-research-intent` will treat missing new-template sections as gaps.
