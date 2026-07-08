## Context

Project Web currently consumes several backend read models: topic overview, project explorer nodes, graph views, idea details, record descriptors, record files, diagnostics, and rendered content. The endpoint specs describe many of these APIs, but there is no single documentation area for GUI contract authors, and there is no Python schema layer that checks the minimal fields the TypeScript GUI requires before the payload reaches the browser.

Research agents and extension code often add metadata that the GUI does not need immediately. The contract layer must therefore validate required GUI fields while allowing extra fields to pass through, so richer payloads remain useful for future viewers and JSON inspection.

## Goals / Non-Goals

**Goals:**

- Create `docs/ui/contracts/` as the human-readable home for GUI-usable data contracts.
- Add permissive Python schemas for Project Web read models and GUI-consumed artifact fragments.
- Make required GUI fields explicit, including stable ids, titles, node labels, relationship endpoints, Markdown availability, file openability, and diagnostics.
- Provide tests that prove missing required fields fail and extra fields are accepted.
- Keep documentation and schemas aligned enough that future agents can update both together.

**Non-Goals:**

- Do not replace Workspace Runtime, query-index, or Research Idea storage schemas.
- Do not require agents to omit extra metadata from records or payloads.
- Do not add a database migration.
- Do not duplicate the TypeScript zod schemas as the only source of truth.
- Do not force every backend endpoint to validate every response synchronously if a cheaper boundary check is enough.

## Decisions

### Use Pydantic models with permissive extras

Add a Python module under `src/isomer_labs/web/` for GUI data contracts, using Pydantic v2 models with `extra="allow"` or equivalent permissive behavior. Pydantic is already present through the FastAPI stack, supports nested validation, and fits the existing Python service boundary.

Alternative considered: JSON Schema files only. That would help documentation and cross-language validation, but it would add a second runtime validation path or require a validator dependency. Python models are cheaper for the current backend and can later export JSON Schema if needed.

### Separate UI contracts from canonical storage contracts

The docs and schemas will describe what Project Web needs to render safely, not what agents must store in Workspace Runtime. A query-index export may include more fields than the GUI consumes, and a structured payload may contain richer scientific metadata than any current viewer knows how to render.

Alternative considered: make UI schemas validate canonical payloads. That would overfit frontend needs to research storage and would make agents treat the GUI as the storage authority.

### Document one page per user-facing contract shape

Create `docs/ui/contracts/index.md` plus focused pages such as topic overview, graph view, idea detail, record viewer, record files, diagnostics, and display paths. Each page should name required fields, optional useful fields, extra-field policy, and examples.

Alternative considered: one large contract document. It would be quicker to write, but it would be harder for agents to update when one viewer changes.

### Validate at backend and test boundaries

Backend read-model code should validate payloads where a response becomes a GUI contract, especially topic overview, graph view, idea detail, and record file payloads. Unit tests should also validate representative fixture payloads, including extra fields, so regressions are caught before browser code breaks.

Alternative considered: validate only in the browser with zod. The TypeScript schemas are useful but too late for backend-generated fixtures, Python API tests, and agent-authored data normalization.

## Risks / Trade-offs

- Schema drift between docs, Python, and TypeScript → Add tests for representative payloads and require docs updates when schema fields change.
- Over-validation could reject useful agent metadata → Configure schemas to allow extra fields and only require GUI-critical fields.
- Under-validation could miss semantic issues → Keep deeper invariants in existing domain validators, query-index validation, and runtime validation.
- Developers may confuse UI contracts with storage contracts → State the boundary in `docs/ui/contracts/index.md` and schema module docstrings.

## Migration Plan

1. Add `docs/ui/contracts/` with initial contract pages for existing Project Web views.
2. Add permissive Python schema models for the same contract shapes.
3. Add unit tests that validate current fixture-like payloads and extra-field tolerance.
4. Wire backend read-model responses through the schema layer where practical without changing API shapes.
5. Keep existing frontend zod parsing in place as a browser-side guard.

Rollback is simple: remove schema enforcement call sites while keeping the docs and models for reference. No persisted data migration is involved.

## Open Questions

- Should the Python schema models later export JSON Schema files for TypeScript generation, or should TypeScript zod schemas remain maintained manually?
- Which GUI contract pages should be considered mandatory for first implementation: all existing Project Web panels, or only topic overview, idea lineage, idea detail, and record files?
