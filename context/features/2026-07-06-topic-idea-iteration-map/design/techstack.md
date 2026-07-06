# Tech Stack

## App Shape

Build the GUI as a routable single-page research workbench, not as a single fixed screen. The app should have one React shell with URL-backed topic and artifact routes, and users should work inside dockable tabs for graphs, Markdown files, PDFs, tables, and diagnostics.

Treat Houmao's `apps/ag-ui-workbench` as the reference implementation for agent/session interaction patterns. Isomer should keep its Python/FastAPI backend, but should align with Houmao's browser workbench choices for Dockview panes, RxJS runtime effects, AG-UI streams, tmux tabs, terminal rendering, and generated UI components.

## Frontend Foundation

Use Vite with React and TypeScript. This keeps the local development loop fast, gives us typed UI code, and produces static assets that the Isomer FastAPI service can serve.

## Routing

Use TanStack Router for topic routes, artifact routes, typed search params, and bookmarkable viewer state. Route state should capture durable navigation such as selected topic, selected artifact, active view type, and graph filters; ephemeral pane layout should stay in Dockview state.

## Workbench Layout

Use Dockview for dockable tabs, split panes, draggable panels, floating panels, and layout save/restore. Persist per-project or per-topic layouts locally first, then add explicit saved layouts only if users need to share workbench arrangements.

## Explorer Trees

Use Headless Tree with `@headless-tree/core` and `@headless-tree/react` for the left semantic Project Explorer. It is a headless tree library, so the GUI can keep an IDE-like custom sidebar while relying on library support for accessibility props, keybindings, search, renaming, drag-and-drop, and virtualization. The React binding exposes `useTree` and a flat visible-node model, which fits Isomer's semantic `openable item` tree better than a raw filesystem widget. References: [Headless Tree docs](https://headless-tree.lukasbach.com/), [Get Started](https://headless-tree.lukasbach.com/getstarted/), and [GitHub](https://github.com/lukasbach/headless-tree).

Render semantic nodes such as Research Topics, Graphs, Records, Runtime, Topic Actors, Agent Workspaces, Repositories, diagnostics, and referenced artifacts. Do not add a Files Explorer mode; raw filesystem browsing should stay in the user's editor, shell, or file manager.

## Idea Lineage Graph

Use React Flow for interactive artifact and idea lineage maps. Pair it with ELK.js for automatic DAG layout, so the view can show parents, siblings, branches, revisions, experiment dependencies, and evidence links without hand-positioning nodes.

Use Plotly.js for generated analytical charts and agent-authored chart components. React Flow remains the graph-editor/viewer for relationship topology; Plotly handles generated quantitative graphics, experiment plots, dashboards, and future AG-UI-rendered chart payloads.

Split graph rendering by artifact density. Use React Flow for sparse, high-touch materials such as ideas, hypotheses, decisions, and selected reasoning paths where users need readable cards, comments, edits, and deep inspection. Use Sigma.js with Graphology for dense overview maps such as experiment records, run outputs, paper revisions, generated figures, result summaries, and repeated logs.

Keep the graph API renderer-neutral so the same artifact relationship data can power either view. The frontend should choose React Flow for detail graphs and Sigma.js for large overview graphs, then let users click from the Sigma.js map into expanded detail tabs.

## Frontend Data Layer

Use TanStack Query for API fetching, cache invalidation, stale-data handling, background refresh, and fallback polling. Keep the GUI read-only for this feature: terminal-side work writes artifacts, the backend indexes them, and the frontend refreshes the affected topic views.

Queries must be scoped to active workbench tabs. A viewer should fetch, poll, subscribe, or render expensive derived state only while its Dockview panel is open and relevant; closed panels should unregister their subscriptions and keep at most cheap cached data.

## Interaction Event Layer

Introduce RxJS early for complex user interaction and research-control event flows. Use it for stop, pause, resume, retry, live search, command progress, stream cancellation, debouncing, fan-in across panels, and cross-tab coordination; do not use it as a replacement for TanStack Query's server-state cache.

RxJS should also model future terminal-control flows when the GUI maps a running `tmux` session into a frontend panel. Treat session output, user input, resize events, interrupt commands, stop/resume commands, and reconnect events as streams that can be composed, throttled, cancelled, and routed per open tab.

Follow Houmao's split: React owns short-lived component state and DOM refs, while RxJS owns long-lived runtime effects, watched targets, session attachment state, reconnect behavior, active thread/session selection, and cross-panel event routing.

## Tables

Use TanStack Table for artifact indexes, idea lists, evidence lists, experiment result tables, diagnostics, and record lists. Keep table filters connected to the graph selection when both views are open in the same workbench.

## Markdown Viewer

Use `react-markdown` with `remark-gfm` for Markdown rendering. Add `remark-math` and `rehype-katex` for math, and render fenced `mermaid` blocks through Mermaid with conservative security settings because local research artifacts should still be treated as viewer input.

## PDF Viewer

