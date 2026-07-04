## Why

Production DeepSci skills currently place User Skill Callback handling as an unnumbered reminder inside `## Workflow`. That is inconsistent with the local skill format, where agents are expected to execute the numbered workflow steps from beginning to end.

## What Changes

- Replace unnumbered `User Skill Callback reminder` prose with explicit numbered workflow steps in participating production DeepSci skills.
- Require `begin` callback resolution to appear as an ordered workflow step after mandatory context or entry checks and before the first skill-specific research action.
- Require `end` callback resolution to appear as an ordered workflow step after tentative outputs exist and before completion, handoff, or final response.
- Update validation to reject callback guidance that is only present as free-floating reminder prose.
- Preserve the existing callback registry, source, CLI, merge-order, and authority model.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `research-paradigm-skills`: Require production DeepSci callback participation to be represented as numbered workflow steps and validate that shape.
- `user-skill-callbacks`: Clarify that callbacks are consumed by explicit owning-skill workflow steps rather than implicit injected hooks or reminders.

## Impact

- Affected assets: production `src/isomer_labs/assets/system_skills/research-paradigm/deepsci/isomer-deepsci-*/SKILL.md` files.
- Affected validation: `scripts/validate_research_paradigm_skillset.py` and associated unit tests.
- Affected behavior: no CLI behavior changes; `project skill-callbacks resolve` remains the same, but participating skill instructions become stricter and easier for agents to follow.
