## Why

The idea lineage graph currently opens idea detail on single click, which makes selection, inspection, and navigation feel too eager. The idea detail page also mixes the main reading view with several raw JSON blocks and a top-level JSON copy action, which makes the primary idea content harder to scan.

## What Changes

- Change idea graph node interaction so hover shows a delayed compact Markdown summary tooltip, single click only selects or highlights the node, and double click opens the detail tab.
- Keep hover previews lightweight by using graph node summary fields instead of fetching full record detail.
- Revise the idea detail toolbar to keep `View JSON`, `Copy Markdown`, and refresh actions while removing top-level `Copy JSON`.
- Move lineage, realizations, and diagnostics JSON into tabs inside the JSON dialog.
- Make the JSON dialog default to a `Main Record` tab for the idea record JSON.

## Capabilities

### New Capabilities
- `project-web-idea-detail-interactions`: Covers idea graph hover, selection, double-click open behavior, and the idea detail JSON viewing layout.

### Modified Capabilities

## Impact

- Affects the TypeScript Project Web GUI under `web/ui/src/`.
- Adds or updates frontend tests for ReactFlow interaction behavior, hover previews, and idea detail JSON dialog layout.
- Does not change backend APIs, query-index storage, or topic artifact formats.
