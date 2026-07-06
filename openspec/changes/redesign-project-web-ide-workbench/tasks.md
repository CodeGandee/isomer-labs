## 1. Explorer Read Models

- [x] 1.1 Define backend explorer node and openable item payload shapes for Project tree and item descriptors.
- [x] 1.2 Implement Project Explorer read-model helpers with an initial quiet skeleton from Project Manifest, Research Topics, Project diagnostics, and collapsed topic nodes, then load or reveal deeper topic children from Effective Topic Context, Topic Workspace Manifest, runtime inspection, query-index summaries, actors, and repository refs.
- [x] 1.3 Add deterministic explorer revision metadata and diagnostics to Project Explorer responses.
- [x] 1.4 Implement openable item descriptor resolution for project overview, topic overview, graph scopes, record collections, records, referenced artifacts, runtime views, diagnostics, actors, agent workspaces, and repositories.
- [x] 1.5 Ensure semantic descriptors can open file-backed record or artifact content without exposing a filesystem tree.
- [x] 1.6 Ensure explorer and descriptor reads are read-only and never rebuild, cleanup, repair, migrate, backfill, write index rows, or read heavy file contents.

## 2. Backend Routes and Query-index Metadata

- [x] 2.1 Add Project Web API routes for Project Explorer tree and openable item descriptor lookup.
- [x] 2.2 Reuse existing query-index summaries, file/list/export metadata, and record detail routes for semantic descriptor targets without adding a filesystem browsing API.
- [x] 2.3 Add validation and error payloads for unknown explorer mode, missing topic, missing openable item, stale descriptor source, unsupported item kind, and unsafe file refs, with detailed non-openable refs surfaced through diagnostics rather than Explorer leaf nodes.
- [x] 2.4 Add Python tests for semantic Project tree nodes, descriptor routing, safe file-backed semantic descriptors, no filesystem browsing route, and read-only mutation flags.

## 3. Frontend Dependencies and API Client

- [x] 3.1 Add `@headless-tree/core` and `@headless-tree/react` to the Vite React frontend dependencies and lockfile.
- [x] 3.2 Add TypeScript and Zod schemas for explorer tree responses, explorer nodes, openable item descriptors, item kinds, and tab targets.
- [x] 3.3 Add typed frontend API clients for Project Explorer tree and openable item descriptor lookup.
- [x] 3.4 Add frontend tests for explorer response validation and item-to-tab command mapping.

## 4. IDE Workbench Shell

- [x] 4.1 Refactor the React shell into `ExplorerPane` on the left and `WorkbenchTabs` on the right, with Dockview as the outermost right-side tab container.
- [x] 4.2 Replace the topic-list-only sidebar with a semantic Project Explorer and no Files mode.
- [x] 4.3 Render the Project Explorer tree through Headless Tree using backend-provided row metadata and custom Isomer styling.
- [x] 4.4 Open only the selected or first Research Topic Overview tab at startup when a topic is available.
- [x] 4.5 Implement one `openItem` command that resolves descriptors, creates deterministic Dockview tab ids, and focuses existing tabs on repeat opens.
- [x] 4.6 Move graph scope navigation from the global topbar into Project Explorer nodes and open graph scopes as normal workbench tabs.
- [x] 4.7 Preserve URL-backed topic/open-item state where useful without remounting unrelated tabs when a graph scope opens.

## 5. Tab Components and Resource Policy

- [x] 5.1 Convert existing graph, dense graph, records, diagnostics, record detail, Markdown, PDF/image/table/JSON fallback viewers, runtime, and topic overview surfaces into tab components opened by descriptors.
- [x] 5.2 Add file-backed artifact viewer tabs that open only from semantic descriptors and respect backend openability metadata.
- [x] 5.3 Ensure closed tabs stop polling, SSE-triggered refetches, graph layout, graph rendering, Markdown rendering, Mermaid rendering, KaTeX rendering, PDF loading, and future session attachment work.
- [x] 5.4 Keep explorer queries lightweight and invalidate only mounted explorer/tree queries and open tabs whose topic id or item kind intersects topic change events.
- [x] 5.5 Add Explorer warning badges plus Diagnostics tab details for partial explorer data, unsafe file refs, missing files, stale records, and unsupported item kinds.

## 6. Responsive UI and Verification

- [x] 6.1 Update CSS for IDE-like layout, stable Explorer sizing, compact narrow-width behavior, and no text overlap in tree rows or tabs.
- [x] 6.2 Update Vitest coverage for Headless Tree rendering, quiet Project Explorer startup with one Topic Overview tab, deterministic tab ids, tab reuse, and tab cleanup behavior.
- [x] 6.3 Update Playwright smoke coverage to open the GUI, select Project Explorer nodes, open idea lineage, open a record detail tab, open file-backed content from a semantic detail view, resize the browser, and verify no stale static assets or surprising API errors.
- [x] 6.4 Validate against the existing Flash Attention topic without changing the topic workspace and against at least one minimal fixture or mocked project state that does not share its filenames.
- [x] 6.5 Run `pixi run lint`, `pixi run typecheck`, `pixi run test`, frontend tests, TypeScript checks, build, and relevant Playwright checks.
