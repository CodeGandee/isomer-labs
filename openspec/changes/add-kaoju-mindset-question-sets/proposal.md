## Why

Each Kaoju Mindset Source currently exposes one flat question list, so every Run using that mindset receives the same questions even when the concrete task calls for a narrower examination posture. Kaoju needs task-sensitive question bundles without replacing the existing rule that a stage resolves one mindset.

## What Changes

- Add Mindset Source v2 with a reusable question catalog and named question sets whose `question_ids` value is either `"all"` or an ordered list of question references; explicit references form a many-to-many mapping.
- Require every v2 Mindset Source to contain exactly one question set named `default`.
- Give each question set one descriptive `triggering_condition`; individual questions do not carry triggering conditions.
- Have the agent select exactly one specialized question set whose condition best matches the task and active Run context, or select `default` when no specialized set applies.
- Materialize only the selected question set's ordered questions into the Run-scoped Mindset Record and preserve the selected set, condition, and selection rationale in the immutable Source snapshot.
- Upgrade packaged defaults, topic-creation guidance, validation, rendering, and tests to produce and consume v2 Sources.
- Preserve existing valid v1 topic Sources by interpreting their flat question list as an implicit `default` question set until the user explicitly replaces or regenerates them.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `kaoju-mindsets`: Extend Mindset Sources and Mindset Records with task-selected, reusable question sets and a mandatory `default` fallback while retaining one mindset resolution per applicable Run.

## Impact

The change affects Kaoju Mindset Source schemas and validators, Mindset Record materialization and rendering, packaged mindset defaults, the checked survey-process contract, topic-creation and consumer skill guidance, canonical domain-language descriptions, and Kaoju unit and integration tests. Existing Run mindset resolution, Source paths, mindset keys, Artifact semantic IDs, and the `project runs resolve-mindset` interface remain unchanged.
