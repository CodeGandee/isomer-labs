## Context

Isomer Projects already expose Project discovery, Research Topic selection, Workspace Runtime inspection, structured record payloads, artifact-format rendering, and query-index export through Python APIs and CLI commands. The missing piece is a local GUI that can browse this information as a directory-backed research log without requiring users to inspect raw SQLite rows, payload files, or generated Markdown.

The first GUI release should serve one Project root per process. It should preserve the current storage model: Workspace Runtime state lives in each Topic Workspace, managed payload JSON files are canonical record content, query-index rows are derived, and Markdown is only a display/export transform.

## Goals / Non-Goals

**Goals:**
- Provide `isomer-cli project web serve --root <Project>` to start a local FastAPI service and packaged TypeScript frontend.
- Expose Project, Research Topic, Topic Workspace, Workspace Runtime, and research-record read models through JSON APIs.
- Let users browse indexed records, timeline/dashboard exports, payload JSON, rendered Markdown, lineage, files, and normalized facets.
- Keep index validation, rebuild, and cleanup as explicit user-triggered maintenance actions.
- Keep the GUI single-user and local-first.

**Non-Goals:**
- No multi-user accounts, central service, external database, or remote synchronization.
- No agent launch/control plane in the first release.
- No direct editing of research records from the GUI.
- No Markdown parsing as authoritative data extraction.

## Decisions

1. Add a `src/isomer_labs/web/` package with a FastAPI app factory.
   - Rationale: the project already depends on FastAPI, and an app factory is testable without starting a real server.
   - Alternative considered: serve by shelling out to CLI commands. This would duplicate serialization, be slower, and make error handling harder.

2. Add a Project-scoped `project web serve` CLI command.
   - Rationale: the GUI targets an Isomer Project root, so it belongs under the existing Project command group and can reuse `--root`.
   - Alternative considered: a top-level `web serve` command. This is shorter, but it loses the Project-scoped command shape already used by the CLI.

3. Use existing Python read/write APIs as the backend boundary.
   - Rationale: `discover_project`, `build_project_state`, `resolve_effective_topic_context`, runtime inspection, record query export, record show, render, index validate, rebuild, and cleanup already encode the domain rules.
   - Alternative considered: direct SQLite and filesystem reads from route handlers. This would bypass validation and make future schema changes harder.

4. Serve packaged static frontend assets from FastAPI and keep TypeScript source in a frontend tree.
   - Rationale: users can start one local Python service and open one URL, while frontend work remains TypeScript-native.
   - Alternative considered: requiring a separate Vite dev server for normal use. This is useful for development but too much ceremony for the default local GUI.

5. Keep read endpoints non-mutating.
   - Rationale: current specs require read operations not to repair or backfill query-index rows. The GUI should report stale indexes and offer explicit rebuild/cleanup actions.
   - Alternative considered: auto-rebuild on page load. This is convenient but hides mutations and can surprise users on large Topic Workspaces.

6. Render Markdown on demand through artifact-format processing.
   - Rationale: managed payload JSON is the durable source, and `render_record` already returns Markdown without writing files unless an output path is supplied.
   - Alternative considered: browse existing `.md` files first. This would preserve older artifacts but repeats the readability issue that motivated payload-backed records.

## Risks / Trade-offs

- Large Topic Workspaces can produce large export payloads. Mitigation: expose list/detail endpoints and keep full exports as explicit view requests.
- The first frontend will be less rich than a full graph UI. Mitigation: ship dense tables and timeline/detail views first, then add graph visualization later.
- Optional static asset packaging can drift from TypeScript source. Mitigation: add tests for static file availability and keep the static bundle small until a full build pipeline lands.
- Local services can expose project files if bound broadly. Mitigation: bind to `127.0.0.1` by default and only serve project-local, API-mediated content.
