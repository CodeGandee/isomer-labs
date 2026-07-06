## Context

The current Project Web GUI has a React shell, topic selector sidebar, global graph scope controls, Dockview panels, graph viewers, record lists, record detail tabs, and live invalidation. That is useful for a first idea lineage viewer, but it still feels like a dashboard: navigation is mostly global, graph scope changes remount the workbench, and the left side cannot represent the wider Project, Topic Workspace, runtime, actor, repository, and semantic research surfaces.

The target interaction should feel closer to VS Code or Eclipse: a stable Explorer on the left opens semantic items into a persistent tab container on the right.

```text
┌─────────────────────────────────────────────────────────────────────┐
│ Project Web GUI                                                     │
├───────────────────────┬─────────────────────────────────────────────┤
│ Explorer              │ Workbench Tabs                              │
│ Project Explorer      │ ┌────────┬────────────┬───────────────┐    │
│                       │ │ Topic  │ Idea Graph │ Record Detail │    │
│ semantic tree         │ └────────┴────────────┴───────────────┘    │
│                       │ active tab content                          │
└───────────────────────┴─────────────────────────────────────────────┘
```

The canonical Isomer terms matter here. The Project Explorer should expose Project, Project Manifest, Research Topics, Topic Workspaces, Workspace Runtime, Research Records, Topic Actors, Agent Workspaces, and Topic Main Development Repository as semantic objects. It should not provide a raw filesystem browser or a separate Files view; users can use their preferred local tools for ordinary filesystem browsing.

## Goals / Non-Goals

**Goals:**

- Turn the left panel into a Headless Tree-powered semantic Project Explorer.
- Start with a quiet Project Explorer and open a selected or first Research Topic overview tab by default.
- Make the right panel the outermost Dockview tab container and route every openable item into deterministic tabs.
- Add backend read models for semantic Project Explorer trees and openable item descriptors.
- Preserve lazy resource behavior: explorer trees fetch lightweight metadata, while graph layout, Markdown rendering, PDF loading, and detail queries run only inside open tabs.
- Keep ordinary browsing read-only and path-safe.

**Non-Goals:**

- Do not add editing, rename, move, delete, drag-write, or filesystem mutation behavior.
- Do not expose a filesystem browser or separate Files view.
- Do not add tmux control, AG-UI execution, or generated UI authoring in this slice.
- Do not infer authoritative semantic relationships from Markdown prose.
- Do not hard-code the Flash Attention sample topic structure.

## Decisions

### Use Headless Tree for the Project Explorer

Use `@headless-tree/core` and `@headless-tree/react` for the Explorer. Headless Tree gives the GUI a tree state engine, accessibility props, keyboard behavior, search, selection, drag capability for future use, and virtualized rendering options while letting Isomer keep custom row styling and custom open commands.

Alternative considered: React Arborist. It is strong for a ready-made filesystem-like explorer, but the Project view is semantic and must not look like a raw directory tree. Headless Tree better matches a domain tree where backend nodes carry explicit `item_kind`, diagnostics, badges, and tab targets.

### Backend owns explorer read models

Add Project Web read-model helpers that return tree nodes and openable item descriptors. The backend should derive Project Explorer nodes from Project Manifest, Effective Topic Context, Topic Workspace Manifest, Workspace Runtime, query-index summaries, topic actors, repositories, and diagnostics. File-backed content remains reachable from semantic record or artifact descriptors, not from a general file tree.

Alternative considered: assemble trees in the frontend from existing APIs. That would duplicate Isomer semantics in TypeScript, create topic-specific path heuristics, and make path safety harder to test.

### Project Explorer starts with a quiet skeleton

The initial Project Explorer payload should show Project, Project Manifest, Research Topics, Project diagnostics, and collapsed topic nodes. When a Project has at least one Research Topic, the workbench should open the selected or first Research Topic overview tab, while deeper topic children such as Graphs, Records, Runtime, Topic Actors, Agent Workspaces, and Repositories load when the user expands a topic node.

Alternative considered: show selected-topic sections immediately. That is useful, but it makes the first sidebar busier and weakens the split between overview context in the workbench and semantic navigation in the Explorer.

### Treat all navigation as opening an item

Introduce a single `openItem` command in the frontend. Each explorer node that can be opened carries an `openable_item_id`, `item_kind`, deterministic `tab_id`, preferred component, label, topic id when relevant, and URLs or route parameters needed by the tab.

Alternative considered: keep graph scope buttons and record rows as separate command paths. That preserves today’s dashboard model and makes it harder to reason about tab deduplication.

### Dockview is the outer right-side workbench

Keep Dockview as the right panel’s outermost container. When the Project has at least one Research Topic, startup should open only the selected or first Research Topic Overview tab. Project Overview, diagnostics, graph, record, runtime, file-backed artifact, repository, actor, and future terminal views should all open as normal Dockview tabs from semantic Explorer nodes or in-tab commands.

Alternative considered: keep a topbar with graph mode and a nested Dockview below it. That makes graph scope a page-level mode and causes remounts when users are really just opening another workbench tab.

### No Files Explorer view

Do not add a Files Explorer view. Record detail, Markdown, PDF, image, table, and artifact tabs may still open file-backed content when a semantic record or artifact descriptor references it, but the left Explorer should not try to duplicate shell, editor, or operating-system filesystem browsing.

Alternative considered: expose a curated or shallow filesystem listing and filter client-side. That still creates an underpowered filesystem browser, risks performance problems, and makes the GUI responsible for choices that are better served by a user's editor, shell, or file manager.

### Keep non-openable semantic refs in diagnostics

When semantic refs cannot open because they are missing, stale, unresolved, outside accepted surfaces, or unsupported, the Project Explorer should show warning badges and diagnostic counts on the owning Project, Research Topic, or semantic group rows. Detailed non-openable refs should appear in Diagnostics tabs, not as broken-looking Explorer leaves.

Alternative considered: show every non-openable semantic ref inline under its owning group. That gives precise locality, but it can make the Explorer feel like an error listing instead of a navigation surface.

## Risks / Trade-offs

- Explorer API shape may become too generic → Keep `item_kind` vocabulary explicit and version the read model if needed.
- Headless Tree integration may require more custom rendering than Arborist → Keep the first tree row simple and defer rename/drag features.
- Large projects may produce large semantic trees → Use lightweight summaries, collapsed nodes, optional child loading, and virtualization before adding deep semantic surfaces.
- Existing Playwright checks may assume the old global graph buttons → Update browser checks to open graph tabs through Project Explorer nodes.

## Migration Plan

1. Add explorer read-model builders and API routes without removing existing graph, records, detail, render, lineage, sibling, files, facets, runtime, and event routes.
2. Add Headless Tree dependencies and refactor the React shell into `ExplorerPane` plus `WorkbenchTabs`.
3. Move existing graph, records, diagnostics, and record-detail components into tab components opened through `openItem`.
4. Add the semantic Project Explorer tree using backend-provided nodes.
5. Keep existing route/search params as compatibility inputs where practical, mapping them to opened tabs.
6. Update tests and Playwright smoke checks to select Project Explorer nodes and assert tab reuse, no stale assets, responsive layout, and read-only behavior.

Rollback is straightforward: the existing read APIs remain, and the previous static build can be restored if the new explorer shell fails.

## Open Questions

None for this change. Future slices still need separate decisions for terminal control and generative UI behavior.
