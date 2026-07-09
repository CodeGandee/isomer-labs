## 1. Explorer Read Model

- [x] 1.1 Update the Project Explorer topic child construction so `Workspace Runtime`, `Topic Actors`, and `Repositories` are no longer emitted as left-panel topic rows.
- [x] 1.2 Keep `Overview`, `Graphs`, graph scope rows, `Records`, and diagnostics-driven rows available in the Explorer.
- [x] 1.3 Preserve tolerant openable item handling for stale runtime, actor, or repository item ids if existing routes depend on it.

## 2. Frontend Behavior

- [x] 2.1 Update frontend Explorer expectations so the removed rows are not rendered or advertised in the left panel.
- [x] 2.2 Remove or leave unused runtime, actor, and repository panel code only after confirming stale session recovery and tests remain safe.

## 3. Verification

- [x] 3.1 Update backend and frontend tests that assert Project Explorer topic children or openable tab labels.
- [x] 3.2 Run focused Project Web GUI tests for Explorer rendering and openable item routing.
- [x] 3.3 Run `openspec validate remove-left-panel-runtime-actors-repositories --strict`.