Start with the browser PDF viewer through an `iframe`, object embed, or direct dock tab backed by a FastAPI file endpoint. Add PDF.js later only if the GUI needs custom page navigation, annotation overlays, synchronized citations, or integrated PDF text search.

## Runtime Validation

Use Zod at the frontend API boundary when the TypeScript client consumes new or unstable endpoints. Prefer generated or shared types later if the backend API grows large enough to justify it.

Use AG-UI protocol schemas and Houmao implementation schemas for agent-authored UI messages. The frontend should validate typed component payloads before rendering, show explicit unknown-component or invalid-payload fallbacks, and never inject raw HTML, raw SVG, or JavaScript from agent messages.

## Backend Service

Use the existing FastAPI and Uvicorn service shape in `src/isomer_labs/web/`. Add Pydantic response models for topic summaries, artifact descriptors, viewer descriptors, lineage nodes, lineage edges, generation groups, diagnostics, and file-serving metadata.

## Backend Data Access

Use the existing SQLite-backed Isomer record index and SQLAlchemy where ORM access is useful. The GUI backend should query indexed topic artifacts and return view models; it should not mutate research records during ordinary browsing.

## Live Updates

Use server-sent events with `watchfiles` for live topic updates, then let TanStack Query refetch affected queries. Keep polling as a fallback and expose lightweight backend fields such as `index_revision`, `last_indexed_at`, and `diagnostics_count`.

Live updates should be filtered by open viewer interest. The backend may expose broad topic change events, but the frontend should only refetch queries for mounted tabs whose topic, artifact, record kind, or graph scope intersects the event.

## Terminal Session Control

Use WebSocket for bidirectional `tmux` session control when the GUI needs to attach to Project Operator or actor/agent sessions. The backend should own the `tmux` integration and expose status, session listing, attach, output stream, input write, resize, interrupt, stop, resume, and detach operations through a local API.

Keep terminal control separate from read-model updates. Use SSE for topic artifact/index change notifications, and use WebSocket for interactive session I/O and control commands.

Follow Houmao's tmux bridge pattern: list local sessions, attach through a backend-owned PTY bridge, support read-only and read-write modes, route scroll and resize as structured control messages, and close only the browser attachment when a tab closes. Add `xterm.js` when terminal tabs enter the implementation slice.

## AG-UI and Generative UI

Add AG-UI support as the protocol path for agent-authored GUI output. The GUI should connect to Houmao or Houmao-compatible per-agent gateways, consume AG-UI SSE streams, render standard run events, and display typed Isomer/Houmao components in dockable panes.

Use Plotly.js as the required Layer 1 generated-chart renderer. Support a curated `plotly2d` template payload for safe bar, scatter, heatmap, table, sankey, treemap, and other non-3D analytical plots; keep Vega-Lite as a later Layer 2 option for charts that need richer declarative grammar.

Keep AG-UI lifecycle separate from tmux lifecycle. AG-UI connect/run/event streams carry agent-authored UI state and generated components; tmux WebSockets carry terminal bytes and terminal control.

## Resource Policy

Default to lazy loading. Open tabs own their data subscriptions, hidden but mounted tabs may keep lightweight state, and closed tabs must stop polling, SSE-derived refetches, PDF rendering, Mermaid rendering, graph layout work, and large Markdown parsing.

Apply the same policy to generative UI and terminal panes. Closed AG-UI viewers should detach or stop watching unless the user explicitly keeps a background watch, and closed tmux tabs should close only their attachment process without killing the underlying session.

## Testing

Use pytest or unittest for Python read-model tests, Vitest and Testing Library for React tests, and Playwright for browser checks. Include one fixture topic with idea branches, siblings, revisions, Markdown with Mermaid and KaTeX, PDF artifacts, missing optional metadata, and partial records.

## Initial Dependency Set

- Frontend: `vite`, `react`, `react-dom`, `typescript`, `@vitejs/plugin-react`
- Routing: `@tanstack/react-router`
- Workbench: `dockview-react`
- Explorer trees: `@headless-tree/core`, `@headless-tree/react`
- Graph detail views: `@xyflow/react`, `elkjs`
- Large graph overview: `sigma`, `graphology`
- Generated charts: `plotly.js-dist-min`
- Data fetching: `@tanstack/react-query`
- Interaction events: `rxjs`
- Tables: `@tanstack/react-table`
- Markdown: `react-markdown`, `remark-gfm`, `remark-math`, `rehype-katex`, `mermaid`, `katex`
- Agent UI protocol: `@ag-ui/core`
- Validation: `zod`
- Terminal tabs: `@xterm/xterm`, `@xterm/addon-fit`
- Frontend tests: `vitest`, `@testing-library/react`, `playwright`
- Backend: existing `fastapi`, `uvicorn`, `pydantic`, `sqlalchemy`
- Backend live updates: `watchfiles`; add an SSE helper only if plain FastAPI streaming is too clumsy
- Terminal control: backend-owned `tmux` integration over FastAPI WebSocket; use Python-side tmux/PTTY integration or Houmao adapter paths rather than browser-owned process control
