## Context

The current Project Web GUI now has two Graphs views: Idea Graph and Idea Timeline. The first display-key implementation assigns short keys such as `I1`, exposes them in graph/timeline read models, and lets the timeline render configurable row colors. After using it against an existing topic workspace, two usability issues became clear: `I1` looks like a natural row index, and the timeline search/filter surface is more complicated than the Idea Graph search pattern.

The next revision should keep the display key concept but make the visible format less row-number-like, simplify search to one fuzzy text box, and reduce visual noise by making timeline row coloring opt-in. Existing topic data must remain under operator control: GUI browsing must not silently rewrite stored display keys.

## Goals / Non-Goals

**Goals:**

- Use `I-<index>` as the Research Idea display-key format for new assignments and explicit repairs.
- Provide an explicit repair or migration path from existing `I<index>` keys to `I-<index>`.
- Keep display keys stable, topic-scoped, unique, and not reused after allocation.
- Make Idea Timeline search a single fuzzy text search bar, matching Idea Graph usage.
- Let fuzzy search match all meaningful timeline row fields, including supporting-row fields, while keeping Supporting Records visibility controlled by the existing flag.
- Make Idea Timeline row colorization default off and configurable from Project Settings.
- Ensure Idea Graph and Idea Timeline visible labels use the same display-key format.

**Non-Goals:**

- Do not introduce a new table, search, or fuzzy-matching library unless existing code cannot support the needed behavior.
- Do not automatically mutate existing topic runtime databases during Project Web browsing, graph loading, timeline loading, or unrelated runtime reads.
- Do not change canonical `idea_id` semantics or use display keys as durable external ids.
- Do not remove the Supporting Records toggle; search should not become a visibility control.

## Decisions

1. Display keys use `I-<positive decimal>` and remain stored in Workspace Runtime.

The hyphen makes the key read as a label rather than a visible row number while preserving the compact shape and monotonic allocation. The runtime validator should reject old `I<index>` keys for newly written or explicitly migrated records once this change lands, and the repair/migration command should convert existing `I<index>` keys to matching `I-<index>` keys when no conflict exists.

Alternative considered: keep `I<index>` and only change labels in the frontend. That would make storage and display disagree, and it would leave API consumers unsure which format is canonical.

2. Existing keys migrate only through explicit operator action.

The current principle remains correct: Project Web read paths must not backfill, repair, or migrate identity data. Implementation should update the existing `ideas repair --apply` path or add a narrowly named migration path that rewrites `I1` to `I-1`, preserves already-correct `I-1` keys, and reports collisions before mutation.

Alternative considered: auto-upgrade on writable runtime open. That would surprise users because unrelated write operations could change visible GUI identity.

3. Timeline search uses one fuzzy text input.

The timeline should match the Idea Graph mental model: type text, see matching ideas. The row derivation can still evaluate many fields internally, but the visible UI should expose one search box and the existing Supporting Records toggle. Status/relation controls should be removed from the timeline view unless they remain hidden implementation details for graph requests.

Alternative considered: keep separate status and relation inputs. That is precise but heavier than the desired exploration workflow, and it makes the timeline feel unlike the graph view.

4. Search evaluates supporting rows before visibility filtering.

The search index should include both primary and supporting idea rows so a query can be ready to reveal supporting matches when the user enables Supporting Records. The final rendered row set still applies the Supporting Records visibility flag, so search does not unexpectedly display supporting rows.

Alternative considered: search only visible rows. That is simpler, but it makes enabling Supporting Records after searching feel inconsistent because the search result set has to be rebuilt differently.

5. Row colorization defaults off.

Color remains useful as an optional visual cue, but default-off keeps the table quieter and avoids over-weighting category color. Project Settings should retain the enable switch and color swatches, with stored browser-local defaults.

Alternative considered: keep color default-on with lighter colors. That still makes category coloring the first visual impression of the table.

## Risks / Trade-offs

- Existing databases may contain `I<index>` keys → provide an explicit repair/migration command, tests against old schema/old keys, and clear diagnostics when old keys remain.
- `I-<index>` migration can collide with manually authored keys → validate the complete plan before applying, reject collisions, and do not silently remap.
- Fuzzy search over all fields can match surprising rows → keep row detail visible enough to explain the match through display key, title, parent keys, status, family, and supporting-row toggle behavior.
- Default-off colorization may reduce category salience → preserve non-color cues such as status/visibility text, row class names, selection cue, and settings-controlled opt-in colors.
- Removing timeline status/relation inputs may reduce precision for expert filtering → the single search box still covers status and relation kind text, and graph view can keep its own search pattern.

## Migration Plan

1. Update runtime validation and allocation to use `I-<index>`.
2. Add explicit repair/migration handling for existing `I<index>` display keys and existing missing display keys.
3. Update Project Web graph/timeline label formatting and docs to describe `I-<index>`.
4. Simplify Timeline controls to one fuzzy search input plus Supporting Records and entry-count/sort controls.
5. Change settings defaults so row coloring initializes off for new browser-local settings.
6. Rebuild static GUI assets and run backend/frontend validation.

Rollback is straightforward for code, but any applied data migration from `I1` to `I-1` is a user-visible identity rewrite. If rollback is needed after migration, operators should restore the pre-migration `state.sqlite` snapshot or run a deliberate reverse migration.

## Open Questions

- Should the explicit migration be part of `ideas repair --apply`, a new `ideas display-keys migrate` command, or both with one shared implementation?
- Should old `I<index>` keys remain accepted as warnings during a transition window, or become validation errors immediately for current-schema writes?
