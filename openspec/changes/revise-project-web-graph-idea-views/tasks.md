## 1. Backend Navigation and Read Models

- [ ] 1.1 Update Project Explorer graph children so visible Research Topic `Graphs` entries are Idea Graph and Idea Timeline only.
- [ ] 1.2 Add or revise openable descriptors so Idea Graph opens the existing idea relationship graph component and Idea Timeline opens a timeline/table component.
- [ ] 1.3 Preserve read-only behavior for graph and timeline data requests, with no index rebuild, cleanup, repair, migration, backfill, or Workspace Runtime writes.
- [ ] 1.4 Decide and implement compatibility behavior for old `artifact-overview`, `experiment-records`, and `paper-revisions` deep links or API requests.

## 2. Frontend View Identity and Routing

- [ ] 2.1 Update graph/view TypeScript types, workbench history parsing, event invalidation scopes, and view labels for Idea Graph and Idea Timeline.
- [ ] 2.2 Remove the visible dense graph panel route from normal explorer navigation while keeping any chosen compatibility path explicit.
- [ ] 2.3 Ensure Idea Graph still opens the existing idea-lineage relationship view and keeps current hover, selection, and double-click behavior.
- [ ] 2.4 Add Dockview component registration and openable handling for the Idea Timeline view.

## 3. Idea Timeline Table

- [ ] 3.1 Implement timeline row derivation from topic-scoped idea graph/read-model data, including stable idea identity, title, creation time, updated time fallback, and parent edge refs.
- [ ] 3.2 Sort timeline rows by creation time with deterministic fallback to updated time, title, and idea id.
- [ ] 3.3 Assign display indexes from `1..N` after current sort and filtering.
- [ ] 3.4 Render parent indexes from the same visible index map, with stable fallback labels for hidden or missing parents.
- [ ] 3.5 Render the timeline table with columns for creation time, display index, idea title, and parents.
- [ ] 3.6 Implement row single-select behavior without opening detail.
- [ ] 3.7 Implement row double-click and touch double-tap behavior that opens the same idea detail tab as graph node opening.

## 4. Contracts and Documentation

- [ ] 4.1 Update `docs/ui/contracts/` to document the Idea Timeline payload or extend the topic graph contract for timeline use.
- [ ] 4.2 Update GUI schema validation coverage for timeline-required fields and graph/view metadata.
- [ ] 4.3 Update manual or developer Project Web docs that mention the previous dense graph sections.

## 5. Tests and Validation

- [ ] 5.1 Add or update backend tests for Project Explorer graph entries and openable descriptors.
- [ ] 5.2 Add frontend tests for Idea Timeline row derivation, sorting, display indexes, parent indexes, and row opening.
- [ ] 5.3 Update existing tests that assume `Artifact Overview`, `Experiment Records`, and `Paper Revisions` are visible graph entries.
- [ ] 5.4 Run `pixi run lint`.
- [ ] 5.5 Run `pixi run typecheck`.
- [ ] 5.6 Run `pixi run test`.
