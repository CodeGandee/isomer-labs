## Why

Isomer already records rich topic state, structured research payloads, and query-indexed research facets, but users must inspect them through CLI calls and raw files. A local TensorBoard-style GUI will make Project and Topic Workspace state easier to browse while preserving the existing file-backed, single-user workflow.

## What Changes

- Add a local FastAPI web service that starts against one Isomer Project root and serves a packaged TypeScript frontend.
- Add read-only JSON APIs for Project summary, Research Topic listing, Topic Workspace details, Workspace Runtime summaries, record export views, record detail, payload files, rendered Markdown, lineage, files, and facets.
- Add explicit GUI maintenance actions for query-index validation, rebuild, and cleanup preview/apply.
- Add a TypeScript frontend for project overview, topic overview, record browser, timeline/graph-style exports, idea/experiment/claim dashboards, and record detail views.
- Keep canonical storage unchanged: Workspace Runtime and managed payload JSON files remain authoritative, query-index rows remain derived, and Markdown remains display/export output.

## Capabilities

### New Capabilities
- `project-web-gui`: Local single-user Project web service, API, and TypeScript GUI for browsing Research Topics, Topic Workspaces, Workspace Runtime state, and research records.

### Modified Capabilities
- `research-record-query-index`: Clarify GUI-facing read/export and explicit maintenance behavior used by the web service.

## Impact

- Adds FastAPI web modules under `src/isomer_labs/web/`.
- Adds a TypeScript frontend source tree and build/package hooks.
- Extends the CLI command surface with a Project web serve command.
- Reuses existing Workspace Runtime, research record, artifact-format rendering, and query-index APIs.
- May add frontend build tooling and an ASGI server dependency.
