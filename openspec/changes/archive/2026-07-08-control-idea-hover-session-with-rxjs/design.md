## Context

The idea lineage graph currently keeps hover timers in `IdeaLineagePanel.tsx` with local refs such as `hoverDelayRef`, `hoverCloseDelayRef`, and `suppressHoverUntilNodeExitRef`. Single-click selection dispatches `nodeSelected`, but it does not cancel a pending hover delay, so a tooltip can appear after the user already clicked the node.

The Project Web state model already uses RxJS at event boundaries and reducer-owned feature state for complex interactions. This change should move hover timing and cancellation into a named RxJS effect while keeping the reducer pure and testable.

## Goals / Non-Goals

**Goals:**
- Model mouse hover as a session that starts on node enter and ends on node leave.
- Make click cancel or close the active hover preview and suppress rearming until the pointer leaves and re-enters the node.
- Use RxJS for delayed hover, cancellation, close behavior, and stale event suppression.
- Keep React handlers thin: they publish typed semantic events and dispatch direct non-delayed actions such as selection.
- Preserve existing Markdown hover preview, tooltip positioning rules, settings-driven delay, double-click open, and touch long-press behavior.

**Non-Goals:**
- Do not change backend graph APIs, topic data, or record data.
- Do not redesign the idea detail tab or Markdown preview renderer.
- Do not change the meaning of single-click selection or double-click opening.
- Do not introduce a global GUI state framework beyond the existing store, reducer, and RxJS boundary pattern.

## Decisions

Use a per-panel RxJS interaction boundary for idea lineage pointer events. React Flow handlers should call methods such as `nodeEnter`, `nodeMove`, `nodeLeave`, `nodeClick`, `nodeOpen`, `tooltipEnter`, `tooltipLeave`, and touch equivalents on a small feature event API. The API owns writable Subjects internally and exposes only typed methods plus a `dispose` hook.

Keep reducers pure and session-aware. Add a hover session id to hover actions or hover state so delayed emissions can be ignored when the active session has changed, ended, or been canceled. This prevents old timers from showing a tooltip after click, leave, open, panel disposal, or graph reload.

Use `switchMap`, `timer`, `takeUntil`, and typed cancellation streams to define the session lifecycle. On `nodeEnter`, create a session and dispatch `hoverStarted`. The delayed visible event uses `timer(settings.hoverPreviewDelayMs)` and is canceled by click, open, leave, graph disposal, or a new enter session. On `nodeClick`, dispatch `hoverClosed` for the active session and mark the session as canceled until its leave event arrives.

Preserve tooltip positioning by using pointer move only while the hover is pending. Once the tooltip is visible, movement within the node should not move the tooltip. This matches the existing usability fix that lets the user move from the node into the popup.

Treat double-click and open as stronger click events. The open path should close or cancel hover first, then dispatch `nodeOpened`, preserving the existing behavior that no stale tooltip remains after returning from the detail tab.

Keep touch long-press compatible with the same preview state. It can either remain as a separate stream that emits the same session-aware hover actions or be folded into the same boundary with a distinct `touchLongPress` event source. The implementation should prefer the smallest migration that removes ad hoc timers from the component.

## Risks / Trade-offs

- RxJS stream logic can become hard to inspect if too much interaction behavior is hidden in one pipeline. Mitigation: keep the boundary feature-specific, use typed event names, and cover the lifecycle with focused tests.
- Session ids add a small amount of ceremony to hover actions. Mitigation: this buys deterministic stale-event handling and keeps reducer behavior testable.
- Tooltip and node hover areas may have subtle leave timing. Mitigation: keep the existing close-delay behavior for moving from node to popup, but make click cancellation immediate.
- Touch and mouse paths may drift. Mitigation: route both paths to the same hover preview state and add at least one touch long-press regression test if the implementation changes that path.

## Migration Plan

1. Add a small idea lineage interaction event boundary near the existing feature store code.
2. Replace local hover `setTimeout` refs in `IdeaLineagePanel.tsx` with typed event API calls.
3. Add session ids to hover actions and update the reducer to ignore stale hover delay and close events.
4. Keep cleanup in panel disposal by disposing the event boundary subscription.
5. Add unit tests for reducer stale-event behavior and stream lifecycle behavior.
6. Add a component-level or Playwright regression for click-before-delay and click-after-visible behavior.

Rollback is straightforward because this change is frontend-only: restore the previous local timer handlers and reducer action shape if the stream boundary introduces regressions.

## Open Questions

- None. The intended user behavior is specified: a click terminates the current hover session, and only a new enter after leave can show the tooltip again.
