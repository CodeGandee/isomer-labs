## 1. Backend Graph Contract

- [x] 1.1 Inspect the current Topic Graph API, query-index relationship model, and Flash Attention topic data to confirm which fields identify `material_kind="idea"` versus supporting material.
- [x] 1.2 Make the idea-lineage overview response return only idea nodes when secondary material is not requested.
- [x] 1.3 Implement collapsed idea-to-idea edge projection from canonical lineage, accepted query-index relationships, or unambiguous secondary paths.
- [x] 1.4 Attach relation kind, collapsed-edge metadata, source relationship refs, and projection diagnostics to projected edges where available.
- [x] 1.5 Ensure ambiguous or missing lineage stays diagnostic instead of inventing authoritative idea edges.
- [x] 1.6 Ensure all idea-lineage overview and drill-down responses report read-only behavior and do not rebuild, repair, migrate, backfill, or write topic data.

## 2. Selected Idea Details

- [x] 2.1 Add or adapt a selected-idea detail read model that exposes source record refs, lineage, siblings, facets, files, diagnostics, and supporting secondary material for one idea.
- [x] 2.2 Lazy-load selected-idea detail data only after the user selects or opens an idea.
- [x] 2.3 Keep route decisions, claims, evidence, metrics, files, and diagnostics labeled as supporting details rather than peer ideas.

## 3. Frontend Workbench Behavior

- [x] 3.1 Change Idea Lineage defaults so the frontend does not request secondary material on initial open.
- [x] 3.2 Render only user-facing idea nodes in the default Idea Lineage tab and keep labels sourced from idea-facing text.
- [x] 3.3 Add an explicit advanced control for secondary material without changing filters for unrelated tabs or graph scopes.
- [x] 3.4 Open or reveal selected-idea details when the user selects an idea node, reusing existing tabs or panels where appropriate.
- [x] 3.5 Avoid fetching full payloads, rendered Markdown, Mermaid, KaTeX, PDF content, or expensive graph layouts until the relevant tab or detail surface is opened.

## 4. Tests and Validation

- [x] 4.1 Add backend tests for default idea-only graphs, collapsed edge metadata, diagnostics for ambiguous projections, topic-general behavior, and read-only responses.
- [x] 4.2 Add frontend tests for the default secondary-material filter, secondary opt-in control, selected-idea drill-down, and graph-scope filter isolation.
- [x] 4.3 Add or update Playwright smoke coverage so the Flash Attention topic opens with a clean idea overview, can opt into supporting details, and can open one idea's detail context.
- [x] 4.4 Run the relevant Python tests, frontend tests, lint or type checks touched by the implementation, and an OpenSpec validation for this change.
