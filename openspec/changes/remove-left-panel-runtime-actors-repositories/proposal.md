## Why

The Project Web left panel has drifted toward low-level implementation surfaces that distract from the current research navigation flow. Removing `Workspace Runtime`, `Topic Actors`, and `Repositories` from the Explorer keeps the GUI focused on topic overview, graphs, records, and diagnostics.

## What Changes

- Remove the `Workspace Runtime`, `Topic Actors`, and `Repositories` rows from each topic in the left Project Explorer.
- Keep `Overview`, `Graphs`, `Records`, and diagnostics-driven entries available in the left panel.
- Preserve existing backend read APIs for runtime, actors, and topic repository context unless implementation work finds unused frontend-only code that can be safely removed.
- Preserve safe behavior for stale links or already-open tabs: removing Explorer entries must not crash the workbench if an old session references one of these item kinds.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `project-web-ide-workbench`: Change the semantic Project Explorer navigation contract so topic-level `Workspace Runtime`, `Topic Actors`, and `Repositories` are no longer shown as left-panel rows.

## Impact

- Affected frontend: Explorer navigation rendering, tab routing tests if they assert these rows are present, and any snapshots or contract tests for topic children.
- Affected backend: Project Explorer read model construction for topic child nodes and possibly openable item descriptors for hidden item kinds.
- No new runtime dependency or technology stack is needed.
