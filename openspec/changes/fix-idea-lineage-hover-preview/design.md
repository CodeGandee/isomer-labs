## Context

The Project Web idea lineage graph currently renders hover content from graph node metadata. That path is fast, but it cannot show the full idea Markdown preview used by the idea detail panel, and the hover card has `pointer-events: none`, so users cannot move into it or scroll it. The graph also opens nodes through click and double-click flows; hover state must be cleared when those flows start so previews do not remain after navigation.

## Goals / Non-Goals

**Goals:**
- Reuse the existing idea detail API and `buildJsonMarkdownPreview` Markdown conversion path for hover previews.
- Show a fixed-size hover popup immediately with a loading state while idea Markdown data loads.
- Keep the loaded content inside the same bounded popup and make the popup interactive and scrollable.
- Clear hover state when a node opens and ignore stale loads from an abandoned hover target.

**Non-Goals:**
- Add new backend endpoints or expand the graph payload with full idea content.
- Change graph layout, lineage semantics, node labels, or record detail rendering.
- Make dense Sigma graph hover previews match this behavior in the same change.

## Decisions

- Use lazy frontend fetching for full hover content. The hover card will use the node `idea_id` and existing `getIdeaDetail` API, then build Markdown with `buildJsonMarkdownPreview`, matching the idea detail page. This avoids growing graph payloads and benefits from TanStack Query caching across repeated hovers.
- Keep a lightweight metadata fallback. If the node has no idea id, or if detail loading fails, the hover card can still render the existing metadata Markdown with a clear non-blocking state.
- Make the hover shell interactive. The card remains fixed-size with internal overflow, but pointer events are enabled and graph wheel/pointer propagation is stopped inside the card so scrolling the preview does not pan or zoom React Flow.
- Model hover lifecycle explicitly. Node hover schedules the popup, popup entry keeps it alive, popup leave closes it, and all open-node paths clear the preview before emitting workbench commands.

## Risks / Trade-offs

- Extra API requests on hover → Use delayed hover intent, query caching, and no prefetch on every mouse move.
- Stale async results after navigation → Key preview state by node id and clear state on open/unmount so a late query result has no visible target.
- Interactive popup can obscure graph nodes → Keep current bounded size and viewport clamping, and close on pointer leave.
- Markdown preview content may be long → Keep popup height fixed and scroll internally rather than expanding with content.
