# Design

## Purpose

This folder captures the technical design for the Topic Idea Iteration Map feature: how the Project Web GUI reads topic artifacts, renders sparse and dense relationship views, opens record details, and reacts to new artifacts while topic work continues in the terminal.

## Status

Draft. The design is ready to drive an implementation handoff, with a few open decisions around graph defaults, index revision tokens, dense clustering, and the first tmux control slice.

## Artifacts

| File | Purpose |
| --- | --- |
| [public-interfaces.md](public-interfaces.md) | Backend APIs, frontend contracts, live-update events, renderer rules, and future tmux or AG-UI boundaries. |
| [techstack.md](techstack.md) | Recommended TypeScript and Python stack for the research viewer workbench. |
| [gui-perf-notes.md](gui-perf-notes.md) | Performance notes from DeepScientist and renderer split guidance for sparse versus dense graphs. |

## Module Map

| Module | Responsibility |
| --- | --- |
| Project Web Backend | Resolve Project, Research Topic, Effective Topic Context, Topic Workspace, Workspace Runtime, and query-index read models. |
| Topic Graph Read Model | Convert query-index rows and canonical lineage into renderer-neutral graph scopes such as `idea-lineage`, `artifact-overview`, `experiment-records`, and `paper-revisions`. |
| Workbench Shell | Manage TanStack Router navigation, Dockview panels, tab lifecycle, and local layout persistence. |
| Live Update Runtime | Use SSE, RxJS, and TanStack Query invalidation so only open relevant tabs refresh after topic artifact changes. |
| Sparse Graph Viewer | Use React Flow for idea, hypothesis, decision, and selected reasoning path inspection. |
| Dense Graph Viewer | Use Sigma.js and Graphology for large experiment, result, paper revision, and artifact overview maps. |
| Record Viewers | Open Markdown with Mermaid and KaTeX, browser-backed PDF, images, tables, JSON fallback, and file detail panels. |
| Future Session Control | Attach to tmux sessions through backend-owned WebSocket bridges without killing or mutating sessions on tab close. |
| Future Generative UI | Render AG-UI typed components with Plotly.js charts, tables, metric grids, dashboards, and safe fallbacks. |

## Covered Use Cases

- `UC-01`: Inspect Live Idea Lineage While Continuing Topic Work.

## Open Questions

- Should `idea-lineage` include Decision Records and evidence as secondary nodes by default, or only in selected-node detail?
- What exact `index_revision` token should the backend expose: SQLite WAL revision, query-index max `indexed_at`, or a Workspace Runtime sequence?
- Should Sigma.js dense graph clustering run on the backend, in a Web Worker, or inside the renderer adapter?
- Which tmux control actions belong in the first session-control slice: attach only, interrupt, stop, resume, or prompt injection?
