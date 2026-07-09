## Context

Project Web already has a local web service, a Dockview-based TypeScript frontend, graph read APIs, and an idea-lineage panel backed by topic-scoped Research Idea graph data. The current Project Explorer exposes four entries under `Graphs`: `Idea Lineage`, `Artifact Overview`, `Experiment Records`, and `Paper Revisions`. The latter three route to a dense Sigma.js graph panel and currently produce an overview that is hard to use for research-progress navigation.

The domain language makes Research Idea the right lead concept for this surface. A Research Idea is a durable topic-scoped concept with status, visibility, aliases, realizations, and typed idea-level lineage edges. The GUI should therefore help users move between idea relationships and a chronological list of ideas before exposing dense artifact-specific maps.

## Goals / Non-Goals

**Goals:**

- Make the visible `Graphs` section idea-led by exposing separate `Idea Graph` and `Idea Timeline` views.
- Remove `Artifact Overview`, `Experiment Records`, and `Paper Revisions` from visible graph navigation for this iteration.
- Reuse the existing `idea-lineage` graph read model for the relationship view.
- Add a timeline/table view that sorts Research Ideas by creation time and shows short display keys and parent display-key references from the same idea graph data.
- Add search and filtering controls for Idea Timeline, aligned with the graph view's search, status, relation, and Supporting Records filters where applicable.
- Add sortable column headers and an in-view entry-count control for Idea Timeline.
- Add a Supporting Records toggle for Idea Timeline while keeping Primary Ideas as the default view.
- Add configurable row category coloring for Idea Timeline, defaulting on with light green Primary Idea rows and light yellow supporting idea rows.
- Guard against live data churn, missing ideas, deleted ideas, changed lineage relationships, malformed edges, cycles, and non-interpretable timeline data without crashing the GUI.
- Add a backend recent-errors query capability for recent read-model interpretation failures and warnings.
- Open the existing idea detail page from both graph nodes and timeline rows.
- Preserve read-only browsing behavior and avoid query-index repair, rebuild, migration, or Workspace Runtime writes.

**Non-Goals:**

- Do not create, edit, merge, or reorder Research Ideas from the GUI.
- Do not redesign the idea detail page beyond using it as the common open target.
- Do not implement a new canonical timeline storage table.
- Do not use SQLite row position, rowid, or current table order as the user-facing idea handle.
- Do not render raw source records as peer rows in the first Idea Timeline table.
- Do not remove the underlying canonical record, artifact, experiment, or paper data from Workspace Runtime.
- Do not make the timeline a final product shape; it is a separate view that can grow later.
- Do not enforce data-integrity limits on what users or research runs can do to Research Idea data; the GUI must tolerate imperfect data instead of becoming an authority that rejects it.

## Decisions

### Keep `Graphs` as the Navigation Home

Keep the new views under the existing `Graphs` explorer group rather than creating a top-level `Ideas` group. This follows the user's correction and keeps graph-adjacent research navigation in one place.

Alternative considered: replace `Graphs` with a top-level `Ideas` group. That would make the information architecture cleaner for the current two views, but it would make the future return of non-idea graph views less obvious and contradicts the requested placement.

### Make Idea Graph and Idea Timeline Sibling Views

Expose graph presentation and timeline/table presentation as distinct openable views. The relationship view remains the idea graph; the timeline view is a separate graph-section view that can later grow into richer chronological progress tracking.

Alternative considered: use tabs inside one idea panel. That would share state easily, but it would blur two navigation targets and make browser history less explicit.

### Derive Timeline Relationships From `idea-lineage`

Build the first timeline/table from the topic graph read model for `idea-lineage`: nodes supply idea identity, short display keys, titles, timestamps, status, and detail refs; edges supply parent-child relationships. The frontend can sort rows for presentation, but it should not invent the readable idea handle.

Alternative considered: add a dedicated backend timeline endpoint immediately. That gives a cleaner long-term contract, but the current data is already available and the first version does not require a new persistence model.

### Default to Primary Ideas With Supporting Records Toggle

The Idea Timeline defaults to Primary Ideas so the first table remains a readable progress view. It also exposes an explicit Supporting Records toggle, matching the graph-side label, so users can include supporting Research Ideas when they need a broader chronology. Raw source records may appear as row metadata, links, or detail content, but they are not peer table rows in this first timeline version because they do not have idea display keys or idea parent references.

Alternative considered: Primary Ideas only. That would be simpler, but it would make supporting material inaccessible from the timeline even though the timeline is expected to grow. Another alternative was to include all ideas by default; that risks recreating the dense-view noise this change removes.

### Match Graph View Search and Filtering

