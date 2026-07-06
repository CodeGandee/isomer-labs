## 1. Backend Service

- [x] 1.1 Add the `isomer_labs.web` package with a FastAPI app factory, project-root settings, and static frontend mounting.
- [x] 1.2 Implement Project, topic, actor, runtime, record query, record detail, render, lineage, files, facets, and index maintenance route handlers using existing Python APIs.
- [x] 1.3 Add `isomer-cli project web serve` with host, port, reload, and no-browser options, and wire it into the CLI help surface.

## 2. Frontend

- [x] 2.1 Add a TypeScript frontend source tree with project/topic navigation, record table, export summary panels, and record detail panes.
- [x] 2.2 Add packaged static assets served by FastAPI so the GUI works without a separate frontend dev server.

## 3. Validation

- [x] 3.1 Add unit tests for the web read model, API routes, static shell, and CLI command registration.
- [x] 3.2 Run focused tests and project validation commands for the implemented slice.
