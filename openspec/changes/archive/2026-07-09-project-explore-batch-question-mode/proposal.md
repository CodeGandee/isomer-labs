## Why

The `imsight-project-explore` skill currently enforces sequential questioning: one question per message with a proposed option. This works well for deep, dependency-heavy decisions, but it is slow when the user already has a good sense of the design space and only wants to scan, override a few items, and accept the rest. Users need a batch mode that lists all questions at once with recommended choices so they can quickly pick what to modify and say "accept the rest".

## What Changes

- Add a batch question mode to `imsight-project-explore`.
- Make batch mode opt-in from the user prompt via explicit phrases such as "list all at once", "batch mode", "show all options", or "let me pick which ones to change".
- Encode the sequential-vs-batch branch as a numbered workflow step in each affected mode, not as a side notice.
- Update `commands/auto.md`, `commands/design-choice.md`, and `commands/any-open-question.md` to detect batch mode and present all questions with proposed options in one message.
- Add integration rules for batch responses: process overrides in order, accept proposed defaults for unmentioned items, and flag downstream proposals invalidated by an earlier override.
- Update `SKILL.md` Invocation Contract to mention the batch-mode trigger phrases.

## Capabilities

### New Capabilities

- `imsight-project-explore-batch-mode`: Allow users to request a batch list of exploration questions with recommended options in `auto`, `design-choice`, and `any-open-question` modes.

### Modified Capabilities

- None.

## Impact

- Affects `extern/orphan/houmao-agents/skillset/imsight-skills/imsight-project-explore/SKILL.md`, `commands/auto.md`, `commands/design-choice.md`, and `commands/any-open-question.md`.
- Default behavior remains sequential; batch mode is triggered only by explicit user request.
