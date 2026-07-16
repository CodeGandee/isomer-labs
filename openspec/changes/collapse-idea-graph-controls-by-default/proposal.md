## Why

The Idea Graph currently expands Graph Controls on every initial render, consuming vertical space before the user asks to adjust focus or layout. The controls should begin collapsed so the graph canvas remains the primary surface.

## What Changes

- Render the Idea Graph-local Graph Controls surface collapsed when the panel first mounts.
- Keep the Graph Controls summary visible and preserve native user-controlled expansion and collapse behavior.
- Update frontend coverage so tests assert the initial collapsed state and explicitly expand the controls before interacting with them.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `project-web-idea-graph-layout`: Define the initial Graph Controls state as collapsed while retaining access to Layout and Focus controls through the summary trigger.

## Impact

This change affects the Idea Graph controls component and its frontend component and browser smoke tests. It does not change backend graph APIs, layout algorithms, saved presets, or dependencies.
