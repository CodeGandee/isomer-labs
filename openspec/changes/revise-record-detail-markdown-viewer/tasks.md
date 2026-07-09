## 1. Backend Read Model

- [x] 1.1 Extend record viewer descriptor/detail read models to expose Topic Workspace-relative path and absolute artifact filepath when available from payload, render, or primary file metadata.
- [x] 1.2 Derive optional direct parent idea metadata from structured lineage, idea realization, parents JSON, facets, or payload refs without parsing prose.
- [x] 1.3 Preserve existing record detail, render, lineage, siblings, files, and facets endpoints as read-only responses with `mutated: false`.

## 2. Contracts and Schemas

- [x] 2.1 Update `docs/ui/contracts/record-inspection.md` with Markdown-first detail behavior, path fields, parent idea fields, and JSON modal grouping.
- [x] 2.2 Update Python Project Web contract models and tests for the new optional record inspection fields.
- [x] 2.3 Update TypeScript schemas and representative fixtures/tests for record descriptor/detail/render payloads.

## 3. Frontend Record Detail

- [x] 3.1 Refactor the record detail panel to use the same primary layout pattern as idea detail: heading, metadata row, toolbar, Markdown preview, and JSON dialog.
- [x] 3.2 Add `View JSON`, `Copy Markdown`, `Refresh`, and `Copy Filepath` toolbar actions with disabled states and visible copy status.
- [x] 3.3 Move descriptor/detail/render/lineage/siblings/files/facets/diagnostics JSON into tabbed `View JSON` content instead of always-visible JSON columns.
- [x] 3.4 Keep PDF, image, table, and file artifact viewer behavior intact for records whose descriptor selects those viewers.

## 4. Verification

- [x] 4.1 Add or update backend tests for record detail metadata, direct parent idea metadata, read-only behavior, and contract validation.
- [x] 4.2 Add or update frontend tests for the Markdown-first record detail panel, JSON dialog, copy controls, disabled states, and refresh behavior.
- [x] 4.3 Rebuild packaged frontend static assets if frontend code changes.
- [x] 4.4 Run focused backend/frontend tests for record detail and contract coverage.
- [x] 4.5 Run `openspec validate revise-record-detail-markdown-viewer --strict`.
