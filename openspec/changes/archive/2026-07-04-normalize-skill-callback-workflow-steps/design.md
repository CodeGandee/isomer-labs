## Context

The User Skill Callback registry and CLI already provide deterministic `begin` and `end` callback resolution. The problem is in participating skill assets and validation: production DeepSci skills place callback handling as an unnumbered reminder inside `## Workflow`, while the skill format says agents execute the numbered workflow steps in order.

## Goals / Non-Goals

**Goals:**

- Make callback participation a first-class numbered workflow step in every production DeepSci `SKILL.md`.
- Keep the `begin` callback step after context and entry checks and before the first skill-specific research action.
- Keep the `end` callback step after tentative outputs or validation state exists and before completion, handoff, or final response.
- Update validation so it checks numbered workflow placement and rejects the old reminder-only pattern.

**Non-Goals:**

- Do not change callback registry storage, CLI command names, source kinds, scope precedence, or callback safety rules.
- Do not execute callbacks automatically from Python code.
- Do not rewrite archived source-copy skills under `org/src`.

## Decisions

- Represent callback participation as numbered steps in `## Workflow`. This matches the repository skill format and makes the callback order visible to agents without relying on ambient prose.
- Keep callback CLI resolution manual and explicit inside skill instructions. The system still returns supplemental instructions; the owning skill decides how to apply them under its guardrails.
- Validate the shape in `scripts/validate_research_paradigm_skillset.py` by inspecting the numbered workflow lines, not by searching for the phrase `User Skill Callback reminder`.
- Preserve concise per-skill wording instead of moving callback instructions to a shared hidden template. The command includes the concrete skill name, and the numbered step keeps each skill self-contained.

## Risks / Trade-offs

- [Risk] Renumbering workflow steps can create noisy diffs across many skill files. Mitigation: apply a mechanical, narrow rewrite around the existing callback paragraph and keep existing step text unchanged.
- [Risk] Validator placement checks can be brittle. Mitigation: check simple textual markers in numbered workflow steps rather than trying to parse Markdown as an AST.
- [Risk] Some skills have slightly different workflow endings. Mitigation: require a numbered `end` callback step before completion language, but allow each skill to keep its existing final validation or continuity step wording.

## Migration Plan

1. Rewrite production DeepSci `SKILL.md` workflow sections to remove the unnumbered reminder and add numbered begin/end callback steps.
2. Update research-paradigm skill validation to require callback resolution in numbered steps and to reject the old reminder phrase.
3. Update unit tests and run the focused validation suite.
4. Run strict OpenSpec validation and the repository test command.

## Open Questions

- None.
