## 1. Documentation

- [x] 1.1 Create `docs/ui/contracts/index.md` that explains UI read contracts, permissive extra-field handling, and the boundary from canonical storage contracts.
- [x] 1.2 Create a topic overview contract page covering overview source metadata, Markdown content, supporting JSON payloads, diagnostics, and missing-file behavior.
- [x] 1.3 Create a topic graph contract page covering graph identity, nodes, edges, groups, facets, paging, renderer hints, and diagnostics.
- [x] 1.4 Create an idea detail contract page covering canonical idea metadata, realizations, lineage, source provenance, source JSON availability, and optional exact source JSON.
- [x] 1.5 Create a record inspection contract page covering viewer descriptors, rendered content, record files, lineage, siblings, facets, and file openability metadata.
- [x] 1.6 Create shared contract pages for diagnostics and topic-relative display paths used by GUI status rows and file lists.

## 2. Python Schema Models

- [x] 2.1 Add a `src/isomer_labs/web/contracts/` package with permissive Pydantic base model configuration and public validation helpers.
- [x] 2.2 Implement shared schema models for diagnostics, paging, file metadata, viewer descriptors, and topic identity fields.
- [x] 2.3 Implement topic overview response schema models that require the fields consumed by `TopicOverviewPanel` while allowing extra metadata.
- [x] 2.4 Implement topic graph response schema models that require GUI-critical graph, node, edge, and group fields while allowing extra metadata.
- [x] 2.5 Implement idea detail response schema models that require GUI-critical idea, realization, source, lineage, and diagnostic fields while allowing extra metadata.
- [x] 2.6 Implement record inspection schema models for record details, rendered records, file lists, lineage, siblings, and facets where Project Web consumes them directly.

## 3. Backend Integration

- [x] 3.1 Validate topic overview payloads at the Project Web read-model boundary before returning them to FastAPI.
- [x] 3.2 Validate topic graph payloads at the graph read-model boundary before returning them to FastAPI.
- [x] 3.3 Validate idea detail payloads at the idea detail read-model boundary before returning them to FastAPI.
- [x] 3.4 Validate record viewer and record file payloads at the record read-model boundary before returning them to FastAPI.
- [x] 3.5 Keep validation failures deterministic by surfacing a diagnostic or safe error payload instead of crashing ordinary GUI routes.

## 4. Tests

- [x] 4.1 Add unit tests proving representative payloads with extra top-level and nested fields pass schema validation.
- [x] 4.2 Add unit tests proving missing GUI-required fields fail schema validation with clear validation errors.
- [x] 4.3 Add backend read-model tests proving current topic overview, graph, idea detail, record viewer, and file-list payloads validate.
- [x] 4.4 Add regression tests for topic-relative path display contract examples where full Topic Workspace paths are rendered as relative UI labels.

## 5. Verification

- [x] 5.1 Run `pixi run test` for Python unit tests.
- [x] 5.2 Run `npm test -- --run` from `web/ui` for frontend unit tests if frontend contract usage changes.
- [x] 5.3 Run `openspec validate add-gui-data-contract-schemas`.
