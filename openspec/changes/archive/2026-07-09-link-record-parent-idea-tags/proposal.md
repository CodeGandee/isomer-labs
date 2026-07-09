## Why

Record detail pages already show a direct parent idea when structured artifact metadata provides one, but the tag is display-only. Users reviewing artifacts should be able to jump from an artifact back to the idea that produced or owns it without returning to the graph or manually searching.

## What Changes

- Make the `parent idea: ...` metadata tag in record/artifact detail pages clickable when the backend supplies a stable `direct_parent_idea.idea_id`.
- Open the existing idea node detail tab for that parent idea using the workbench's semantic openable item flow.
- Keep the parent idea tag non-clickable when only a label, display key, or title exists.
- Preserve read-only behavior and existing record detail APIs.
- Show a safe user-facing failure notification when a stale parent idea link cannot be opened.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `project-web-research-viewer`: Record detail drill-down now includes parent idea navigation from artifact metadata when a stable idea id is available.

## Impact

- Affected frontend: record detail panel, workbench command/openable navigation, record detail tests, and static frontend bundle.
- Affected backend: no API or data-contract change expected; existing `direct_parent_idea.idea_id` metadata is reused.
- Dependencies: no new runtime dependency.
