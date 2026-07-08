## Why

The idea lineage graph can still show a hover tooltip after the user clicks a node because hover timers and click handlers are managed separately. This makes click, hover, and open interactions feel out of order when the user is trying to inspect or select an idea.

## What Changes

- Treat each node hover as a bounded hover session that starts on pointer enter and ends on pointer leave.
- Use an RxJS event pipeline to own hover delay, hover cancellation, tooltip close, and stale timer suppression.
- Make node click terminate the active hover session for tooltip purposes: pending tooltips are canceled, visible tooltips close, and the same hover cannot show a tooltip again.
- Require the user to move out of the node and back in before a tooltip may appear after a click.
- Preserve existing single-click selection, double-click opening, touch long-press preview, and Markdown-capable tooltip behavior.
- Add regression tests for click-before-delay, click-after-visible, same-hover suppression, and leave-enter rearming.

## Capabilities

### New Capabilities
- `project-web-idea-hover-session`: Covers event ordering, cancellation, and RxJS ownership for idea lineage hover tooltip sessions.

### Modified Capabilities

## Impact

- Idea lineage graph interaction code in `web/ui/src/features/idea-lineage/`.
- Idea lineage interaction reducer and tests in `web/ui/src/features/idea-lineage/idea-lineage-state.ts` and related test files.
- RxJS event boundary or feature-store code used by the Project Web GUI.
- No backend API, storage schema, or topic data change is expected.
