## 1. Event Boundary

- [x] 1.1 Add a typed idea lineage hover event boundary or feature effect that owns node enter, move, leave, click, open, tooltip enter, tooltip leave, and touch long-press events.
- [x] 1.2 Implement hover session creation on node enter using RxJS and the configured hover preview delay.
- [x] 1.3 Implement cancellation streams so click, open, leave, panel disposal, and new hover sessions cancel pending delayed hover emissions.
- [x] 1.4 Preserve the existing close-delay behavior for moving between node and hover popup.

## 2. Interaction State

- [x] 2.1 Add hover session identity to hover actions or hover state.
- [x] 2.2 Update the idea lineage reducer to ignore stale hover delay and close events whose session id is no longer active.
- [x] 2.3 Keep single-click selection, double-click opening, and selected-neighborhood highlight behavior unchanged.
- [x] 2.4 Keep touch long-press preview behavior aligned with the same visible hover preview state.

## 3. Panel Wiring

- [x] 3.1 Replace local hover timer refs in `IdeaLineagePanel.tsx` with calls into the typed event boundary.
- [x] 3.2 Make node click immediately close or cancel the active hover session before or alongside selection.
- [x] 3.3 Ensure mouse movement within a clicked node does not rearm hover until node leave and re-enter.
- [x] 3.4 Dispose event subscriptions when the panel store or panel component is disposed.

## 4. Tests and Verification

- [x] 4.1 Add reducer tests for stale hover delay and stale close events.
- [x] 4.2 Add RxJS boundary tests for click-before-delay, click-after-visible, same-hover suppression, and leave-enter rearming.
- [x] 4.3 Add or update component tests for single-click selection without tooltip reappearance.
- [x] 4.4 Run the relevant frontend test suite.
- [x] 4.5 Run `openspec validate control-idea-hover-session-with-rxjs`.