Idea Timeline should expose search and filtering controls similar to the Idea Graph view so users can narrow the chronological list without leaving the graph section. The first slice should support free-text search over display key, title, aliases, one-liner, family, status, and parent display-key labels; status filtering for idea lifecycle status; relation filtering using parent-child lineage edge kinds where available; and the Supporting Records toggle described above. Filtering changes the visible rows only and must not rewrite display keys, mutate Workspace Runtime, or change row-open identity.

Alternative considered: table-only browser controls with no search. That keeps the first timeline smaller, but it makes the view weak for large research topics and inconsistent with graph navigation. Another alternative was search-only without status or relation filters; that is simpler, but users already have a graph-side filtering vocabulary that should carry over.

### Sort and Limit Entries In the Timeline View

Idea Timeline should let users sort entries by every visible table column: creation time, display key, idea title, and parents. The default sort remains chronological by creation time with deterministic fallback to updated time, title, and `idea_id`. Clicking or activating a column header should toggle the sort direction for that column, with stable fallback ordering so repeated refreshes do not shuffle equal values. Parent-column sorting should use the rendered parent display-key list, falling back to parent idea ids when display keys are unavailable. The view should also expose an in-panel entry-count control, such as a compact rows-per-page or entries-shown selector, so users can choose the number of rows shown without opening the settings panel. Sorting and entry-count changes affect visible rows only and must not mutate Workspace Runtime, rewrite display keys, or change row-open identity.

Alternative considered: put row-count control in Project Web settings. That would keep the timeline toolbar smaller, but the user explicitly wants to change the number of shown entries inside the view while browsing. Another alternative was fixed chronological sorting only; that is too limiting once the table has searchable columns.

### Use Configurable Row Category Coloring

Idea Timeline should color rows by category by default: light green for Primary Ideas and light yellow for supporting ideas. The setting should be configurable in Project Web settings and users must be able to turn category coloring off. Row category should also remain available through text, metadata, or other non-color cues so disabling color does not remove the meaning.

Alternative considered: no row coloring. That keeps the table visually quieter, but it makes primary/supporting distinction harder to scan once supporting rows are enabled. Another alternative was fixed non-configurable coloring; that is simpler but leaves no escape hatch for accessibility or personal preference.

### Persist Short Research Idea Display Keys

Each Research Idea should have a short topic-scoped `display_key` used by the GUI as a readable handle. Use monotonic decimal keys such as `I1`, `I2`, and `I3` within each Topic Workspace. The key must be unique for each idea record in a Topic Workspace, with uniqueness enforced by the Workspace Runtime database schema, stable across GUI refreshes, and not derived from the current visible table rows. Parent references in the timeline should use parent display keys when available, with `idea_id` as a fallback and a warning when the referenced parent is missing.

Alternative considered: derive display indexes from the current sorted set. That keeps implementation lighter, but it shifts when ideas are added, deleted, hidden, or filtered. Another alternative was SQLite row order or rowid; that is unsuitable for GUI handles because it is implementation-local and fragile across imports, rebuilds, or migrations.

### Allocate Display Keys at Idea Write or Repair Time

Display keys should be assigned when a Research Idea is first written, imported, or repaired. Existing ideas without a display key should be handled by an explicit operator-invoked migration or repair path, not silently renumbered by ordinary GUI browsing, generic runtime open, or unrelated write activity. The allocator should issue the next unused monotonic decimal key for the Topic Workspace and must not automatically reuse a deleted idea's display key. If an import or repair proposes a display key that already belongs to another Research Idea in the same Topic Workspace, validation should reject the write and surface diagnostics; the implementation must not silently remap a provided key. If hard deletes are supported, Workspace Runtime needs persisted allocator state or deleted-key tombstone history sufficient to prevent accidental reuse.

Alternative considered: generate keys only in the graph read model. That would keep storage unchanged, but it would make the readable handle less durable and harder to use in later docs, warnings, or operator instructions.

### Preserve Timeline State on Live Updates by Identity and Display Key

The GUI should treat `idea_id` as the durable selection/opening identity and `display_key` as the readable handle. New ideas should arrive with new display keys. Deleted ideas disappear without forcing surviving ideas to receive new keys. Changed lineage edges should recompute parent display-key references from the latest graph/timeline payload.

Alternative considered: preserve row positions across live updates. That would make the table look stable, but row position is not the concept the user wants to track.

### Treat Non-interpretable Idea Data as Diagnostics

The GUI must not crash when idea data is inconsistent. Missing edge endpoints, deleted parent ideas, duplicate node ids, invalid timestamps, cycles, malformed relationship rows, or contradictory graph payloads should produce visible warnings and degraded rows where possible. If the data cannot be interpreted enough to render safely, the view should show a warning/empty state and link or expose recent errors from the backend.

