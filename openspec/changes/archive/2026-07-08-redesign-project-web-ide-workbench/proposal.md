## Why

The Project Web GUI currently behaves like a topic dashboard with graph mode buttons and supporting panels, but users need an IDE-like workbench where the left side navigates Project and Topic Workspace material and the right side opens persistent tabs. This redesign makes semantic Isomer objects easy to browse without binding the GUI to one sample topic or raw filesystem layout. It does not add a filesystem browser; users should keep using their preferred local tools for raw file browsing.

## What Changes

- Replace the topic-list-only sidebar with a semantic Project Explorer pane.
- Add a Headless Tree-backed explorer tree for semantic Project nodes.
- Make the right side a persistent outer Dockview tab container that owns all opened views.
- Introduce a unified openable item contract so semantic items, records, graphs, runtime views, actor workspaces, repositories, and referenced artifacts open or focus deterministic tabs.
- Move graph scope selection out of global topbar state and into openable Project Explorer nodes.
- Add read-only backend explorer tree APIs that derive semantic trees from Project Manifest, Effective Topic Context, Workspace Runtime, query-index summaries, topic actors, repositories, and diagnostics.
- Keep ordinary browsing read-only and keep expensive data fetching scoped to open tabs.

## Capabilities

### New Capabilities

- `project-web-ide-workbench`: IDE-style Project Web GUI shell with a left Explorer pane and right Dockview tab workbench driven by openable semantic items.
- `project-web-explorer-read-api`: Read-only backend APIs that return Project Explorer tree models plus openable item descriptors.

## Impact

- Affects `src/isomer_labs/web/` FastAPI routes, read-model helpers, explorer tree builders, and tests.
- Affects `web/ui/` React TypeScript layout, Dockview tab orchestration, navigation state, and dependencies.
- Adds `@headless-tree/core` and `@headless-tree/react` to frontend dependencies.
- Reuses existing graph, record, render, lineage, sibling, file, facet, runtime, and SSE APIs where possible.
- Does not add write actions, filesystem browsing, tmux control, AG-UI execution, or topic-specific GUI assumptions in this change.
