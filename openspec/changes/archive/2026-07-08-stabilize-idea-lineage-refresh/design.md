## Context

Project Web currently subscribes to topic events and also emits a synthetic invalidation every 15 seconds. Active idea lineage graph queries refetch on that synthetic event, and every graph response carries a fresh `generated_at` timestamp, so the graph panel treats identical graph content as new data and reruns React Flow conversion plus async ELK layout.

The idea lineage panel also clears `selectedNodeId` whenever the current graph data lacks that node. That is right after a confirmed graph change removes the node, but it is too aggressive for loading windows, transient empty/error responses, or unchanged graph content.

## Goals / Non-Goals

**Goals:**

- Refresh active graph queries when the backend reports a real topic index revision change or the user requests refresh.
- Avoid relayout and React Flow object churn for graph responses whose nodes and edges are unchanged.
- Preserve UI selection and lineage highlights during idle time, hover preview loading, and harmless background refresh.
- Separate backend idea status styling from UI interaction selection styling.
- Add focused tests that reproduce the idle-refresh class of bug.

**Non-Goals:**

- Do not replace TanStack Query, React Flow, RxJS, or the existing event API.
- Do not redesign dense graph rendering, Dockview, or URL navigation.
- Do not change backend persistence, record indexing, or graph response schema.

## Decisions

### Use revision-aware invalidation instead of heartbeat invalidation

The frontend should keep the server-sent event stream as the source of backend freshness, but it should only invalidate topic graph queries when a received index revision differs from the last revision seen for that topic. Manual refresh remains a direct invalidation path because it is user intent.

Alternative considered: keep the 15 second polling fallback but suppress graph invalidation if revision matches. That still runs unnecessary event work and hides the real ownership problem, so it should be a fallback only if SSE is unavailable and can read a revision cheaply.

### Key graph rendering off stable content, not response timestamp

The idea lineage graph should derive a stable content signature from the graph scope, node ids, edge ids, and core node or edge fields used by rendering. `generated_at`, `index_revision`, and other response metadata should not force layout. If the signature is unchanged, the panel should preserve existing base nodes, base edges, selected node, and layout positions.

Alternative considered: remove `generated_at` from the backend response. That could help, but it would make response metadata less useful and still leaves the frontend vulnerable to unrelated metadata changes.

### Treat empty/error refresh as transient unless graph content truly changes

When a refetch is loading, errors, or returns a graph with no usable nodes for a topic that previously had nodes, the panel should keep the last-good graph render state. The selected node should clear only when a confirmed content update has a valid node set that excludes it.

Alternative considered: always clear state on missing nodes. That is simple, but it creates the observed idle highlight disappearance.

### Reserve `selected` for React Flow interaction state

Backend idea state should render through status classes such as `status-selected` or a dedicated backend token. UI interaction selection should use React Flow `node.selected` and a UI class such as `ui-selected`. This avoids one selector accidentally stripping another layer's visual meaning.

Alternative considered: keep sharing the `selected` class and carefully preserve it. Shared semantics are brittle because backend status and UI interaction selection change for different reasons.

## Risks / Trade-offs

- [Risk] If SSE disconnects silently, revision-aware invalidation may miss updates. → Mitigation: keep manual refresh and consider a later revision polling fallback that checks revision without invalidating graphs by default.
- [Risk] Content signatures can omit a field that affects rendering. → Mitigation: build the signature from ids, labels, status, material kind, source refs, and relation kinds used by graph utilities, and cover this with tests.
- [Risk] Keeping last-good graph data can hide a true empty graph after deletion. → Mitigation: clear only when the response is successful and its stable content signature confirms a new empty graph state.

## Migration Plan

1. Add a revision-aware topic invalidation helper and tests for unchanged revision behavior.
2. Add graph content signature helpers and use them in the idea lineage panel to skip relayout for unchanged content.
3. Preserve selected-node state across loading and transient responses, while still clearing it when a successful changed graph excludes the selected node.
4. Rename UI selection classes so backend status styling is separate from interaction selection.
5. Verify with unit tests and a browser check against the running GUI.
