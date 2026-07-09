## Why

The current tutorials explain project setup, but they do not teach how a user conducts a research topic through Isomer after the project is ready. The FlashAttention/B200 topic chatlog provides a concrete, real workflow that can be distilled into reusable tutorials for research operators.

## What Changes

- Add a research-workflow tutorial suite under the existing `docs/tutorial/` directory using the local FlashAttention/B200 Topic Workspace and the public `CodeGandee/isomer-example-fa4-analytical-model` repository as example material.
- Cover six stages: intent authoring, topic environment preparation, human-steered research passes, real-evidence validation, white-box model development, and paper writing/inspection.
- Update tutorial navigation so users can follow project creation and the research workflow in one section without reading raw chatlogs.
- Keep the existing tutorial section focused on project creation plus research workflow; remove Web GUI tutorial material from this section.
- Teach prompt-driven interaction with agents equipped with Isomer system skills; keep low-level CLI examples in "Under the Hood" sections only.

## Capabilities

### New Capabilities
- `research-workflow-tutorial-suite`: Tutorial contract for teaching a complete human-steered research workflow from research intent authoring through paper artifact inspection.

### Modified Capabilities
- None.

## Impact

- Affected docs: `docs/tutorial/`, tutorial indexes, MkDocs navigation, and the docs validation required-page list.
- Affected source material: `context/topic-chatlogs/merged-timeline.md`, `confusion-analysis.md`, the local Topic Workspace under `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model`, and the public example repository `https://github.com/CodeGandee/isomer-example-fa4-analytical-model` as case-study inputs.
- Affected validation: documentation validation and MkDocs strict build should continue to pass after the new pages are added.
