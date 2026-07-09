## Why

Record detail tabs currently expose too much raw JSON in the primary surface, while idea detail tabs already provide a clearer pattern: readable Markdown first, raw data behind `View JSON`, and practical copy/refresh controls. Aligning record detail with idea detail makes Records useful for research review rather than database inspection.

## What Changes

- Revise record detail tabs opened from the Records section so the primary detail surface is a Markdown preview, using the same interaction pattern as idea node detail.
- Add record detail toolbar actions: `View JSON`, `Copy Markdown`, `Refresh`, and a top-right `Copy Filepath` action.
- Move raw canonical/detail JSON, rendered payload data, lineage, siblings, files, facets, and diagnostics into the `View JSON` dialog instead of showing them as primary columns.
- Show record metadata directly under the title: path relative to the Topic Workspace, direct parent idea when known, and useful source status.
- Add backend/read-model fields as needed for relative artifact path, absolute artifact filepath, and direct parent idea linkage.
- Preserve read-only behavior: opening, refreshing, rendering Markdown, viewing JSON, and copying paths must not mutate Workspace Runtime or query-index state.

## Capabilities

### New Capabilities

- `project-web-record-detail-interactions`: Defines the record detail page interaction model, toolbar actions, metadata row, JSON modal, and copy behavior.

### Modified Capabilities

- `project-web-research-viewer`: Record drill-down behavior changes from multi-column raw inspection to Markdown-first record detail.
- `project-web-data-contracts`: Record inspection contracts need fields for rendered Markdown, JSON modal payload grouping, relative path, absolute filepath, and direct parent idea metadata.
- `project-web-gui`: Record detail APIs may need to include or expose path and parent-idea metadata required by the GUI.

## Impact

- Affected backend: Project Web record detail, descriptor, render, files, facets, lineage, and schema contracts.
- Affected frontend: `RecordDetailPanel`, shared Markdown preview and JSON dialog behavior, clipboard controls, refresh behavior, and tests.
- Affected docs/tests: `docs/ui/contracts/record-inspection.md`, Python contract validation, TypeScript schema/tests, and focused GUI tests.
- No new external dependency or storage migration is expected.
