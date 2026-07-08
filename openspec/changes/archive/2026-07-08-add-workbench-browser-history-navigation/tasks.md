## 1. Navigation State Model

- [x] 1.1 Add a typed frontend workbench history state shape covering topic id, graph scope, open item id, active panel id, opened panel id, and close-on-back behavior.
- [x] 1.2 Refactor the URL state helper so callers can choose push, replace, or silent state synchronization.
- [x] 1.3 Keep app boot, default topic selection, and URL canonicalization on replace or silent synchronization.
- [x] 1.4 Ensure live refresh, SSE invalidation, polling, and query refetches do not write browser history.

## 2. Dockview Open-item Integration

- [x] 2.1 Change the open-panel helper to return structured panel metadata, including whether a tab was created or focused.
- [x] 2.2 Update `openItem` so user-initiated semantic opens push history entries with the correct open item and panel metadata.
- [x] 2.3 Keep descriptor resolution, deterministic tab ids, and duplicate-tab prevention unchanged.
- [x] 2.4 Make in-app commands for records, files, graphs, runtime, diagnostics, repository, actor, and topic overview use the same navigation mode rules.

## 3. Browser Back and Forward Reconciliation

- [x] 3.1 Add popstate handling that reads the target semantic state and reconciles Dockview without pushing another history entry.
- [x] 3.2 Focus or open the target semantic item when browser Back or Forward changes the URL.
- [x] 3.3 Close only the panel created by the popped-away entry when `closeOnBack` is true and the panel is not the target.
- [x] 3.4 Preserve pre-existing panels when a history entry only focused them.
- [x] 3.5 Ensure browser Forward can reopen a panel that Back closed.

## 4. Tests and Validation

- [x] 4.1 Add frontend unit tests for push versus replace URL writes, structured history state, and silent popstate synchronization.
- [x] 4.2 Add frontend unit tests for open-panel metadata and duplicate-tab prevention.
- [x] 4.3 Add Playwright coverage that opens a semantic tab, uses browser Back to return to the prior workbench state, and uses browser Forward to restore the tab.
- [x] 4.4 Verify the GUI still lazy-loads tab content and that closed history-created tabs stop their expensive work.
- [x] 4.5 Run relevant frontend tests, Playwright smoke coverage, and OpenSpec validation.
