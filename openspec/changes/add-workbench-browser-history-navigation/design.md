## Context

The Project Web GUI already has the right architecture shape: Explorer rows and graph/table interactions call a unified `openItem` command, `openItem` resolves an openable item descriptor, and Dockview opens or focuses a deterministic tab. URL state is also centralized in `useUrlState`, but it currently writes with `window.history.replaceState` for every state change.

That means a user action such as opening a record detail tab overwrites the current history entry. Browser Back cannot return to the previous workbench state, so it may leave the GUI or reload an older state instead of undoing the tab open.

## Goals / Non-Goals

**Goals:**

- Make browser Back and Forward operate on semantic workbench navigation.
- Treat user-initiated tab opens and tab focuses as navigation actions.
- Keep boot-time default topic selection and URL canonicalization out of browser history.
- Reconcile Dockview state on `popstate` without remounting the whole app.
- Close only tabs created by the popped-away navigation entry when that is safe and intentional.
- Preserve lazy tab resource policy and existing backend read APIs.

**Non-Goals:**

- Do not persist the full Dockview layout in the URL.
- Do not replace Dockview, TanStack Query, RxJS, or the Explorer read model.
- Do not make browser history track every keystroke, filter edit, live refresh, resize, or data invalidation.
- Do not change backend APIs or Workspace Runtime state.
- Do not implement multi-user shared layout history.

## Decisions

### Split URL Writes by Navigation Intent

Use `replaceState` for app boot, default topic selection, URL canonicalization, and lightweight in-tab state updates that should not create a new browser step. Use `pushState` for user-initiated semantic item opens or focus changes where users naturally expect Back to undo the action.

Alternative considered: always use `pushState`. That would make filter typing, startup redirects, and automatic refreshes produce noisy history stacks.

### Add a Workbench History State Model

Store minimal semantic state in `history.state`, separate from the query string:

```ts
type WorkbenchHistoryState = {
  kind: "isomer-workbench"
  topicId?: string
  graphScope: GraphScope
  openItemId?: string
  activePanelId?: string
  openedPanelId?: string
  closeOnBack?: boolean
  navigationIndex?: number
}
```

The query string remains bookmarkable and shareable with `topic`, `graph`, and `open`. The structured state lets the app know whether the most recent navigation created a tab that can be closed when the user goes back. `navigationIndex` lets the app distinguish Back from Forward, since `popstate` only provides the target entry.

Alternative considered: encode all of this in the query string. That would make URLs noisier and expose implementation details such as Dockview panel ids as durable route syntax.

### Return Structured Panel-open Results

Change the frontend descriptor helper from returning only `"created" | "focused" | "ignored"` to returning a result that includes the panel id and whether a panel was created:

```ts
type OpenPanelResult = {
  status: "created" | "focused" | "ignored"
  panelId?: string
}
```

`openItem` can then decide whether the history entry should set `openedPanelId` and `closeOnBack`.

Alternative considered: infer created/focused state in `openItem` before calling the helper. That duplicates tab lookup logic and makes tests more brittle.

### Reconcile Dockview on Popstate

On `popstate`, the URL and history state become the source of navigation intent. The workbench should:

1. Read the target `topic`, `graph`, and `open` values.
2. Open or focus the target `openItemId` if present.
3. Fall back to the selected topic overview when no `open` value is present.
4. Compare `navigationIndex` values to tell Back from Forward.
5. On Back, close the panel recorded by the previous popped-away state when that panel was created by that entry and is no longer the target.
6. On Forward, reopen or focus the target entry without closing the panel from the previous entry.
7. Avoid pushing a new history entry while servicing `popstate`.

Alternative considered: let `popstate` only update React state and rely on startup effects. That explains the current bad behavior: Dockview is not reconciled to the previous semantic workbench state.

### Treat Already-active Opens as No-ops

If a user opens the semantic item that is already active and the URL already represents that item, the workbench should not push a duplicate browser history entry. If the item exists in Dockview but is inactive, focusing it is a semantic navigation action and should push a history entry that records the focused panel without `closeOnBack`.

Alternative considered: push a new entry for every click. That would make browser Back step through repeated clicks that did not change workbench state.

### Keep Dockview Close Local in the First Slice

Closing a tab with Dockview's close affordance should mutate local workbench layout only. If the closed tab is the URL-selected semantic item, the app should replace the current browser entry with a safe semantic fallback, such as the selected topic overview or another already-open semantic item, rather than pushing a new close-navigation entry.

Alternative considered: treat tab close as a browser navigation action. That can be added later, but it requires a stronger policy for choosing the previous semantic item and could surprise users by making a local layout cleanup alter their browser Back stack.

### Keep Layout Local and Semantic Navigation URL-backed

Dockview remains the layout owner. Browser history only records semantic navigation targets, not full split panes, floating positions, sizes, or every open tab. Local layout persistence can remain a separate future concern.

Alternative considered: serialize the full Dockview layout into each history entry. That would make Back/Forward precise but heavy, fragile, and hostile to bookmarkable URLs.

## Risks / Trade-offs

- Closing a tab on Back could surprise users if they expected it to remain open. → Only close panels that the popped-away history entry created and mark this behavior with `closeOnBack`.
- Browser Forward after Back must recreate a closed tab. → Keep `openItemId` in the target history entry and let normal descriptor routing reopen it.
- Popstate reconciliation could push a new entry accidentally. → Add an explicit navigation mode such as `historyMode: "push" | "replace" | "silent"` or a `syncUrl: false` path while servicing Back/Forward.
- Existing startup logic may reopen default tabs at the wrong time. → Treat default topic overview as canonical boot state, then stop startup effects from overriding explicit browser history.
- Tests may become timing-sensitive around Dockview. → Put pure history-state and open-panel behavior in unit tests, then use Playwright only for end-to-end Back/Forward behavior.

## Migration Plan

1. Extend URL state helpers to support `push`, `replace`, and silent local state updates.
2. Extend `openPanelFromDescriptor` to return panel metadata.
3. Update `openItem` to write navigation history only for user-initiated semantic opens.
4. Add a popstate reconciliation path that focuses or opens the target item and closes only eligible history-created panels.
5. Update frontend unit tests around URL history and panel routing.
6. Update Playwright smoke coverage to open a tab, press browser Back, verify the prior tab state, then press Forward and verify the opened tab returns.

Rollback is to keep using `replaceState` for all URL writes and ignore structured history state. Backend APIs and stored project data are unaffected.
