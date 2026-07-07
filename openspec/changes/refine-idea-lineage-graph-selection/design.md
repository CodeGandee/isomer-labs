## Context

The Project Web idea lineage graph is rendered with ReactFlow from the topic graph API. The backend already projects canonical idea lineage as directed parent-to-child edges, but the frontend currently renders plain edge paths and only marks the selected node itself.

## Goals / Non-Goals

**Goals:**
- Make hover preview intent deliberate by using a 2 second delay.
- Show edge direction visually without changing the backend graph contract.
- Highlight a selected node's direct parents and direct children with different classes and colors.
- Keep the implementation inside the existing ReactFlow graph path and existing tests.

**Non-Goals:**
- Change canonical idea lineage semantics or stored records.
- Add a new graph endpoint, graph schema field, or database migration.
- Add recursive ancestor or descendant highlighting beyond direct neighbors.
- Change Sigma overview graph behavior in this follow-up.

## Decisions

- Use the existing graph edge direction as authoritative. The topic graph API already sends `source` as parent and `target` as child for canonical idea lineage, so ReactFlow should add closed arrow markers to the current edges instead of deriving direction from labels or layout.
- Decorate nodes and edges in the panel from the selected node id. This keeps graph conversion pure enough for base node and edge mapping while letting UI selection state drive transient classes such as `lineage-parent`, `lineage-child`, `lineage-incoming`, and `lineage-outgoing`.
- Highlight only direct neighbors. Direct parents and children match the user's selection context, stay readable on branching graphs, and avoid turning a large lineage into a saturated path highlight.
- Share the 2 second delay between mouse hover and touch long press. Both gestures represent preview intent, so keeping one constant prevents divergent timing across input modes.

## Risks / Trade-offs

- Arrowheads may inherit low-contrast edge colors in some themes → Style edge markers through ReactFlow marker color and CSS variables, and keep selected-neighborhood edge colors stronger.
- Node class updates can be lost when graph data relayouts → Recompute decoration from `flowNodes`, `flowEdges`, and selected id on render instead of storing parent/child classes permanently in the laid-out nodes.
- Direct-neighbor highlighting may hide longer paths users care about → Keep the scope direct for this change and leave recursive path exploration for a later interaction.
