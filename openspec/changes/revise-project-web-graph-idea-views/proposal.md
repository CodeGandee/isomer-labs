## Why

The current Project Web `Graphs` section exposes dense Sigma.js views for artifacts, experiment records, and paper revisions, but those views do not help users track research progress. The GUI should make Research Ideas the lead object, with one view for idea relationships and another chronological table view for scanning how ideas emerged over time.

## What Changes

- Remove `Artifact Overview`, `Experiment Records`, and `Paper Revisions` from the visible `Graphs` section in the Project Explorer.
- Keep graph presentation and timeline/table presentation as separate sibling views under `Graphs`.
- Rename or present the existing idea relationship view as the idea graph view, backed by the current `idea-lineage` read model and existing idea detail opening path.
- Add an idea timeline/table view that lists ideas sorted by time and shows creation time, display index, idea title, and parent idea indexes.
- Make double-click and double-tap on an idea row open the same idea detail page used by graph node opening.
- Preserve read-only browsing behavior: graph and timeline views must not rebuild, repair, migrate, or write Workspace Runtime or query-index state.

## Capabilities

### New Capabilities
- `project-web-idea-timeline-view`: Provides the idea timeline/table view under Project Web `Graphs`, including time sorting, display indexes, parent indexes, and row opening behavior.

### Modified Capabilities
- `project-web-gui`: Changes the visible Project Explorer graph navigation to remove dense non-idea graph sections and expose idea graph and idea timeline views.
- `topic-graph-read-api`: Adds a timeline-friendly idea read model contract using the same topic-scoped graph data semantics without introducing mutations.
- `project-web-data-contracts`: Updates GUI contract coverage for the idea timeline/table payload shape and graph scope/view metadata used by the frontend.
- `topic-idea-lineage-overview`: Clarifies that the existing idea relationship graph remains a separate graph view under `Graphs`, not a merged tab inside another panel.

## Impact

- Affected frontend code: `web/ui/src/App.tsx`, `web/ui/src/features/idea-lineage/IdeaLineagePanel.tsx`, graph utilities, workbench history, event invalidation scope handling, table styling, and related tests.
- Affected backend code: Project Explorer openable descriptors and graph/read-model helpers under `src/isomer_labs/web/`.
- Affected contracts and docs: `docs/ui/contracts/topic-graph.md` or a new focused idea timeline contract page, plus schema tests for the frontend/backend payload shape.
- No database migration is expected. The timeline can derive from canonical Research Idea graph nodes and lineage edges already returned for `idea-lineage`.
