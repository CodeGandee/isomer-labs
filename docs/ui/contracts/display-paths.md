# Display Paths Contract

Display paths are human-facing labels shown in status rows, file lists, and similar UI elements. They should be topic-relative when a path points inside the current Topic Workspace.

## Required Behavior

- Absolute paths inside the current Topic Workspace should render relative to the Topic Workspace root.
- Already-relative paths should render unchanged.
- JSON paths such as `$.sections.raw_ideas[0]` should render unchanged.
- Paths outside the current Topic Workspace should render unchanged unless a backend-provided display label exists.

## Extra Fields

Backend payloads may provide full machine paths for resolution and optional display fields for UI labels. The GUI should use display fields when available and otherwise derive a topic-relative label from the known topic id or Topic Workspace path.

## Example

```text
/data/ssd1/huangzhe/code/isomer-labs/isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model/intent/src/topic-overview.md
```

renders as:

```text
intent/src/topic-overview.md
```
