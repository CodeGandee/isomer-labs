# Idea Graph and Timeline Design Choices

## Context

The Project Web `Graphs` section is being revised into idea-led navigation. The existing dense graph sections are removed as a breaking change, while Idea Graph and Idea Timeline remain separate views under `Graphs`.

## Decisions

| Question | Decision |
| --- | --- |
| Display-key format | Use monotonic topic-scoped decimal keys such as `I1`, `I2`, and `I3`. Do not automatically reuse deleted keys. |
| Existing ideas without keys | Assign missing keys only through explicit operator-invoked migration or repair. Project Web browsing, generic runtime open, and unrelated writes do not backfill keys. |
| Recent-errors storage | Use a service-local bounded in-memory ring buffer owned by the running Project Web process. Recent errors are live troubleshooting state, not durable audit history. |
| Display-key collisions | Enforce topic-scoped `display_key` uniqueness in the Workspace Runtime database schema. Reject colliding provided keys with diagnostics instead of silently remapping them. |
| Supporting Records toggle | Include supporting Research Idea rows only. Raw source records may appear as metadata, links, or detail content, but not as peer timeline rows. |
| Timeline row coloring | Default row category coloring on: light green for Primary Ideas and light yellow for supporting ideas. Make colors configurable in Project Web settings and provide an off switch. |
| Timeline search and filtering | Provide graph-like controls for search, status, lineage relation, and Supporting Records filtering. Filtering changes visible rows only and does not mutate stored display keys or runtime data. |
| Timeline sorting and entry count | Allow sorting by every visible column and provide an in-view entry-count control. Sorting and entry-count changes affect visible rows only and keep row identity bound to `idea_id`. |

## Rejected Alternatives

- View-local row indexes were rejected because hidden, deleted, filtered, or newly added ideas would shift labels.
- SQLite row position or rowid was rejected because it is local implementation detail and fragile across imports, rebuilds, or migrations.
- Automatic display-key backfill during Project Web browsing was rejected because the GUI must remain read-only.
- Durable recent-error storage in Workspace Runtime was rejected because read-model failures should not create runtime writes or retention obligations.
- Mixed idea and raw-record timeline rows were rejected for the first slice because raw records do not have idea display keys or idea parent references.
- A static timeline table with no search/filtering was rejected because large research topics need the same narrowing affordances as the graph view.
- A settings-only row-count control was rejected because users need to change how many entries are shown while browsing the timeline view.

## Evidence

- `src/isomer_labs/runtime/sqlite.py` defines current `research_ideas` storage without `display_key`.
- `src/isomer_labs/runtime/store.py` orders ideas by `created_at, idea_id`, which is useful for presentation but not a durable GUI handle.
- `web/ui/src/features/graph/GraphPanels.tsx` already exposes a `Supporting Records` control in graph filters.
- `web/ui/src/features/graph/GraphPanels.tsx` also exposes search, status, and relation filter inputs that should guide the timeline filtering pattern.
- `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` defines Research Idea, Primary Idea, Idea Realization, and Idea Lineage Edge as the relevant domain terms.
