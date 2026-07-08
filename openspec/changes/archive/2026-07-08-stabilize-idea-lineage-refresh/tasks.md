## 1. Refresh Invalidation

- [x] 1.1 Replace unconditional topic graph heartbeat invalidation with revision-aware event invalidation.
- [x] 1.2 Keep manual refresh as an explicit invalidation path.
- [x] 1.3 Add tests proving unchanged topic revisions do not invalidate graph queries and changed revisions do.

## 2. Idea Graph Render Stability

- [x] 2.1 Add stable graph content signature helpers that ignore response-only metadata such as `generated_at`.
- [x] 2.2 Update the idea lineage panel to skip React Flow conversion and ELK relayout when graph content is unchanged.
- [x] 2.3 Preserve last-good graph render state during loading, failed, or transient empty refresh states.

## 3. Selection and Styling

- [x] 3.1 Preserve selected-node lineage highlights when a benign refresh returns unchanged content.
- [x] 3.2 Clear selection only when a successful changed graph no longer contains the selected node.
- [x] 3.3 Separate backend selected/status styling from UI-selected interaction styling.

## 4. Verification

- [x] 4.1 Run focused frontend unit tests for idea graph and event invalidation behavior.
- [x] 4.2 Use Playwright or an equivalent browser check against the running GUI to watch the idea graph across an idle refresh window.
- [x] 4.3 Run the relevant broader validation command available in the repo.
