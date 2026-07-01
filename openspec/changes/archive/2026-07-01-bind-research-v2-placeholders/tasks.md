## 1. Research Record Extension

- [x] 1.1 Add a runtime-backed research records service that can create, show, list, update, and archive generic research records in a selected Topic Workspace.
- [x] 1.2 Register `isomer-cli ext research records create/show/list/update/delete` commands with deterministic JSON and topic-context errors.
- [x] 1.3 Add unit tests for record CRUD, body storage, filtering, placeholder metadata, and archive behavior.

## 2. Placeholder Binding Pages

- [x] 2.1 Generate `placeholder-bindings.md` for each active v2 research skill that has `migrate/placeholders.md`.
- [x] 2.2 Update v2 skill entrypoints and workspace-manager reference routing so agents read `placeholder-bindings.md` before writing durable placeholder outputs.

## 3. Validation

- [x] 3.1 Extend research-paradigm validation to require binding pages and exact placeholder coverage.
- [x] 3.2 Add unit tests for missing binding page, missing placeholder binding, and extra placeholder binding diagnostics.

## 4. Documentation

- [x] 4.1 Document `ext research records` in CLI docs and command surface text.
- [x] 4.2 Update the storage support plan to describe the transitional extension-backed binding layer.

## 5. Verification

- [x] 5.1 Run focused unit tests for the research records extension and research-paradigm validation.
- [x] 5.2 Run repository validation commands relevant to docs and research skillsets.
