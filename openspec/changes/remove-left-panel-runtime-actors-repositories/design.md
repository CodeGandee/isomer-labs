## Context

The Project Web GUI builds the left Explorer from backend Project Explorer nodes. Topic children currently include user-facing research surfaces and lower-level implementation surfaces: `Workspace Runtime`, `Topic Actors`, and `Repositories`. The frontend renders whatever the Explorer read model returns, then opens a Dockview tab through the openable item descriptor route.

The user-facing design direction is to keep the left panel focused on research navigation. Runtime, actor, and repository data can still exist in APIs and diagnostics, but they should not compete with `Overview`, `Graphs`, `Records`, and diagnostics in the primary navigation tree.

## Goals / Non-Goals

**Goals:**

- Remove topic-level `Workspace Runtime`, `Topic Actors`, and `Repositories` rows from the left Project Explorer.
- Keep the change small and contract-driven: backend Explorer output changes first, frontend tests follow the new tree shape.
- Avoid crashes if a stale session, already-open tab, or manually constructed openable id references a removed Explorer item kind.

**Non-Goals:**

- Remove Workspace Runtime, Topic Actor, or repository backend APIs.
- Redesign topic overview content or diagnostics.
- Add a replacement settings flag or advanced navigation mode for these rows.

## Decisions

1. Remove the rows at the Project Explorer read-model source. The backend already owns semantic tree construction, and the frontend should not need a hard-coded denylist for Isomer domain concepts. Alternative considered: filter rows in React. That would leave API consumers and contract tests seeing a stale tree shape.

2. Keep hidden item handling tolerant. If the existing openable descriptor route still knows how to resolve runtime, actor, or repository item ids, the implementation may leave that route in place for stale browser state. Alternative considered: delete the route immediately. That is cleaner, but it risks unnecessary tab recovery or browser-history breakage for a navigation-only change.

3. Update tests around the tree contract rather than adding a new UI setting. This change is intended to simplify the default left panel, not create another user preference.

## Risks / Trade-offs

- Stale test expectations may still assert the old topic child count. Mitigation: update backend and frontend contract tests that inspect Explorer rows.
- Hidden-but-resolvable item descriptors may keep some dead frontend panel code alive. Mitigation: treat component cleanup as optional during implementation, and remove only code that tests prove unused.
- Users who depended on these rows for raw inspection lose one-click access. Mitigation: keep diagnostics and backend read APIs available, and let future work decide whether a deliberate advanced inspector belongs elsewhere.

## Migration Plan

Implement as a normal GUI behavior change. Existing data does not need migration. Rollback is limited to restoring the three topic child nodes in the Project Explorer read model and associated tests.

## Open Questions

None.
