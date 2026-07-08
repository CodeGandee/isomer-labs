## Why

The idea lineage graph already carries parent-to-child edge data, but the GUI does not make direction or selected-node context obvious enough for inspection. Hover previews also appear a bit too quickly for dense graph work, which causes accidental popups while users are aiming at nodes.

## What Changes

- Increase the idea hover preview trigger delay to 2 seconds for mouse hover and touch long press.
- Render idea lineage edges with visible direction from parent idea to child idea.
- When a node is selected, highlight direct parents and direct children with distinct visual states.
- Highlight incoming and outgoing edges around the selected node so direction and neighborhood are easy to scan.
- Add focused tests for delay, arrow markers, and parent/child selection classes.

## Capabilities

### New Capabilities
- `project-web-idea-lineage-selection`: Covers Project Web idea lineage graph direction rendering and selected-node neighborhood highlighting.

### Modified Capabilities

## Impact

- Affects the TypeScript Project Web graph conversion and ReactFlow panel behavior under `web/ui/src/`.
- Affects Project Web CSS styling for ReactFlow nodes and edges.
- Updates generated static web assets under `src/isomer_labs/web/static/` after rebuilding the frontend.
- No backend API, database, or record schema changes are required.
