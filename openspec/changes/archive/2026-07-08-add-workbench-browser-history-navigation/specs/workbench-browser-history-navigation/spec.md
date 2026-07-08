## ADDED Requirements

### Requirement: Semantic Tab Opens Create Reversible Browser History
The Project Web GUI SHALL map user-initiated semantic tab opens to browser history entries that can be reversed with browser Back.

#### Scenario: Opening a new semantic item pushes history
- **WHEN** a user opens an Explorer item, graph node, record row, file action, graph tab, diagnostics tab, runtime view, repository view, or actor view through the workbench open-item path
- **THEN** the GUI pushes a browser history entry for the new semantic `openable_item_id`
- **AND** the URL remains bookmarkable with the selected topic, graph scope when relevant, and open item id
- **AND** the history entry records whether the action created a new Dockview panel

#### Scenario: Opening an existing semantic item focuses without duplication
- **WHEN** a user opens a semantic item whose deterministic Dockview panel already exists
- **THEN** the GUI focuses the existing panel instead of creating a duplicate
- **AND** the pushed browser history entry records the focused panel without marking it as a newly created panel

#### Scenario: Opening the already-active semantic item is a no-op
- **WHEN** a user opens the semantic item that is already active
- **AND** the current URL already represents that item
- **THEN** the GUI does not push a duplicate browser history entry
- **AND** the Dockview tab set remains unchanged

#### Scenario: Startup canonicalization does not pollute history
- **WHEN** the GUI chooses a default topic, opens the default topic overview, or canonicalizes an initial URL during app boot
- **THEN** it uses replacement or silent state synchronization rather than pushing a user-visible browser history entry

### Requirement: Browser Back Reconciles Dockview State
The Project Web GUI SHALL reconcile Dockview tabs to the previous semantic workbench state when the user activates browser Back.

#### Scenario: Back returns to previous open item
- **WHEN** the user opens a semantic item that creates or focuses a Dockview tab
- **AND** the user activates browser Back
- **THEN** the GUI focuses or opens the semantic item represented by the previous history entry
- **AND** it does not reload or destroy the whole Project Web GUI shell

#### Scenario: Back closes history-created tab
- **WHEN** the current history entry created a new Dockview panel
- **AND** the user activates browser Back to a previous semantic item
- **THEN** the GUI closes the panel created by the popped-away history entry when it is not the target panel
- **AND** tab-scoped expensive work for that closed panel stops according to the open-tab resource policy

#### Scenario: Back does not close pre-existing tab
- **WHEN** the current history entry focused a panel that already existed before the entry was pushed
- **AND** the user activates browser Back
- **THEN** the GUI restores the previous semantic active item
- **AND** it does not close the pre-existing panel solely because it was focused by the popped-away entry

### Requirement: Browser Forward Restores Popped Semantic Navigation
The Project Web GUI SHALL support browser Forward after browser Back for semantic workbench navigation.

#### Scenario: Forward reopens a history-created tab
- **WHEN** browser Back closed a panel that was created by the popped-away entry
- **AND** the user activates browser Forward
- **THEN** the GUI resolves the forward entry's openable item descriptor again
- **AND** it opens or focuses the corresponding Dockview panel
- **AND** it restores the URL to the forward semantic workbench state

#### Scenario: Forward does not duplicate existing panel
- **WHEN** the panel for the forward entry already exists
- **AND** the user activates browser Forward
- **THEN** the GUI focuses that panel without creating a duplicate

### Requirement: Non-navigation Updates Avoid Browser History Noise
The Project Web GUI SHALL keep browser history focused on semantic navigation rather than every local UI change.

#### Scenario: Lightweight tab state does not push history by default
- **WHEN** a user edits search text, graph filters, table filters, local layout, resize state, or other lightweight in-tab controls
- **THEN** the GUI does not create a browser history entry for every change by default

#### Scenario: Closing a Dockview tab stays local
- **WHEN** a user closes a Dockview tab with the tab close affordance
- **THEN** the GUI does not push a new browser history entry for that close action
- **AND** if the closed tab was the URL-selected item, the GUI replaces the current entry with a safe semantic fallback

#### Scenario: Live updates do not mutate navigation history
- **WHEN** SSE, polling, manual refresh, or TanStack Query invalidation refreshes topic data
- **THEN** the GUI does not push or replace browser navigation history solely because read-model data changed

#### Scenario: Popstate handling is silent
- **WHEN** the GUI handles browser Back or Forward through a `popstate` event
- **THEN** its Dockview reconciliation does not push a new browser history entry while servicing that event
