## Context

Project Web already has a local web service, a Dockview-based TypeScript frontend, graph read APIs, and an idea-lineage panel backed by topic-scoped Research Idea graph data. The current Project Explorer exposes four entries under `Graphs`: `Idea Lineage`, `Artifact Overview`, `Experiment Records`, and `Paper Revisions`. The latter three route to a dense Sigma.js graph panel and currently produce an overview that is hard to use for research-progress navigation.

The domain language makes Research Idea the right lead concept for this surface. A Research Idea is a durable topic-scoped concept with status, visibility, aliases, realizations, and typed idea-level lineage edges. The GUI should therefore help users move between idea relationships and a chronological list of ideas before exposing dense artifact-specific maps.

## Goals / Non-Goals

**Goals:**

- Make the visible `Graphs` section idea-led by exposing separate `Idea Graph` and `Idea Timeline` views.
- Remove `Artifact Overview`, `Experiment Records`, and `Paper Revisions` from visible graph navigation for this iteration.
- Reuse the existing `idea-lineage` graph read model for the relationship view.
- Add a timeline/table view that sorts Research Ideas by creation time and derives display indexes and parent indexes from the same idea graph data.
- Open the existing idea detail page from both graph nodes and timeline rows.
- Preserve read-only browsing behavior and avoid query-index repair, rebuild, migration, or Workspace Runtime writes.

**Non-Goals:**

- Do not create, edit, merge, or reorder Research Ideas from the GUI.
- Do not redesign the idea detail page beyond using it as the common open target.
- Do not implement a new canonical timeline storage table.
- Do not remove the underlying canonical record, artifact, experiment, or paper data from Workspace Runtime.
- Do not make the timeline a final product shape; it is a separate view that can grow later.

## Decisions

### Keep `Graphs` as the Navigation Home

Keep the new views under the existing `Graphs` explorer group rather than creating a top-level `Ideas` group. This follows the user's correction and keeps graph-adjacent research navigation in one place.

Alternative considered: replace `Graphs` with a top-level `Ideas` group. That would make the information architecture cleaner for the current two views, but it would make the future return of non-idea graph views less obvious and contradicts the requested placement.

### Make Idea Graph and Idea Timeline Sibling Views

Expose graph presentation and timeline/table presentation as distinct openable views. The relationship view remains the idea graph; the timeline view is a separate graph-section view that can later grow into richer chronological progress tracking.

Alternative considered: use tabs inside one idea panel. That would share state easily, but it would blur two navigation targets and make browser history less explicit.

### Derive the First Timeline From `idea-lineage`

Build the first timeline/table from the topic graph read model for `idea-lineage`: nodes supply idea identity, titles, timestamps, status, and detail refs; edges supply parent-child relationships. The frontend can derive display index and parent indexes after sorting.

Alternative considered: add a dedicated backend timeline endpoint immediately. That gives a cleaner long-term contract, but the current data is already available and the first version does not require a new persistence model.

### Use Display Indexes as View-local Labels

The timeline assigns indexes from `1..N` after applying the current sort and filter. Parent indexes refer to the same visible index map when possible. If a parent is outside the visible set, the row should show a stable fallback such as the parent idea title or idea id instead of inventing a visible number.

Alternative considered: persist idea display indexes. Persisted indexes would be stable across filters but would create another identity-like field and conflict with the user's request to re-index for display.

### Open Idea Detail From Timeline Rows

Double-click on desktop and double-tap on touch open the same idea detail tab used by idea graph node opening. The open target should be `idea:<topicId>:<ideaId>` when the graph node has an `idea_id`, with existing record fallback only for legacy heuristic nodes.

Alternative considered: open the source record detail directly. That would be consistent with older record-centric views, but it would undercut the idea-led model and split graph and timeline behavior.

### Hide Dense Non-idea Views First

Remove `Artifact Overview`, `Experiment Records`, and `Paper Revisions` from the visible Project Explorer and frontend navigation for this change. Backend compatibility can remain temporarily if tests or old URLs depend on it, but new UI paths should not advertise or open those dense graph scopes.

Alternative considered: keep the sections but add warnings. That would preserve discoverability, but it leaves the least useful surfaces in the primary navigation and dilutes the idea-led workflow.

## Risks / Trade-offs

- Timeline rows with missing `created_at` values can sort unpredictably → Use a deterministic fallback order: `created_at`, `updated_at`, title, then `idea_id`, and keep missing times visibly blank or marked unknown.
- Parent indexes can become confusing when filters hide parent nodes → Use the visible index when available and a stable fallback label when the parent is hidden.
- Existing tests may assume four graph scopes → Update tests and history parsing to cover visible idea views while keeping backend compatibility explicit where retained.
- Large idea graphs may still be hard to render as React Flow → The timeline remains useful for large topics, and the graph view can keep existing renderer selection behavior for now.
- Users may expect dense artifact views to exist because old docs mention them → Update Project Web docs and UI contract docs to describe the current idea-led graph navigation.

## Migration Plan

1. Update Project Explorer graph children and openable descriptors so visible navigation contains idea graph and idea timeline entries.
2. Add the frontend idea timeline panel, table derivation logic, and row-open interaction.
3. Update graph scope/view typing, history parsing, event invalidation scopes, and tests for the visible view set.
4. Update contracts and documentation for the idea timeline view and the current graph navigation.
5. Keep rollback simple: restoring the previous Project Explorer graph scope list and dense panel route restores the old visible sections.

## Open Questions

- Should old deep links to `artifact-overview`, `experiment-records`, and `paper-revisions` keep rendering during a compatibility window, or should the API reject them immediately once the GUI stops exposing them?
- Should the timeline default to all primary ideas only, or should it offer an explicit supporting-record toggle later, matching Idea Lineage?
