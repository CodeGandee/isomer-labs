## Context

The Project Web GUI already renders sparse idea lineage with ReactFlow and opens idea details through the shared workbench tab model. It also renders idea record JSON, lineage, realizations, and diagnostics in the idea detail panel, but those raw JSON surfaces compete with the Markdown reading surface.

## Goals / Non-Goals

**Goals:**
- Make idea graph inspection less accidental by separating selection from opening.
- Provide fast hover summaries without fetching full record detail.
- Keep the idea detail panel focused on readable Markdown while moving raw JSON into an explicit dialog.
- Preserve the existing workbench tab, graph API, and record detail API contracts.

**Non-Goals:**
- Do not change backend graph or record endpoints.
- Do not change query-index schema, topic artifacts, or research record payload format.
- Do not redesign dense Sigma.js graph behavior beyond keeping the open-on-double-click contract where practical.

## Decisions

- Use graph node metadata for hover previews. The graph payload already carries `title`, `one_liner`, `summary`, `status`, and record references, so hover preview should not trigger record-detail fetches.
- Treat single click as selection only. This preserves ReactFlow selection semantics and gives the user a low-cost way to inspect or orient on a node.
- Treat double click as the explicit open gesture. This matches IDE-like navigation where selection and opening are separate actions.
- Render hover content with the existing Markdown renderer in a compact wrapper. This keeps Markdown, KaTeX, Mermaid fallback behavior, and CSS fixes consistent without introducing a second parser.
- Replace top-level JSON copying with JSON-dialog copying. The detail panel should expose readable content first; raw JSON belongs in `View JSON`, where the active tab determines what gets copied.
- Keep `Main Record` as the default JSON tab. Lineage, realizations, and diagnostics are supporting data and should not outrank the idea record itself.

## Risks / Trade-offs

- Hover previews can obscure the graph → Limit width and height, position near the cursor, and hide on mouse leave or node open.
- Double click is less discoverable than single click → Selection still gives visual feedback, and hover gives the preview needed before opening.
- Compact Markdown may inherit spacing tuned for full panels → Add a dedicated compact class around the shared renderer.
- Some nodes may lack summaries → Fall back to one-liner, title, status, and record id so the tooltip remains useful.
