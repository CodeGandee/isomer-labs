## Why

The Project Web GUI currently rewrites the current URL entry when a user opens a Dockview tab, so browser Back cannot undo the tab-open action. Users expect Back to return the workbench to the prior semantic state, such as closing or deactivating the newly opened tab, not leaving the app or forcing a heavy reload.

## What Changes

- Add browser-history semantics for workbench navigation actions.
- Treat user-initiated semantic tab opens as navigation events that use `pushState`.
- Keep startup canonicalization, default topic selection, lightweight filter edits, and live refreshes from polluting browser history.
- Add a small history-state model that records the active openable item, active panel, and whether a history entry created a panel that should close when popped away.
- Reconcile Dockview tabs on `popstate` by focusing the URL-selected semantic item and closing history-created panels when appropriate.
- Preserve Dockview as the layout owner and avoid a broad GUI architecture refactor.

## Capabilities

### New Capabilities
- `workbench-browser-history-navigation`: Defines how Project Web workbench semantic navigation maps to browser history and Dockview tab reconciliation.

### Modified Capabilities
- None.

## Impact

- Affects `web/ui/src/App.tsx`, `web/ui/src/view-model.ts`, URL state helpers, workbench open-item routing, frontend tests, and Playwright smoke coverage.
- Does not require backend API changes, database changes, or new third-party dependencies.
- Does not change read-only browsing behavior or tab-scoped resource policy.
