## 1. Backend Navigation and Read Models

- [x] 1.1 Update Project Explorer graph children so visible Research Topic `Graphs` entries are Idea Graph and Idea Timeline only.
- [x] 1.2 Add or revise openable descriptors so Idea Graph opens the existing idea relationship graph component and Idea Timeline opens a timeline/table component.
- [x] 1.3 Preserve read-only behavior for graph and timeline data requests, with no index rebuild, cleanup, repair, migration, backfill, or Workspace Runtime writes.
- [x] 1.4 Remove support for old `artifact-overview`, `experiment-records`, and `paper-revisions` deep links or API requests, and ensure they use unsupported graph-scope behavior.
- [x] 1.5 Add bounded service-local in-memory recent-errors query support for graph and timeline read-model interpretation warnings or failures.
- [x] 1.6 Add Research Idea `display_key` storage and topic-scoped uniqueness validation backed by a Workspace Runtime database unique constraint.
- [x] 1.7 Assign short monotonic decimal display keys such as `I1`, `I2`, and `I3` when Research Ideas are created, imported, or repaired, and reject colliding provided keys instead of silently remapping them.
- [x] 1.8 Add explicit operator-invoked migration or repair support for existing Research Ideas without display keys.
- [x] 1.9 Add persisted allocator state or deleted-key tombstone handling so hard-deleted idea keys are not automatically reused.

## 2. Frontend View Identity and Routing

- [x] 2.1 Update graph/view TypeScript types, workbench history parsing, event invalidation scopes, and view labels for Idea Graph and Idea Timeline.
- [x] 2.2 Remove dense graph panel routing from the supported frontend graph view set.
- [x] 2.3 Ensure Idea Graph still opens the existing idea-lineage relationship view and keeps current hover, selection, and double-click behavior.
- [x] 2.4 Add Dockview component registration and openable handling for the Idea Timeline view.
- [x] 2.5 Wire timeline warning states to recent-errors query access when current data is non-interpretable.
- [x] 2.6 Add Project Web settings support for Idea Timeline row category coloring, with default-on behavior, configurable Primary Idea/supporting idea colors, and an off switch.
- [x] 2.7 Add Idea Timeline search and filtering controls aligned with the graph view controls, including search, status, relation, and Supporting Records filtering.
- [x] 2.8 Add sortable Idea Timeline column headers for every visible column and an in-view entry-count control that does not require opening the settings panel.

## 3. Idea Timeline Table

- [x] 3.1 Implement timeline row derivation from topic-scoped idea graph/read-model data, including stable idea identity, title, visibility/supporting metadata, creation time, updated time fallback, and parent edge refs.
- [x] 3.2 Sort timeline rows by creation time with deterministic fallback to updated time, title, and idea id.
- [x] 3.3 Render each idea row using the persisted short `display_key` from the read model, not the visible row position.
- [x] 3.4 Render parent references using parent display keys when available, with idea-id fallback and warnings for missing parents.
- [x] 3.5 Render the timeline table with columns for creation time, display key, idea title, and parents.
- [x] 3.6 Implement row single-select behavior without opening detail.
- [x] 3.7 Implement row double-click and touch double-tap behavior that opens the same idea detail tab as graph node opening.
- [x] 3.8 Add a Supporting Records toggle that defaults off and includes supporting Research Idea rows only when explicitly enabled, without rendering raw source records as peer timeline rows.
- [x] 3.9 Preserve timeline selection by `idea_id` across live refreshes and clear it with a warning when the selected idea disappears.
- [x] 3.10 Add defensive handling for missing parents, malformed edges, duplicate ids, invalid timestamps, cycles, and non-interpretable payloads.
- [x] 3.11 Render timeline row category coloring using light green for Primary Ideas and light yellow for supporting ideas by default, while preserving non-color category cues.
- [x] 3.12 Apply timeline search and filters over display key, title, aliases, one-liner, family, status, parent display-key labels, and lineage relation kinds without mutating stored data.
- [x] 3.13 Preserve or clear timeline selection predictably when active filters hide the selected idea.
- [x] 3.14 Apply column sorting over creation time, display key, title, and parent display-key lists with deterministic fallback ordering.
- [x] 3.15 Apply the in-view entry-count control after filtering and sorting, while preserving row identity by `idea_id`.

## 4. Contracts and Documentation

- [x] 4.1 Update `docs/ui/contracts/` to document the Idea Timeline payload or extend the topic graph contract for timeline use.
- [x] 4.2 Update `docs/ui/contracts/` to document recent-errors payloads or extend diagnostics contract coverage for recent read-model errors, including the service-local in-memory lifetime.
- [x] 4.3 Update GUI schema validation coverage for timeline-required fields, recent-errors fields, graph/view metadata, timeline row-coloring settings, timeline search/filter state, timeline sort state, and entry-count state.
- [x] 4.4 Update manual or developer Project Web docs that mention the previous dense graph sections.

## 5. Tests and Validation

- [x] 5.1 Add or update backend tests for Project Explorer graph entries and openable descriptors.
- [x] 5.2 Add backend tests for recent-errors query behavior, malformed graph/timeline diagnostics, database-backed display-key uniqueness, colliding provided-key rejection, and the absence of automatic display-key backfill during Project Web browsing or unrelated runtime opens.
- [x] 5.3 Add frontend tests for Idea Timeline row derivation, column sorting, entry-count control, display keys, parent display-key references, supporting-record toggle, search/filtering behavior, row category coloring settings, live refresh selection, warnings, and row opening.
- [x] 5.4 Update existing tests that assume `Artifact Overview`, `Experiment Records`, and `Paper Revisions` are visible graph entries.
- [x] 5.5 Run `pixi run lint`.
- [x] 5.6 Run `pixi run typecheck`.
- [x] 5.7 Run `pixi run test`.
