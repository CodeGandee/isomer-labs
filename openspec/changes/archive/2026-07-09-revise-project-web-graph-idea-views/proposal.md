## Why

The current Project Web `Graphs` section exposes dense Sigma.js views for artifacts, experiment records, and paper revisions, but those views do not help users track research progress. The GUI should make Research Ideas the lead object, with one view for idea relationships and another chronological table view for scanning how ideas emerged over time.

## What Changes

- Remove `Artifact Overview`, `Experiment Records`, and `Paper Revisions` from the visible `Graphs` section in the Project Explorer.
- **BREAKING**: Remove support for old dense graph URLs and graph scopes for `artifact-overview`, `experiment-records`, and `paper-revisions`; old URLs using those scopes will no longer work.
- Keep graph presentation and timeline/table presentation as separate sibling views under `Graphs`.
- Rename or present the existing idea relationship view as the idea graph view, backed by the current `idea-lineage` read model and existing idea detail opening path.
- Add an idea timeline/table view that lists ideas sorted by time and shows creation time, short display key, idea title, and parent display keys.
- Add search and filtering controls to Idea Timeline, matching the graph view's search, status, relation, and Supporting Records filtering pattern where applicable.
- Add sortable table headers for every visible Idea Timeline column and an in-view entry-count control so users can choose how many rows are shown without opening settings.
- Add a Supporting Records toggle to Idea Timeline: Primary Ideas are the default view, and users can opt into supporting Research Idea rows when needed.
- Add configurable timeline row category coloring, defaulting on, with light green rows for Primary Ideas and light yellow rows for supporting ideas.
- Add a short topic-scoped `display_key` for each Research Idea record so the GUI can show stable readable handles such as `I1`, `I2`, and `I3` instead of long ids, with topic-scoped uniqueness enforced by the Workspace Runtime database schema.
- Add resilient handling for live research changes: new ideas, deleted ideas, changed lineage edges, and malformed or non-interpretable graph data must not crash the GUI.
- Add backend recent-error query capability backed by a service-local bounded in-memory ring buffer so the GUI can show recent read-model or interpretation errors when timeline or lineage data becomes inconsistent.
- Make double-click and double-tap on an idea row open the same idea detail page used by graph node opening.
- Preserve read-only browsing behavior: graph and timeline views must not rebuild, repair, migrate, or write Workspace Runtime or query-index state.

## Capabilities

### New Capabilities
- `project-web-idea-timeline-view`: Provides the idea timeline/table view under Project Web `Graphs`, including time sorting, short display keys, parent display-key references, and row opening behavior.
- `research-idea-display-key`: Provides short, unique, topic-scoped display keys for Research Ideas.
- `project-web-recent-errors-query`: Provides a backend read API for recent Project Web read-model and interpretation errors observed by the running GUI service process.

### Modified Capabilities
- `project-web-gui`: Changes the visible Project Explorer graph navigation to remove dense non-idea graph sections and expose idea graph and idea timeline views.
- `topic-graph-read-api`: Adds a timeline-friendly idea read model contract using the same topic-scoped graph data semantics and Research Idea display keys without introducing browsing mutations.
- `project-web-data-contracts`: Updates GUI contract coverage for the idea timeline/table payload shape and graph scope/view metadata used by the frontend.
- `topic-idea-lineage-overview`: Clarifies that the existing idea relationship graph remains a separate graph view under `Graphs`, not a merged tab inside another panel.

## Impact

- Affected frontend code: `web/ui/src/App.tsx`, `web/ui/src/features/idea-lineage/IdeaLineagePanel.tsx`, graph utilities, workbench history, event invalidation scope handling, settings handling, table styling, and related tests.
- Affected backend code: Research Idea runtime model, Research Idea database schema constraints, Research Idea write/import/repair paths, display-key allocator state or tombstone tracking, Project Explorer openable descriptors, and graph/read-model helpers under `src/isomer_labs/web/`.
- Affected contracts and docs: `docs/ui/contracts/topic-graph.md` or a new focused idea timeline contract page, plus schema tests for the frontend/backend payload shape.
- Affected diagnostics APIs: add a read-only recent-errors query surface for recent graph/timeline interpretation failures and warnings held in service-local memory.
- A Workspace Runtime schema migration or compatibility upgrade is expected to add monotonic decimal Research Idea display-key storage and allocator history. Existing Research Ideas receive display keys only through an explicit migration or repair operation, not through Project Web browsing or unrelated runtime opens. Timeline rows can still derive relationships from canonical Research Idea graph nodes and lineage edges.
