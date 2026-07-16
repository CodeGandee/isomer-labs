# Idea Timeline Contract

The Idea Timeline view is a separate Graphs view from the Idea Graph. It derives table rows from the `idea-lineage` topic graph payload and does not request a separate mutating backend projection.

## Source Payload

The timeline reads `/api/topics/{topic_id}/graphs/idea-lineage` as a read-only source payload and derives table rows in the browser. It fetches primary and supporting Research Idea nodes for local row derivation; the visible Supporting Records flag controls whether supporting rows render. The request must not rebuild indexes, repair Workspace Runtime data, migrate old display keys, or assign missing display keys.

## Row Fields

Each rendered row is keyed by `idea_id` and shows `created_at`, `display_key`, `title`, parent display keys, exploration, decision, evidence, archive, and visibility facets. The GUI uses `display_key` in the `I-<index>` format as the short visible identity and falls back to `idea_id` only when old data has not been repaired yet. Backend-selected meaning and browser row selection remain separate.

Parent labels come from incoming graph edges. The GUI renders each parent by parent `display_key` when available, with parent `idea_id` as the fallback.

## Filtering and Sorting

Timeline search is one fuzzy text query. It covers display key, title, summary, aliases, family, status, idea id, parent display-key labels, parent titles, relation kinds, and other rendered table-entry fields. Search evaluates primary and supporting Research Idea rows, but Supporting Records defaults off and includes supporting rows only when enabled; hidden ideas keep their display keys in storage but are not rendered as normal timeline rows.

All visible columns are sortable. Sorting uses the selected column first and then falls back to creation time, updated time, title, and idea id. The in-view entry-count control is applied after filtering and sorting. Timeline and graph use the same fixed portfolio presets and local predicate from [Research Idea Portfolio](idea-portfolio.md), but restore browser state independently for each view.

## Settings

Timeline row coloring is a browser setting. It defaults off. Users can turn coloring on in Project Settings and configure light green for Primary Idea rows and light yellow for supporting idea rows. Selection remains visible through a non-color row cue and a footer badge.