Alternative considered: enforce strict data integrity before rendering. That would simplify the frontend but contradicts the product boundary: users and research runs may alter these records freely, and Project Web is a read-only inspector.

### Add Recent Errors Query Capability

Add a read-only backend endpoint for recent Project Web read-model or interpretation errors, scoped by topic when possible. Back it with a bounded in-memory ring buffer owned by the running Project Web service process. This endpoint should return bounded, newest-first errors with timestamps, topic id, source view, severity, code, message, and optional record/idea refs. Timeline and graph views can use it to show recent problems without crashing or hiding all context.

Alternative considered: persist recent errors in Workspace Runtime. That would preserve errors across Project Web restarts, but it would turn read-model failures into runtime writes and introduce retention concerns. Another alternative was to rely only on per-response diagnostics. Per-response diagnostics remain useful, but a recent-errors query gives the GUI and operator a way to inspect problems that happened during auto-refresh, SSE invalidation, or previous failed interpretations.


### Open Idea Detail From Timeline Rows

Double-click on desktop and double-tap on touch open the same idea detail tab used by idea graph node opening. The open target should be `idea:<topicId>:<ideaId>` when the graph node has an `idea_id`, with existing record fallback only for legacy heuristic nodes.

Alternative considered: open the source record detail directly. That would be consistent with older record-centric views, but it would undercut the idea-led model and split graph and timeline behavior.

### Remove Dense Non-idea Views Cleanly

Remove `Artifact Overview`, `Experiment Records`, and `Paper Revisions` from visible Project Explorer navigation and from supported Project Web graph scope handling. This is an intentional breaking change: old URLs or API calls for `artifact-overview`, `experiment-records`, and `paper-revisions` should fail with the normal unsupported graph-scope behavior instead of rendering compatibility views.

Alternative considered: hide the sections from navigation while keeping backend and deep-link compatibility. That would reduce migration risk, but it would preserve code paths for views that the product is intentionally removing. A clean break makes the implementation and tests easier to reason about.

## Risks / Trade-offs

- Timeline rows with missing `created_at` values can sort unpredictably → Use a deterministic fallback order: `created_at`, `updated_at`, title, then `idea_id`, and keep missing times visibly blank or marked unknown.
- Display-key allocation can collide during imports or repair → Enforce topic-scoped uniqueness in the Workspace Runtime database schema and surface deterministic diagnostics when a proposed key collides.
- Hard-deleted ideas can remove evidence of prior display keys → Persist allocator state or deleted-key tombstones so new ideas do not automatically reuse old keys.
- Existing ideas may lack display keys → Add an explicit migration or repair task that assigns keys only when invoked and reports any ideas that still lack keys.
- Parent display keys can be missing when parent ideas are deleted or malformed → Use `idea_id` fallback labels and visible warnings when lineage is no longer interpretable.
- Timeline search/filtering can hide selected rows or parents → Preserve selection by `idea_id` when still visible, clear or mark it when filtered out, and keep parent fallback warnings independent of filtering.
- Timeline sorting or entry-count changes can hide or move selected rows → Preserve selection by `idea_id` when the row remains visible, and keep activation bound to idea identity rather than row position.
- Recent error reporting can grow noisy → Bound recent-error results, include severity/source fields, and keep per-view warnings concise.
- In-memory recent errors disappear when Project Web restarts → Treat the endpoint as live troubleshooting support, not durable audit history.
- Row coloring can conflict with accessibility or user preference → Keep coloring configurable, default it on, and provide a setting to turn it off.
- Existing tests may assume four graph scopes → Update tests and history parsing to cover the new idea view set and unsupported-scope behavior for removed dense scopes.
- Large idea graphs may still be hard to render as React Flow → The timeline remains useful for large topics, and the graph view can keep existing renderer selection behavior for now.
- Users may expect dense artifact views to exist because old docs mention them → Update Project Web docs and UI contract docs to describe the current idea-led graph navigation.

## Migration Plan

1. Update Project Explorer graph children and openable descriptors so visible navigation contains idea graph and idea timeline entries.
2. Add Research Idea display-key storage, allocation, uniqueness validation, and explicit operator-invoked migration or repair support.
3. Add recent-error collection/query support for graph and timeline interpretation failures.
4. Add the frontend idea timeline panel, table derivation logic, search/filter controls, column sorting, in-view entry-count control, supporting-record toggle, warning state, and row-open interaction.
5. Update graph scope/view typing, history parsing, event invalidation scopes, and tests for the visible view set.
6. Update contracts and documentation for the idea timeline view, recent errors query, display keys, and the current graph navigation.
7. Keep rollback simple: restoring the previous Project Explorer graph scope list and dense panel route restores the old visible sections; display keys can remain harmless extra Research Idea metadata.

## Open Questions

No blocking open questions remain for the first implementation slice.
